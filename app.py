"""
WEB-BASED 3-TIER 資料維護系統 - Streamlit 版
Tier1: Streamlit UI  |  Tier2: Python 業務邏輯  |  Tier3: SQL Server
"""
import streamlit as st
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

    st.markdown("""
    <style>
    .card-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;max-width:560px;margin:24px auto}
    .card-link{text-decoration:none}
    .card-box{background:#fff;border-radius:10px;padding:36px 20px 32px;text-align:center;
              box-shadow:0 2px 8px rgba(0,0,0,.08);cursor:pointer;
              transition:box-shadow .2s,transform .2s;border-top:5px solid}
    .card-box:hover{box-shadow:0 8px 24px rgba(0,0,0,.16);transform:translateY(-4px)}
    .card-box:active{transform:translateY(-1px)}
    .c-icon{font-size:40px;margin-bottom:16px}
    .c-en{font-size:13px;color:#999;letter-spacing:1px;font-weight:600}
    .c-zh{font-size:17px;font-weight:700;color:#1a1a1a;margin-top:4px}
    .u{border-top-color:#1677ff}.c{border-top-color:#52c41a}
    .f{border-top-color:#fa8c16}.i{border-top-color:#722ed1}
    </style>
    <div class="card-grid">
      <a class="card-link" href="?nav=user">
        <div class="card-box u"><div class="c-icon">👤</div><div class="c-en">USER</div><div class="c-zh">用戶資料維護</div></div>
      </a>
      <a class="card-link" href="?nav=cust">
        <div class="card-box c"><div class="c-icon">🏢</div><div class="c-en">CUST</div><div class="c-zh">客戶資料維護</div></div>
      </a>
      <a class="card-link" href="?nav=fact">
        <div class="card-box f"><div class="c-icon">🏭</div><div class="c-en">FACT</div><div class="c-zh">廠商資料維護</div></div>
      </a>
      <a class="card-link" href="?nav=item">
        <div class="card-box i"><div class="c-icon">📦</div><div class="c-en">ITEM</div><div class="c-zh">商品資料維護</div></div>
      </a>
    </div>
    """, unsafe_allow_html=True)

# ── 表格樣式 ─────────────────────────────────────────────────
TABLE_CSS = """
<style>
.tbl{width:100%;border-collapse:collapse;font-size:14px}
.tbl th{background:#fafafa;padding:10px 12px;text-align:left;font-weight:600;
        color:#555;border-bottom:2px solid #f0f0f0;white-space:nowrap}
.tbl td{padding:9px 12px;border-bottom:1px solid #f5f5f5;color:#333;vertical-align:middle}
.tbl tr:hover td{background:#fafafa}
</style>
"""

def render_table(df, pk_col, on_edit, on_del):
    """每列內嵌修改/刪除按鈕，對齊前端 Table + 操作欄設計"""
    st.markdown(TABLE_CSS, unsafe_allow_html=True)

    # 表頭（欄位列 + 操作欄）
    data_cols = list(df.columns)
    widths = [3] * len(data_cols) + [1, 1]
    header = st.columns(widths)
    for i, col in enumerate(data_cols):
        header[i].markdown(f"**{col}**")
    header[-2].markdown("**操作**")

    st.divider()

    # 資料列
    for _, row in df.iterrows():
        cols = st.columns(widths)
        for i, col in enumerate(data_cols):
            val = row[col]
            cols[i].write("" if val is None else str(val))
        with cols[-2]:
            if st.button("修改", key=f"e_{row[pk_col]}", use_container_width=True):
                on_edit(row.to_dict())
        with cols[-1]:
            if st.button("刪除", key=f"d_{row[pk_col]}", type="primary",
                         use_container_width=True):
                on_del(row.to_dict())

# ── 刪除確認 Dialog ───────────────────────────────────────────
@st.dialog("確認刪除")
def del_confirm_dlg(del_fn, pk_col):
    row = st.session_state.dlg_row
    st.warning(f"確認刪除「**{row.get(pk_col, '')}**」？此操作無法復原。")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("確認刪除", type="primary", use_container_width=True):
            try:
                del_fn(row[pk_col])
                st.toast("刪除成功")
                close_dlg()
            except Exception as e:
                st.error(str(e))
    with c2:
        if st.button("取消", use_container_width=True):
            close_dlg()

# ── 共用 CRUD 頁 ─────────────────────────────────────────────
def crud_page(title, load_fn, pk_col, add_form_fn, edit_form_fn, del_fn):
    # 標題列
    hc1, hc2 = st.columns([1, 9])
    with hc1:
        if st.button("← 返回"): nav("main")
    with hc2:
        st.subheader(title)

    # 新增按鈕
    if st.button("＋ 新增", type="primary"):
        open_dlg("add")

    # 資料表格（每列有修改/刪除）
    df = load_fn()
    st.caption(f"共 {len(df)} 筆")
    render_table(df, pk_col,
                 on_edit=lambda r: open_dlg("edit", r),
                 on_del =lambda r: open_dlg("del",  r))

    # 彈窗
    dlg = st.session_state.dlg
    if dlg == "add":
        add_form_fn()
    elif dlg == "edit":
        edit_form_fn(st.session_state.dlg_row)
    elif dlg == "del":
        del_confirm_dlg(del_fn, pk_col)

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
