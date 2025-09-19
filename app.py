import streamlit as st
from typing import Optional
import sqlite3
import json

# Cấu hình trang
st.set_page_config(
    page_title="Giải Pickleball",
    page_icon="🏓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Kết nối SQLite
conn = sqlite3.connect('pickleball.db', check_same_thread=False)
cursor = conn.cursor()

# Tạo bảng matches nếu chưa tồn tại
cursor.execute('''
CREATE TABLE IF NOT EXISTS matches (
    id TEXT PRIMARY KEY,
    data TEXT NOT NULL
)
''')
conn.commit()

def save_matches_to_db(matches):
    for match in matches:
        cursor.execute('''
            INSERT OR REPLACE INTO matches (id, data) VALUES (?, ?)
        ''', (match['id'], json.dumps(match)))
    conn.commit()

def load_matches_from_db():
    cursor.execute('SELECT data FROM matches')
    rows = cursor.fetchall()
    if not rows:
        return None
    return [json.loads(row[0]) for row in rows]

# Custom CSS cho mobile
st.markdown("""
<style>
    /* CSS styles như phần trước */
    /* ... (bạn có thể giữ nguyên phần CSS đã có) ... */
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

# Khởi tạo session_state.matches từ DB hoặc mặc định
if 'matches' not in st.session_state:
    loaded_matches = load_matches_from_db()
    if loaded_matches is not None:
        st.session_state.matches = loaded_matches
    else:
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
        save_matches_to_db(st.session_state.matches)

if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 'group'

if 'group_standings' not in st.session_state:
    st.session_state.group_standings = {"A": [], "B": []}

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
        {"id": "SF1", "team1": first_a, "team2": second_b, "score1": None, "score2": None, "stage": "semi"},
        {"id": "SF2", "team1": first_b, "team2": second_a, "score1": None, "score2": None, "stage": "semi"}
    ]
    
    group_matches = [match for match in st.session_state.matches if match["stage"] == "group"]
    st.session_state.matches = group_matches + semi_matches
    st.session_state.current_stage = 'semi'
    save_matches_to_db(st.session_state.matches)

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
        "stage": "final"
    }
    
    other_matches = [match for match in st.session_state.matches if match["stage"] != "final"]
    st.session_state.matches = other_matches + [final_match]
    st.session_state.current_stage = 'final'
    save_matches_to_db(st.session_state.matches)

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

def reset_scores(stage: Optional[str] = None):
    for match in st.session_state.matches:
        if stage is None or match["stage"] == stage:
            match["score1"] = None
            match["score2"] = None
    calculate_standings()
    save_matches_to_db(st.session_state.matches)
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
            save_matches_to_db(st.session_state.matches)
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
            save_matches_to_db(st.session_state.matches)
    with col5:
        st.markdown(f"""
        <div class="team-info">
            <div class="team-name">{match['team2']['name']}</div>
            <div class="team-players">{' + '.join(match['team2']['players'])}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

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