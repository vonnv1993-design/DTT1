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

# Custom CSS (giữ nguyên như trước nhưng thêm login styles)
st.markdown("""
<style>
    /* Existing styles... */
    .main .block-container {
        padding: 1rem 0.5rem;
        max-width: 100%;
    }
    
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.5rem;
        }
    }
    
    /* Login form styles */
    .login-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
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
        margin-bottom: 2rem;
    }
    
    .user-info {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 0.75rem 1rem;
        border-radius: 8px;
        color: white;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .admin-badge {
        background: #dc2626;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    
    .referee-badge {
        background: #059669;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    
    .save-indicator {
        background: #10b981;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        text-align: center;
        animation: fadeIn 0.3s ease-in;
    }
    
    .edit-indicator {
        background: #f59e0b;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        margin-left: 0.5rem;
    }
    
    /* Mobile-optimized styles from previous version */
    .mobile-header {
        background: linear-gradient(135deg, #b8860b 0%, #daa520 100%);
        padding: 1.5rem 1rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(184, 134, 11, 0.3);
    }
    
    .mobile-header h1 {
        margin: 0;
        font-size: clamp(1.5rem, 5vw, 2.5rem);
        font-weight: bold;
    }
    
    .mobile-header p {
        margin: 0.5rem 0 0 0;
        font-size: clamp(0.875rem, 3vw, 1rem);
        opacity: 0.9;
    }
    
    .group-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 2px 10px rgba(30, 64, 175, 0.2);
    }
    
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
        font-weight: bold;
        font-size: clamp(0.875rem, 3vw, 1rem);
        margin-bottom: 0.75rem;
        color: #1e40af;
        text-align: center;
    }
    
    .team-info {
        text-align: center;
        padding: 0.5rem;
    }
    
    .team-name {
        font-weight: bold;
        font-size: clamp(0.875rem, 3vw, 1rem);
        margin-bottom: 0.25rem;
        color: #111827;
    }
    
    .team-players {
        font-size: clamp(0.75rem, 2.5vw, 0.875rem);
        color: #6b7280;
        font-style: italic;
    }
    
    .vs-text {
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: #6b7280;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.5rem;
    }
    
    .standings-header {
        background: linear-gradient(135deg, #b8860b 0%, #daa520 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .standing-item {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        background: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .standing-item.qualified {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        color: #1e40af;
        font-weight: bold;
        border-left: 4px solid #1e40af;
    }
    
    .standing-item.not-qualified {
        background: #f3f4f6;
        color: #374151;
        border-left: 4px solid #d1d5db;
    }
    
    .standing-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    .final-match {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 3px solid #b8860b;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(184, 134, 11, 0.2);
    }
    
    .ranking-item {
        background: linear-gradient(135deg, #fef3c7 0%, #dbeafe 100%);
        border-radius: 12px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        border-left: 5px solid #b8860b;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.1);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Hệ thống người dùng
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

def hash_password(password):
    """Hash mật khẩu"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Xác thực mật khẩu"""
    return hash_password(password) == hashed

def authenticate(username, password):
    """Xác thực người dùng"""
    if username in USERS and USERS[username]["password"] == password:
        return USERS[username]
    return None

def save_match_data():
    """Lưu dữ liệu trận đấu vào session state"""
    if 'saved_matches' not in st.session_state:
        st.session_state.saved_matches = {}
    
    # Lưu với timestamp
    timestamp = datetime.now().isoformat()
    st.session_state.saved_matches[timestamp] = {
        "matches": st.session_state.matches.copy(),
        "user": st.session_state.current_user["name"],
        "stage": st.session_state.current_stage
    }

def can_edit_match(user, match):
    """Kiểm tra quyền chỉnh sửa trận đấu"""
    if user["role"] == "admin":
        return True
    
    if user["role"] == "referee":
        if match.get("group") == user.get("group"):
            return True
    
    return False

def show_login():
    """Hiển thị form đăng nhập"""
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
        
        submit = st.form_submit_button("🔓 Đăng nhập", use_container_width=True, type="primary")
        
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
    
    # Hướng dẫn sử dụng
    with st.expander("📖 Hướng dẫn sử dụng", expanded=True):
        st.markdown("""
        **Tài khoản mẫu:**
        
        🔴 **Admin** (Quản trị viên)
        - Tên đăng nhập: `admin`
        - Mật khẩu: `123456`
        - Quyền: Xem và chỉnh sửa tất cả, quản lý hệ thống
        
        🟢 **Trọng tài Tú** (Bảng A)
        - Tên đăng nhập: `tu` 
        - Mật khẩu: `123456`
        - Quyền: Chỉ chỉnh sửa các trận ở Bảng A
        
        🔵 **Trọng tài Quang** (Bảng B)
        - Tên đăng nhập: `quang`
        - Mật khẩu: `123456` 
        - Quyền: Chỉ chỉnh sửa các trận ở Bảng B
        """)

# Dữ liệu đội (giữ nguyên)
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

# Các hàm tính toán (giữ nguyên logic)
def calculate_standings():
    """Tính toán bảng xếp hạng"""
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
    """Tạo trận bán kết"""
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
    """Tạo trận chung kết"""
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
    """Lấy bảng xếp hạng cuối cùng"""
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
    """Render match card với kiểm soát quyền"""
    current_user = st.session_state.current_user
    can_edit = can_edit_match(current_user, match)
    
    card_class = "final-match" if is_final else "match-card"
    if not can_edit and current_user["role"] != "admin":
        card_class += " readonly"
    
    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
    
    # Match title với thông tin chỉnh sửa
    title = ""
    if match["stage"] == "group":
        title = f"Trận {match['id']}"
    elif match["stage"] == "semi":
        title = "Bán kết 1" if match["id"] == "SF1" else "Bán kết 2"
    elif match["stage"] == "final":
        title = "🏆 Chung kết"
    
    # Hiển thị thông tin chỉnh sửa
    edit_info = ""
    if match.get("edited_by"):
        edit_info = f'<span class="edit-indicator">Cập nhật bởi: {match["edited_by"]}</span>'
    
    st.markdown(f'<div class="match-title">{title} {edit_info}</div>', unsafe_allow_html=True)
    
    # Teams and scores
    col1, col2, col3, col4, col5 = st.columns([3, 1.5, 0.5, 1.5, 3])
    
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
                label="Score 1",
                min_value=0,
                value=match["score1"] or 0,
                key=f"score1_{match['id']}",
                label_visibility="collapsed"
            )
            if score1 != (match["score1"] or 0):
                match["score1"] = score1
                match["edited_by"] = current_user["name"]
                match["edited_at"] = datetime.now().isoformat()
                save_match_data()
        else:
            st.markdown(f"""
            <div style="background: #f3f4f6; padding: 0.75rem; border-radius: 8px; text-align: center; font-weight: bold; font-size: 1.25rem;">
                {match["score1"] or 0}
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="vs-text">-</div>', unsafe_allow_html=True)
    
    with col4:
        if can_edit or current_user["role"] == "admin":
            score2 = st.number_input(
                label="Score 2",
                min_value=0,
                value=match["score2"] or 0,
                key=f"score2_{match['id']}",
                label_visibility="collapsed"
            )
            if score2 != (match["score2"] or 0):
                match["score2"] = score2
                match["edited_by"] = current_user["name"]
                match["edited_at"] = datetime.now().isoformat()
                save_match_data()
        else:
            st.markdown(f"""
            <div style="background: #f3f4f6; padding: 0.75rem; border-radius: 8px; text-align: center; font-weight: bold; font-size: 1.25rem;">
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
        <button onclick="window.location.reload();" style="background: #dc2626; color: white; border: none; padding: 0.25rem 0.5rem; border-radius: 4px; cursor: pointer;">
            🚪 Đăng xuất
        </button>
    </div>
</div>
""", unsafe_allow_html=True)

# Logout button
if st.button("🚪 Đăng xuất", key="logout"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Tính toán bảng xếp hạng
calculate_standings()

# Header
st.markdown("""
<div class="mobile-header">
    <h1>🏓 Giải Pickleball</h1>
    <p>Hệ thống xếp hạng tự động</p>
</div>
""", unsafe_allow_html=True)

# Navigation
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Vòng bảng", key="nav_group", use_container_width=True):
        st.session_state.current_stage = 'group'

with col2:
    if st.button("Bán kết", key="nav_semi", use_container_width=True):
        st.session_state.current_stage = 'semi'

with col3:
    if st.button("Chung kết", key="nav_final", use_container_width=True):
        st.session_state.current_stage = 'final'

# Admin panel
if current_user["role"] == "admin":
    with st.expander("🔧 Bảng điều khiển Admin", expanded=False):
        st.markdown("### 📊 Thống kê hệ thống")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            total_matches = len(st.session_state.matches)
            st.metric("Tổng số trận", total_matches)
        
        with col2:
            completed_matches = len([m for m in st.session_state.matches if m["score1"] is not None and m["score2"] is not None])
            st.metric("Trận đã hoàn thành", completed_matches)
        
        with col3:
            save_count = len(st.session_state.get('saved_matches', {}))
            st.metric("Lần lưu dữ liệu", save_count)
        
        # Reset data
        if st.button("🔄 Reset toàn bộ dữ liệu", type="secondary"):
            if st.checkbox("Xác nhận reset (thao tác không thể hoàn tác)"):
                for key in ['matches', 'saved_matches', 'group_standings']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.success("✅ Đã reset toàn bộ dữ liệu!")
                st.rerun()

# Main content based on stage
if st.session_state.current_stage == 'group':
    # Group A
    if current_user["role"] == "admin" or current_user.get("group") == "A":
        st.markdown('<div class="group-header"><h3>Bảng A - Lịch thi đấu</h3></div>', unsafe_allow_html=True)
        
        group_a_matches = [match for match in st.session_state.matches if match.get("group") == "A"]
        for match in group_a_matches:
            render_match_card(match)
    
    # Group B
    if current_user["role"] == "admin" or current_user.get("group") == "B":
        st.markdown('<div class="group-header"><h3>Bảng B - Lịch thi đấu</h3></div>', unsafe_allow_html=True)
        
        group_b_matches = [match for match in st.session_state.matches if match.get("group") == "B"]
        for match in group_b_matches:
            render_match_card(match)
    
    # Save button cho trọng tài
    if current_user["role"] == "referee":
        if st.button("💾 Lưu tỷ số vòng bảng", use_container_width=True, type="primary"):
            save_match_data()
            st.markdown('<div class="save-indicator">✅ Đã lưu tỷ số thành công!</div>', unsafe_allow_html=True)
    
    # Standings
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="standings-header"><h3>Bảng xếp hạng A</h3></div>', unsafe_allow_html=True)
        
        for i, standing in enumerate(st.session_state.group_standings["A"]):
            css_class = "qualified" if i < 2 else "not-qualified"
            st.markdown(f"""
            <div class="standing-item {css_class}">
                <div class="standing-row">
                    <div>
                        <div class="team-name">{i+1}. {standing["team"]["name"]}</div>
                        <div class="team-players">{" + ".join(standing["team"]["players"])}</div>
                    </div>
                    <div style="text-align: right; font-size: 0.875rem;">
                        <div>{standing["wins"]}T - {standing["losses"]}B</div>
                        <div>HS: {'+' if standing["points_diff"] >= 0 else ''}{standing["points_diff"]}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="standings-header"><h3>Bảng xếp hạng B</h3></div>', unsafe_allow_html=True)
        
        for i, standing in enumerate(st.session_state.group_standings["B"]):
            css_class = "qualified" if i < 2 else "not-qualified"
            st.markdown(f"""
            <div class="standing-item {css_class}">
                <div class="standing-row">
                    <div>
                        <div class="team-name">{i+1}. {standing["team"]["name"]}</div>
                        <div class="team-players">{" + ".join(standing["team"]["players"])}</div>
                    </div>
                    <div style="text-align: right; font-size: 0.875rem;">
                        <div>{standing["wins"]}T - {standing["losses"]}B</div>
                        <div>HS: {'+' if standing["points_diff"] >= 0 else ''}{standing["points_diff"]}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Generate knockout (chỉ admin)
    if current_user["role"] == "admin":
        if (len(st.session_state.group_standings["A"]) >= 2 and 
            len(st.session_state.group_standings["B"]) >= 2):
            if st.button("🚀 Tạo lịch vòng loại trực tiếp", use_container_width=True, type="primary"):
                generate_knockout_matches()
                st.success("✅ Đã tạo lịch bán kết!")
                st.rerun()

elif st.session_state.current_stage == 'semi':
    st.markdown('<div class="group-header"><h3>⚡ Vòng bán kết</h3></div>', unsafe_allow_html=True)
    
    semi_matches = [match for match in st.session_state.matches if match["stage"] == "semi"]
    for match in semi_matches:
        render_match_card(match)
    
    if current_user["role"] == "admin":
        if st.button("🏆 Tạo lịch chung kết", use_container_width=True, type="primary"):
            generate_final_matches()
            st.success("✅ Đã tạo lịch chung kết!")
            st.rerun()

elif st.session_state.current_stage == 'final':
    st.markdown('<div class="group-header"><h3>🏆 Trận chung kết</h3></div>', unsafe_allow_html=True)
    
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
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 1.2em; font-weight: bold; color: #b8860b; margin-bottom: 0.5rem;">{ranking["title"]}</div>
                        <div style="font-weight: bold; margin-bottom: 0.25rem;">{ranking["team"]["name"]}</div>
                        <div style="color: #6b7280; font-size: 0.9em;">{" + ".join(ranking["team"]["players"])}</div>
                    </div>
                    <div style="font-size: 3em; font-weight: bold; color: #1e40af;">#{ranking["position"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 1rem; color: #6b7280; font-size: 0.875rem;">
    <p>🏓 Giải Pickleball - Hệ thống Trọng tài</p>
    <p>Phiên bản: 2.0 | Người dùng: <strong>{current_user['name']}</strong></p>
</div>
""", unsafe_allow_html=True)