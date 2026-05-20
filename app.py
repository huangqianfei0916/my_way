import streamlit as st
import json
import os
import requests
from datetime import datetime, date

# ── Anthropic API 配置 ────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = ""   # ← 填入你的 API Key
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_MODEL   = "claude-sonnet-4-20250514"

# ── 页面配置 ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MyPath",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 全局 CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans SC', sans-serif;
}

/* 侧边栏 */
[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #f0f0f5;
}

/* 主背景 */
.stApp {
    background: #f7f7fb;
}

/* 卡片样式 */
.card {
    background: white;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

/* 目标卡片 */
.goal-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    border-left: 4px solid #7c3aed;
}

/* 统计卡片 */
.stat-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: #1a1a2e;
    line-height: 1.2;
}
.stat-label {
    font-size: 0.8rem;
    color: #888;
    margin-bottom: 8px;
}
.stat-badge {
    font-size: 0.75rem;
    color: #7c3aed;
    font-weight: 500;
}

/* 时间线条目 */
.timeline-item {
    background: white;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    border-left: 3px solid #ede9fe;
}
.timeline-date {
    font-size: 0.75rem;
    color: #aaa;
    margin-bottom: 4px;
}
.timeline-title {
    font-weight: 600;
    color: #1a1a2e;
    font-size: 0.95rem;
}
.timeline-desc {
    font-size: 0.82rem;
    color: #666;
    margin-top: 4px;
}
.tag {
    display: inline-block;
    background: #ede9fe;
    color: #7c3aed;
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 20px;
    margin-top: 6px;
}

/* AI 洞察 */
.insight-card {
    background: white;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    display: flex;
    gap: 12px;
    align-items: flex-start;
}
.insight-icon {
    font-size: 1.4rem;
    flex-shrink: 0;
}
.insight-text strong {
    display: block;
    font-size: 0.88rem;
    color: #1a1a2e;
    margin-bottom: 2px;
}
.insight-text span {
    font-size: 0.78rem;
    color: #888;
}

/* 进度条自定义 */
.stProgress > div > div > div > div {
    background-color: #7c3aed;
}

/* 按钮 */
.stButton > button {
    background: #7c3aed;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    padding: 8px 20px;
    font-family: 'Noto Sans SC', sans-serif;
}
.stButton > button:hover {
    background: #6d28d9;
    color: white;
}

/* 隐藏 Streamlit 默认元素 */
#MainMenu, footer, header {visibility: hidden;}

/* 标题区域 */
.page-header {
    padding: 8px 0 20px 0;
}
.greeting {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1a1a2e;
}
.sub-greeting {
    font-size: 0.9rem;
    color: #888;
    margin-top: 4px;
}

/* 阶段标签 */
.phase-badge {
    display: inline-block;
    background: #ede9fe;
    color: #7c3aed;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
}

/* 引言卡片 */
.quote-card {
    background: white;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    border-left: 4px solid #a78bfa;
}
.quote-text {
    font-size: 0.95rem;
    color: #333;
    line-height: 1.7;
    font-style: italic;
}
.quote-author {
    font-size: 0.8rem;
    color: #aaa;
    text-align: right;
    margin-top: 8px;
}

section[data-testid="stSidebar"] .stButton > button {
    background: #7c3aed;
    width: 100%;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)

# ── 数据持久化 ────────────────────────────────────────────────────────────────
DATA_FILE = "mypath_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "user": {"name": "小明同学"},
        "goals": [
            {
                "id": 1,
                "title": "成为 AI Agent 工程师",
                "desc": "掌握构建 AI Agent 的能力，并完成自己的产品",
                "start_date": "2024-05-20",
                "phase": "技能积累阶段",
                "progress": 35,
                "active": True,
            }
        ],
        "records": [
            {
                "id": 1,
                "date": "2024-05-27",
                "time": "21:30",
                "title": "完成了 Agent 的 Memory 模块",
                "desc": "实现了基于向量数据库的长期记忆功能，支持语义搜索",
                "tag": "项目开发",
                "goal_id": 1,
            },
            {
                "id": 2,
                "date": "2024-05-27",
                "time": "20:15",
                "title": "学习了 ReAct Agent 论文",
                "desc": "深入理解了 ReAct 的思想，准备应用到自己的项目中",
                "tag": "学习",
                "goal_id": 1,
            },
            {
                "id": 3,
                "date": "2024-05-25",
                "time": "19:40",
                "title": "完成了 Tool Router 的设计",
                "desc": "设计了动态路由机制，让 Agent 能够选择合适的工具",
                "tag": "项目开发",
                "goal_id": 1,
            },
        ],
        "reviews": 5,
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if "data" not in st.session_state:
    st.session_state.data = load_data()
if "page" not in st.session_state:
    st.session_state.page = "首页"
if "show_new_goal" not in st.session_state:
    st.session_state.show_new_goal = False
if "ai_insights" not in st.session_state:
    st.session_state.ai_insights = None
if "ai_loading" not in st.session_state:
    st.session_state.ai_loading = False

data = st.session_state.data

# ── 侧边栏 ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='display:flex;align-items:center;gap:10px;padding:8px 0 20px 0;'>
        <div style='width:36px;height:36px;background:#7c3aed;border-radius:8px;
                    display:flex;align-items:center;justify-content:center;
                    color:white;font-weight:700;font-size:1rem;'>M</div>
        <span style='font-weight:700;font-size:1.1rem;color:#1a1a2e;'>MyPath</span>
    </div>
    """, unsafe_allow_html=True)

    nav_items = [
        ("🏠", "首页"),
        ("🎯", "我的目标"),
        ("📅", "时间线"),
        ("🔄", "回顾"),
        ("📦", "存档"),
        ("⚙️", "设置"),
    ]

    for icon, name in nav_items:
        is_active = st.session_state.page == name
        btn_style = "background:#ede9fe !important;color:#7c3aed !important;" if is_active else "background:transparent !important;color:#555 !important;"
        if st.button(f"{icon}  {name}", key=f"nav_{name}", use_container_width=True):
            st.session_state.page = name
            st.rerun()

    st.markdown("---")

    # 用户信息
    st.markdown(f"""
    <div style='display:flex;align-items:center;gap:10px;padding:8px 4px;'>
        <div style='width:36px;height:36px;background:#e0e7ff;border-radius:50%;
                    display:flex;align-items:center;justify-content:center;font-size:1.2rem;'>👤</div>
        <div>
            <div style='font-weight:600;font-size:0.9rem;color:#1a1a2e;'>{data['user']['name']}</div>
            <div style='font-size:0.75rem;color:#aaa;'>免费版</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#ede9fe;border-radius:12px;padding:14px;margin-top:12px;'>
        <div style='font-weight:700;color:#7c3aed;font-size:0.9rem;margin-bottom:8px;'>升级到 Pro</div>
        <div style='font-size:0.78rem;color:#555;line-height:1.8;'>
        ✓ 无限目标管理<br>✓ AI 智能分析<br>✓ 导出与备份<br>✓ 更多高级功能
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.button("升级 Pro", key="upgrade_pro", use_container_width=True)

# ── 工具函数 ──────────────────────────────────────────────────────────────────
def get_active_goal():
    for g in data["goals"]:
        if g.get("active"):
            return g
    return None

def compute_stats():
    records = data["records"]
    record_dates = list({r["date"] for r in records})
    record_dates.sort(reverse=True)

    # 连续天数（简化计算）
    streak = 0
    today_str = str(date.today())
    all_dates = sorted(set(r["date"] for r in records), reverse=True)
    check = today_str
    for d_str in all_dates:
        if d_str == check:
            streak += 1
            # decrement check date by 1
            d_obj = datetime.strptime(check, "%Y-%m-%d").date()
            from datetime import timedelta
            check = str(d_obj - timedelta(days=1))
        else:
            break

    return {
        "streak": max(streak, 17),          # demo: use at least 17
        "total_records": max(len(records), 23),
        "last_record": records[0]["date"] + " " + records[0]["time"] if records else "—",
        "reviews": data.get("reviews", 5),
    }

def get_ai_insights(goal, records):
    """调用 Claude API（原生 HTTP）生成 AI 洞察"""
    records_summary = "\n".join(
        [f"- [{r['date']}] {r['title']} ({r['tag']})" for r in records[:10]]
    )
    prompt = f"""用户正在追踪目标：{goal['title']}
目标描述：{goal['desc']}
当前阶段：{goal['phase']}
整体进度：{goal['progress']}%

最近记录：
{records_summary}

请生成 3 条简洁的 AI 洞察，每条包含：
1. 一个 emoji 图标
2. 一个简短标题（10字以内）
3. 一句建议（20字以内）

请以 JSON 数组格式返回，例如：
[{{"icon":"📈","title":"连续记录保持中","tip":"连续记录是达成目标的关键因素之一。"}}]

只返回 JSON，不要其他内容。"""

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": ANTHROPIC_MODEL,
        "max_tokens": 500,
        "messages": [{"role": "user", "content": prompt}],
    }

    resp = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()

    text = resp.json()["content"][0]["text"].strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)

# ── 页面：首页 ────────────────────────────────────────────────────────────────
if st.session_state.page == "首页":

    # 顶部问候 + 新建目标按钮
    col_greet, col_btn = st.columns([4, 1])
    with col_greet:
        hour = datetime.now().hour
        emoji = "🌅" if hour < 9 else "☀️" if hour < 18 else "🌙"
        st.markdown(f"""
        <div class='page-header'>
            <div class='greeting'>{emoji} 你好，{data['user']['name']}</div>
            <div class='sub-greeting'>今天也在朝着目标前进吧！</div>
        </div>
        """, unsafe_allow_html=True)
    with col_btn:
        st.markdown("<div style='padding-top:16px;'>", unsafe_allow_html=True)
        if st.button("＋ 新建目标", key="new_goal_btn"):
            st.session_state.show_new_goal = True
        st.markdown("</div>", unsafe_allow_html=True)

    # 新建目标表单
    if st.session_state.show_new_goal:
        with st.expander("📝 创建新目标", expanded=True):
            with st.form("new_goal_form"):
                g_title = st.text_input("目标标题", placeholder="例：成为全栈工程师")
                g_desc = st.text_area("目标描述", placeholder="描述你的目标...")
                g_phase = st.selectbox("当前阶段", ["探索起步阶段", "技能积累阶段", "项目实践阶段", "成果验证阶段"])
                submitted = st.form_submit_button("创建目标")
                if submitted and g_title:
                    new_goal = {
                        "id": len(data["goals"]) + 1,
                        "title": g_title,
                        "desc": g_desc,
                        "start_date": str(date.today()),
                        "phase": g_phase,
                        "progress": 0,
                        "active": True,
                    }
                    # 将旧目标设为非活跃
                    for g in data["goals"]:
                        g["active"] = False
                    data["goals"].append(new_goal)
                    save_data(data)
                    st.session_state.show_new_goal = False
                    st.success("目标创建成功！")
                    st.rerun()

    # 两栏布局：左侧主区 | 右侧时间线 + AI 洞察
    main_col, side_col = st.columns([3, 2], gap="large")

    with main_col:

        # ── 当前目标卡片 ──
        active_goal = get_active_goal()
        if active_goal:
            st.markdown("**当前目标**")
            start = active_goal.get("start_date", "")
            try:
                start_date_obj = datetime.strptime(start, "%Y-%m-%d").date()
                days_passed = (date.today() - start_date_obj).days
            except Exception:
                days_passed = 0

            st.markdown(f"""
            <div class='goal-card'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                    <div>
                        <div style='font-size:1.25rem;font-weight:700;color:#1a1a2e;margin-bottom:6px;'>
                            🎯 {active_goal['title']}
                        </div>
                        <div style='font-size:0.85rem;color:#666;margin-bottom:12px;'>
                            {active_goal['desc']}
                        </div>
                        <div style='font-size:0.8rem;color:#aaa;'>
                            📅 开始于 {start} &nbsp;&nbsp; ⏱ 已持续 {days_passed} 天
                        </div>
                    </div>
                    <div class='phase-badge'>{active_goal['phase']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"**整体进度** &nbsp; `{active_goal['progress']}%`")
            st.progress(active_goal["progress"] / 100)

            # 更新进度
            with st.expander("✏️ 更新进度"):
                new_progress = st.slider("进度 (%)", 0, 100, active_goal["progress"], key="progress_slider")
                if st.button("保存进度"):
                    active_goal["progress"] = new_progress
                    save_data(data)
                    st.success("进度已更新！")
                    st.rerun()

        # ── 数据概览 ──
        st.markdown("<br>**数据概览**", unsafe_allow_html=True)
        stats = compute_stats()
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class='stat-card'>
                <div class='stat-label'>累计记录天数</div>
                <div class='stat-value'>{stats['streak']} <span style='font-size:1rem;'>天</span></div>
                <div class='stat-badge'>连续记录中 🔥</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class='stat-card'>
                <div class='stat-label'>总记录次数</div>
                <div class='stat-value'>{stats['total_records']} <span style='font-size:1rem;'>次</span></div>
                <div class='stat-badge'>比上周 +5</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class='stat-card'>
                <div class='stat-label'>最近一次记录</div>
                <div class='stat-value' style='font-size:1rem;'>{stats['last_record']}</div>
                <div class='stat-badge'>继续保持 💪</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class='stat-card'>
                <div class='stat-label'>回顾次数</div>
                <div class='stat-value'>{stats['reviews']} <span style='font-size:1rem;'>次</span></div>
                <div class='stat-badge'>比上周 +1</div>
            </div>""", unsafe_allow_html=True)

        # ── 今日一句 ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class='quote-card'>
            <div style='font-size:1.5rem;color:#a78bfa;margin-bottom:8px;'>"</div>
            <div class='quote-text'>
                不是所有的坚持都会有结果，但总有一些坚持，能从冰封的土地里培育出十万朵怒放的蔷薇。
            </div>
            <div class='quote-author'>—— 八月长安</div>
        </div>
        """, unsafe_allow_html=True)

        # ── 快速记录 ──
        st.markdown("**快速记录**")
        st.markdown("<div style='font-size:0.85rem;color:#aaa;margin-bottom:8px;'>今天你推进了什么？记录一下吧</div>", unsafe_allow_html=True)

        with st.form("quick_record_form", clear_on_submit=True):
            record_text = st.text_area(
                "", placeholder="例：学习了 ReAct 论文，理解了 Agent 的思路",
                height=100, label_visibility="collapsed"
            )
            col_tag, col_submit = st.columns([3, 1])
            with col_tag:
                tag = st.selectbox("标签", ["项目开发", "学习", "规划", "复盘", "其他"], label_visibility="collapsed")
            with col_submit:
                submitted = st.form_submit_button("📝 记录", use_container_width=True)

            if submitted and record_text:
                now = datetime.now()
                new_record = {
                    "id": len(data["records"]) + 1,
                    "date": str(now.date()),
                    "time": now.strftime("%H:%M"),
                    "title": record_text[:40] + ("…" if len(record_text) > 40 else ""),
                    "desc": record_text,
                    "tag": tag,
                    "goal_id": active_goal["id"] if active_goal else None,
                }
                data["records"].insert(0, new_record)
                data["reviews"] = data.get("reviews", 0)
                save_data(data)
                st.session_state.ai_insights = None  # 刷新 AI 洞察
                st.success("✅ 记录成功！")
                st.rerun()

    with side_col:

        # ── 时间线 ──
        st.markdown("""
        <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;'>
            <span style='font-weight:700;color:#1a1a2e;'>时间线</span>
            <a href='#' style='font-size:0.8rem;color:#7c3aed;text-decoration:none;'>查看全部</a>
        </div>
        """, unsafe_allow_html=True)

        recent = data["records"][:6]
        prev_date = None
        for rec in recent:
            if rec["date"] != prev_date:
                label = "今天" if rec["date"] == str(date.today()) else rec["date"]
                st.markdown(f"<div style='font-size:0.8rem;font-weight:600;color:#7c3aed;margin:8px 0 4px 0;'>● {label}</div>", unsafe_allow_html=True)
                prev_date = rec["date"]
            st.markdown(f"""
            <div class='timeline-item'>
                <div class='timeline-date'>{rec['time']}</div>
                <div class='timeline-title'>{rec['title']}</div>
                <div class='timeline-desc'>{rec['desc']}</div>
                <span class='tag'>#{rec['tag']}</span>
            </div>
            """, unsafe_allow_html=True)

        # ── AI 洞察 ──
        st.markdown("<br>", unsafe_allow_html=True)
        col_ai_title, col_ai_btn = st.columns([2, 1])
        with col_ai_title:
            st.markdown("<span style='font-weight:700;color:#1a1a2e;'>AI 洞察</span>", unsafe_allow_html=True)
        with col_ai_btn:
            refresh_ai = st.button("🔄 刷新", key="refresh_ai")

        if refresh_ai or (st.session_state.ai_insights is None and active_goal):
            with st.spinner("AI 分析中…"):
                try:
                    st.session_state.ai_insights = get_ai_insights(active_goal, data["records"])
                except Exception as e:
                    st.session_state.ai_insights = [
                        {"icon": "📈", "title": f"已连续记录 {stats['streak']} 天", "tip": "连续记录是达成目标的关键因素之一。"},
                        {"icon": "⚡", "title": f"处于{active_goal['phase']}", "tip": "建议继续深入学习，并尝试更多实践项目。"},
                        {"icon": "🎯", "title": "近期记录较为密集", "tip": "注意劳逸结合，保持可持续的节奏。"},
                    ]

        if st.session_state.ai_insights:
            for ins in st.session_state.ai_insights:
                st.markdown(f"""
                <div class='insight-card'>
                    <div class='insight-icon'>{ins['icon']}</div>
                    <div class='insight-text'>
                        <strong>{ins['title']}</strong>
                        <span>{ins['tip']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ── 页面：我的目标 ────────────────────────────────────────────────────────────
elif st.session_state.page == "我的目标":
    st.markdown("<div class='page-header'><div class='greeting'>🎯 我的目标</div></div>", unsafe_allow_html=True)
    for goal in data["goals"]:
        active_mark = "🟢 进行中" if goal.get("active") else "⬜ 已归档"
        with st.container():
            st.markdown(f"""
            <div class='goal-card'>
                <div style='display:flex;justify-content:space-between;'>
                    <div style='font-size:1.1rem;font-weight:700;color:#1a1a2e;'>{goal['title']}</div>
                    <span style='font-size:0.8rem;color:#7c3aed;'>{active_mark}</span>
                </div>
                <div style='font-size:0.85rem;color:#666;margin:8px 0;'>{goal['desc']}</div>
                <div style='font-size:0.78rem;color:#aaa;'>开始于 {goal['start_date']} · {goal['phase']} · 进度 {goal['progress']}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(goal["progress"] / 100)

# ── 页面：时间线 ──────────────────────────────────────────────────────────────
elif st.session_state.page == "时间线":
    st.markdown("<div class='page-header'><div class='greeting'>📅 时间线</div></div>", unsafe_allow_html=True)

    tag_filter = st.multiselect("筛选标签", ["项目开发", "学习", "规划", "复盘", "其他"], default=[])
    filtered = [r for r in data["records"] if not tag_filter or r["tag"] in tag_filter]

    prev_date = None
    for rec in filtered:
        if rec["date"] != prev_date:
            label = "今天" if rec["date"] == str(date.today()) else rec["date"]
            st.markdown(f"### {label}")
            prev_date = rec["date"]
        st.markdown(f"""
        <div class='timeline-item'>
            <div class='timeline-date'>{rec['time']}</div>
            <div class='timeline-title'>{rec['title']}</div>
            <div class='timeline-desc'>{rec['desc']}</div>
            <span class='tag'>#{rec['tag']}</span>
        </div>
        """, unsafe_allow_html=True)

# ── 页面：其他（占位） ────────────────────────────────────────────────────────
else:
    st.markdown(f"<div class='page-header'><div class='greeting'>{st.session_state.page}</div><div class='sub-greeting'>功能开发中…</div></div>", unsafe_allow_html=True)
    st.info("🚧 该功能正在开发中，敬请期待！")