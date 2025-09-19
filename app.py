import streamlit as st
import pandas as pd
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional

# Cấu hình trang
st.set_page_config(
    page_title="Giải Pickleball",
    page_icon="🏓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS hoàn toàn responsive cho mobile
st.markdown("""
<style>
    /* Import font tối ưu */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
        box-sizing: border-box;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stActionButton {display:none;}
    
    /* Mobile-first container */
    .main .block-container {
        padding: 0.5rem !important;
        max-width: 100vw !important;
        width: 100% !important;
        margin: 0 !important;
    }
    
    /* Responsive breakpoints */
    @media (min-width: 768px) {
        .main .block-container {
            max-width: 500px !important;
            margin: 0 auto !important;
            padding: 1rem !important;
        }
    }
    
    /* Remove default Streamlit spacing */
    .stVerticalBlock > [data-testid="stVerticalBlockBorderWrapper"] {
        gap: 0.5rem !important;
    }
    
    /* Login styles */
    .login-container {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #e5e7eb;
    }
    
    .login-header {
        background: linear-gradient(135deg, #b59410 0%, #eab308 100%);
        padding: 2rem 1rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .login-header h1 {
        font-size: clamp(1.8rem, 8vw, 2.5rem) !important;
        margin: 0 !important;
        font-weight: 800 !important;
        letter-spacing: -0.025em;
    }
    
    .login-header p {
        font-size: clamp(1rem, 4vw, 1.25rem) !important;
        margin: 0.75rem 0 0 0 !important;
        opacity: 0.95;
        font-weight: 500;
    }
    
    /* User info bar responsive */
    .user-info {
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1rem;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        gap: 0.75rem;
        font-size: clamp(0.875rem, 4vw, 1rem) !important;
    }
    
    @media (max-width: 480px) {
        .user-info {
            flex-direction: column;
            text-align: center;
        }
    }
    
    .role-badge {
        padding: 0.375rem 0.75rem;
        border-radius: 6px;
        font-size: clamp(0.75rem, 3vw, 0.875rem) !important;
        font-weight: 700;
        white-space: nowrap;
    }
    
    .admin-badge {
        background: #dc2626;
    }
    
    .referee-badge {
        background: #059669;
    }
    
    /* Main header responsive */
    .app-header {
        background: linear-gradient(135deg, #b59410 0%, #eab308 100%);
        padding: clamp(1.5rem, 5vw, 2.5rem) 1rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(181, 148, 16, 0.25);
    }
    
    .app-header h1 {
        margin: 0;
        font-size: clamp(2rem, 8vw, 3rem) !important;
        font-weight: 800 !important;
        letter-spacing: -0.025em;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .app-header p {
        margin: 0.75rem 0 0 0;
        font-size: clamp(1.125rem, 4vw, 1.5rem) !important;
        opacity: 0.95;
        font-weight: 600;
    }
    
    /* Navigation responsive */
    .nav-container {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    .stButton button {
        font-size: clamp(0.875rem, 3.5vw, 1.125rem) !important;
        font-weight: 700 !important;
        padding: 1rem 0.5rem !important;
        border-radius: 10px !important;
        min-height: 56px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        text-transform: uppercase;
        letter-spacing: 0.025em;
    }
    
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%) !important;
        border: none !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(29, 78, 216, 0.3) !important;
    }
    
    .stButton button[kind="secondary"] {
        background: white !important;
        border: 2px solid #1d4ed8 !important;
        color: #1d4ed8 !important;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 12px rgba(29, 78, 216, 0.2);
    }
    
    .section-header h3 {
        margin: 0;
        font-size: clamp(1.25rem, 5vw, 1.625rem) !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em;
    }
    
    /* Match cards mobile-first */
    .match-card {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.75rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .match-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .match-card.readonly {
        background: #f9fafb;
        border-color: #d1d5db;
    }
    
    .match-card.final-match {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 3px solid #b59410;
        box-shadow: 0 6px 20px rgba(181, 148, 16, 0.2);
    }
    
    /* Match title */
    .match-title {
        font-weight: 800 !important;
        font-size: clamp(1.125rem, 4.5vw, 1.375rem) !important;
        margin-bottom: 1rem;
        color: #1d4ed8;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    /* Edit indicator */
    .edit-badge {
        background: #f59e0b;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: clamp(0.75rem, 3vw, 0.875rem) !important;
        font-weight: 600;
        margin-left: 0.5rem;
        display: inline-block;
    }
    
    /* Team info mobile responsive */
    .team-section {
        text-align: center;
        padding: 0.5rem;
    }
    
    .team-name {
        font-weight: 800 !important;
        font-size: clamp(1.125rem, 4.5vw, 1.375rem) !important;
        margin-bottom: 0.375rem;
        color: #111827;
        line-height: 1.1;
    }
    
    .team-players {
        font-size: clamp(0.875rem, 3.5vw, 1.125rem) !important;
        color: #6b7280;
        font-weight: 600;
        line-height: 1.2;
    }
    
    /* Score inputs - PERFECT FOR 2 DIGITS */
    .stNumberInput {
        width: 100% !important;
    }
    
    .stNumberInput > div > div > input {
        text-align: center !important;
        font-size: clamp(1.75rem, 7vw, 2.25rem) !important;
        font-weight: 900 !important;
        padding: 1rem 0.5rem !important;
        border-radius: 12px !important;
        border: 3px solid #d1d5db !important;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        height: 70px !important;
        width: 90px !important;
        max-width: 90px !important;
        min-width: 90px !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin: 0 auto !important;
        display: block !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #1d4ed8 !important;
        box-shadow: 0 0 0 4px rgba(29, 78, 216, 0.2), inset 0 2px 4px rgba(0, 0, 0, 0.06) !important;
        outline: none !important;
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        transform: scale(1.02);
    }
    
    /* Readonly score display */
    .readonly-score {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%) !important;
        border: 3px solid #d1d5db !important;
        border-radius: 12px !important;
        height: 70px !important;
        width: 90px !important;
        margin: 0 auto !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: clamp(1.75rem, 7vw, 2.25rem) !important;
        font-weight: 900 !important;
        color: #374151 !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.04) !important;
    }
    
    /* VS separator */
    .vs-separator {
        text-align: center;
        font-size: clamp(1.5rem, 6vw, 2rem) !important;
        font-weight: 900 !important;
        color: #6b7280;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 70px;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    /* Match layout grid */
    .match-grid {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        gap: 1rem;
        align-items: center;
        margin-top: 1rem;
    }
    
    @media (max-width: 480px) {
        .match-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
            text-align: center;
        }
        
        .match-scores {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1rem;
            margin: 1rem 0;
        }
    }
    
    /* Standings responsive */
    .standings-header {
        background: linear-gradient(135deg, #b59410 0%, #eab308 100%);
        color: white;
        padding: 1.25rem;
        border-radius: 12px;
        margin: 1.25rem 0;
        text-align: center;
        box-shadow: 0 4px 16px rgba(181, 148, 16, 0.2);
    }
    
    .standings-header h3 {
        margin: 0;
        font-size: clamp(1.25rem, 5vw, 1.625rem) !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em;
    }
    
    .standing-card {
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border-left: 5px solid transparent;
        transition: transform 0.2s ease;
    }
    
    .standing-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .standing-card.qualified {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left-color: #1d4ed8;
        color: #1e3a8a;
    }
    
    .standing-card.not-qualified {
        background: #f9fafb;
        border-left-color: #d1d5db;
        color: #374151;
    }
    
    .standing-info {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1rem;
    }
    
    @media (max-width: 480px) {
        .standing-info {
            flex-direction: column;
            text-align: center;
            gap: 0.75rem;
        }
    }
    
    .team-details h4 {
        font-size: clamp(1.125rem, 4.5vw, 1.375rem) !important;
        font-weight: 800 !important;
        margin: 0 0 0.25rem 0 !important;
        line-height: 1.1;
    }
    
    .team-details p {
        font-size: clamp(0.875rem, 3.5vw, 1.125rem) !important;
        margin: 0 !important;
        font-weight: 600;
        opacity: 0.8;
    }
    
    .team-stats {
        text-align: right;
        font-size: clamp(0.875rem, 3.5vw, 1rem) !important;
        font-weight: 700;
        line-height: 1.3;
    }
    
    @media (max-width: 480px) {
        .team-stats {
            text-align: center;
        }
    }
    
    /* Rankings mobile-optimized */
    .ranking-card {
        background: linear-gradient(135deg, #fef3c7 0%, #dbeafe 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 6px solid #b59410;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    @media (max-width: 480px) {
        .ranking-card {
            flex-direction: column;
            text-align: center;
            gap: 1rem;
        }
    }
    
    .ranking-info {
        flex: 1;
    }
    
    .ranking-title {
        font-size: clamp(1.25rem, 5vw, 1.75rem) !important;
        font-weight: 800 !important;
        color: #b59410;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    .ranking-team {
        font-size: clamp(1.125rem, 4.5vw, 1.5rem) !important;
        font-weight: 700 !important;
        margin-bottom: 0.375rem;
        color: #111827;
    }
    
    .ranking-players {
        font-size: clamp(0.875rem, 3.5vw, 1.125rem) !important;
        color: #6b7280;
        font-weight: 600;
    }
    
    .ranking-position {
        font-size: clamp(3rem, 12vw, 5rem) !important;
        font-weight: 900 !important;
        color: #1d4ed8;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.15);
        line-height: 0.8;
    }
    
    /* Action buttons responsive */
    .action-btn {
        width: 100% !important;
        margin: 1rem 0 !important;
    }
    
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%) !important;
        color: white !important;
        border: none !important;
        font-size: clamp(1.125rem, 4.5vw, 1.375rem) !important;
        font-weight: 800 !important;
        padding: 1.25rem 2rem !important;
        border-radius: 12px !important;
        min-height: 64px !important;
        box-shadow: 0 6px 20px rgba(29, 78, 216, 0.3) !important;
        text-transform: uppercase;
        letter-spacing: 0.025em;
    }
    
    .stButton button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(29, 78, 216, 0.4) !important;
    }
    
    /* Success indicators */
    .success-alert {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        font-size: clamp(1rem, 4vw, 1.25rem) !important;
        font-weight: 700;
        animation: slideInUp 0.5s ease-out;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.25);
    }
    
    /* Form elements responsive */
    .stSelectbox > div > div {
        font-size: clamp(1rem, 4vw, 1.25rem) !important;
        padding: 1rem !important;
        border-radius: 10px !important;
        min-height: 56px !important;
        border: 2px solid #d1d5db !important;
    }
    
    .stTextInput > div > div > input {
        font-size: clamp(1rem, 4vw, 1.25rem) !important;
        padding: 1rem 1.25rem !important;
        border-radius: 10px !important;
        min-height: 56px !important;
        border: 2px solid #d1d5db !important;
    }
    
    /* Expander responsive */
    .streamlit-expanderHeader {
        font-size: clamp(1rem, 4vw, 1.25rem) !important;
        font-weight: 700 !important;
        padding: 1rem !important;
    }
    
    /* Metrics grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .metric-card {
        text-align: center;
        padding: 1.25rem 1rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border: 1px solid #e5e7eb;
    }
    
    .metric-value {
        font-size: clamp(1.875rem, 7vw, 2.5rem) !important;
        font-weight: 900 !important;
        color: #1d4ed8;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: clamp(0.875rem, 3.5vw, 1rem) !important;
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.025em;
    }
    
    /* Footer responsive */
    .footer {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
        border-radius: 12px;
        margin-top: 2rem;
        border: 1px solid #e5e7eb;
    }
    
    .footer p {
        margin: 0.5rem 0 !important;
        font-size: clamp(0.875rem, 3.5vw, 1.125rem) !important;
        color: #6b7280;
        font-weight: 600;
    }
    
    .footer strong {
        color: #1d4ed8;
    }
    
    /* Animations */
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Touch optimization */
    @media (hover: none) and (pointer: coarse) {
        .match-card:hover,
        .standing-card:hover,
        .stButton button:hover {
            transform: none !important;
        }
    }
    
    /* Accessibility */
    .sr-only {
        position: absolute !important;
        width: 1px !important;
        height: 1px !important;
        padding: 0 !important;
        margin: -1px !important;
        overflow: hidden !important;
        clip: rect(0, 0, 0, 0) !important;
        white-space: nowrap !important;
        border: 0 !important;
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
            <h1>🏓 Đăng nhập Hệ thống</h1>
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
    
    with st.expander("📖 Hướng dẫn sử dụng", expanded=True):
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

# Các hàm tính toán (giữ nguyên)
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
    """Render match card responsive với score inputs tối ưu"""
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
        title = f"TRẬN {match['id']}"
    elif match["stage"] == "semi":
        title = "BÁN KẾT 1" if match["id"] == "SF1" else "BÁN KẾT 2"
    elif match["stage"] == "final":
        title = "🏆 CHUNG KẾT"
    
    # Edit info
    edit_info = ""
    if match.get("edited_by"):
        edit_info = f'<span class="edit-badge">{match["edited_by"]}</span>'
    
    st.markdown(f'<div class="match-title">{title}{edit_info}</div>', unsafe_allow_html=True)
    
    # Desktop/Tablet layout
    st.markdown('<div class="match-grid">', unsafe_allow_html=True)
    
    # Team 1 info
    st.markdown(f"""
    <div class="team-section">
        <div class="team-name">{match['team1']['name']}</div>
        <div class="team-players">{' + '.join(match['team1']['players'])}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Scores section cho mobile
    st.markdown('<div class="match-scores">', unsafe_allow_html=True)
    
    # Team 1 score
    col1, col2, col3 = st.columns([1, 0.3, 1])
    
    with col1:
        if can_edit or current_user["role"] == "admin":
            score1 = st.number_input(
                label="Tỷ số đội 1",
                min_value=0,
                max_value=99,
                value=match["score1"] or 0,
                key=f"score1_{match['id']}",
                label_visibility="collapsed",
                help="Tỷ số (0-99)"
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
    
    with col2:
        st.markdown('<div class="vs-separator">-</div>', unsafe_allow_html=True)
    
    with col3:
        if can_edit or current_user["role"] == "admin":
            score2 = st.number_input(
                label="Tỷ số đội 2",
                min_value=0,
                max_value=99,
                value=match["score2"] or 0,
                key=f"score2_{match['id']}",
                label_visibility="collapsed",
                help="Tỷ số (0-99)"
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
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close match-scores
    
    # Team 2 info
    st.markdown(f"""
    <div class="team-section">
        <div class="team-name">{match['team2']['name']}</div>
        <div class="team-players">{' + '.join(match['team2']['players'])}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close match-grid
    st.markdown('</div>', unsafe_allow_html=True)  # Close match-card

# === MAIN APP ===

# Kiểm tra xác thực
if not st.session_state.authenticated:
    show_login()
    st.stop()

# User info
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

# Logout
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
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
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

st.markdown('</div>', unsafe_allow_html=True)

# Admin panel
if current_user["role"] == "admin":
    with st.expander("🔧 BẢNG ĐIỀU KHIỂN ADMIN", expanded=False):
        st.markdown("### 📊 THỐNG KÊ HỆ THỐNG")
        
        total_matches = len(st.session_state.matches)
        completed_matches = len([m for m in st.session_state.matches if m["score1"] is not None and m["score2"] is not None])
        save_count = len(st.session_state.get('saved_matches', {}))
        
        st.markdown(f"""
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">{total_matches}</div>
                <div class="metric-label">Tổng trận</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{completed_matches}</div>
                <div class="metric-label">Hoàn thành</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{save_count}</div>
                <div class="metric-label">Lần lưu</div>
            </div>
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
        st.markdown('<div class="section-header"><h3>BẢNG A - LỊCH THI ĐẤU</h3></div>', unsafe_allow_html=True)
        
        group_a_matches = [match for match in st.session_state.matches if match.get("group") == "A"]
        for match in group_a_matches:
            render_match_card(match)
    
    # Group B
    if current_user["role"] == "admin" or current_user.get("group") == "B":
        st.markdown('<div class="section-header"><h3>BẢNG B - LỊCH THI ĐẤU</h3></div>', unsafe_allow_html=True)
        
        group_b_matches = [match for match in st.session_state.matches if match.get("group") == "B"]
        for match in group_b_matches:
            render_match_card(match)
    
    # Save button cho trọng tài
    if current_user["role"] == "referee":
        if st.button("💾 LƯU TỶ SỐ VÒNG BẢNG", use_container_width=True, type="primary"):
            save_match_data()
            st.markdown('<div class="success-alert">✅ ĐÃ LƯU TỶ SỐ THÀNH CÔNG!</div>', unsafe_allow_html=True)
    
    # Standings
    st.markdown("---")
    
    # Group A Standings
    st.markdown('<div class="standings-header"><h3>BẢNG XẾP HẠNG A</h3></div>', unsafe_allow_html=True)
    
    for i, standing in enumerate(st.session_state.group_standings["A"]):
        css_class = "qualified" if i < 2 else "not-qualified"
        st.markdown(f"""
        <div class="standing-card {css_class}">
            <div class="standing-info">
                <div class="team-details">
                    <h4>{i+1}. {standing["team"]["name"]}</h4>
                    <p>{" + ".join(standing["team"]["players"])}</p>
                </div>
                <div class="team-stats">
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
        <div class="standing-card {css_class}">
            <div class="standing-info">
                <div class="team-details">
                    <h4>{i+1}. {standing["team"]["name"]}</h4>
                    <p>{" + ".join(standing["team"]["players"])}</p>
                </div>
                <div class="team-stats">
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
            if st.button("🚀 TẠO LỊCH VÒNG LOẠI TRỰC TIẾP", key="gen_knockout", use_container_width=True, type="primary"):
                generate_knockout_matches()
                st.success("✅ Đã tạo lịch bán kết!")
                st.rerun()

elif st.session_state.current_stage == 'semi':
    st.markdown('<div class="section-header"><h3>⚡ VÒNG BÁN KẾT</h3></div>', unsafe_allow_html=True)
    
    semi_matches = [match for match in st.session_state.matches if match["stage"] == "semi"]
    for match in semi_matches:
        render_match_card(match)
    
    if current_user["role"] == "admin":
        if st.button("🏆 TẠO LỊCH CHUNG KẾT", key="gen_final", use_container_width=True, type="primary"):
            generate_final_matches()
            st.success("✅ Đã tạo lịch chung kết!")
            st.rerun()

elif st.session_state.current_stage == 'final':
    st.markdown('<div class="section-header"><h3>🏆 TRẬN CHUNG KẾT</h3></div>', unsafe_allow_html=True)
    
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
            <div class="ranking-card">
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
    <p><strong>🏓 GIẢI PICKLEBALL - HỆ THỐNG TRỌNG TÀI ĐIỆN TỬ</strong></p>
    <p>Phiên bản: 3.0 Mobile-First | <strong>{current_user['name']}</strong></p>
    <p>📱 Responsive Design | 🎯 Touch Optimized</p>
</div>
""", unsafe_allow_html=True)