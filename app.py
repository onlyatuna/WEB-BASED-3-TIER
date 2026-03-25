"""
WEB-BASED 3-TIER 資料維護系統 - Streamlit 版
Tier1: Streamlit UI  |  Tier2: Python 業務邏輯  |  Tier3: SQL Server
"""
import streamlit as st
import pyodbc
import pandas as pd

st.set_page_config(page_title="資料維護系統", layout="wide")

# ═══════════════════════════════════════════════════════════════
# Tier 3 – Data Access Layer
# ═══════════════════════════════════════════════════════════════

def get_conn():
    s = st.secrets["db"]
    return pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={s['server']},{s['port']};"
        f"DATABASE={s['database']};"
        f"UID={s['uid']};PWD={s['pwd']};"
        f"TrustServerCertificate=yes"
    )

def qry(sql, params=()):
    conn = get_conn()
    try:
        return pd.read_sql(sql, conn, params=list(params) if params else None)
    finally:
        conn.close()

def cmd(sql, params=()):
    conn = get_conn()
    try:
        conn.execute(sql, params)
        conn.commit()
    finally:
        conn.close()

# USER
def user_all():   return qry("SELECT userid AS 用戶代碼, username AS 用戶名稱, pwd AS 用戶密碼 FROM [user]")
def user_ins(a,b,c): cmd("INSERT INTO [user](userid,username,pwd) VALUES(?,?,?)",(a,b,c))
def user_upd(a,b,c): cmd("UPDATE [user] SET username=?,pwd=? WHERE userid=?",(b,c,a))
def user_del(a):     cmd("DELETE FROM [user] WHERE userid=?",(a,))

# CUST
def cust_all():   return qry("SELECT cust_code AS 客戶代碼, cust_name AS 客戶名稱, remark AS 備註說明 FROM cust")
def cust_ins(a,b,c): cmd("INSERT INTO cust(cust_code,cust_name,remark) VALUES(?,?,?)",(a,b,c))
def cust_upd(a,b,c): cmd("UPDATE cust SET cust_name=?,remark=? WHERE cust_code=?",(b,c,a))
def cust_del(a):     cmd("DELETE FROM cust WHERE cust_code=?",(a,))

# FACT
def fact_all():   return qry("SELECT fact_code AS 廠商代碼, fact_name AS 廠商名稱, remark AS 備註說明 FROM fact")
def fact_raw():   return qry("SELECT fact_code, fact_name FROM fact ORDER BY fact_code")
def fact_ins(a,b,c): cmd("INSERT INTO fact(fact_code,fact_name,remark) VALUES(?,?,?)",(a,b,c))
def fact_upd(a,b,c): cmd("UPDATE fact SET fact_name=?,remark=? WHERE fact_code=?",(b,c,a))
def fact_del(a):     cmd("DELETE FROM fact WHERE fact_code=?",(a,))

# ITEM
def item_all():
    return qry("""
        SELECT i.item_code AS 商品代碼, i.item_name AS 商品名稱,
               i.fact_code AS 廠商代碼, f.fact_name AS 廠商名稱
        FROM item i LEFT JOIN fact f ON i.fact_code=f.fact_code
    """)
def item_ins(a,b,c): cmd("INSERT INTO item(item_code,item_name,fact_code) VALUES(?,?,?)",(a,b,c))
def item_upd(a,b,c): cmd("UPDATE item SET item_name=?,fact_code=? WHERE item_code=?",(b,c,a))
def item_del(a):     cmd("DELETE FROM item WHERE item_code=?",(a,))

# ═══════════════════════════════════════════════════════════════
# Tier 2 – Business Logic Layer
# ═══════════════════════════════════════════════════════════════

def validate(**fields):
    missing = [cap for cap, val in fields.items() if not str(val).strip()]
    return missing

# ═══════════════════════════════════════════════════════════════
# Tier 1 – Presentation Layer
# ═══════════════════════════════════════════════════════════════

if "page" not in st.session_state:
    st.session_state.page = "main"

def nav(p):
    st.session_state.page = p
    st.rerun()

# ── 共用 CRUD 區塊 ───────────────────────────────────────────
def crud_form(title, pk_label, pk_key, fields, load_fn, ins_fn, upd_fn, del_fn,
              extra_widget=None, extra_key=None):
    """
    fields: list of (field_key, label, multiline)
    extra_widget: callable(current_value) -> new_value  (for dropdowns)
    extra_key: field key for extra_widget
    """
    st.subheader(title)
    op = st.radio("功能", ["查詢", "新增", "修改", "刪除"], horizontal=True, key=f"{pk_key}_op")

    df = load_fn()

    if op == "查詢":
        st.dataframe(df, use_container_width=True, hide_index=True)
        return

    if op == "新增":
        with st.form(f"{pk_key}_ins"):
            pk_val = st.text_input(pk_label)
            vals = {}
            for fk, fl, ml in fields:
                if fk == extra_key and extra_widget:
                    vals[fk] = extra_widget(None)
                else:
                    vals[fk] = st.text_area(fl) if ml else st.text_input(fl)
            if st.form_submit_button("新增", type="primary"):
                miss = validate(**{pk_label: pk_val}, **{fl: vals[fk] for fk, fl, _ in fields if fl != extra_key})
                if miss:
                    st.error(f"必填：{', '.join(miss)}")
                else:
                    try:
                        args = [pk_val] + [vals[fk] for fk, _, _ in fields]
                        ins_fn(*args)
                        st.success("新增成功")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))

    else:  # 修改 / 刪除
        ids = df.iloc[:, 0].tolist()
        if not ids:
            st.info("無資料")
            return
        sel = st.selectbox(f"選擇{pk_label}", ids, key=f"{pk_key}_sel")
        row = df[df.iloc[:, 0] == sel].iloc[0]

        if op == "修改":
            with st.form(f"{pk_key}_upd"):
                st.text_input(pk_label, value=sel, disabled=True)
                vals = {}
                for fk, fl, ml in fields:
                    col_name = fl if fl in df.columns else df.columns[fields.index((fk, fl, ml)) + 1]
                    cur = row.get(col_name, row.iloc[fields.index((fk, fl, ml)) + 1])
                    if fk == extra_key and extra_widget:
                        vals[fk] = extra_widget(cur)
                    else:
                        vals[fk] = st.text_area(fl, value=str(cur) if cur else "") if ml \
                                   else st.text_input(fl, value=str(cur) if cur else "")
                if st.form_submit_button("修改", type="primary"):
                    try:
                        args = [sel] + [vals[fk] for fk, _, _ in fields]
                        upd_fn(*args)
                        st.success("修改成功")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))

        elif op == "刪除":
            st.dataframe(df[df.iloc[:, 0] == sel], use_container_width=True, hide_index=True)
            if st.button("確認刪除", type="primary", key=f"{pk_key}_del"):
                try:
                    del_fn(sel)
                    st.success("刪除成功")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

# ── 各功能頁 ─────────────────────────────────────────────────
def page_user():
    if st.button("← 返回主選單"): nav("main")
    crud_form("USER 用戶資料維護", "用戶代碼", "user",
              [("username","用戶名稱",False), ("pwd","用戶密碼",False)],
              user_all, user_ins, user_upd, user_del)

def page_cust():
    if st.button("← 返回主選單"): nav("main")
    crud_form("CUST 客戶資料維護", "客戶代碼", "cust",
              [("cust_name","客戶名稱",False), ("remark","備註說明",True)],
              cust_all, cust_ins, cust_upd, cust_del)

def page_fact():
    if st.button("← 返回主選單"): nav("main")
    crud_form("FACT 廠商資料維護", "廠商代碼", "fact",
              [("fact_name","廠商名稱",False), ("remark","備註說明",True)],
              fact_all, fact_ins, fact_upd, fact_del)

def page_item():
    if st.button("← 返回主選單"): nav("main")
    # 廠商下拉選項
    try:
        df_fact = fact_raw()
        fact_opts = {f"{r['fact_code']} {r['fact_name']}": r["fact_code"] for _, r in df_fact.iterrows()}
    except:
        fact_opts = {}

    def fact_select(cur_val):
        labels = list(fact_opts.keys())
        idx = 0
        if cur_val:
            for i, (lbl, code) in enumerate(fact_opts.items()):
                if code == cur_val:
                    idx = i
                    break
        chosen = st.selectbox("主供應商", labels, index=idx, key="item_fact_sel")
        return fact_opts.get(chosen, chosen)

    crud_form("ITEM 商品資料維護", "商品代碼", "item",
              [("item_name","商品名稱",False), ("fact_code","主供應商",False)],
              item_all, item_ins, item_upd, item_del,
              extra_widget=fact_select, extra_key="fact_code")

def page_main():
    st.title("資料維護系統")
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("👤  USER　用戶資料維護", use_container_width=True): nav("user")
        if st.button("🏢  CUST　客戶資料維護", use_container_width=True): nav("cust")
    with c2:
        if st.button("🏭  FACT　廠商資料維護", use_container_width=True): nav("fact")
        if st.button("📦  ITEM　商品資料維護", use_container_width=True): nav("item")

# ── Router ────────────────────────────────────────────────────
pages = {"main": page_main, "user": page_user,
         "cust": page_cust, "fact": page_fact, "item": page_item}
pages[st.session_state.page]()
