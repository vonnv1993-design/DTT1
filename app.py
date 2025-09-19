import streamlit as st
import pandas as pd
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional

# Cấu hình trang
st.set_page_config(
    page_title="Giải Pickleball - Hệ thống Trọng tài",
    page_icon="🏓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS cho web interface
st.markdown("""
<style>
    /* Import font chuyên nghiệp */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stActionButton {display:none;}
    
    /* Container setup */
    .main .block-container {
        padding: 1rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Login form */
    .login-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
    }
    
    .login-header {
        background: linear-gradient(135deg, #b59410 0%, #eab308 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .login-header h2 {
        font-size: 1.75rem !important;
        margin: 0 !important;
        font-weight: 700 !important;
    }
    
    .login-header p {
        font-size: 1.1rem !important;
        margin: 0.5rem 0 0 0 !important;
        opacity: 0.95;
    }
    
    /* User info bar */
    .user-info {
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 1rem;
    }
    
    .role-badge {
        padding: 0.375rem 0.75rem;
        border-radius: 5px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-left: 0.75rem;
    }
    
    .admin-badge {
        background: #dc2626;
        color: white;
    }
    
    .referee-badge {
        background: #059669;
        color: white;
    }
    
    /* Main header */
    .app-header {
        background: linear-gradient(135deg, #b59410 0%, #eab308 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 6px 20px rgba(181, 148, 16, 0.2);
    }
    
    .app-header h1 {
        margin: 0;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .app-header p {
        margin: 0.75rem 0 0 0;
        font-size: 1.25rem !important;
        opacity: 0.95;
        font-weight: 500;
    }
    
    /* Navigation */
    .nav-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .stButton button {
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 0.875rem 1.5rem !important;
        border-radius: 8px !important;
        min-height: 48px !important;
        transition: all 0.2s ease !important;
        text-transform: uppercase;
        letter-spacing: 0.025em;
    }
    
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%) !important;
        border: none !important;
        color: white !important;
        box-shadow: 0 3px 10px rgba(29, 78, 216, 0.3) !important;
    }
    
    .stButton button[kind="secondary"] {
        background: white !important;
        border: 2px solid #1d4ed8 !important;
        color: #1d4ed8 !important;
    }
    
    .stButton button:hover {
        transform: translateY(-1px) !important;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1.5rem 0 1rem 0;
        text-align: center;
        box-shadow: 0 3px 12px rgba(29, 78, 216, 0.2);
    }
    
    .section-header h3 {
        margin: 0;
        font-size: 1.375rem !important;
        font-weight: 600 !important;
    }
    
    /* Match cards */
    .match-card {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    
    .match-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .match-card.readonly {
        background: #f9fafb;
        border-color: #d1d5db;
    }
    
    .match-card.final-match {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 3px solid #b59410;
        box-shadow: 0 4px 16px rgba(181, 148, 16, 0.2);
    }
    
    /* Match title */
    .match-title {
        font-weight: 700 !important;
        font-size: 1.125rem !important;
        margin-bottom: 1rem;
        color: #1d4ed8;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .edit-badge {
        background: #f59e0b;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem !important;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    
    /* Match layout */
    .match-layout {
        display: grid;
        grid-template-columns: 1fr auto auto auto 1fr;
        gap: 1rem;
        align-items: center;
    }
    
    /* Team info */
    .team-info {
        text-align: center;
        padding: 0.75rem;
    }
    
    .team-name {
        font-weight: 600 !important;
        font-size: 1.125rem !important;
        margin-bottom: 0.375rem;
        color: #111827;
    }
    
    .team-players {
        font-size: 0.875rem !important;
        color: #6b7280;
        font-weight: 500;
    }
    
    /* Score inputs - Compact for web */
    .stNumberInput > div > div > input {
        text-align: center !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        padding: 0.75rem 0.5rem !important;
        border-radius: 8px !important;
        border: 2px solid #d1d5db !important;
        background: #f8fafc !important;
        width: 70px !important;
        height: 50px !important;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.2s ease !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #1d4ed8 !important;
        box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.15) !important;
        outline: none !important;
        background: #dbeafe !important;
    }
    
    /* Readonly scores */
    .readonly-score {
        background: #f3f4f6 !important;
        border: 2px solid #d1d5db !important;
        border-radius: 8px !important;
        width: 70px !important;
        height: 50px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #374151 !important;
    }
    
    /* VS separator */
    .vs-text {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #6b7280;
        text-align: center;
        padding: 0.5rem;
    }
    
    /* Standings */
    .standings-header {
        background: linear-gradient(135deg, #b59410 0%, #eab308 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0 1rem 0;
        text-align: center;
        box-shadow: 0 3px 12px rgba(181, 148, 16, 0.2);
    }
    
    .standings-header h3 {
        margin: 0;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
    }
    
    .standing-item {
        background: white;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        border-left: 4px solid transparent;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .standing-item.qualified {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left-color: #1d4ed8;
        color: #1e3a8a;
        font-weight: 600;
    }
    
    .standing-item.not-qualified {
        background: #f9fafb;
        border-left-color: #d1d5db;
        color: #374151;
    }
    
    .team-info-standing {
        flex: 1;
    }
    
    .team-name-standing {
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.25rem;
    }
    
    .team-players-standing {
        font-size: 0.875rem !important;
        color: #6b7280;
        font-weight: 500;
    }
    
    .team-stats {
        text-align: right;
        font-size: 0.875rem !important;
        font-weight: 600;
        line-height: 1.4;
    }
    
    /* Rankings */
    .ranking-item {
        background: linear-gradient(135deg, #fef3c7 0%, #dbeafe 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #b59410;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .ranking-info {
        flex: 1;
    }
    
    .ranking-title {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #b59410;
        margin-bottom: 0.5rem;
    }
    
    .ranking-team {
        font-size: 1.125rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.25rem;
        color: #111827;
    }
    
    .ranking-players {
        font-size: 0.875rem !important;
        color: #6b7280;
        font-weight: 500;
    }
    
    .ranking-position {
        font-size: 3rem !important;
        font-weight: 900 !important;
        color: #1d4ed8;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Action buttons */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%) !important;
        color: white !important;
        border: none !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        border-radius: 8px !important;
        min-height: 44px !important;
        box-shadow: 0 3px 12px rgba(29, 78, 216, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 5px 16px rgba(29, 78, 216, 0.4) !important;
    }
    
    .stButton button[kind="secondary"] {
        background: white !important;
        border: 2px solid #6b7280 !important;
        color: #6b7280 !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
        border-radius: 8px !important;
    }
    
    /* Success alerts */
    .success-alert {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-size: 0.875rem !important;
        font-weight: 600;
        animation: fadeIn 0.3s ease-in;
    }
    
    /* Form elements */
    .stSelectbox > div > div {
        font-size: 1rem !important;
        padding: 0.75rem !important;
        border-radius: 6px !important;
        min-height: 44px !important;
    }
    
    .stTextInput > div > div > input {
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
        border-radius: 6px !important;
        min-height: 44px !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    
    /* Metrics */
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .metric-card {
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e5e7eb;
    }
    
    .metric-value {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #1d4ed8;
        margin-bottom: 0.25rem;
    }
    
    .metric-label {
        font-size: 0.875rem !important;
        color: #6b7280;
        font-weight: 500;
        text-transform: uppercase;
    }
    
    /* Two column layout for groups */
    .groups-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin: 2rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem;
        background: #f9fafb;
        border-radius: 8px;
        margin-top: 2rem;
        border: 1px solid #e5e7eb;
    }
    
    .footer p {
        margin: 0.25rem 0 !important;
        font-size: 0.875rem !important;
        color: #6b7280;
    }
    
    .footer strong {
        color: #1d4ed8;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        .groups-container {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .match-layout {
            grid-template-columns: 1fr;
            gap: 1rem;
            text-align: center;
        }
        
        .standing-item {
            flex-direction: column;
            text-align: center;
            gap: 0.5rem;
        }
        
        .team-stats {
            text-align: center;
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Dữ liệu người dùng
USERS = {
    "admin": {
        "password": "123456",
        "role": "admin",
        "name": "Administrator",
        "permissions": ["view", "edit", "admin"]
    },
    "tu": {
        "password": "123456", 
        "role": "referee",
        "name": "Trọng tài Tú",
        "group": "A",
        "permissions": ["view", "edit_group_A"]
    },
    "quang": {
        "password": "123456",
        "role": "referee", 
        "name": "Trọng tài Quang",
        "group": "B",
        "permissions": ["view", "edit_group_B"]
    }
}

def authenticate(username, password):
    if username in USERS and USERS[username]["password"] == password:
        return USERS[username]
    return None

def save_match_data():
    if 'saved_matches' not in st.session_state:
        st.session_state.saved_matches = {}
    
    timestamp = datetime.now().isoformat()
    st.session_state.saved_matches[timestamp] = {
        "matches": st.session_state.matches.copy(),
        "user": st.session_state.current_user["name"],
        "stage": st.session_state.current_stage
    }

def can_edit_match(user, match):
    if user["role"] == "admin":
        return True
    
    if user["role"] == "referee":
        if match.get("group") == user.get("group"):
            return True
    
    return False

def show_login():
    st.markdown("""
    <div class="login-container">
        <div class="login-header">
            <h2>🏓 Đăng nhập Hệ thống</h2>
            <p>Giải Pickleball - Trọng tài</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.markdown("### 👤 Thông tin đăng nhập")
        
        username = st.selectbox(
            "Chọn tài khoản:",
            ["", "admin", "tu", "quang"],
            help="Chọn tài khoản của bạn"
        )
        
        password = st.text_input(
            "Mật khẩu:",
            type="password",
            help="Nhập mật khẩu (mặc định: 123456)"
        )
        
        submit = st.form_submit_button("🔓 ĐĂNG NHẬP", use_container_width=True, type="primary")
        
        if submit:
            if username and password:
                user = authenticate(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.current_user = user
                    st.session_state.username = username
                    st.success(f"✅ Đăng nhập thành công! Chào mừng {user['name']}")
                    st.rerun()
                else:
                    st.error("❌ Sai tên đăng nhập hoặc mật khẩu!")
            else:
                st.warning("⚠️ Vui lòng nhập đầy đủ thông tin!")
    
    with st.expander("📖 Hướng dẫn sử dụng", expanded=False):
        st.markdown("""
        **Tài khoản có sẵn:**
        
        🔴 **Admin** - Quản trị viên
        - Đăng nhập: `admin` | Mật khẩu: `123456`
        - Quyền: Xem và chỉnh sửa tất cả, quản lý hệ thống
        
        🟢 **Trọng tài Tú** - Phụ trách Bảng A  
        - Đăng nhập: `tu` | Mật khẩu: `123456`
        - Quyền: Chỉ chỉnh sửa các trận ở Bảng A
        
        🔵 **Trọng tài Quang** - Phụ trách Bảng B
        - Đăng nhập: `quang` | Mật khẩu: `123456`
        - Quyền: Chỉ chỉnh sửa các trận ở Bảng B
        """)

# Dữ liệu đội
teams = [
    {"id": 1, "name": "Đội 1", "players": ["Quân", "Quỳnh"], "group": "A"},
    {"id": 2, "name": "Đội 2", "players": ["Thông", "Linh"], "group": "A"},
    {"id": 3, "name": "Đội 3", "players": ["Thành", "Sơn"], "group": "A"},
    {"id": 4, "name": "Đội 4", "players": ["Minh", "Quang"], "group": "A"},
    {"id": 5, "name": "Đội 5", "players": ["Tú", "Tiến"], "group": "B"},
    {"id": 6, "name": "Đội 6", "players": ["Tuấn", "Diệp"], "group": "B"},
    {"id": 7, "name": "Đội 7", "players": ["Vơn", "Ngân"], "group": "B"},
    {"id": 8, "name": "Đội 8", "players": ["Trung", "Kiên"], "group": "B"},
]

# Khởi tạo session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'matches' not in st.session_state:
    st.session_state.matches = [
        # Group A
        {"id": "A1", "team1": teams[0], "team2": teams[1], "score1": None, "score2": None, "stage": "group", "group": "A", "edited_by": None, "edited_at": None},
        {"id": "A2", "team1": teams[2], "team2": teams[3], "score1": None, "score2": None, "stage": "group", "group": "A", "edited_by": None, "edited_at": None},
        {"id": "A3", "team1": teams[0], "team2": teams[2], "score1": None, "score2": None, "stage": "group", "group": "A", "edited_by": None, "edited_at": None},
        {"id": "A4", "team1": teams[1], "team2": teams[3], "score1": None, "score2": None, "stage": "group", "group": "A", "edited_by": None, "edited_at": None},
        {"id": "A5", "team1": teams[1], "team2": teams[2], "score1": None, "score2": None, "stage": "group", "group": "A", "edited_by": None, "edited_at": None},
        {"id": "A6", "team1": teams[0], "team2": teams[3], "score1": None, "score2": None, "stage": "group", "group": "A", "edited_by": None, "edited_at": None},
        # Group B
        {"id": "B1", "team1": teams[5], "team2": teams[7], "score1": None, "score2": None, "stage": "group", "group": "B", "edited_by": None, "edited_at": None},
        {"id": "B2", "team1": teams[6], "team2": teams[7], "score1": None, "score2": None, "stage": "group", "group": "B", "edited_by": None, "edited_at": None},
        {"id": "B3", "team1": teams[4], "team2": teams[6], "score1": None, "score2": None, "stage": "group", "group": "B", "edited_by": None, "edited_at": None},
        {"id": "B4", "team1": teams[4], "team2": teams[5], "score1": None, "score2": None, "stage": "group", "group": "B", "edited_by": None, "edited_at": None},
        {"id": "B5", "team1": teams[5], "team2": teams[6], "score1": None, "score2": None, "stage": "group", "group": "B", "edited_by": None, "edited_at": None},
        {"id": "B6", "team1": teams[4], "team2": teams[7], "score1": None, "score2": None, "stage": "group", "group": "B", "edited_by": None, "edited_at": None},
    ]

if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 'group'

if 'group_standings' not in st.session_state:
    st.session_state.group_standings = {"A": [], "B": []}

# Các hàm tính toán
def calculate_standings():
    for group in ["A", "B"]:
        group_teams = [team for team in teams if team["group"] == group]
        group_matches = [match for match in st.session_state.matches if match.get("group") == group]
        
        standings = []
        for team in group_teams:
            standing = {
                "team": team,
                "wins": 0,
                "losses": 0,
                "points_for": 0,
                "points_against": 0,
                "points_diff": 0
            }
            standings.append(standing)
        
        for match in group_matches:
            if match["score1"] is not None and match["score2"] is not None:
                team1_standing = next(s for s in standings if s["team"]["id"] == match["team1"]["id"])
                team2_standing = next(s for s in standings if s["team"]["id"] == match["team2"]["id"])
                
                team1_standing["points_for"] += match["score1"]
                team1_standing["points_against"] += match["score2"]
                team2_standing["points_for"] += match["score2"]
                team2_standing["points_against"] += match["score1"]
                
                if match["score1"] > match["score2"]:
                    team1_standing["wins"] += 1
                    team2_standing["losses"] += 1
                elif match["score2"] > match["score1"]:
                    team2_standing["wins"] += 1
                    team1_standing["losses"] += 1
        
        for standing in standings:
            standing["points_diff"] = standing["points_for"] - standing["points_against"]
        
        standings.sort(key=lambda x: (-x["wins"], -x["points_diff"], -x["points_for"]))
        st.session_state.group_standings[group] = standings

def generate_knockout_matches():
    if len(st.session_state.group_standings["A"]) < 2 or len(st.session_state.group_standings["B"]) < 2:
        return
    
    first_a = st.session_state.group_standings["A"][0]["team"]
    second_a = st.session_state.group_standings["A"][1]["team"]
    first_b = st.session_state.group_standings["B"][0]["team"]
    second_b = st.session_state.group_standings["B"][1]["team"]
    
    semi_matches = [
        {"id": "SF1", "team1": first_a, "team2": second_b, "score1": None, "score2": None, "stage": "semi", "edited_by": None, "edited_at": None},
        {"id": "SF2", "team1": first_b, "team2": second_a, "score1": None, "score2": None, "stage": "semi", "edited_by": None, "edited_at": None}
    ]
    
    group_matches = [match for match in st.session_state.matches if match["stage"] == "group"]
    st.session_state.matches = group_matches + semi_matches
    st.session_state.current_stage = 'semi'
    save_match_data()

def generate_final_matches():
    semi_matches = [match for match in st.session_state.matches if match["stage"] == "semi"]
    if len(semi_matches) < 2:
        return
    
    sf1 = next((match for match in semi_matches if match["id"] == "SF1"), None)
    sf2 = next((match for match in semi_matches if match["id"] == "SF2"), None)
    
    if (not sf1 or not sf2 or 
        sf1["score1"] is None or sf1["score2"] is None or
        sf2["score1"] is None or sf2["score2"] is None):
        return
    
    sf1_winner = sf1["team1"] if sf1["score1"] > sf1["score2"] else sf1["team2"]
    sf2_winner = sf2["team1"] if sf2["score1"] > sf2["score2"] else sf2["team2"]
    
    final_match = {
        "id": "FINAL",
        "team1": sf1_winner,
        "team2": sf2_winner,
        "score1": None,
        "score2": None,
        "stage": "final",
        "edited_by": None,
        "edited_at": None
    }
    
    other_matches = [match for match in st.session_state.matches if match["stage"] != "final"]
    st.session_state.matches = other_matches + [final_match]
    st.session_state.current_stage = 'final'
    save_match_data()

def get_ranking_list():
    final_match = next((match for match in st.session_state.matches if match["stage"] == "final"), None)
    semi_matches = [match for match in st.session_state.matches if match["stage"] == "semi"]
    
    if not final_match or final_match["score1"] is None or final_match["score2"] is None:
        return []
    
    champion = final_match["team1"] if final_match["score1"] > final_match["score2"] else final_match["team2"]
    runner_up = final_match["team2"] if final_match["score1"] > final_match["score2"] else final_match["team1"]
    
    if len(semi_matches) < 2:
        return []
    
    sf1 = next((match for match in semi_matches if match["id"] == "SF1"), None)
    sf2 = next((match for match in semi_matches if match["id"] == "SF2"), None)
    
    if (not sf1 or not sf2 or
        sf1["score1"] is None or sf1["score2"] is None or
        sf2["score1"] is None or sf2["score2"] is None):
        return []
    
    sf1_loser = sf1["team2"] if sf1["score1"] > sf1["score2"] else sf1["team1"]
    sf2_loser = sf2["team2"] if sf2["score1"] > sf2["score2"] else sf2["team1"]
    
    return [
        {"position": 1, "team": champion, "title": "🏆 Vô địch"},
        {"position": 2, "team": runner_up, "title": "🥈 Á quân"},
        {"position": 3, "team": sf1_loser, "title": "🥉 Đồng giải 3"},
        {"position": 3, "team": sf2_loser, "title": "🥉 Đồng giải 3"},
    ]

def render_match_card(match, is_final=False):
    """Render match card với layout tối ưu cho web"""
    current_user = st.session_state.current_user
    can_edit = can_edit_match(current_user, match)
    
    card_class = "match-card"
    if is_final:
        card_class += " final-match"
    if not can_edit and current_user["role"] != "admin":
        card_class += " readonly"
    
    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
    
    # Match title
    title = ""
    if match["stage"] == "group":
        title = f"Trận {match['id']}"
    elif match["stage"] == "semi":
        title = "Bán kết 1" if match["id"] == "SF1" else "Bán kết 2"
    elif match["stage"] == "final":
        title = "🏆 Chung kết"
    
    # Edit info
    edit_info = ""
    if match.get("edited_by"):
        edit_info = f'<span class="edit-badge">Cập nhật: {match["edited_by"]}</span>'
    
    st.markdown(f'<div class="match-title">{title}{edit_info}</div>', unsafe_allow_html=True)
    
    # Match layout: Team1 - Score1 - VS - Score2 - Team2
    col1, col2, col3, col4, col5 = st.columns([3, 1, 0.5, 1, 3])
    
    with col1:
        st.markdown(f"""
        <div class="team-info">
            <div class="team-name">{match['team1']['name']}</div>
            <div class="team-players">{' + '.join(match['team1']['players'])}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if can_edit or current_user["role"] == "admin":
            score1 = st.number_input(
                label="Tỷ số đội 1",
                min_value=0,
                max_value=99,
                value=match["score1"] or 0,
                key=f"score1_{match['id']}",
                label_visibility="collapsed",
                help="Tỷ số đội 1"
            )
            if score1 != (match["score1"] or 0):
                match["score1"] = score1
                match["edited_by"] = current_user["name"]
                match["edited_at"] = datetime.now().isoformat()
                save_match_data()
        else:
            st.markdown(f"""
            <div class="readonly-score">
                {match["score1"] or 0}
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="vs-text">-</div>', unsafe_allow_html=True)
    
    with col4:
        if can_edit or current_user["role"] == "admin":
            score2 = st.number_input(
                label="Tỷ số đội 2",
                min_value=0,
                max_value=99,
                value=match["score2"] or 0,
                key=f"score2_{match['id']}",
                label_visibility="collapsed",
                help="Tỷ số đội 2"
            )
            if score2 != (match["score2"] or 0):
                match["score2"] = score2
                match["edited_by"] = current_user["name"]
                match["edited_at"] = datetime.now().isoformat()
                save_match_data()
        else:
            st.markdown(f"""
            <div class="readonly-score">
                {match["score2"] or 0}
            </div>
            """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="team-info">
            <div class="team-name">{match['team2']['name']}</div>
            <div class="team-players">{' + '.join(match['team2']['players'])}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# === MAIN APP ===

# Kiểm tra xác thực
if not st.session_state.authenticated:
    show_login()
    st.stop()

# User info bar
current_user = st.session_state.current_user
role_badge_class = "admin-badge" if current_user["role"] == "admin" else "referee-badge"
role_text = "ADMIN" if current_user["role"] == "admin" else f"TRỌNG TÀI {current_user.get('group', '')}"

st.markdown(f"""
<div class="user-info">
    <div>
        <strong>👤 {current_user['name']}</strong>
        <span class="role-badge {role_badge_class}">{role_text}</span>
    </div>
    <div>
        <strong>🏓 Giải Pickleball 2024</strong>
    </div>
</div>
""", unsafe_allow_html=True)

# Logout button
if st.button("🚪 Đăng xuất", key="logout", type="secondary"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Calculate standings
calculate_standings()

# Main header
st.markdown("""
<div class="app-header">
    <h1>🏓 GIẢI PICKLEBALL</h1>
    <p>Hệ thống Trọng tài Điện tử</p>
</div>
""", unsafe_allow_html=True)

# Navigation
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📋 VÒNG BẢNG", key="nav_group", use_container_width=True, type="primary" if st.session_state.current_stage == 'group' else "secondary"):
        st.session_state.current_stage = 'group'

with col2:
    if st.button("⚡ BÁN KẾT", key="nav_semi", use_container_width=True, type="primary" if st.session_state.current_stage == 'semi' else "secondary"):
        st.session_state.current_stage = 'semi'

with col3:
    if st.button("🏆 CHUNG KẾT", key="nav_final", use_container_width=True, type="primary" if st.session_state.current_stage == 'final' else "secondary"):
        st.session_state.current_stage = 'final'

# Admin panel
if current_user["role"] == "admin":
    with st.expander("🔧 Bảng điều khiển Admin", expanded=False):
        st.markdown("### 📊 Thống kê hệ thống")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_matches = len(st.session_state.matches)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_matches}</div>
                <div class="metric-label">Tổng số trận</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            completed_matches = len([m for m in st.session_state.matches if m["score1"] is not None and m["score2"] is not None])
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{completed_matches}</div>
                <div class="metric-label">Trận hoàn thành</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            save_count = len(st.session_state.get('saved_matches', {}))
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{save_count}</div>
                <div class="metric-label">Lần lưu dữ liệu</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Reset data
        if st.button("🔄 Reset toàn bộ dữ liệu", type="secondary"):
            if st.checkbox("✅ Xác nhận reset (không thể hoàn tác)"):
                for key in ['matches', 'saved_matches', 'group_standings']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.success("✅ Đã reset toàn bộ dữ liệu!")
                st.rerun()

# Main content
if st.session_state.current_stage == 'group':
    
    # Layout 2 cột cho desktop, 1 cột cho mobile
    st.markdown('<div class="groups-container">', unsafe_allow_html=True)
    
    # Group A column
    if current_user["role"] == "admin" or current_user.get("group") == "A":
        st.markdown('<div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><h3>Bảng A - Lịch thi đấu</h3></div>', unsafe_allow_html=True)
        
        group_a_matches = [match for match in st.session_state.matches if match.get("group") == "A"]
        for match in group_a_matches:
            render_match_card(match)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Group B column
    if current_user["role"] == "admin" or current_user.get("group") == "B":
        st.markdown('<div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><h3>Bảng B - Lịch thi đấu</h3></div>', unsafe_allow_html=True)
        
        group_b_matches = [match for match in st.session_state.matches if match.get("group") == "B"]
        for match in group_b_matches:
            render_match_card(match)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Save button cho trọng tài
    if current_user["role"] == "referee":
        if st.button("💾 Lưu tỷ số vòng bảng", use_container_width=True, type="primary"):
            save_match_data()
            st.markdown('<div class="success-alert">✅ Đã lưu tỷ số thành công!</div>', unsafe_allow_html=True)
    
    # Standings layout 2 cột
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="standings-header"><h3>Bảng xếp hạng A</h3></div>', unsafe_allow_html=True)
        
        for i, standing in enumerate(st.session_state.group_standings["A"]):
            css_class = "qualified" if i < 2 else "not-qualified"
            st.markdown(f"""
            <div class="standing-item {css_class}">
                <div class="team-info-standing">
                    <div class="team-name-standing">{i+1}. {standing["team"]["name"]}</div>
                    <div class="team-players-standing">{" + ".join(standing["team"]["players"])}</div>
                </div>
                <div class="team-stats">
                    {standing["wins"]} Thắng - {standing["losses"]} Thua<br>
                    Hiệu số: {'+' if standing["points_diff"] >= 0 else ''}{standing["points_diff"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="standings-header"><h3>Bảng xếp hạng B</h3></div>', unsafe_allow_html=True)
        
        for i, standing in enumerate(st.session_state.group_standings["B"]):
            css_class = "qualified" if i < 2 else "not-qualified"
            st.markdown(f"""
            <div class="standing-item {css_class}">
                <div class="team-info-standing">
                    <div class="team-name-standing">{i+1}. {standing["team"]["name"]}</div>
                    <div class="team-players-standing">{" + ".join(standing["team"]["players"])}</div>
                </div>
                <div class="team-stats">
                    {standing["wins"]} Thắng - {standing["losses"]} Thua<br>
                    Hiệu số: {'+' if standing["points_diff"] >= 0 else ''}{standing["points_diff"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Generate knockout (chỉ admin)
    if current_user["role"] == "admin":
        if (len(st.session_state.group_standings["A"]) >= 2 and 
            len(st.session_state.group_standings["B"]) >= 2):
            st.markdown("---")
            if st.button("🚀 Tạo lịch vòng loại trực tiếp", key="gen_knockout", use_container_width=True, type="primary"):
                generate_knockout_matches()
                st.success("✅ Đã tạo lịch bán kết!")
                st.rerun()

elif st.session_state.current_stage == 'semi':
    st.markdown('<div class="section-header"><h3>⚡ Vòng bán kết</h3></div>', unsafe_allow_html=True)
    
    semi_matches = [match for match in st.session_state.matches if match["stage"] == "semi"]
    for match in semi_matches:
        render_match_card(match)
    
    if current_user["role"] == "admin":
        st.markdown("---")
        if st.button("🏆 Tạo lịch chung kết", key="gen_final", use_container_width=True, type="primary"):
            generate_final_matches()
            st.success("✅ Đã tạo lịch chung kết!")
            st.rerun()

elif st.session_state.current_stage == 'final':
    st.markdown('<div class="section-header"><h3>🏆 Trận chung kết</h3></div>', unsafe_allow_html=True)
    
    final_matches = [match for match in st.session_state.matches if match["stage"] == "final"]
    for match in final_matches:
        render_match_card(match, is_final=True)
    
    # Final Rankings
    rankings = get_ranking_list()
    if rankings:
        st.markdown("---")
        st.markdown('<div class="standings-header"><h3>🎖️ Kết quả cuối cùng</h3></div>', unsafe_allow_html=True)
        
        for ranking in rankings:
            st.markdown(f"""
            <div class="ranking-item">
                <div class="ranking-info">
                    <div class="ranking-title">{ranking["title"]}</div>
                    <div class="ranking-team">{ranking["team"]["name"]}</div>
                    <div class="ranking-players">{" + ".join(ranking["team"]["players"])}</div>
                </div>
                <div class="ranking-position">#{ranking["position"]}</div>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div class="footer">
    <p><strong>🏓 Giải Pickleball - Hệ thống Trọng tài Điện tử</strong></p>
    <p>Phiên bản: 3.0 Web Interface | Người dùng: <strong>{current_user['name']}</strong></p>
    <p>💻 Tối ưu cho Desktop & Tablet</p>
</div>
""", unsafe_allow_html=True)
