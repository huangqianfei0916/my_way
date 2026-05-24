import streamlit as st
import json
import os
from datetime import datetime, date, timedelta

# ── 页面配置 ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MyPath",
    page_icon="✦",
    layout="wide",
)

# ── 全局 CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,400;0,600;0,700;1,400&family=Noto+Sans+SC:wght@300;400;500;600&display=swap');

:root {
    --bg:          #F7F5F0;
    --surface:     #FFFFFF;
    --surface-2:   #FAF8F4;
    --border:      #EAE6DF;
    --border-dark: #D6CFC4;
    --ink-1:       #1C1917;
    --ink-2:       #57534E;
    --ink-3:       #A8A29E;
    --gold:        #B45309;
    --gold-mid:    #D97706;
    --gold-light:  #FEF3C7;
    --gold-bg:     #FFFBEB;
    --green:       #15803D;
    --green-light: #DCFCE7;
    --red:         #DC2626;
    --red-light:   #FEF2F2;
    --shadow-sm:   0 1px 3px rgba(28,25,23,0.06), 0 1px 2px rgba(28,25,23,0.04);
    --shadow-md:   0 4px 12px rgba(28,25,23,0.08), 0 2px 4px rgba(28,25,23,0.04);
    --radius-sm:   8px;
    --radius-md:   12px;
    --radius-lg:   16px;
}

html, body, [class*="css"] {
    font-family: 'Noto Sans SC', sans-serif;
    color: var(--ink-1);
}
.stApp { background: var(--bg) !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ══ 顶部导航栏 ═════════════════════════════════════════════════ */
.nav-bar {
    display: flex; align-items: center; gap: 4px;
    padding: 12px 0 16px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
}
.nav-brand {
    display: flex; align-items: center; gap: 8px; margin-right: 16px;
}
.nav-brand-mark {
    width: 28px; height: 28px;
    background: var(--ink-1); border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    color: #FAFAF7;
    font-family: 'Fraunces', serif; font-size: 0.85rem; font-weight: 700;
}
.nav-brand-name {
    font-family: 'Fraunces', serif;
    font-size: 0.95rem; font-weight: 600;
    color: var(--ink-1); letter-spacing: -0.01em;
}
.nav-spacer { flex: 1; }
.nav-user {
    font-size: 0.82rem; color: var(--ink-2);
    display: flex; align-items: center; gap: 6px;
}

/* ══ 隐藏默认侧边栏 ═══════════════════════════════════════════ */
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }

/* ══ 所有按钮基础（导航 / 普通操作） ════════════════════════════ */
.stButton > button {
    background: transparent !important;
    color: var(--ink-2) !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Noto Sans SC', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 400 !important;
    padding: 8px 12px !important;
    transition: all 0.15s ease !important;
    box-shadow: none !important;
}
.stButton > button:hover {
    background: var(--gold-bg) !important;
    color: var(--gold) !important;
}

/* Submit 按钮（表单提交） */
div[data-testid="stFormSubmitButton"] > button {
    background: var(--ink-1) !important;
    color: #FAFAF7 !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    padding: 9px 20px !important;
}
div[data-testid="stFormSubmitButton"] > button:hover {
    background: #292524 !important;
    color: #FAFAF7 !important;
}

/* 删除按钮：key 以 del_ 开头 → 灰色边框小按钮 */
[data-testid="stButton"]:has(button[kind="secondary"]) button,
div[data-testid^="stButton"] > button[data-testid*="del_"],
div[data-testid^="stButton"] > button[data-testid*="confirm_"] { }

/* 通用：带边框的小操作按钮（通过容器 class 区分） */
.btn-del button {
    background: transparent !important;
    color: var(--ink-3) !important;
    border: 1px solid var(--border-dark) !important;
    font-size: 0.8rem !important;
    padding: 4px 12px !important;
}
.btn-del button:hover {
    background: var(--red-light) !important;
    color: var(--red) !important;
    border-color: #FECACA !important;
}
.btn-confirm button {
    background: var(--red) !important;
    color: #fff !important;
    border: none !important;
    font-size: 0.8rem !important;
    padding: 4px 14px !important;
}
.btn-confirm button:hover {
    background: #B91C1C !important;
    color: #fff !important;
}

/* ══ 输入框 ══════════════════════════════════════════════════════ */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input {
    background: var(--surface) !important;
    color: var(--ink-1) !important;
    border: 1px solid var(--border-dark) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Noto Sans SC', sans-serif !important;
    font-size: 0.88rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--gold-mid) !important;
    box-shadow: 0 0 0 3px rgba(217,119,6,0.1) !important;
}

/* ══ Selectbox ══════════════════════════════════════════════════ */
[data-testid="stSelectbox"] > div > div {
    background: var(--surface) !important;
    color: var(--ink-1) !important;
    border: 1px solid var(--border-dark) !important;
    border-radius: var(--radius-sm) !important;
}

/* ══ Multiselect ════════════════════════════════════════════════ */
[data-testid="stMultiSelect"] > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border-dark) !important;
    border-radius: var(--radius-sm) !important;
}

/* ══ Slider ═════════════════════════════════════════════════════ */
[data-testid="stSlider"] [role="slider"] {
    background: var(--gold-mid) !important;
    border: none !important;
}

/* ══ 进度条 ═════════════════════════════════════════════════════ */
[data-testid="stProgress"] > div {
    background: var(--border) !important;
    border-radius: 100px !important;
    height: 5px !important;
}
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--gold-mid), #F59E0B) !important;
    border-radius: 100px !important;
}

/* ══ Expander ═══════════════════════════════════════════════════ */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    box-shadow: var(--shadow-sm) !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background: var(--surface-2) !important;
    padding: 16px !important;
    border-top: 1px solid var(--border) !important;
}

/* ══ Alert ══════════════════════════════════════════════════════ */
[data-testid="stAlert"] {
    border-radius: var(--radius-sm) !important;
    font-size: 0.85rem !important;
}

/* ══ 自定义组件 ══════════════════════════════════════════════════ */
.page-title {
    font-family: 'Fraunces', serif;
    font-size: 1.65rem; font-weight: 600;
    color: var(--ink-1); letter-spacing: -0.02em;
    line-height: 1.2; margin-bottom: 4px;
}
.page-subtitle {
    font-size: 0.85rem; color: var(--ink-3); margin-bottom: 22px;
}

/* Objective 卡片 */
.obj-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 20px 22px 16px 22px;
    margin-bottom: 8px;
    box-shadow: var(--shadow-sm);
    position: relative; overflow: hidden;
}
.obj-card::before {
    content: '';
    position: absolute; top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, var(--gold-mid), #F59E0B);
}
.obj-title {
    font-family: 'Fraunces', serif;
    font-size: 1.1rem; font-weight: 600;
    color: var(--ink-1); letter-spacing: -0.01em;
}
.obj-desc {
    font-size: 0.83rem; color: var(--ink-2);
    line-height: 1.6; margin: 6px 0 12px 0;
}
.obj-meta {
    font-size: 0.75rem; color: var(--ink-3);
    display: flex; gap: 14px; align-items: center;
}

/* KR 条目 */
.kr-item {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 12px 16px;
    margin-bottom: 8px;
}
.kr-header {
    display: flex; justify-content: space-between;
    align-items: flex-start; margin-bottom: 8px;
}
.kr-title {
    font-size: 0.88rem; font-weight: 500; color: var(--ink-1);
    line-height: 1.4; flex: 1;
}
.kr-progress-text {
    font-family: 'Fraunces', serif;
    font-size: 0.95rem; font-weight: 600;
    color: var(--gold-mid); white-space: nowrap; margin-left: 12px;
}
.kr-sub {
    font-size: 0.75rem; color: var(--ink-3); margin-top: 6px;
}

/* 统计卡片 */
.stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px 14px;
    box-shadow: var(--shadow-sm);
}
.stat-num {
    font-family: 'Fraunces', serif;
    font-size: 1.9rem; font-weight: 600;
    color: var(--ink-1); line-height: 1; letter-spacing: -0.03em;
}
.stat-unit { font-size: 0.82rem; color: var(--ink-2); font-weight: 300; }
.stat-label { font-size: 0.73rem; color: var(--ink-3); margin-top: 5px; }
.stat-badge {
    display: inline-block; font-size: 0.68rem;
    color: var(--green); background: var(--green-light);
    padding: 2px 6px; border-radius: 100px; margin-top: 5px;
}

/* 时间线 */
.tl-date-header {
    font-size: 0.7rem; font-weight: 600; color: var(--ink-3);
    text-transform: uppercase; letter-spacing: 0.08em;
    margin: 14px 0 8px 0;
    display: flex; align-items: center; gap: 8px;
}
.tl-date-header::after {
    content: ''; flex: 1; height: 1px; background: var(--border);
}
.tl-item {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 11px 14px; margin-bottom: 7px;
    box-shadow: var(--shadow-sm);
}
.tl-item:hover { border-color: var(--gold-mid); }
.tl-time { font-size: 0.68rem; color: var(--ink-3); letter-spacing: 0.04em; margin-bottom: 3px; }
.tl-title { font-size: 0.88rem; font-weight: 500; color: var(--ink-1); line-height: 1.4; }
.tl-desc { font-size: 0.79rem; color: var(--ink-2); margin-top: 4px; line-height: 1.5; }
.tag {
    display: inline-flex; align-items: center;
    font-size: 0.67rem; color: var(--gold);
    background: var(--gold-bg); border: 1px solid #FDE68A;
    padding: 2px 7px; border-radius: 100px; margin-top: 5px; font-weight: 500;
}
.kr-tag {
    display: inline-flex; align-items: center;
    font-size: 0.67rem; color: var(--ink-2);
    background: var(--surface-2); border: 1px solid var(--border);
    padding: 2px 7px; border-radius: 100px; margin-top: 5px; margin-left: 4px;
}

/* 引言 */
.quote-card {
    background: var(--ink-1); border-radius: var(--radius-lg);
    padding: 20px 22px; position: relative; overflow: hidden;
}
.quote-card::before {
    content: '❝';
    position: absolute; right: 18px; top: 8px;
    font-family: 'Fraunces', serif; font-size: 3.5rem;
    color: rgba(255,255,255,0.05); line-height: 1;
}
.quote-text {
    font-family: 'Fraunces', serif; font-size: 0.92rem;
    color: #FAF8F4; line-height: 1.75; font-style: italic;
}
.quote-author { font-size: 0.73rem; color: rgba(250,248,244,0.4); text-align: right; margin-top: 8px; }

.section-header {
    display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;
}
.section-title {
    font-size: 0.75rem; font-weight: 600; color: var(--ink-3);
    text-transform: uppercase; letter-spacing: 0.08em;
}

.phase-badge {
    display: inline-flex; align-items: center;
    background: var(--gold-bg); color: var(--gold);
    border: 1px solid #FDE68A; font-size: 0.7rem; font-weight: 500;
    padding: 3px 9px; border-radius: 100px; white-space: nowrap;
}

.user-info {
    display: flex; align-items: center; gap: 9px;
    padding: 10px 12px;
    background: var(--surface-2); border: 1px solid var(--border);
    border-radius: var(--radius-md);
}
.avatar {
    width: 30px; height: 30px;
    background: var(--gold-bg); border: 1px solid #FDE68A;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem; flex-shrink: 0;
}
.user-name { font-size: 0.85rem; font-weight: 600; color: var(--ink-1); }
.user-plan { font-size: 0.7rem; color: var(--ink-3); }

.empty-state {
    text-align: center; padding: 40px 20px;
    background: var(--surface); border: 1px dashed var(--border-dark);
    border-radius: var(--radius-lg);
}
.empty-icon { font-size: 2rem; margin-bottom: 10px; }
.empty-text { font-size: 0.88rem; color: var(--ink-3); }

@media (max-width: 768px) {
    .page-title { font-size: 1.3rem !important; }
    .obj-card, .kr-item { padding: 12px 14px !important; }
    .stat-num { font-size: 1.5rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ── 数据持久化 ────────────────────────────────────────────────────────────────
DATA_FILE = "mypath_data.json"

def default_data():
    return {
        "user": {"name": "小黄同学"},
        "objectives": [],
        "records": [],
    }

def migrate(d):
    """将旧版 goals 结构迁移到新版 objectives 结构"""
    if "goals" in d and "objectives" not in d:
        d["objectives"] = []
        for g in d.get("goals", []):
            d["objectives"].append({
                "id":           g.get("id", 1),
                "title":        g.get("title", ""),
                "desc":         g.get("desc", ""),
                "start_date":   g.get("start_date", str(date.today())),
                "phase":        g.get("phase", "技能积累阶段"),
                "active":       g.get("active", False),
                "key_results":  [],          # 旧数据没有 KR，留空
            })
        del d["goals"]
    # 兼容旧 records 字段：goal_id → obj_id
    for r in d.get("records", []):
        if "goal_id" in r and "obj_id" not in r:
            r["obj_id"] = r.pop("goal_id")
        r.setdefault("kr_id", None)
    # 确保顶层字段齐全
    d.setdefault("objectives", [])
    d.setdefault("records", [])
    d.setdefault("user", {"name": "同学"})
    return d

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return migrate(raw)
    return default_data()

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def next_id(lst):
    return max((x["id"] for x in lst), default=0) + 1

# ── Session State ─────────────────────────────────────────────────────────────
if "data"              not in st.session_state: st.session_state.data = load_data()
if "page"              not in st.session_state: st.session_state.page = "首页"

data = st.session_state.data

# ── 工具函数 ──────────────────────────────────────────────────────────────────
def get_active_obj():
    for o in data["objectives"]:
        if o.get("active"):
            return o
    return None

def compute_stats():
    records = data["records"]
    objectives = data["objectives"]
    streak, check = 0, str(date.today())
    for d_str in sorted(set(r["date"] for r in records), reverse=True):
        if d_str == check:
            streak += 1
            check = str(datetime.strptime(check, "%Y-%m-%d").date() - timedelta(days=1))
        else:
            break

    active_obj = get_active_obj()
    return {
        "objective_count": len(objectives),
        "record_count": len(records),
        "streak": streak,
    }

# ── 删除操作 ──────────────────────────────────────────────────────────────────
def delete_objective(obj_id):
    deleted_active = False
    for o in data["objectives"]:
        if o["id"] == obj_id:
            deleted_active = o.get("active", False)
    data["objectives"] = [o for o in data["objectives"] if o["id"] != obj_id]
    data["records"]    = [r for r in data["records"]    if r.get("obj_id") != obj_id]
    if deleted_active and data["objectives"]:
        data["objectives"][0]["active"] = True
    save_data(data)
    st.session_state.data = data

def delete_record(rec_id):
    data["records"] = [r for r in data["records"] if r["id"] != rec_id]
    save_data(data)
    st.session_state.data = data

# ── 顶部导航栏 ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='nav-bar'>
    <div class='nav-brand'>
        <div class='nav-brand-mark'>M</div>
        <div class='nav-brand-name'>MyPath</div>
    </div>
</div>
""", unsafe_allow_html=True)

nav_items = [("🏠","首页"), ("🎯","目标"), ("📅","时间线")]
nav_cols = st.columns([1, 1, 1, 4])
for i, (icon, name) in enumerate(nav_items):
    with nav_cols[i]:
        if st.button(f"{icon}  {name}", key=f"nav_{name}", use_container_width=True):
            st.session_state.page = name
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# 首页
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "首页":
    hour = datetime.now().hour
    greet = "早上好" if hour < 10 else "下午好" if hour < 18 else "晚上好"
    emoji = "🌅" if hour < 10 else "☀️" if hour < 18 else "🌙"
    st.markdown(f"""
    <div class='page-title'>{emoji}  {greet}，{data['user']['name']}</div>
    <div class='page-subtitle'>今天也在朝着目标前进吧 ✦</div>
    """, unsafe_allow_html=True)

    main_col, side_col = st.columns([3, 2], gap="large")

    with main_col:
        active_obj = get_active_obj()

        # ── 当前 Objective ──
        if active_obj:
            col_title, col_btn = st.columns([5, 1])
            with col_title:
                st.markdown("<div class='section-title' style='margin-bottom:10px;'>当前目标</div>", unsafe_allow_html=True)
            with col_btn:
                if st.button("＋ 新建", key="home_new_obj"):
                    st.session_state.page = "目标"
                    st.rerun()
            start = active_obj.get("start_date", "")
            try:
                days_passed = (date.today() - datetime.strptime(start, "%Y-%m-%d").date()).days
            except Exception:
                days_passed = 0
            rec_count = sum(1 for r in data["records"] if r.get("obj_id") == active_obj["id"])

            st.markdown(f"""
            <div class='obj-card'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;'>
                    <div class='obj-title'>✦ {active_obj['title']}</div>
                </div>
                <div class='obj-meta'>
                    <span>📅 {start}</span>
                    <span>⏱ 已坚持 {days_passed} 天</span>
                    <span>📝 {rec_count} 条记录</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.popover("🗑 删除目标", key=f"home_del_obj_{active_obj['id']}"):
                st.write("确定删除这个目标吗？")
                if st.button("确认删除", key=f"home_confirm_obj_{active_obj['id']}", type="primary"):
                    delete_objective(active_obj["id"])
                    st.rerun()
        else:
            st.markdown("""
            <div class='empty-state'>
                <div class='empty-icon'>🎯</div>
                <div class='empty-text'>还没有目标</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("＋ 创建目标", key="home_obj_empty_create"):
                st.session_state.page = "目标"
                st.rerun()

        # ── 数据概览 ──
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-title' style='margin-bottom:10px;'>数据概览</div>", unsafe_allow_html=True)
        stats = compute_stats()
        c1, c2, c3 = st.columns(3)
        for col, val, unit, label, badge in [
            (c1, stats["objective_count"], "个", "目标",     "方向明确"),
            (c2, stats["record_count"],    "条", "总记录",    "积少成多"),
            (c3, stats["streak"],          "天", "连续打卡",   "🔥 连续中"),
        ]:
            with col:
                st.markdown(f"""
                <div class='stat-card'>
                    <div><span class='stat-num'>{val}</span><span class='stat-unit'> {unit}</span></div>
                    <div class='stat-label'>{label}</div>
                    <div class='stat-badge'>{badge}</div>
                </div>
                """, unsafe_allow_html=True)

        # ── 所有目标 ──
        if len(data["objectives"]) > 1:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.markdown("<div class='section-title' style='margin-bottom:10px;'>所有目标</div>", unsafe_allow_html=True)
            for obj in data["objectives"]:
                if obj is active_obj:
                    continue  # 当前目标已在上面展示
                r_count = sum(1 for r in data["records"] if r.get("obj_id") == obj["id"])
                o_start = obj.get("start_date", "")
                st.markdown(f"""
                <div class='obj-card' style='opacity:0.75;'>
                    <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;'>
                        <div class='obj-title' style='font-size:0.95rem;'>✦ {obj['title']}</div>
                    </div>
                    <div class='obj-meta'>
                        <span>📅 {o_start}</span>
                        <span>📝 {r_count} 条记录</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                with st.popover("🗑 删除", key=f"home_del_other_{obj['id']}"):
                    st.write("确定删除这个目标吗？")
                    if st.button("确认删除", key=f"home_confirm_other_{obj['id']}", type="primary"):
                        delete_objective(obj["id"])
                        st.rerun()

        # ── 引言 ──
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='quote-card'>
            <div class='quote-text'>不是所有的坚持都会有结果，但总有一些坚持，能从冰封的土地里培育出十万朵怒放的蔷薇。</div>
            <div class='quote-author'>—— 八月长安</div>
        </div>
        """, unsafe_allow_html=True)

        # ── 快速记录 ──
        st.markdown("<div class='section-title' style='margin:18px 0 6px;'>快速记录</div>", unsafe_allow_html=True)

        if not data["objectives"]:
            st.markdown("""
            <div class='empty-state'>
                <div class='empty-icon'>🎯</div>
                <div class='empty-text'>请先创建目标，再开始记录</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("＋ 创建目标", key="home_create_obj_first"):
                st.session_state.page = "目标"
                st.rerun()
        else:
            with st.form("quick_record_form", clear_on_submit=True):
                record_text = st.text_area("记录内容", placeholder="今天推进了什么？写下来，积少成多…",
                                           height=85, label_visibility="collapsed")
                col_obj, col_tag, col_sub = st.columns([2.5, 2, 1])
                with col_obj:
                    obj_options = [o["title"] for o in data["objectives"]]
                    # 默认选择 active 目标
                    active_obj = get_active_obj()
                    default_idx = 0
                    if active_obj:
                        for i, o in enumerate(data["objectives"]):
                            if o["id"] == active_obj["id"]:
                                default_idx = i
                                break
                    sel_obj_idx = st.selectbox("关联目标", range(len(obj_options)),
                                               format_func=lambda i: obj_options[i],
                                               index=default_idx,
                                               label_visibility="collapsed")
                with col_tag:
                    tag = st.selectbox("标签", ["项目开发", "学习", "规划", "复盘", "其他"],
                                       label_visibility="collapsed")
                with col_sub:
                    submitted = st.form_submit_button("记录 →", use_container_width=True)

                if submitted and record_text:
                    now = datetime.now()
                    selected_obj = data["objectives"][sel_obj_idx]
                    new_rec = {
                        "id": next_id(data["records"]),
                        "date": str(now.date()),
                        "time": now.strftime("%H:%M"),
                        "title": record_text[:40] + ("…" if len(record_text) > 40 else ""),
                        "desc": record_text,
                        "tag": tag,
                        "obj_id": selected_obj["id"],
                    }
                    data["records"].insert(0, new_rec)
                    save_data(data)
                    st.success("✅ 记录成功！")
                    st.rerun()

    with side_col:
        # ── 时间线（只读预览） ──
        st.markdown("""
        <div class='section-header'>
            <span class='section-title'>最近记录</span>
        </div>
        """, unsafe_allow_html=True)

        active_obj = get_active_obj()

        prev_date = None
        for rec in data["records"][:8]:
            if rec["date"] != prev_date:
                label = "今天" if rec["date"] == str(date.today()) else rec["date"]
                st.markdown(f"<div class='tl-date-header'>{label}</div>", unsafe_allow_html=True)
                prev_date = rec["date"]
            st.markdown(f"""
            <div class='tl-item'>
                <div class='tl-time'>{rec['time']}</div>
                <div class='tl-title'>{rec['title']}</div>
                <div class='tl-desc'>{rec['desc']}</div>
                <span class='tag'>#{rec['tag']}</span>
            </div>
            """, unsafe_allow_html=True)

            with st.popover("🗑", key=f"home_del_rec_{rec['id']}"):
                st.write("确定删除这条记录吗？")
                if st.button("确认删除", key=f"home_confirm_rec_{rec['id']}", type="primary"):
                    delete_record(rec["id"])
                    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# 目标 页
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "目标":
    st.markdown("<div class='page-title'>目标</div><div class='page-subtitle'>设定方向，专注前行</div>", unsafe_allow_html=True)

    if not data["objectives"]:
        st.markdown("""
        <div class='empty-state'>
            <div class='empty-icon'>🎯</div>
            <div class='empty-text'>还没有目标，在下方输入框创建一个吧</div>
        </div>
        """, unsafe_allow_html=True)

    for obj in data["objectives"]:
        start = obj.get("start_date", "")
        active_mark = "进行中" if obj.get("active") else "已归档"
        badge_c = "var(--green)" if obj.get("active") else "var(--ink-3)"
        badge_bg = "var(--green-light)" if obj.get("active") else "var(--border)"

        # 统计该目标关联的记录数
        rec_count = sum(1 for r in data["records"] if r.get("obj_id") == obj["id"])

        st.markdown(f"""
        <div class='obj-card'>
            <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;'>
                <div class='obj-title'>✦ {obj['title']}</div>
                <span style='font-size:0.7rem;color:{badge_c};background:{badge_bg};
                             padding:3px 9px;border-radius:100px;font-weight:500;'>{active_mark}</span>
            </div>
            <div class='obj-meta'>
                <span>📅 {start}</span>
                <span>📝 {rec_count} 条记录</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 删除 Objective
        with st.popover("🗑 删除", use_container_width=True):
            st.write("确定删除这个目标吗？")
            if st.button("确认删除", key=f"confirm_obj_{obj['id']}", type="primary"):
                delete_objective(obj["id"])
                st.rerun()

        st.markdown("<hr style='border:none;border-top:1px solid var(--border);margin:20px 0;'>", unsafe_allow_html=True)

    # ── 底部内联创建目标 ──
    if len(data["objectives"]) >= 5:
        st.markdown("""
        <div class='empty-state'>
            <div class='empty-icon'>📋</div>
            <div class='empty-text'>已达到目标数量上限（5个），请删除不再需要的目标后再创建</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='section-title' style='margin-bottom:8px;'>＋ 新建目标</div>", unsafe_allow_html=True)
        with st.form("new_obj_form_bottom", clear_on_submit=True):
            g_title = st.text_input("输入目标名称", placeholder="例：成为全栈工程师、每天阅读…", label_visibility="collapsed")
            if st.form_submit_button("创建"):
                if g_title:
                    for o in data["objectives"]: o["active"] = False
                    data["objectives"].append({
                        "id": next_id(data["objectives"]),
                        "title": g_title,
                        "start_date": str(date.today()),
                        "active": True,
                    })
                    save_data(data)
                    st.session_state.data = data
                    st.session_state.page = "首页"
                    st.success("目标已创建！")
                    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# 时间线
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "时间线":
    st.markdown("<div class='page-title'>时间线</div><div class='page-subtitle'>你的每一条记录，都是进步的证明</div>", unsafe_allow_html=True)

    tag_filter = st.multiselect("筛选标签", ["项目开发", "学习", "规划", "复盘", "其他"])
    filtered = [r for r in data["records"] if not tag_filter or r["tag"] in tag_filter]

    if not filtered:
        st.markdown("<div class='empty-state'><div class='empty-icon'>📋</div><div class='empty-text'>暂无记录</div></div>", unsafe_allow_html=True)

    prev_date = None
    for rec in filtered:
        if rec["date"] != prev_date:
            label = "今天" if rec["date"] == str(date.today()) else rec["date"]
            st.markdown(f"<div class='tl-date-header' style='margin-top:18px;'>{label}</div>", unsafe_allow_html=True)
            prev_date = rec["date"]

        st.markdown(f"""
        <div class='tl-item'>
            <div class='tl-time'>{rec['time']}</div>
            <div class='tl-title'>{rec['title']}</div>
            <div class='tl-desc'>{rec['desc']}</div>
            <span class='tag'>#{rec['tag']}</span>
        </div>
        """, unsafe_allow_html=True)

        # 删除记录
        with st.popover("🗑 删除", use_container_width=True):
            st.write("确定删除这条记录吗？")
            if st.button("确认删除", key=f"confirm_rec_{rec['id']}", type="primary"):
                delete_record(rec["id"])
                st.rerun()

        st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 其他页面占位
# ═══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown(f"<div class='page-title'>{st.session_state.page}</div><div class='page-subtitle'>该功能正在建设中，敬请期待</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='empty-state' style='margin-top:24px;'>
        <div class='empty-icon'>🚧</div>
        <div class='empty-text'>功能开发中</div>
    </div>
    """, unsafe_allow_html=True)