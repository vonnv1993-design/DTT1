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

# Custom CSS với typography tối ưu cho mobile
st.markdown("""
<style>
    /* Import font lớn và rõ nét */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Roboto', sans-serif !important;
    }
    
    /* Reset và base styles */
    .main .block-container {
        padding: 0.5rem;
        max-width: 480px;
        margin: 0 auto;
        font-size: 16px !important;
    }
    
    /* Mobile-first responsive */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.25rem;
            font-size: 18px !important;
        }
        
        .stColumns {
            gap: 0.5rem;
        }
    }
    
    /* Login form styles */
    .login-container {
        max-width: 400px;
        margin: 1rem auto;
        padding: 1.5rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border: 2px solid #e5e7eb;
    }
    
    .login-header {
        background: linear-gradient(135deg, #b8860b 0%, #daa520 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .login-header h2 {
        font-size: clamp(1.5rem, 6vw, 2rem) !important;
        margin: 0 !important;
        font-weight: 700 !important;
    }
    
    .login-header p {
        font-size: clamp(1rem, 4vw, 1.2rem) !important;
        margin: 0.5rem 0 0 0 !important;
        opacity: 0.95;
    }
    
    /* User info bar */
    .user-info {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: clamp(0.9rem, 4vw, 1rem) !important;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    .admin-badge, .referee-badge {
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        font-size: clamp(0.75rem, 3vw, 0.85rem) !important;
        font-weight: 700;
        margin-left: 0.5rem;
    }
    
    .admin-badge {
        background: #dc2626;
        color: white;
    }
    
    .referee-badge {
        background: #059669;
        color: white;
    }
    
    /* Header mobile-friendly */
    .mobile-header {
        background: linear-gradient(135deg, #b8860b 0%, #daa520 100%);
        padding: 1.5rem 1rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 16px rgba(184, 134, 11, 0.3);
    }
    
    .mobile-header h1 {
        margin: 0;
        font-size: clamp(1.8rem, 7vw, 2.5rem) !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .mobile-header p {
        margin: 0.5rem 0 0 0;
        font-size: clamp(1rem, 4vw, 1.3rem) !important;
        opacity: 0.95;
        font-weight: 500;
    }
    
    /* Navigation buttons */
    .stButton button {
        font-size: clamp(0.9rem, 4vw, 1.1rem) !important;
        font-weight: 600 !important;
        padding: 0.8rem 1rem !important;
        border-radius: 10px !important;
        min-height: 50px !important;
        transition: all 0.3s ease !important;
    }
    
    /* Group headers */
    .group-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 2px 10px rgba(30, 64, 175, 0.2);
    }
    
    .group-header h3 {
        margin: 0;
        font-size: clamp(1.2rem, 5vw, 1.5rem) !important;
        font-weight: 600 !important;
    }
    
    /* Match cards compact */
    .match-card {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.75rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        position: relative;
    }
    
    .match-card.readonly {
        background: #f9fafb;
        border-color: #d1d5db;
    }
    
    .match-title {
        font-weight: 700 !important;
        font-size: clamp(1rem, 4vw, 1.3rem) !important;
        margin-bottom: 0.75rem;
        color: #1e40af;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Team info compact */
    .team-info {
        text-align: center;
        padding: 0.5rem;
    }
    
    .team-name {
        font-weight: 700 !important;
        font-size: clamp(1rem, 4vw, 1.2rem) !important;
        margin-bottom: 0.25rem;
        color: #111827;
        line-height: 1.2;
    }
    
    .team-players {
        font-size: clamp(0.8rem, 3.5vw, 1rem) !important;
        color: #6b7280;
        font-style: italic;
        font-weight: 500;
        line-height: 1.2;
    }
    
    /* Score inputs - TỐI ƯU CHO 2 KÝ TỰ */
    .stNumberInput > div > div > input {
        text-align: center !important;
        font-size: clamp(1.5rem, 6vw, 2rem) !important;
        font-weight: 900 !important;
        padding: 0.75rem 0.25rem !important;
        border-radius: 10px !important;
        border: 3px solid #d1d5db !important;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        min-height: 60px !important;
        max-width: 80px !important;
        width: 80px !important;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
        margin: 0 auto !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #1e40af !important;
        box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.25), inset 0 1px 3px rgba(0, 0, 0, 0.1) !important;
        outline: none !important;
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
    }
    
    /* Readonly score display compact */
    .readonly-score {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%) !important;
        padding: 0.75rem 0.25rem !important;
        border-radius: 10px !important;
        text-align: center !important;
        font-weight: 900 !important;
        font-size: clamp(1.5rem, 6vw, 2rem) !important;
        color: #374151 !important;
        border: 3px solid #d1d5db !important;
        min-height: 60px !important;
        max-width: 80px !important;
        width: 80px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05) !important;
        margin: 0 auto !important;
    }
    
    /* VS text */
    .vs-text {
        text-align: center;
        font-size: clamp(1.5rem, 6vw, 2rem) !important;
        font-weight: 900 !important;
        color: #6b7280;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    /* Standings header */
    .standings-header {
        background: linear-gradient(135deg, #b8860b 0%, #daa520 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 2px 10px rgba(184, 134, 11, 0.2);
    }
    
    .standings-header h3 {
        margin: 0;
        font-size: clamp(1.2rem, 5vw, 1.5rem) !important;
        font-weight: 600 !important;
    }
    
    /* Standing items */
    .standing-item {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.75rem 0;
        background: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border-left: 4px solid transparent;
    }
    
    .standing-item.qualified {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        color: #1e40af;
        font-weight: 600;
        border-left-color: #1e40af;
    }
    
    .standing-item.not-qualified {
        background: #f9fafb;
        color: #374151;
        border-left-color: #d1d5db;
    }
    
    .standing-team-name {
        font-size: clamp(1rem, 4vw, 1.2rem) !important;
        font-weight: 700 !important;
        margin-bottom: 0.25rem;
        line-height: 1.2;
    }
    
    .standing-team-players {
        font-size: clamp(0.8rem, 3vw, 1rem) !important;
        color: #6b7280;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .standing-stats {
        font-size: clamp(0.9rem, 3.5vw, 1rem) !important;
        font-weight: 600;
        text-align: right;
    }
    
    /* Final match special styling */
    .final-match {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 3px solid #b8860b;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(184, 134, 11, 0.2);
    }
    
    /* Rankings */
    .ranking-item {
        background: linear-gradient(135deg, #fef3c7 0%, #dbeafe 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 6px solid #b8860b;
        box-shadow: 0 3px 15px rgba(0, 0, 0, 0.1);
    }
    
    .ranking-title {
        font-size: clamp(1.2rem, 5vw, 1.6rem) !important;
        font-weight: 700 !important;
        color: #b8860b;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    .ranking-team-name {
        font-weight: 700 !important;
        margin-bottom: 0.25rem;
        font-size: clamp(1rem, 4vw, 1.3rem) !important;
        color: #111827;
    }
    
    .ranking-team-players {
        color: #6b7280;
        font-size: clamp(0.9rem, 3.5vw, 1.1rem) !important;
        font-weight: 500;
    }
    
    .ranking-position {
        font-size: clamp(2.5rem, 10vw, 4rem) !important;
        font-weight: 900 !important;
        color: #1e40af;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        line-height: 0.9;
    }
    
    /* Action buttons */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%) !important;
        color: white !important;
        border: none !important;
        font-size: clamp(1rem, 4vw, 1.3rem) !important;
        font-weight: 700 !important;
        padding: 1rem 1.5rem !important;
        border-radius: 12px !important;
        min-height: 60px !important;
        box-shadow: 0 4px 15px rgba(30, 64, 175, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(30, 64, 175, 0.4) !important;
    }
    
    /* Save indicator */
    .save-indicator {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-size: clamp(1rem, 4vw, 1.2rem) !important;
        font-weight: 600;
        animation: fadeIn 0.5s ease-in;
        box-shadow: 0 2px 10px rgba(16, 185, 129, 0.3);
    }
    
    /* Edit indicator */
    .edit-indicator {
        background: #f59e0b;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-size: clamp(0.7rem, 2.5vw, 0.8rem) !important;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    
    /* Form elements */
    .stSelectbox > div > div {
        font-size: clamp(1rem, 4vw, 1.2rem) !important;
        padding: 0.75rem !important;
        border-radius: 8px !important;
        min-height: 50px !important;
    }
    
    .stTextInput > div > div > input {
        font-size: clamp(1rem, 4vw, 1.2rem) !important;
        padding: 0.75rem 1rem !important;
        border-radius: 8px !important;
        min-height: 50px !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-size: clamp(1rem, 4vw, 1.2rem) !important;
        font-weight: 600 !important;
    }
    
    /* Mobile responsive adjustments */
    @media (max-width: 640px) {
        .match-card {
            padding: 0.75rem;
        }
        
        .mobile-header {
            padding: 1.25rem 0.75rem;
        }
        
        .user-info {
            flex-direction: column;
            text-align: center;
            gap: 0.75rem;
        }
        
        .ranking-item {
            text-align: center;
        }
        
        .standing-stats {
            text-align: center !important;
            margin-top: 0.5rem;
        }
        
        .standing-row {
            flex-direction: column;
            text-align: center;
            gap: 0.5rem;
        }
    }
    
    /* Touch improvements */
    @media (hover: none) and (pointer: coarse) {
        .stButton button:hover {
            transform: none !important;
        }
    }
    
    /* Metrics compact */
    .metric-container {
        text-align: center;
        padding: 0.75rem;
        background: white;
        border-radius: 8px;
        box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: clamp(1.5rem, 6vw, 2rem) !important;
        font-weight: 700 !important;
        color: #1e40af;
    }
    
    .metric-label {
        font-size: clamp(0.8rem, 3vw, 1rem) !important;
        color: #6b7280;
        font-weight: 500;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
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
            "Tên đăng nhập:",
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
    
    with st.expander("📖 Hướng dẫn sử dụng", expanded=True):
        st.markdown("""
        **Tài khoản mẫu:**
        
        🔴 **Admin** (Quản trị viên)
        - Tên đăng nhập: `admin` | Mật khẩu: `123456`
        - Quyền: Xem và chỉnh sửa tất cả, quản lý hệ thống
        
        🟢 **Trọng tài Tú** (Bảng A)
        - Tên đăng nhập: `tu` | Mật khẩu: `123456`
        - Quyền: Chỉ chỉnh sửa các trận ở Bảng A
        
        🔵 **Trọng tài Quang** (Bảng B)
        - Tên đăng nhập: `quang` | Mật khẩu: `123456`
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
    """Render match card với input box tối ưu cho nhập 2 ký tự"""
    current_user = st.session_state.current_user
    can_edit = can_edit_match(current_user, match)
    
    card_class = "final-match" if is_final else "match-card"
    if not can_edit and current_user["role"] != "admin":
        card_class += " readonly"
    
    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
    
    # Match title
    title = ""
    if match["stage"] == "group":
        title = f"TRẬN {match['id']}"
    elif match["stage"] == "semi":
        title = "BÁN KẾT 1" if match["id"] == "SF1" else "BÁN KẾT 2"
    elif match["stage"] == "final":
        title = "🏆 CHUNG KẾT"
    
    # Thông tin chỉnh sửa
    edit_info = ""
    if match.get("edited_by"):
        edit_info = f'<span class="edit-indicator">{match["edited_by"]}</span>'
    
    st.markdown(f'<div class="match-title">{title} {edit_info}</div>', unsafe_allow_html=True)
    
    # Layout: Team - Score - VS - Score - Team
    col1, col2, col3, col4, col5 = st.columns([3, 1.2, 0.6, 1.2, 3])
    
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
                help="Nhập tỷ số đội 1 (0-99)"
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
                help="Nhập tỷ số đội 2 (0-99)"
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
role_badge = "admin-badge" if current_user["role"] == "admin" else "referee-badge"
role_text = "ADMIN" if current_user["role"] == "admin" else f"TRỌNG TÀI {current_user.get('group', '')}"

st.markdown(f"""
<div class="user-info">
    <div>
        <strong>👤 {current_user['name']}</strong>
        <span class="{role_badge}">{role_text}</span>
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

# Tính toán bảng xếp hạng
calculate_standings()

# Header
st.markdown("""
<div class="mobile-header">
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
    with st.expander("🔧 BẢNG ĐIỀU KHIỂN ADMIN", expanded=False):
        st.markdown("### 📊 THỐNG KÊ HỆ THỐNG")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            total_matches = len(st.session_state.matches)
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{total_matches}</div>
                <div class="metric-label">Tổng số trận</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            completed_matches = len([m for m in st.session_state.matches if m["score1"] is not None and m["score2"] is not None])
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{completed_matches}</div>
                <div class="metric-label">Trận hoàn thành</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            save_count = len(st.session_state.get('saved_matches', {}))
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{save_count}</div>
                <div class="metric-label">Lần lưu dữ liệu</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Reset data
        if st.button("🔄 RESET TOÀN BỘ DỮ LIỆU", type="secondary"):
            if st.checkbox("✅ Xác nhận reset (không thể hoàn tác)"):
                for key in ['matches', 'saved_matches', 'group_standings']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.success("✅ Đã reset toàn bộ dữ liệu!")
                st.rerun()

# Main content
if st.session_state.current_stage == 'group':
    # Group A
    if current_user["role"] == "admin" or current_user.get("group") == "A":
        st.markdown('<div class="group-header"><h3>BẢNG A - LỊCH THI ĐẤU</h3></div>', unsafe_allow_html=True)
        
        group_a_matches = [match for match in st.session_state.matches if match.get("group") == "A"]
        for match in group_a_matches:
            render_match_card(match)
    
    # Group B
    if current_user["role"] == "admin" or current_user.get("group") == "B":
        st.markdown('<div class="group-header"><h3>BẢNG B - LỊCH THI ĐẤU</h3></div>', unsafe_allow_html=True)
        
        group_b_matches = [match for match in st.session_state.matches if match.get("group") == "B"]
        for match in group_b_matches:
            render_match_card(match)
    
    # Save button cho trọng tài
    if current_user["role"] == "referee":
        if st.button("💾 LƯU TỶ SỐ VÒNG BẢNG", use_container_width=True, type="primary"):
            save_match_data()
            st.markdown('<div class="save-indicator">✅ ĐÃ LƯU TỶ SỐ THÀNH CÔNG!</div>', unsafe_allow_html=True)
    
    # Standings
    st.markdown("---")
    
    # Group A Standings
    st.markdown('<div class="standings-header"><h3>BẢNG XẾP HẠNG A</h3></div>', unsafe_allow_html=True)
    
    for i, standing in enumerate(st.session_state.group_standings["A"]):
        css_class = "qualified" if i < 2 else "not-qualified"
        st.markdown(f"""
        <div class="standing-item {css_class}">
            <div class="standing-row">
                <div>
                    <div class="standing-team-name">{i+1}. {standing["team"]["name"]}</div>
                    <div class="standing-team-players">{" + ".join(standing["team"]["players"])}</div>
                </div>
                <div class="standing-stats">
                    {standing["wins"]} THẮNG - {standing["losses"]} THUA<br>
                    HIỆU SỐ: {'+' if standing["points_diff"] >= 0 else ''}{standing["points_diff"]}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Group B Standings
    st.markdown('<div class="standings-header"><h3>BẢNG XẾP HẠNG B</h3></div>', unsafe_allow_html=True)
    
    for i, standing in enumerate(st.session_state.group_standings["B"]):
        css_class = "qualified" if i < 2 else "not-qualified"
        st.markdown(f"""
        <div class="standing-item {css_class}">
            <div class="standing-row">
                <div>
                    <div class="standing-team-name">{i+1}. {standing["team"]["name"]}</div>
                    <div class="standing-team-players">{" + ".join(standing["team"]["players"])}</div>
                </div>
                <div class="standing-stats">
                    {standing["wins"]} THẮNG - {standing["losses"]} THUA<br>
                    HIỆU SỐ: {'+' if standing["points_diff"] >= 0 else ''}{standing["points_diff"]}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Generate knockout (chỉ admin)
    if current_user["role"] == "admin":
        if (len(st.session_state.group_standings["A"]) >= 2 and 
            len(st.session_state.group_standings["B"]) >= 2):
            if st.button("🚀 TẠO LỊCH VÒNG LOẠI TRỰC TIẾP", use_container_width=True, type="primary"):
                generate_knockout_matches()
                st.success("✅ Đã tạo lịch bán kết!")
                st.rerun()

elif st.session_state.current_stage == 'semi':
    st.markdown('<div class="group-header"><h3>⚡ VÒNG BÁN KẾT</h3></div>', unsafe_allow_html=True)
    
    semi_matches = [match for match in st.session_state.matches if match["stage"] == "semi"]
    for match in semi_matches:
        render_match_card(match)
    
    if current_user["role"] == "admin":
        if st.button("🏆 TẠO LỊCH CHUNG KẾT", use_container_width=True, type="primary"):
            generate_final_matches()
            st.success("✅ Đã tạo lịch chung kết!")
            st.rerun()

elif st.session_state.current_stage == 'final':
    st.markdown('<div class="group-header"><h3>🏆 TRẬN CHUNG KẾT</h3></div>', unsafe_allow_html=True)
    
    final_matches = [match for match in st.session_state.matches if match["stage"] == "final"]
    for match in final_matches:
        render_match_card(match, is_final=True)
    
    # Final Rankings
    rankings = get_ranking_list()
    if rankings:
        st.markdown("---")
        st.markdown('<div class="standings-header"><h3>🎖️ KẾT QUẢ CUỐI CÙNG</h3></div>', unsafe_allow_html=True)
        
        for ranking in rankings:
            st.markdown(f"""
            <div class="ranking-item">
                <div style="display: flex; justify-content: space-between; align-items: center; gap: 1rem;">
                    <div style="flex: 1;">
                        <div class="ranking-title">{ranking["title"]}</div>
                        <div class="ranking-team-name">{ranking["team"]["name"]}</div>
                        <div class="ranking-team-players">{" + ".join(ranking["team"]["players"])}</div>
                    </div>
                    <div class="ranking-position">#{ranking["position"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 1.5rem; color: #6b7280; font-size: clamp(0.9rem, 3.5vw, 1.1rem); background: #f9fafb; border-radius: 10px; margin-top: 1.5rem;">
    <p><strong>🏓 GIẢI PICKLEBALL - HỆ THỐNG TRỌNG TÀI ĐIỆN TỬ</strong></p>
    <p>Phiên bản: 2.2 Mobile-Optimized | Người dùng: <strong>{current_user['name']}</strong></p>
    <p>📱 Tối ưu hoàn toàn cho điện thoại di động</p>
</div>
""", unsafe_allow_html=True)
