import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import sqlite3
from datetime import date
import random

# ----------------- 頁面基礎設定 -----------------
st.set_page_config(
    page_title="小獅子的集點卡",
    page_icon="🦁",
    layout="centered"
)

# ----------------- 本地 SQLite 資料庫 -----------------
DB_FILE = "running_simple.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_date TEXT NOT NULL,
            distance REAL NOT NULL,
            duration_mins INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_run(run_date, distance, duration_mins):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO runs (run_date, distance, duration_mins)
        VALUES (?, ?, ?)
    ''', (str(run_date), float(distance), int(duration_mins)))
    conn.commit()
    conn.close()

def get_runs():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM runs ORDER BY run_date DESC, id DESC", conn)
    conn.close()
    return df

def delete_run(run_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM runs WHERE id = ?", (run_id,))
    conn.commit()
    conn.close()

init_db()

# ----------------- 自訂暖心鼓勵語錄庫 -----------------
PRAISES = [
    "🌟 好厲害！今天也是很棒的一天喔！",
    "🦁🐨 小獅子和無尾熊在機艙為你熱烈鼓掌中！太厲害了！",
    "✈️ 今天的流汗超值得！集點印章成功蓋下，機票又更近一步！",
    "💖 意志力滿分！給認真跑步的你一個大大的擁抱！",
    "☁️ 咕嚕咕嚕～飛機加滿能量，今天也是超棒的一天！",
    "🐨 太棒了！無尾熊給你一個大抱抱！",
    "🦁 你好棒！成為更強壯的小獅子了！"
]

# ----------------- 柔和可愛插畫 CSS -----------------
st.markdown("""
<style>
    .stApp {
        background-color: #FDFBF7;
    }
    .hero-title {
        text-align: center;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #5D4037;
        margin-top: -15px;
        margin-bottom: 25px;
        font-weight: 800;
    }
    .stamp-item-active {
        width: 52px;
        height: 52px;
        background: #FFF3E0;
        border: 2px solid #FFB74D;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        box-shadow: 0 2px 5px rgba(255, 183, 77, 0.3);
        transform: rotate(-3deg);
    }
    .stamp-item-active .label {
        font-size: 10px;
        color: #E65100;
        font-weight: bold;
    }
    .stamp-item-empty {
        width: 52px;
        height: 52px;
        border: 2px dashed #CFD8DC;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #B0BEC5;
        font-size: 13px;
        font-weight: 500;
        background: #FAFAFA;
    }
    .metric-pill {
        background-color: #FFF8E1;
        border: 1px solid #FFE082;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- 頂部小獅子與無尾熊搭飛機插畫 -----------------
svg_html = """
<div style="display: flex; justify-content: center; align-items: center; width: 100%;">
<svg width="340" height="150" viewBox="0 0 340 150" fill="none" xmlns="http://www.w3.org/2000/svg">
    <!-- 雲朵 -->
    <path d="M40 110 A15 15 0 0 1 65 95 A25 25 0 0 1 105 100 A15 15 0 0 1 125 110 Z" fill="#E1F5FE" opacity="0.8"/>
    <path d="M220 50 A18 18 0 0 1 250 35 A28 28 0 0 1 295 40 A18 18 0 0 1 315 50 Z" fill="#E1F5FE" opacity="0.7"/>
    
    <!-- 飛機本體 -->
    <path d="M80 85 C80 60 210 60 250 78 C270 87 270 95 250 100 C200 110 80 105 80 85 Z" fill="#FFE082"/>
    <path d="M110 55 L135 78 L95 78 Z" fill="#FFB74D"/>
    <path d="M160 88 L190 120 L215 120 L195 88 Z" fill="#FFA726"/>
    
    <!-- 機窗 -->
    <circle cx="165" cy="80" r="14" fill="#81D4FA" stroke="#FFF" stroke-width="2"/>
    <circle cx="205" cy="80" r="14" fill="#81D4FA" stroke="#FFF" stroke-width="2"/>
    
    <!-- 窗戶 1: 波浪鬃毛小獅子 🦁 -->
    <g transform="translate(165, 80)">
        <circle cx="0" cy="-9.5" r="4.2" fill="#FFA726"/>
        <circle cx="6.7" cy="-6.7" r="4.2" fill="#FFA726"/>
        <circle cx="9.5" cy="0" r="4.2" fill="#FFA726"/>
        <circle cx="6.7" cy="6.7" r="4.2" fill="#FFA726"/>
        <circle cx="0" cy="9.5" r="4.2" fill="#FFA726"/>
        <circle cx="-6.7" cy="6.7" r="4.2" fill="#FFA726"/>
        <circle cx="-9.5" cy="0" r="4.2" fill="#FFA726"/>
        <circle cx="-6.7" cy="-6.7" r="4.2" fill="#FFA726"/>
        <circle cx="0" cy="0" r="9.5" fill="#FFA726"/>
        
        <circle cx="-5" cy="-6.5" r="2.2" fill="#FB8C00"/>
        <circle cx="5" cy="-6.5" r="2.2" fill="#FB8C00"/>
        
        <circle cx="0" cy="0.5" r="7.2" fill="#FFE082"/>
        
        <circle cx="-2.3" cy="0" r="0.85" fill="#4E342E"/>
        <circle cx="2.3" cy="0" r="0.85" fill="#4E342E"/>
        <ellipse cx="0" cy="2" rx="1.3" ry="0.9" fill="#E65100"/>
    </g>
    
    <!-- 窗戶 2: 無尾熊 🐨 -->
    <circle cx="198" cy="74" r="5" fill="#B0BEC5"/>
    <circle cx="212" cy="74" r="5" fill="#B0BEC5"/>
    <circle cx="205" cy="80" r="9" fill="#CFD8DC"/>
    <circle cx="202" cy="78" r="1" fill="#37474F"/>
    <circle cx="208" cy="78" r="1" fill="#37474F"/>
    <ellipse cx="205" cy="82" rx="2.5" ry="3.5" fill="#455A64"/>
    
    <!-- 愛心氣流 -->
    <g transform="translate(45, 75) scale(0.7)">
        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="#FF8A80"/>
    </g>
</svg>
</div>
"""
components.html(svg_html, height=155)

st.markdown("<h2 class='hero-title'>小獅子的跑步集點卡</h2>", unsafe_allow_html=True)

# ----------------- 讀取資料與點數計算 -----------------
runs_df = get_runs()

BASE_STAMPS = 55
total_stamps = BASE_STAMPS + len(runs_df)
total_dist = float(runs_df['distance'].sum()) if not runs_df.empty else 0.0
total_time = int(runs_df['duration_mins'].sum()) if not runs_df.empty else 0

# ----------------- 打卡輸入表單 -----------------
with st.container():
    with st.form("simple_run_form", clear_on_submit=True):
        st.markdown("#### 📝 今日跑步打卡")
        col_d, col_km, col_t = st.columns([1.2, 1, 1])
        
        with col_d:
            in_date = st.date_input("運動日期", value=date.today())
        with col_km:
            in_dist = st.number_input("跑了幾公里 (km)", min_value=0.1, max_value=100.0, value=3.0, step=0.5)
        with col_t:
            in_time = st.number_input("跑了多久 (分鐘)", min_value=1, max_value=600, value=30, step=1)
            
        submit_btn = st.form_submit_button("打卡蓋章！🦁✨", use_container_width=True)
        
        if submit_btn:
            add_run(in_date, in_dist, in_time)
            praise = random.choice(PRAISES)
            st.session_state['latest_praise'] = praise
            st.rerun()

if 'latest_praise' in st.session_state:
    st.balloons()
    st.success(st.session_state['latest_praise'])
    del st.session_state['latest_praise']

# ----------------- 儀表板數據膠囊 -----------------
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""
    <div class="metric-pill">
        <div style="font-size:12px; color:#8D6E63;">已收集印章</div>
        <div style="font-size:24px; font-weight:bold; color:#E65100;">{total_stamps} <span style="font-size:14px;">枚</span></div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="metric-pill">
        <div style="font-size:12px; color:#8D6E63;">後續累積里程</div>
        <div style="font-size:24px; font-weight:bold; color:#5D4037;">{total_dist:.1f} <span style="font-size:14px;">km</span></div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="metric-pill">
        <div style="font-size:12px; color:#8D6E63;">後續累積時間</div>
        <div style="font-size:24px; font-weight:bold; color:#5D4037;">{total_time} <span style="font-size:14px;">分鐘</span></div>
    </div>
    """, unsafe_allow_html=True)

# ----------------- 邁向機票進度條 -----------------
st.markdown("<br>", unsafe_allow_html=True)
next_target = 100 if total_stamps < 100 else 200
target_name = "單程機票 🎫" if total_stamps < 100 else "來回機票 🎫🎫"
progress = min(total_stamps / 200.0, 1.0)
st.progress(progress)
st.caption(f"🎯 目標進度：目前已完成 **{total_stamps} / {next_target}** 點（邁向 {target_name}）")

# ----------------- 集點印章卡（手機/電腦皆強制一行 5 個） -----------------
sheet_capacity = 20
current_sheet = (total_stamps // sheet_capacity) + 1
stamps_in_cur_sheet = total_stamps % sheet_capacity

if total_stamps > 0 and stamps_in_cur_sheet == 0:
    stamps_in_cur_sheet = sheet_capacity
    current_sheet -= 1

start_num = (current_sheet - 1) * sheet_capacity + 1

# 生成 20 個印章 HTML
stamps_markup = []
for i in range(sheet_capacity):
    num = start_num + i
    if num <= total_stamps:
        stamps_markup.append(f'''
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; width:48px; height:48px; background:#FFF3E0; border:2px solid #FFB74D; border-radius:50%; box-shadow:0 2px 5px rgba(255,183,77,0.3); transform:rotate(-3deg); margin:auto;">
            <span style="font-size:16px; line-height:1;">🦁</span>
            <span style="font-size:10px; color:#E65100; font-weight:bold; line-height:1; margin-top:2px;">#{num}</span>
        </div>
        ''')
    else:
        stamps_markup.append(f'''
        <div style="display:flex; align-items:center; justify-content:center; width:48px; height:48px; border:2px dashed #CFD8DC; border-radius:50%; color:#B0BEC5; font-size:12px; font-weight:500; background:#FAFAFA; margin:auto;">
            {num}
        </div>
        ''')

card_html = f'''
<div style="background:#FFFFFF; border:1.5px dashed #D7CCC8; border-radius:18px; padding:18px 12px 20px 12px; margin:5px 0 10px 0; box-shadow:0 3px 10px rgba(0,0,0,0.03); box-sizing:border-box;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; padding:0 6px;">
        <span style="font-weight:bold; color:#5D4037; font-size:15px;">🔖 集點卡第 {current_sheet} 張</span>
        <span style="font-size:13px; color:#8D6E63;">這張卡片已蓋 {stamps_in_cur_sheet} / {sheet_capacity} 個章</span>
    </div>
    <div style="display:grid; grid-template-columns: repeat(5, 1fr); row-gap:16px; column-gap:6px; justify-items:center; align-items:center;">
        {"".join(stamps_markup)}
    </div>
</div>
'''

components.html(card_html, height=355)

# ----------------- 歷史紀錄與管理 -----------------
with st.expander("📖 查看運動流水帳 / 刪除手誤紀錄"):
    if runs_df.empty:
        st.write("目前尚無新打卡紀錄（基礎 55 點已計入上方集點卡）～開始跑步蓋下第 56 枚印章吧！")
    else:
        show_df = runs_df[['run_date', 'distance', 'duration_mins']].copy()
        show_df.columns = ['日期', '距離 (km)', '時間 (分鐘)']
        st.dataframe(show_df, use_container_width=True, hide_index=True)
        
        del_id = st.selectbox(
            "選擇要刪除的紀錄：",
            options=runs_df['id'].tolist(),
            format_func=lambda x: f"編號 #{x} - {runs_df.loc[runs_df['id']==x, 'run_date'].values[0]} ({runs_df.loc[runs_df['id']==x, 'distance'].values[0]} km)"
        )
        if st.button("確認刪除此筆打卡"):
            delete_run(del_id)
            st.warning("已刪除紀錄！")
            st.rerun()
