import streamlit as st
from typing import Optional

# Cấu hình trang
st.set_page_config(
    page_title="Giải Pickleball",
    page_icon="🏓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS cho mobile
st.markdown("""
<style>
    /* Reset và base styles */
    .main .block-container {
        padding: 1rem 0.5rem;
        max-width: 100%;
    }
    
    /* Mobile-first approach */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.5rem;
        }
        
        .stColumns {
            gap: 0.5rem;
        }
        
        .stColumn {
            min-width: unset !important;
        }
    }
    
    /* Header mobile-friendly */
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
    
    /* Navigation buttons */
    .nav-container {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }
    
    .nav-button {
        flex: 1;
        min-width: 120px;
        padding: 12px 8px;
        border-radius: 8px;
        text-align: center;
        font-weight: 600;
        font-size: clamp(0.75rem, 2.5vw, 0.875rem);
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .nav-button.active {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(30, 64, 175, 0.3);
    }
    
    .nav-button.inactive {
        background: white;
        color: #1e40af;
        border-color: #1e40af;
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
        font-size: clamp(1rem, 4vw, 1.25rem);
    }
    
    /* Match cards mobile-optimized */
    .match-card {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.75rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .match-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
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
    
    /* Score inputs mobile-friendly */
    .score-input {
        width: 100% !important;
        text-align: center !important;
        font-size: 1.25rem !important;
        font-weight: bold !important;
        padding: 0.75rem !important;
        border-radius: 8px !important;
        border: 2px solid #d1d5db !important;
        background: #f9fafb !important;
        min-height: 48px !important; /* Touch-friendly minimum */
    }
    
    .score-input:focus {
        border-color: #1e40af !important;
        box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.1) !important;
        outline: none !important;
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
    
    /* Standings mobile-optimized */
    .standings-header {
        background: linear-gradient(135deg, #b8860b 0%, #daa520 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .standings-header h3 {
        margin: 0;
        font-size: clamp(1rem, 4vw, 1.25rem);
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
    
    .standing-info {
        flex: 1;
        min-width: 150px;
    }
    
    .standing-stats {
        text-align: right;
        font-size: clamp(0.75rem, 2.5vw, 0.875rem);
        white-space: nowrap;
    }
    
    /* Final match special styling */
    .final-match {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 3px solid #b8860b;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(184, 134, 11, 0.2);
    }
    
    /* Rankings */
    .ranking-item {
        background: linear-gradient(135deg, #fef3c7 0%, #dbeafe 100%);
        border-radius: 12px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        border-left: 5px solid #b8860b;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.1);
    }
    
    .ranking-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
    }
    
    .ranking-info {
        flex: 1;
    }
    
    .ranking-title {
        font-size: clamp(1rem, 4vw, 1.25rem);
        font-weight: bold;
        color: #b8860b;
        margin-bottom: 0.5rem;
    }
    
    .ranking-team {
        font-weight: bold;
        margin-bottom: 0.25rem;
        font-size: clamp(0.875rem, 3vw, 1rem);
    }
    
    .ranking-players {
        color: #6b7280;
        font-size: clamp(0.75rem, 2.5vw, 0.875rem);
    }
    
    .ranking-position {
        font-size: clamp(2rem, 8vw, 3rem);
        font-weight: bold;
        color: #1e40af;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Action button */
    .action-button {
        width: 100%;
        padding: 1rem;
        font-size: clamp(1rem, 3vw, 1.125rem);
        font-weight: bold;
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
        cursor: pointer;
        transition: all 0.3s ease;
        min-height: 56px; /* Touch-friendly */
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(30, 64, 175, 0.4);
    }
    
    /* Mobile responsive adjustments */
    @media (max-width: 640px) {
        .match-card {
            padding: 0.75rem;
        }
        
        .standing-row {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.25rem;
        }
        
        .standing-stats {
            text-align: left;
            width: 100%;
        }
        
        .ranking-row {
            flex-direction: column;
            text-align: center;
            gap: 0.75rem;
        }
    }
    
    /* Touch improvements */
    @media (hover: none) and (pointer: coarse) {
        .match-card:hover {
            transform: none;
        }
        
        .action-button:hover {
            transform: none;
        }
    }
    
    /* Accessibility improvements */
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    }
</style>
""", unsafe_allow_html=True)

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
if 'matches' not in st.session_state:
    st.session_state.matches = [
        # Group A
        {"id": "A1", "team1": teams[0], "team2": teams[1], "score1": None, "score2": None, "stage": "group", "group": "A"},
        {"id": "A2", "team1": teams[2], "team2": teams[3], "score1": None, "score2": None, "stage": "group", "group": "A"},
        {"id": "A3", "team1": teams[0], "team2": teams[2], "score1": None, "score2": None, "stage": "group", "group": "A"},
        {"id": "A4", "team1": teams[1], "team2": teams[3], "score1": None, "score2": None, "stage": "group", "group": "A"},
        {"id": "A5", "team1": teams[1], "team2": teams[2], "score1": None, "score2": None, "stage": "group", "group": "A"},
        {"id": "A6", "team1": teams[0], "team2": teams[3], "score1": None, "score2": None, "stage": "group", "group": "A"},
        # Group B
        {"id": "B1", "team1": teams[5], "team2": teams[7], "score1": None, "score2": None, "stage": "group", "group": "B"},
        {"id": "B2", "team1": teams[6], "team2": teams[7], "score1": None, "score2": None, "stage": "group", "group": "B"},
        {"id": "B3", "team1": teams[4], "team2": teams[6], "score1": None, "score2": None, "stage": "group", "group": "B"},
        {"id": "B4", "team1": teams[4], "team2": teams[5], "score1": None, "score2": None, "stage": "group", "group": "B"},
        {"id": "B5", "team1": teams[5], "team2": teams[6], "score1": None, "score2": None, "stage": "group", "group": "B"},
        {"id": "B6", "team1": teams[4], "team2": teams[7], "score1": None, "score2": None, "stage": "group", "group": "B"},
    ]

if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 'group'

if 'group_standings' not in st.session_state:
    st.session_state.group_standings = {"A": [], "B": []}

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
        
        # Tính điểm cho mỗi trận đấu
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
        
        # Tính hiệu số
        for standing in standings:
            standing["points_diff"] = standing["points_for"] - standing["points_against"]
        
        # Sắp xếp theo thứ tự
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
        {"id": "SF1", "team1": first_a, "team2": second_b, "score1": None, "score2": None, "stage": "semi"},
        {"id": "SF2", "team1": first_b, "team2": second_a, "score1": None, "score2": None, "stage": "semi"}
    ]
    
    # Giữ lại các trận vòng bảng và thêm bán kết
    group_matches = [match for match in st.session_state.matches if match["stage"] == "group"]
    st.session_state.matches = group_matches + semi_matches
    st.session_state.current_stage = 'semi'

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
        "stage": "final"
    }
    
    # Giữ lại các trận cũ và thêm chung kết
    other_matches = [match for match in st.session_state.matches if match["stage"] != "final"]
    st.session_state.matches = other_matches + [final_match]
    st.session_state.current_stage = 'final'

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

def reset_scores(stage: Optional[str] = None):
    """Reset điểm số các trận theo stage (group, semi, final) hoặc tất cả nếu stage=None"""
    for match in st.session_state.matches:
        if stage is None or match["stage"] == stage:
            match["score1"] = None
            match["score2"] = None
    calculate_standings()
    st.experimental_rerun()

def render_match_card(match, is_final=False):
    card_class = "final-match" if is_final else "match-card"
    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)

    title = ""
    if match["stage"] == "group":
        title = f"Trận {match['id']}"
    elif match["stage"] == "semi":
        title = "Bán kết 1" if match["id"] == "SF1" else "Bán kết 2"
    elif match["stage"] == "final":
        title = "🏆 Chung kết"
    st.markdown(f'<div class="match-title">{title}</div>', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns([3, 1.5, 0.5, 1.5, 3])
    with col1:
        st.markdown(f"""
        <div class="team-info">
            <div class="team-name">{match['team1']['name']}</div>
            <div class="team-players">{' + '.join(match['team1']['players'])}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        score1 = st.number_input(
            label="Score 1",
            min_value=0,
            value=match["score1"] if match["score1"] is not None else 0,
            key=f"score1_{match['id']}",
            label_visibility="collapsed"
        )
        if score1 != (match["score1"] or 0):
            match["score1"] = score1
            calculate_standings()
    with col3:
        st.markdown('<div class="vs-text">-</div>', unsafe_allow_html=True)
    with col4:
        score2 = st.number_input(
            label="Score 2",
            min_value=0,
            value=match["score2"] if match["score2"] is not None else 0,
            key=f"score2_{match['id']}",
            label_visibility="collapsed"
        )
        if score2 != (match["score2"] or 0):
            match["score2"] = score2
            calculate_standings()
    with col5:
        st.markdown(f"""
        <div class="team-info">
            <div class="team-name">{match['team2']['name']}</div>
            <div class="team-players">{' + '.join(match['team2']['players'])}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

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
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
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

st.markdown('</div>', unsafe_allow_html=True)

# Group Stage
if st.session_state.current_stage == 'group':
    st.markdown('<div class="group-header"><h3>Bảng A - Lịch thi đấu</h3></div>', unsafe_allow_html=True)
    group_a_matches = [m for m in st.session_state.matches if m.get("group") == "A"]
    for match in group_a_matches:
        render_match_card(match)
    st.markdown('<div class="group-header"><h3>Bảng B - Lịch thi đấu</h3></div>', unsafe_allow_html=True)
    group_b_matches = [m for m in st.session_state.matches if m.get("group") == "B"]
    for match in group_b_matches:
        render_match_card(match)
    if st.button("🔄 Reset tỷ số vòng bảng", key="reset_group", use_container_width=True):
        reset_scores(stage="group")

    st.markdown("---")
    st.markdown('<div class="standings-header"><h3>Bảng xếp hạng A</h3></div>', unsafe_allow_html=True)
    for i, standing in enumerate(st.session_state.group_standings["A"]):
        css_class = "qualified" if i < 2 else "not-qualified"
        st.markdown(f"""
        <div class="standing-item {css_class}">
            <div class="standing-row">
                <div class="standing-info">
                    <div class="team-name">{i+1}. {standing["team"]["name"]}</div>
                    <div class="team-players">{" + ".join(standing["team"]["players"])}</div>
                </div>
                <div class="standing-stats">
                    <div>{standing["wins"]}T - {standing["losses"]}B</div>
                    <div>HS: {'+' if standing["points_diff"] >= 0 else ''}{standing["points_diff"]}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('<div class="standings-header"><h3>Bảng xếp hạng B</h3></div>', unsafe_allow_html=True)
    for i, standing in enumerate(st.session_state.group_standings["B"]):
        css_class = "qualified" if i < 2 else "not-qualified"
        st.markdown(f"""
        <div class="standing-item {css_class}">
            <div class="standing-row">
                <div class="standing-info">
                    <div class="team-name">{i+1}. {standing["team"]["name"]}</div>
                    <div class="team-players">{" + ".join(standing["team"]["players"])}</div>
                </div>
                <div class="standing-stats">
                    <div>{standing["wins"]}T - {standing["losses"]}B</div>
                    <div>HS: {'+' if standing["points_diff"] >= 0 else ''}{standing["points_diff"]}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    if (len(st.session_state.group_standings["A"]) >= 2 and 
        len(st.session_state.group_standings["B"]) >= 2):
        if st.button("🚀 Tạo lịch vòng loại trực tiếp", key="generate_knockout", use_container_width=True, type="primary"):
            generate_knockout_matches()
            st.experimental_rerun()

# Semi-finals
elif st.session_state.current_stage == 'semi':
    st.markdown('<div class="group-header"><h3>⚡ Vòng bán kết</h3></div>', unsafe_allow_html=True)
    semi_matches = [m for m in st.session_state.matches if m["stage"] == "semi"]
    for match in semi_matches:
        render_match_card(match)
    if st.button("🔄 Reset tỷ số bán kết", key="reset_semi", use_container_width=True):
        reset_scores(stage="semi")
    if st.button("🏆 Tạo lịch chung kết", key="generate_final", use_container_width=True, type="primary"):
        generate_final_matches()
        st.experimental_rerun()

# Finals
elif st.session_state.current_stage == 'final':
    st.markdown('<div class="group-header"><h3>🏆 Trận chung kết</h3></div>', unsafe_allow_html=True)
    final_matches = [m for m in st.session_state.matches if m["stage"] == "final"]
    for match in final_matches:
        render_match_card(match, is_final=True)
    if st.button("🔄 Reset tỷ số chung kết", key="reset_final", use_container_width=True):
        reset_scores(stage="final")
    rankings = get_ranking_list()
    if rankings:
        st.markdown("---")
        st.markdown('<div class="standings-header"><h3>🎖️ Kết quả cuối cùng</h3></div>', unsafe_allow_html=True)
        for ranking in rankings:
            st.markdown(f"""
            <div class="ranking-item">
                <div class="ranking-row">
                    <div class="ranking-info">
                        <div class="ranking-title">{ranking["title"]}</div>
                        <div class="ranking-team">{ranking["team"]["name"]}</div>
                        <div class="ranking-players">{" + ".join(ranking["team"]["players"])}</div>
                    </div>
                    <div class="ranking-position">#{ranking["position"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #6b7280; font-size: 0.875rem;">
    <p>🏓 Giải Pickleball - Hệ thống quản lý giải đấu</p>
</div>
""", unsafe_allow_html=True)