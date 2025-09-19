import streamlit as st
import pandas as pd
from typing import List, Dict, Optional

# Cấu hình trang
st.set_page_config(
    page_title="Giải Pickleball",
    page_icon="🏓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS để tạo màu sắc đẹp
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #b8860b, #daa520);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .group-header {
        background: linear-gradient(90deg, #1e40af, #3b82f6);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 1rem 0;
    }
    
    .match-card {
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .standings-card {
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .qualified {
        background: linear-gradient(90deg, #dbeafe, #bfdbfe);
        color: #1e40af;
        font-weight: bold;
    }
    
    .not-qualified {
        background: #f3f4f6;
        color: #374151;
    }
    
    .ranking-card {
        background: linear-gradient(90deg, #fef3c7, #dbeafe);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #b8860b;
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

# Tính toán bảng xếp hạng
calculate_standings()

# Header
st.markdown("""
<div class="main-header">
    <h1>🏓 Giải Pickleball</h1>
    <p>Hệ thống xếp hạng tự động</p>
</div>
""", unsafe_allow_html=True)

# Navigation
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Vòng bảng", use_container_width=True, type="primary" if st.session_state.current_stage == 'group' else "secondary"):
        st.session_state.current_stage = 'group'

with col2:
    if st.button("Bán kết", use_container_width=True, type="primary" if st.session_state.current_stage == 'semi' else "secondary"):
        st.session_state.current_stage = 'semi'

with col3:
    if st.button("Chung kết", use_container_width=True, type="primary" if st.session_state.current_stage == 'final' else "secondary"):
        st.session_state.current_stage = 'final'

st.markdown("---")

# Group Stage
if st.session_state.current_stage == 'group':
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="group-header"><h3>Bảng A - Lịch thi đấu</h3></div>', unsafe_allow_html=True)
        
        group_a_matches = [match for match in st.session_state.matches if match.get("group") == "A"]
        for i, match in enumerate(group_a_matches):
            st.markdown('<div class="match-card">', unsafe_allow_html=True)
            st.write(f"**{match['id']}**")
            
            col_team1, col_score1, col_vs, col_score2, col_team2 = st.columns([3, 1, 1, 1, 3])
            
            with col_team1:
                st.write(f"**{match['team1']['name']}**")
                st.write(f"*{' + '.join(match['team1']['players'])}*")
            
            with col_score1:
                score1 = st.number_input("", min_value=0, value=match["score1"] or 0, key=f"score1_{match['id']}")
                if score1 != (match["score1"] or 0):
                    match["score1"] = score1
            
            with col_vs:
                st.write("**-**")
            
            with col_score2:
                score2 = st.number_input("", min_value=0, value=match["score2"] or 0, key=f"score2_{match['id']}")
                if score2 != (match["score2"] or 0):
                    match["score2"] = score2
            
            with col_team2:
                st.write(f"**{match['team2']['name']}**")
                st.write(f"*{' + '.join(match['team2']['players'])}*")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="group-header"><h3>Bảng B - Lịch thi đấu</h3></div>', unsafe_allow_html=True)
        
        group_b_matches = [match for match in st.session_state.matches if match.get("group") == "B"]
        for i, match in enumerate(group_b_matches):
            st.markdown('<div class="match-card">', unsafe_allow_html=True)
            st.write(f"**{match['id']}**")
            
            col_team1, col_score1, col_vs, col_score2, col_team2 = st.columns([3, 1, 1, 1, 3])
            
            with col_team1:
                st.write(f"**{match['team1']['name']}**")
                st.write(f"*{' + '.join(match['team1']['players'])}*")
            
            with col_score1:
                score1 = st.number_input("", min_value=0, value=match["score1"] or 0, key=f"score1_{match['id']}")
                if score1 != (match["score1"] or 0):
                    match["score1"] = score1
            
            with col_vs:
                st.write("**-**")
            
            with col_score2:
                score2 = st.number_input("", min_value=0, value=match["score2"] or 0, key=f"score2_{match['id']}")
                if score2 != (match["score2"] or 0):
                    match["score2"] = score2
            
            with col_team2:
                st.write(f"**{match['team2']['name']}**")
                st.write(f"*{' + '.join(match['team2']['players'])}*")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Standings
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(90deg, #b8860b, #daa520); color: white; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <h3>Bảng xếp hạng A</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for i, standing in enumerate(st.session_state.group_standings["A"]):
            css_class = "qualified" if i < 2 else "not-qualified"
            st.markdown(f"""
            <div class="standings-card {css_class}">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <strong>{i+1}. {standing["team"]["name"]}</strong><br>
                        <small>{" + ".join(standing["team"]["players"])}</small>
                    </div>
                    <div style="text-align: right;">
                        <div>{standing["wins"]}T - {standing["losses"]}B</div>
                        <small>HS: {'+' if standing["points_diff"] >= 0 else ''}{standing["points_diff"]}</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(90deg, #b8860b, #daa520); color: white; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <h3>Bảng xếp hạng B</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for i, standing in enumerate(st.session_state.group_standings["B"]):
            css_class = "qualified" if i < 2 else "not-qualified"
            st.markdown(f"""
            <div class="standings-card {css_class}">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <strong>{i+1}. {standing["team"]["name"]}</strong><br>
                        <small>{" + ".join(standing["team"]["players"])}</small>
                    </div>
                    <div style="text-align: right;">
                        <div>{standing["wins"]}T - {standing["losses"]}B</div>
                        <small>HS: {'+' if standing["points_diff"] >= 0 else ''}{standing["points_diff"]}</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Button to generate knockout
    if (len(st.session_state.group_standings["A"]) >= 2 and 
        len(st.session_state.group_standings["B"]) >= 2):
        st.markdown("---")
        if st.button("Tạo lịch vòng loại trực tiếp", use_container_width=True, type="primary"):
            generate_knockout_matches()
            st.rerun()

# Semi-finals
elif st.session_state.current_stage == 'semi':
    st.markdown('<div class="group-header"><h3>Vòng bán kết</h3></div>', unsafe_allow_html=True)
    
    semi_matches = [match for match in st.session_state.matches if match["stage"] == "semi"]
    for match in semi_matches:
        st.markdown('<div class="match-card">', unsafe_allow_html=True)
        title = "Bán kết 1" if match["id"] == "SF1" else "Bán kết 2"
        st.write(f"**{title}**")
        
        col_team1, col_score1, col_vs, col_score2, col_team2 = st.columns([3, 1, 1, 1, 3])
        
        with col_team1:
            st.write(f"**{match['team1']['name']}**")
            st.write(f"*{' + '.join(match['team1']['players'])}*")
        
        with col_score1:
            score1 = st.number_input("", min_value=0, value=match["score1"] or 0, key=f"score1_{match['id']}")
            if score1 != (match["score1"] or 0):
                match["score1"] = score1
        
        with col_vs:
            st.write("**-**")
        
        with col_score2:
            score2 = st.number_input("", min_value=0, value=match["score2"] or 0, key=f"score2_{match['id']}")
            if score2 != (match["score2"] or 0):
                match["score2"] = score2
        
        with col_team2:
            st.write(f"**{match['team2']['name']}**")
            st.write(f"*{' + '.join(match['team2']['players'])}*")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("Tạo lịch chung kết", use_container_width=True, type="primary"):
        generate_final_matches()
        st.rerun()

# Finals
elif st.session_state.current_stage == 'final':
    st.markdown("""
    <div style="background: linear-gradient(90deg, #b8860b, #daa520); color: white; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <h3>Trận chung kết</h3>
    </div>
    """, unsafe_allow_html=True)
    
    final_matches = [match for match in st.session_state.matches if match["stage"] == "final"]
    for match in final_matches:
        st.markdown("""
        <div style="border: 3px solid #b8860b; background: linear-gradient(90deg, #fef3c7, #fde68a); border-radius: 8px; padding: 1rem; margin: 0.5rem 0;">
        """, unsafe_allow_html=True)
        
        st.write("**Chung kết**")
        
        col_team1, col_score1, col_vs, col_score2, col_team2 = st.columns([3, 1, 1, 1, 3])
        
        with col_team1:
            st.write(f"**{match['team1']['name']}**")
            st.write(f"*{' + '.join(match['team1']['players'])}*")
        
        with col_score1:
            score1 = st.number_input("", min_value=0, value=match["score1"] or 0, key=f"score1_{match['id']}")
            if score1 != (match["score1"] or 0):
                match["score1"] = score1
        
        with col_vs:
            st.write("**-**")
        
        with col_score2:
            score2 = st.number_input("", min_value=0, value=match["score2"] or 0, key=f"score2_{match['id']}")
            if score2 != (match["score2"] or 0):
                match["score2"] = score2
        
        with col_team2:
            st.write(f"**{match['team2']['name']}**")
            st.write(f"*{' + '.join(match['team2']['players'])}*")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Final Rankings
    rankings = get_ranking_list()
    if rankings:
        st.markdown("---")
        st.markdown("""
        <div style="background: linear-gradient(90deg, #b8860b, #daa520); color: white; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <h3>🏆 Kết quả cuối cùng</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for ranking in rankings:
            st.markdown(f"""
            <div class="ranking-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 1.2em; font-weight: bold; color: #b8860b;">{ranking["title"]}</div>
                        <div style="font-weight: bold; margin: 0.5rem 0;">{ranking["team"]["name"]}</div>
                        <div style="color: #6b7280; font-size: 0.9em;">{" + ".join(ranking["team"]["players"])}</div>
                    </div>
                    <div style="font-size: 3em; font-weight: bold; color: #1e40af;">
                        #{ranking["position"]}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)