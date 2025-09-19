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

# Custom CSS (giữ nguyên)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stActionButton {display:none;}
    
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
    
    /* Status indicators */
    .status-pending {
        background: #6b7280;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .status-saved {
        background: #f59e0b;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .status-approved {
        background: #10b981;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
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
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .match-card.pending-approval {
        border-color: #f59e0b;
        background: #fffbeb;
    }
    
    .match-card.approved {
        border-color: #10b981;
        background: #f0fdf4;
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
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5rem;
        flex-wrap: wrap;
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
    
    /* Score inputs */
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
        margin: 0 auto !important;
    }
    
    .vs-text {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #6b7280;
        text-align: center;
        padding: 0.5rem;
    }
    
    /* Approval section */
    .approval-section {
        background: #fffbeb;
        border: 2px solid #f59e0b;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .approval-header {
        color: #92400e;
        font-size: 1.25rem !important;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
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
    
    .warning-alert {
        background: #f59e0b;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-size: 0.875rem !important;
        font-weight: 600;
    }
    
    .info-alert {
        background: #3b82f6;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-size: 0.875rem !important;
        font-weight: 600;
    }
    
    /* Metrics */
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
    
    /* Responsive */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
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
        "permissions": ["view", "edit", "admin", "approve"]
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

def get_match_status(match):
    """Lấy trạng thái của trận đấu"""
    if match.get("approved"):
        return "approved"
    elif match.get("saved_by_referee"):
        return "saved"
    else:
        return "pending"

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
        **Quy trình làm việc:**
        
        1. **Trọng tài** nhập tỷ số và lưu
        2. **Admin** xem tỷ số và phê duyệt  
        3. **Admin** tạo lịch bán kết và chung kết
        4. **Kết quả** được hiển thị tự động
        
        **Tài khoản:**
        
        🔴 **Admin** - `admin` / `123456`
        🟢 **Trọng tài Tú** - `tu` / `123456` (Bảng A)
        🔵 **Trọng tài Quang** - `quang` / `123456` (Bảng B)
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
        {"id": "A1", "team1": teams[0], "team2": teams[1], "score1": None, "score2": None, "stage": "group", "group": "A", "edited_by": None, "edited_at": None, "saved_by_referee": False, "approved": False},
        {"id": "A2", "team1": teams[2], "team2": teams[3], "score1": None, "score2": None, "stage": "group", "group": "A", "edited_by": None, "edited_at": None, "saved_by_referee": False, "approved": False},
        {"id": "A3", "team1": teams[0], "team2": teams[2], "score1": None, "score2": None, "stage": "group", "group": "A", "edited_by": None, "edited_at": None, "saved_by_referee": False, "approved": False},
        {"id": "A4", "team1": teams[1], "team2": teams[3], "score1": None, "score2": None, "stage": "group", "group": "A", "edited_by": None, "edited_at": None, "saved_by_referee": False, "approved": False},
        {"id": "A5", "team1": teams[1], "team2": teams[2], "score1": None, "score2": None, "stage": "group", "group": "A", "edited_by": None, "edited_at": None, "saved_by_referee": False, "approved": False},
        {"id": "A6", "team1": teams[0], "team2": teams[3], "score1": None, "score2": None, "stage": "group", "group": "A", "edited_by": None, "edited_at": None, "saved_by_referee": False, "approved": False},
        # Group B
        {"id": "B1", "team1": teams[5], "team2": teams[7], "score1": None, "score2": None, "stage": "group", "group": "B", "edited_by": None, "edited_at": None, "saved_by_referee": False, "approved": False},
        {"id": "B2", "team1": teams[6], "team2": teams[7], "score1": None, "score2": None, "stage": "group", "group": "B", "edited_by": None, "edited_at": None, "saved_by_referee": False, "approved": False},
        {"id": "B3", "team1": teams[4], "team2": teams[6], "score1": None, "score2": None, "stage": "group", "group": "B", "edited_by": None, "edited_at": None, "saved_by_referee": False, "approved": False},
        {"id": "B4", "team1": teams[4], "team2": teams[5], "score1": None, "score2": None, "stage": "group", "group": "B", "edited_by": None, "edited_at": None, "saved_by_referee": False, "approved": False},
        {"id": "B5", "team1": teams[5], "team2": teams[6], "score1": None, "score2": None, "stage": "group", "group": "B", "edited_by": None, "edited_at": None, "saved_by_referee": False, "approved": False},
        {"id": "B6", "team1": teams[4], "team2": teams[7], "score1": None, "score2": None, "stage": "group", "group": "B", "edited_by": None, "edited_at": None, "saved_by_referee": False, "approved": False},
    ]

if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 'group'

if 'group_standings' not in st.session_state:
    st.session_state.group_standings = {"A": [], "B": []}

if 'group_approved' not in st.session_state:
    st.session_state.group_approved = False

# Các hàm tính toán
def calculate_standings():
    """Chỉ tính từ các trận đã được phê duyệt"""
    for group in ["A", "B"]:
        group_teams = [team for team in teams if team["group"] == group]
        # Chỉ lấy các trận đã được phê duyệt
        group_matches = [match for match in st.session_state.matches 
                        if match.get("group") == group and match.get("approved", False)]
        
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
        {"id": "SF1", "team1": first_a, "team2": second_b, "score1": None, "score2": None, "stage": "semi", "edited_by": None, "edited_at": None, "saved_by_referee": False, "approved": False},
        {"id": "SF2", "team1": first_b, "team2": second_a, "score1": None, "score2": None, "stage": "semi", "edited_by": None, "edited_at": None, "saved_by_referee": False, "approved": False}
    ]
    
    group_matches = [match for match in st.session_state.matches if match["stage"] == "group"]
    st.session_state.matches = group_matches + semi_matches
    st.session_state.current_stage = 'semi'
    st.session_state.group_approved = True
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
        "edited_at": None,
        "saved_by_referee": False,
        "approved": False
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

def render_admin_match_card(match, is_final=False):
    """Render cho admin - LUÔN hiển thị tất cả trận"""
    current_user = st.session_state.current_user
    
    status = get_match_status(match)
    card_class = "match-card"
    if is_final:
        card_class += " final-match"
    elif status == "saved":
        card_class += " pending-approval"
    elif status == "approved":
        card_class += " approved"
    
    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
    
    # Match title với status chi tiết
    title = ""
    if match["stage"] == "group":
        title = f"Trận {match['id']}"
    elif match["stage"] == "semi":
        title = "Bán kết 1" if match["id"] == "SF1" else "Bán kết 2"
    elif match["stage"] == "final":
        title = "🏆 Chung kết"
    
    # Status badge chi tiết
    status_badge = ""
    if status == "pending":
        status_badge = '<span class="status-pending">Chờ nhập</span>'
    elif status == "saved":
        status_badge = '<span class="status-saved">Chờ duyệt</span>'
    elif status == "approved":
        status_badge = '<span class="status-approved">Đã duyệt</span>'
    
    # Thông tin người chỉnh sửa
    edit_info = ""
    if match.get("edited_by"):
        edit_info = f' | Cập nhật: {match["edited_by"]}'
    
    st.markdown(f'<div class="match-title">{title} {status_badge}{edit_info}</div>', unsafe_allow_html=True)
    
    # Match layout - Admin có thể chỉnh sửa mọi lúc
    col1, col2, col3, col4, col5, col6 = st.columns([2.5, 1, 0.3, 1, 2.5, 1.2])
    
    with col1:
        st.markdown(f"""
        <div class="team-info">
            <div class="team-name">{match['team1']['name']}</div>
            <div class="team-players">{' + '.join(match['team1']['players'])}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Admin luôn có thể chỉnh sửa
        score1 = st.number_input(
            label="Tỷ số đội 1",
            min_value=0,
            max_value=99,
            value=match["score1"] if match["score1"] is not None else 0,
            key=f"admin_score1_{match['id']}",
            label_visibility="collapsed",
            help="Tỷ số đội 1"
        )
        # Cập nhật ngay khi thay đổi
        if score1 != (match["score1"] if match["score1"] is not None else 0):
            match["score1"] = score1
            match["edited_by"] = current_user["name"]
            match["edited_at"] = datetime.now().isoformat()
            # Đánh dấu đã có tỷ số
            if match["score1"] is not None and match["score2"] is not None:
                match["saved_by_referee"] = True
    
    with col3:
        st.markdown('<div class="vs-text">-</div>', unsafe_allow_html=True)
    
    with col4:
        score2 = st.number_input(
            label="Tỷ số đội 2",
            min_value=0,
            max_value=99,
            value=match["score2"] if match["score2"] is not None else 0,
            key=f"admin_score2_{match['id']}",
            label_visibility="collapsed",
            help="Tỷ số đội 2"
        )
        # Cập nhật ngay khi thay đổi
        if score2 != (match["score2"] if match["score2"] is not None else 0):
            match["score2"] = score2
            match["edited_by"] = current_user["name"]
            match["edited_at"] = datetime.now().isoformat()
            # Đánh dấu đã có tỷ số
            if match["score1"] is not None and match["score2"] is not None:
                match["saved_by_referee"] = True
    
    with col5:
        st.markdown(f"""
        <div class="team-info">
            <div class="team-name">{match['team2']['name']}</div>
            <div class="team-players">{' + '.join(match['team2']['players'])}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        # Nút phê duyệt riêng từng trận
        if match["stage"] == "group" and status == "saved" and not match.get("approved", False):
            if st.button(f"✅ Duyệt", key=f"approve_{match['id']}", type="primary"):
                match["approved"] = True
                save_match_data()
                st.rerun()
        elif match["stage"] == "group" and match.get("approved", False):
            st.markdown('<span class="status-approved">✅ Đã duyệt</span>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_referee_input_match(match):
    """Render cho trọng tài - input mode"""
    current_user = st.session_state.current_user
    can_edit = can_edit_match(current_user, match)
    
    if not can_edit:
        return
    
    st.markdown('<div class="match-card">', unsafe_allow_html=True)
    
    title = f"Trận {match['id']}"
    st.markdown(f'<div class="match-title">{title}</div>', unsafe_allow_html=True)
    
    # Match layout
    col1, col2, col3, col4, col5 = st.columns([3, 1, 0.5, 1, 3])
    
    with col1:
        st.markdown(f"""
        <div class="team-info">
            <div class="team-name">{match['team1']['name']}</div>
            <div class="team-players">{' + '.join(match['team1']['players'])}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        score1 = st.number_input(
            label="Tỷ số đội 1",
            min_value=0,
            max_value=99,
            value=match["score1"] if match["score1"] is not None else 0,
            key=f"ref_score1_{match['id']}",
            label_visibility="collapsed",
            help="Tỷ số đội 1"
        )
        if score1 != (match["score1"] if match["score1"] is not None else 0):
            match["score1"] = score1
            match["edited_by"] = current_user["name"]
            match["edited_at"] = datetime.now().isoformat()
    
    with col3:
        st.markdown('<div class="vs-text">-</div>', unsafe_allow_html=True)
    
    with col4:
        score2 = st.number_input(
            label="Tỷ số đội 2",
            min_value=0,
            max_value=99,
            value=match["score2"] if match["score2"] is not None else 0,
            key=f"ref_score2_{match['id']}",
            label_visibility="collapsed",
            help="Tỷ số đội 2"
        )
        if score2 != (match["score2"] if match["score2"] is not None else 0):
            match["score2"] = score2
            match["edited_by"] = current_user["name"]
            match["edited_at"] = datetime.now().isoformat()
    
    with col5:
        st.markdown(f"""
        <div class="team-info">
            <div class="team-name">{match['team2']['name']}</div>
            <div class="team-players">{' + '.join(match['team2']['players'])}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_referee_readonly_match(match):
    """Render cho trọng tài - readonly mode"""
    if not match.get("saved_by_referee", False):
        return  # Không hiển thị nếu chưa lưu
    
    status = get_match_status(match)
    status_class = ""
    if status == "saved":
        status_class = "pending-approval"
    elif status == "approved":
        status_class = "approved"
    
    st.markdown(f'<div class="match-card {status_class}">', unsafe_allow_html=True)
    
    # Match title với status
    title = f"Trận {match['id']}"
    status_badge = ""
    if status == "saved":
        status_badge = '<span class="status-saved">Chờ duyệt</span>'
    elif status == "approved":
        status_badge = '<span class="status-approved">Đã duyệt</span>'
    
    st.markdown(f'<div class="match-title">{title} {status_badge}</div>', unsafe_allow_html=True)
    
    # Match layout readonly
    col1, col2, col3, col4, col5 = st.columns([3, 1, 0.5, 1, 3])
    
    with col1:
        st.markdown(f"""
        <div class="team-info">
            <div class="team-name">{match['team1']['name']}</div>
            <div class="team-players">{' + '.join(match['team1']['players'])}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="readonly-score">
            {match["score1"] if match["score1"] is not None else 0}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="vs-text">-</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="readonly-score">
            {match["score2"] if match["score2"] is not None else 0}
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

# Main content
if st.session_state.current_stage == 'group':
    
    if current_user["role"] == "referee":
        # TRỌNG TÀI - Logic không thay đổi
        group = current_user.get("group")
        if group:
            st.markdown(f'<div class="section-header"><h3>Bảng {group} - Nhập tỷ số</h3></div>', unsafe_allow_html=True)
            
            group_matches = [match for match in st.session_state.matches if match.get("group") == group and match["stage"] == "group"]
            
            # Hiển thị form nhập cho các trận chưa lưu
            unsaved_matches = [match for match in group_matches if not match.get("saved_by_referee", False)]
            
            if unsaved_matches:
                st.markdown("#### 📝 Nhập tỷ số các trận:")
                for match in unsaved_matches:
                    render_referee_input_match(match)
                
                # Nút lưu tỷ số
                if st.button("💾 Lưu tỷ số vòng bảng", use_container_width=True, type="primary"):
                    # Đánh dấu tất cả các trận có tỷ số đã được lưu
                    for match in group_matches:
                        if match["score1"] is not None and match["score2"] is not None:
                            match["saved_by_referee"] = True
                    
                    save_match_data()
                    st.markdown('<div class="success-alert">✅ Đã lưu tỷ số thành công! Chờ Admin phê duyệt.</div>', unsafe_allow_html=True)
                    st.rerun()
            else:
                st.markdown('<div class="success-alert">✅ Đã lưu tất cả tỷ số. Chờ Admin phê duyệt.</div>', unsafe_allow_html=True)
            
            # Hiển thị các trận đã lưu
            saved_matches = [match for match in group_matches if match.get("saved_by_referee", False)]
            if saved_matches:
                st.markdown("#### 📋 Tỷ số đã lưu:")
                for match in saved_matches:
                    render_referee_readonly_match(match)
            
            # Hiển thị bảng xếp hạng (chỉ từ trận đã duyệt)
            if st.session_state.group_standings[group]:
                st.markdown("---")
                st.markdown(f'<div class="standings-header"><h3>Bảng xếp hạng {group}</h3></div>', unsafe_allow_html=True)
                
                for i, standing in enumerate(st.session_state.group_standings[group]):
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
    
    elif current_user["role"] == "admin":
        # ADMIN - Fixed để hiển thị TẤT CẢ trận đấu
        st.markdown('<div class="section-header"><h3>🔍 Quản lý và Phê duyệt - Admin View</h3></div>', unsafe_allow_html=True)
        
        # Thống kê tổng quan
        all_group_matches = [match for match in st.session_state.matches if match["stage"] == "group"]
        pending_matches = [match for match in all_group_matches if match.get("saved_by_referee", False) and not match.get("approved", False)]
        saved_matches = [match for match in all_group_matches if match.get("saved_by_referee", False)]
        approved_matches = [match for match in all_group_matches if match.get("approved", False)]
        
        # Hiển thị thống kê
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(all_group_matches)}</div>
                <div class="metric-label">Tổng trận</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(saved_matches)}</div>
                <div class="metric-label">Đã nhập</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(pending_matches)}</div>
                <div class="metric-label">Chờ duyệt</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(approved_matches)}</div>
                <div class="metric-label">Đã duyệt</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Hiển thị cảnh báo nếu có trận chờ duyệt
        if pending_matches:
            st.markdown(f"""
            <div class="approval-section">
                <div class="approval-header">⏳ {len(pending_matches)} trận đang chờ phê duyệt</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Layout 2 cột cho admin - HIỂN THỊ TẤT CẢ TRẬN
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-header"><h3>Bảng A - Tất cả trận đấu</h3></div>', unsafe_allow_html=True)
            
            # HIỂN THỊ TẤT CẢ trận Bảng A (kể cả chưa nhập)
            group_a_matches = [match for match in st.session_state.matches if match.get("group") == "A" and match["stage"] == "group"]
            
            if not group_a_matches:
                st.markdown('<div class="warning-alert">⚠️ Không tìm thấy trận đấu Bảng A</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"**Số trận Bảng A: {len(group_a_matches)}**")
                for match in group_a_matches:
                    render_admin_match_card(match)
        
        with col2:
            st.markdown('<div class="section-header"><h3>Bảng B - Tất cả trận đấu</h3></div>', unsafe_allow_html=True)
            
            # HIỂN THỊ TẤT CẢ trận Bảng B (kể cả chưa nhập)
            group_b_matches = [match for match in st.session_state.matches if match.get("group") == "B" and match["stage"] == "group"]
            
            if not group_b_matches:
                st.markdown('<div class="warning-alert">⚠️ Không tìm thấy trận đấu Bảng B</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"**Số trận Bảng B: {len(group_b_matches)}**")
                for match in group_b_matches:
                    render_admin_match_card(match)
        
        # Nút phê duyệt hàng loạt
        if pending_matches:
            st.markdown("---")
            st.markdown("### 🎯 Phê duyệt hàng loạt")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                pending_a = [m for m in pending_matches if m.get("group") == "A"]
                if pending_a:
                    if st.button(f"✅ Duyệt tất cả Bảng A ({len(pending_a)})", use_container_width=True, type="primary"):
                        for match in pending_a:
                            match["approved"] = True
                        save_match_data()
                        st.success("✅ Đã phê duyệt tất cả trận Bảng A!")
                        st.rerun()
            
            with col2:
                pending_b = [m for m in pending_matches if m.get("group") == "B"]
                if pending_b:
                    if st.button(f"✅ Duyệt tất cả Bảng B ({len(pending_b)})", use_container_width=True, type="primary"):
                        for match in pending_b:
                            match["approved"] = True
                        save_match_data()
                        st.success("✅ Đã phê duyệt tất cả trận Bảng B!")
                        st.rerun()
            
            with col3:
                if st.button(f"✅ Duyệt TẤT CẢ ({len(pending_matches)})", use_container_width=True, type="primary"):
                    for match in pending_matches:
                        match["approved"] = True
                    save_match_data()
                    st.success("✅ Đã phê duyệt tất cả trận!")
                    st.rerun()
        
        # Hiển thị bảng xếp hạng (chỉ từ trận đã duyệt)
        if st.session_state.group_standings["A"] or st.session_state.group_standings["B"]:
            st.markdown("---")
            st.markdown("### 📊 Bảng xếp hạng (từ trận đã duyệt)")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="standings-header"><h3>Bảng xếp hạng A</h3></div>', unsafe_allow_html=True)
                
                if st.session_state.group_standings["A"]:
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
                else:
                    st.markdown('<div class="info-alert">📋 Chưa có trận nào được phê duyệt</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="standings-header"><h3>Bảng xếp hạng B</h3></div>', unsafe_allow_html=True)
                
                if st.session_state.group_standings["B"]:
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
                else:
                    st.markdown('<div class="info-alert">📋 Chưa có trận nào được phê duyệt</div>', unsafe_allow_html=True)
        
        # Tạo bán kết (chỉ khi tất cả đã được phê duyệt)
        all_approved = all(match.get("approved", False) for match in all_group_matches if match.get("saved_by_referee", False))
        total_saved = len([m for m in all_group_matches if m.get("saved_by_referee", False)])
        
        if (len(st.session_state.group_standings["A"]) >= 2 and 
            len(st.session_state.group_standings["B"]) >= 2 and 
            all_approved and total_saved >= 12):
            
            st.markdown("---")
            if st.button("🚀 Tạo lịch vòng loại trực tiếp", key="gen_knockout", use_container_width=True, type="primary"):
                generate_knockout_matches()
                st.success("✅ Đã tạo lịch bán kết!")
                st.rerun()
        else:
            st.markdown("---")
            if total_saved < 12:
                st.markdown('<div class="warning-alert">⚠️ Cần có đủ 12 trận được nhập tỷ số</div>', unsafe_allow_html=True)
            elif not all_approved:
                st.markdown('<div class="warning-alert">⚠️ Cần phê duyệt tất cả trận vòng bảng trước khi tạo bán kết</div>', unsafe_allow_html=True)

elif st.session_state.current_stage == 'semi':
    st.markdown('<div class="section-header"><h3>⚡ Vòng bán kết</h3></div>', unsafe_allow_html=True)
    
    if current_user["role"] == "admin":
        semi_matches = [match for match in st.session_state.matches if match["stage"] == "semi"]
        if semi_matches:
            for match in semi_matches:
                render_admin_match_card(match)
            
            # Tạo chung kết
            semi_completed = all(match["score1"] is not None and match["score2"] is not None 
                               for match in semi_matches)
            
            if semi_completed and len(semi_matches) == 2:
                st.markdown("---")
                if st.button("🏆 Tạo lịch chung kết", key="gen_final", use_container_width=True, type="primary"):
                    generate_final_matches()
                    st.success("✅ Đã tạo lịch chung kết!")
                    st.rerun()
        else:
            st.markdown('<div class="info-alert">📋 Chưa có trận bán kết nào. Vui lòng hoàn thành vòng bảng trước.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="warning-alert">⚠️ Chỉ Admin mới có thể cập nhật tỷ số bán kết</div>', unsafe_allow_html=True)

elif st.session_state.current_stage == 'final':
    st.markdown('<div class="section-header"><h3>🏆 Trận chung kết</h3></div>', unsafe_allow_html=True)
    
    if current_user["role"] == "admin":
        final_matches = [match for match in st.session_state.matches if match["stage"] == "final"]
        if final_matches:
            for match in final_matches:
                render_admin_match_card(match, is_final=True)
        else:
            st.markdown('<div class="info-alert">📋 Chưa có trận chung kết nào. Vui lòng hoàn thành bán kết trước.</div>', unsafe_allow_html=True)
        
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
    else:
        # Trọng tài chỉ xem kết quả
        rankings = get_ranking_list()
        if rankings:
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
        else:
            st.markdown('<div class="warning-alert">⏳ Chờ Admin cập nhật kết quả chung kết</div>', unsafe_allow_html=True)

# Admin panel
if current_user["role"] == "admin":
    with st.expander("🔧 Bảng điều khiển Admin", expanded=False):
        st.markdown("### 🛠️ Công cụ quản trị")
        
        # Debug info
        st.markdown("#### 🔍 Debug Info")
        total_matches = len(st.session_state.matches)
        group_matches = len([m for m in st.session_state.matches if m["stage"] == "group"])
        
        st.write(f"- Tổng số trận trong hệ thống: {total_matches}")
        st.write(f"- Số trận vòng bảng: {group_matches}")
        st.write(f"- Matches data: {len(st.session_state.matches)} items")
        
        # Hiển thị raw data để debug
        if st.checkbox("Hiển thị dữ liệu raw"):
            st.json(st.session_state.matches)
        
        # Reset data
        if st.button("🔄 Reset toàn bộ dữ liệu", type="secondary"):
            if st.checkbox("✅ Xác nhận reset (không thể hoàn tác)"):
                for key in ['matches', 'saved_matches', 'group_standings', 'group_approved']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.success("✅ Đã reset toàn bộ dữ liệu!")
                st.rerun()

# Footer
st.markdown(f"""
<div class="footer">
    <p><strong>🏓 Giải Pickleball - Hệ thống Trọng tài Điện tử</strong></p>
    <p>Phiên bản: 4.1 Fixed Admin View | Người dùng: <strong>{current_user['name']}</strong></p>
    <p>🔄 Quy trình: Nhập → Lưu → Duyệt → Xếp hạng</p>
</div>
""", unsafe_allow_html=True)
