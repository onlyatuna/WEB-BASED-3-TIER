"""
WEB-BASED 3-TIER 資料維護系統 - Streamlit 版
Tier1: Streamlit UI  |  Tier2: Python 業務邏輯  |  Tier3: SQL Server
"""
import streamlit as st
import streamlit.components.v1 as components
import pymssql
import pandas as pd

st.set_page_config(page_title="資料維護系統", layout="wide")

# ═══════════════════════════════════════════════════════════════
# Tier 3 – Data Access Layer
# ═══════════════════════════════════════════════════════════════

def get_conn():
    s = st.secrets["db"]
    return pymssql.connect(
        server=s["server"], port=int(s["port"]),
        database=s["database"], user=s["uid"], password=s["pwd"],
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
        cur = conn.cursor(); cur.execute(sql, params); conn.commit()
    finally:
        conn.close()

# USER
def user_all():      return qry("SELECT userid AS 用戶代碼, username AS 用戶名稱, pwd AS 用戶密碼 FROM [user]")
def user_ins(a,b,c): cmd("INSERT INTO [user](userid,username,pwd) VALUES(%s,%s,%s)",(a,b,c))
def user_upd(a,b,c): cmd("UPDATE [user] SET username=%s,pwd=%s WHERE userid=%s",(b,c,a))
def user_del(a):     cmd("DELETE FROM [user] WHERE userid=%s",(a,))

# CUST
def cust_all():      return qry("SELECT cust_code AS 客戶代碼, cust_name AS 客戶名稱, remark AS 備註說明 FROM cust")
def cust_ins(a,b,c): cmd("INSERT INTO cust(cust_code,cust_name,remark) VALUES(%s,%s,%s)",(a,b,c))
def cust_upd(a,b,c): cmd("UPDATE cust SET cust_name=%s,remark=%s WHERE cust_code=%s",(b,c,a))
def cust_del(a):     cmd("DELETE FROM cust WHERE cust_code=%s",(a,))

# FACT
def fact_all():      return qry("SELECT fact_code AS 廠商代碼, fact_name AS 廠商名稱, remark AS 備註說明 FROM fact")
def fact_raw():      return qry("SELECT fact_code, fact_name FROM fact ORDER BY fact_code")
def fact_ins(a,b,c): cmd("INSERT INTO fact(fact_code,fact_name,remark) VALUES(%s,%s,%s)",(a,b,c))
def fact_upd(a,b,c): cmd("UPDATE fact SET fact_name=%s,remark=%s WHERE fact_code=%s",(b,c,a))
def fact_del(a):     cmd("DELETE FROM fact WHERE fact_code=%s",(a,))

# ITEM
def item_all():
    return qry("""SELECT i.item_code AS 商品代碼, i.item_name AS 商品名稱,
                         i.fact_code AS 廠商代碼, f.fact_name AS 廠商名稱
                  FROM item i LEFT JOIN fact f ON i.fact_code=f.fact_code""")
def item_ins(a,b,c): cmd("INSERT INTO item(item_code,item_name,fact_code) VALUES(%s,%s,%s)",(a,b,c))
def item_upd(a,b,c): cmd("UPDATE item SET item_name=%s,fact_code=%s WHERE item_code=%s",(b,c,a))
def item_del(a):     cmd("DELETE FROM item WHERE item_code=%s",(a,))

# ═══════════════════════════════════════════════════════════════
# Tier 2 – Business Logic Layer
# ═══════════════════════════════════════════════════════════════

def required(*vals):
    return all(str(v).strip() for v in vals)

# ═══════════════════════════════════════════════════════════════
# Tier 1 – Presentation Layer
# ═══════════════════════════════════════════════════════════════

# ── Session state 初始化 ─────────────────────────────────────
for k, v in {"page":"main", "dlg":None, "dlg_row":{}}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def nav(p):
    st.session_state.page = p
    st.session_state.dlg  = None
    st.rerun()

def open_dlg(mode, row={}):
    st.session_state.dlg     = mode   # "add" | "edit" | "del"
    st.session_state.dlg_row = row
    st.rerun()

def close_dlg():
    st.session_state.dlg = None
    st.rerun()

# ── 主選單 ───────────────────────────────────────────────────
def page_main():
    # query param 導航（HTML card click 後觸發）
    if "nav" in st.query_params:
        dest = st.query_params["nav"]
        st.query_params.clear()
        nav(dest)
        return

    st.markdown(
        "<h1 style='text-align:center;padding:40px 0 8px;font-size:2rem'>資料維護系統</h1>",
        unsafe_allow_html=True,
    )

    components.html("""
    <style>
    *{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
    body{background:transparent}
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;max-width:560px;margin:24px auto}
    .card{background:#fff;border-radius:10px;padding:36px 20px 32px;text-align:center;
          box-shadow:0 2px 8px rgba(0,0,0,.08);cursor:pointer;
          transition:box-shadow .2s,transform .2s;border-top:5px solid}
    .card:hover{box-shadow:0 8px 24px rgba(0,0,0,.14);transform:translateY(-4px)}
    .card:active{transform:translateY(-1px)}
    .icon{font-size:40px;margin-bottom:16px}
    .en{font-size:13px;color:#999;letter-spacing:1px;font-weight:600;text-transform:uppercase}
    .zh{font-size:17px;font-weight:700;color:#1a1a1a;margin-top:4px}
    .u{border-top-color:#1677ff}.c{border-top-color:#52c41a}
    .f{border-top-color:#fa8c16}.i{border-top-color:#722ed1}
    </style>
    <div class="grid">
      <div class="card u" onclick="go('user')">
        <div class="icon">👤</div><div class="en">USER</div><div class="zh">用戶資料維護</div>
      </div>
      <div class="card c" onclick="go('cust')">
        <div class="icon">🏢</div><div class="en">CUST</div><div class="zh">客戶資料維護</div>
      </div>
      <div class="card f" onclick="go('fact')">
        <div class="icon">🏭</div><div class="en">FACT</div><div class="zh">廠商資料維護</div>
      </div>
      <div class="card i" onclick="go('item')">
        <div class="icon">📦</div><div class="en">ITEM</div><div class="zh">商品資料維護</div>
      </div>
    </div>
    <script>
    function go(p){
      window.parent.location.href =
        window.parent.location.pathname + '?nav=' + p;
    }
    </script>
    """, height=380, scrolling=False)

# ── 共用 CRUD 頁 ─────────────────────────────────────────────
def crud_page(title, load_fn, pk_col,
              add_form_fn, edit_form_fn, del_fn,
              dialog_fn=None):

    # 標題列
    hc1, hc2 = st.columns([1, 9])
    with hc1:
        if st.button("← 返回"): nav("main")
    with hc2:
        st.subheader(title)

    # 新增按鈕
    if st.button("＋ 新增", type="primary"):
        open_dlg("add")

    # 讀取資料
    df = load_fn()
    st.write(f"共 **{len(df)}** 筆")

    # 表格 (可選列)
    event = st.dataframe(
        df, use_container_width=True, hide_index=True,
        on_select="rerun", selection_mode="single-row",
    )
    selected = event.selection.rows

    # 操作按鈕列
    bc1, bc2, _ = st.columns([1, 1, 8])
    with bc1:
        edit_click = st.button("✏️ 修改", disabled=(not selected))
    with bc2:
        del_click  = st.button("🗑️ 刪除", disabled=(not selected), type="primary")

    if selected:
        row = df.iloc[selected[0]].to_dict()
        if edit_click: open_dlg("edit", row)
        if del_click:  open_dlg("del",  row)

    # 彈窗
    dlg = st.session_state.dlg
    if dlg == "add":
        add_form_fn()
    elif dlg == "edit":
        edit_form_fn(st.session_state.dlg_row)
    elif dlg == "del":
        row = st.session_state.dlg_row
        st.warning(f"確認刪除「{row.get(pk_col, '')}」？")
        dc1, dc2, _ = st.columns([1, 1, 8])
        with dc1:
            if st.button("確認刪除", type="primary"):
                try:
                    del_fn(row[pk_col])
                    st.toast("刪除成功")
                    close_dlg()
                except Exception as e:
                    st.error(str(e))
        with dc2:
            if st.button("取消"): close_dlg()

# ── USER ─────────────────────────────────────────────────────
@st.dialog("用戶資料 - 新增")
def user_add_dlg():
    userid   = st.text_input("用戶代碼 *")
    username = st.text_input("用戶名稱 *")
    pwd      = st.text_input("用戶密碼 *")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("新增", type="primary", use_container_width=True):
            if not required(userid, username, pwd):
                st.error("必填欄位不可空白")
            else:
                try:
                    user_ins(userid, username, pwd)
                    st.toast("新增成功"); close_dlg()
                except Exception as e: st.error(str(e))
    with c2:
        if st.button("取消", use_container_width=True): close_dlg()

@st.dialog("用戶資料 - 修改")
def user_edit_dlg(row):
    st.text_input("用戶代碼", value=row["用戶代碼"], disabled=True)
    username = st.text_input("用戶名稱 *", value=row.get("用戶名稱",""))
    pwd      = st.text_input("用戶密碼 *", value=row.get("用戶密碼",""))
    c1, c2 = st.columns(2)
    with c1:
        if st.button("修改", type="primary", use_container_width=True):
            if not required(username, pwd):
                st.error("必填欄位不可空白")
            else:
                try:
                    user_upd(row["用戶代碼"], username, pwd)
                    st.toast("修改成功"); close_dlg()
                except Exception as e: st.error(str(e))
    with c2:
        if st.button("取消", use_container_width=True): close_dlg()

def page_user():
    crud_page("👤 USER 用戶資料維護", user_all, "用戶代碼",
              user_add_dlg, user_edit_dlg, user_del)

# ── CUST ─────────────────────────────────────────────────────
@st.dialog("客戶資料 - 新增")
def cust_add_dlg():
    code   = st.text_input("客戶代碼 *")
    name   = st.text_input("客戶名稱 *")
    remark = st.text_area("備註說明")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("新增", type="primary", use_container_width=True):
            if not required(code, name):
                st.error("必填欄位不可空白")
            else:
                try:
                    cust_ins(code, name, remark)
                    st.toast("新增成功"); close_dlg()
                except Exception as e: st.error(str(e))
    with c2:
        if st.button("取消", use_container_width=True): close_dlg()

@st.dialog("客戶資料 - 修改")
def cust_edit_dlg(row):
    st.text_input("客戶代碼", value=row["客戶代碼"], disabled=True)
    name   = st.text_input("客戶名稱 *", value=row.get("客戶名稱",""))
    remark = st.text_area("備註說明",    value=row.get("備註說明","") or "")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("修改", type="primary", use_container_width=True):
            if not required(name):
                st.error("必填欄位不可空白")
            else:
                try:
                    cust_upd(row["客戶代碼"], name, remark)
                    st.toast("修改成功"); close_dlg()
                except Exception as e: st.error(str(e))
    with c2:
        if st.button("取消", use_container_width=True): close_dlg()

def page_cust():
    crud_page("🏢 CUST 客戶資料維護", cust_all, "客戶代碼",
              cust_add_dlg, cust_edit_dlg, cust_del)

# ── FACT ─────────────────────────────────────────────────────
@st.dialog("廠商資料 - 新增")
def fact_add_dlg():
    code   = st.text_input("廠商代碼 *")
    name   = st.text_input("廠商名稱 *")
    remark = st.text_area("備註說明")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("新增", type="primary", use_container_width=True):
            if not required(code, name):
                st.error("必填欄位不可空白")
            else:
                try:
                    fact_ins(code, name, remark)
                    st.toast("新增成功"); close_dlg()
                except Exception as e: st.error(str(e))
    with c2:
        if st.button("取消", use_container_width=True): close_dlg()

@st.dialog("廠商資料 - 修改")
def fact_edit_dlg(row):
    st.text_input("廠商代碼", value=row["廠商代碼"], disabled=True)
    name   = st.text_input("廠商名稱 *", value=row.get("廠商名稱",""))
    remark = st.text_area("備註說明",    value=row.get("備註說明","") or "")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("修改", type="primary", use_container_width=True):
            if not required(name):
                st.error("必填欄位不可空白")
            else:
                try:
                    fact_upd(row["廠商代碼"], name, remark)
                    st.toast("修改成功"); close_dlg()
                except Exception as e: st.error(str(e))
    with c2:
        if st.button("取消", use_container_width=True): close_dlg()

def page_fact():
    crud_page("🏭 FACT 廠商資料維護", fact_all, "廠商代碼",
              fact_add_dlg, fact_edit_dlg, fact_del)

# ── ITEM ─────────────────────────────────────────────────────
def _fact_selectbox(cur_code, key):
    df_f = fact_raw()
    opts  = {f"{r['fact_code']}  {r['fact_name']}": r["fact_code"] for _, r in df_f.iterrows()}
    labels = list(opts.keys())
    idx = next((i for i, (_, c) in enumerate(opts.items()) if c == cur_code), 0)
    chosen = st.selectbox("主供應商 *", labels, index=idx, key=key)
    return opts[chosen]

@st.dialog("商品資料 - 新增")
def item_add_dlg():
    code = st.text_input("商品代碼 *")
    name = st.text_input("商品名稱 *")
    fc   = _fact_selectbox(None, "ia_fc")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("新增", type="primary", use_container_width=True):
            if not required(code, name):
                st.error("必填欄位不可空白")
            else:
                try:
                    item_ins(code, name, fc)
                    st.toast("新增成功"); close_dlg()
                except Exception as e: st.error(str(e))
    with c2:
        if st.button("取消", use_container_width=True): close_dlg()

@st.dialog("商品資料 - 修改")
def item_edit_dlg(row):
    st.text_input("商品代碼", value=row["商品代碼"], disabled=True)
    name = st.text_input("商品名稱 *", value=row.get("商品名稱",""))
    fc   = _fact_selectbox(row.get("廠商代碼"), "ie_fc")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("修改", type="primary", use_container_width=True):
            if not required(name):
                st.error("必填欄位不可空白")
            else:
                try:
                    item_upd(row["商品代碼"], name, fc)
                    st.toast("修改成功"); close_dlg()
                except Exception as e: st.error(str(e))
    with c2:
        if st.button("取消", use_container_width=True): close_dlg()

def page_item():
    crud_page("📦 ITEM 商品資料維護", item_all, "商品代碼",
              item_add_dlg, item_edit_dlg, item_del)

# ── Router ────────────────────────────────────────────────────
{"main": page_main, "user": page_user,
 "cust": page_cust, "fact": page_fact,
 "item": page_item}[st.session_state.page]()
