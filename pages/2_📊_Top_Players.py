"""
Cricbuzz LiveStats — Top Players & Career Analytics Arcade
-----------------------------------------------------------
High-performance player analytics engine modeled after the Retail Arcade design system:
Sticky HUD, Control Deck format chips, 6-KPI metrics, Leaderboard charts, and Head-to-Head Faceoff.
"""

import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.ui_components import (
    inject_custom_css,
    render_powerbi_sidebar,
    render_hud,
    render_hero,
    render_6_kpis,
    render_html,
    plot_arcade_bar,
    plot_arcade_pie,
)
from services.player_service import player_service
from services.crud_service import crud_service

st.set_page_config(
    page_title="Player Analytics • Cricbuzz PowerBI Studio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_css()
render_powerbi_sidebar()
render_hud()

render_hero(
    title="PLAYER INTELLIGENCE & LEADERBOARDS",
    subtitle="Global cricketer career analytics, strike rates, bowling economies & head-to-head dossiers",
    icon="📊"
)

# -------------------------------------------------------------
# TOP 6-KPI RIBBON FOR PLAYER STATS
# -------------------------------------------------------------
player_kpis = [
    {"lbl": "ODI RUNS KING", "val": "18,426", "delta": "S. Tendulkar (IND)", "type": "gold"},
    {"lbl": "ODI WICKETS RECORD", "val": "534", "delta": "M. Muralitharan (SL)", "type": "up"},
    {"lbl": "HIGHEST CAREER AVG", "val": "58.7", "delta": "V. Kohli (IND)", "type": "up"},
    {"lbl": "T20I STRIKE RATE", "val": "154.2", "delta": "G. Maxwell (AUS)", "type": "party"},
    {"lbl": "BEST ECONOMY RATE", "val": "4.18", "delta": "R. Khan (AFG)", "type": "up"},
    {"lbl": "TRACKED CRICKETERS", "val": "100+", "delta": "10 Test Playing Nations", "type": "gold"}
]
render_6_kpis(player_kpis)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# CONTROL DECK FOR FORMAT & LIMIT FILTERS
# -------------------------------------------------------------
col_deck1, col_deck2, col_deck3 = st.columns([1.1, 1.2, 1.8])
with col_deck1:
    format_choice = st.pills(
        "Cricket Format:",
        options=["ODI", "Test", "T20I", "ALL"],
        default="ODI",
        key="top_players_format"
    ) or "ODI"
with col_deck2:
    leader_limit = st.pills(
        "Display Limit:",
        options=[5, 10, 15, 20, 25],
        default=10,
        key="top_players_limit"
    ) or 10
with col_deck3:
    role_filter = st.pills(
        "Filter Playing Role:",
        options=["All Roles", "Batsman", "Bowler", "All-Rounder", "Wicketkeeper"],
        default="All Roles",
        key="top_players_role"
    ) or "All Roles"

def cb_reset_top_slicers():
    st.session_state["top_players_format"] = "ODI"
    st.session_state["top_players_limit"] = 10
    st.session_state["top_players_role"] = "All Roles"

def cb_quick_top_5():
    st.session_state["top_players_limit"] = 5

def cb_quick_top_25():
    st.session_state["top_players_limit"] = 25

# Quick action controls
col_act1, col_act2, col_act3, col_stat = st.columns([1.1, 1.1, 1.1, 2.5], vertical_alignment="center")
with col_act1:
    st.button("🔄 Reset Slicers", key="reset_top_slicers", on_click=cb_reset_top_slicers, use_container_width=True)
with col_act2:
    st.button("⚡ Quick Top 5", key="quick_top_5_btn", on_click=cb_quick_top_5, use_container_width=True)
with col_act3:
    st.button("🏆 Full Top 25", key="quick_top_25_btn", on_click=cb_quick_top_25, use_container_width=True)

render_html(
    f"""
    <div class="deck" style="padding: 10px 16px; margin-top: 8px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
        <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
            <span class="deck-title" style="font-size: 10px; color: #8A97AB;">ACTIVE FILTER TELEMETRY:</span>
            <span class="status-tag active"><span class="dot" style="background:#008767"></span>FORMAT: {format_choice}</span>
            <span class="status-tag"><span class="dot" style="background:#E8A33D"></span>LIMIT: TOP {leader_limit}</span>
            <span class="status-tag"><span class="dot" style="background:#38BDF8"></span>ROLE: {role_filter.upper()}</span>
        </div>
        <div class="count">
            Showing <b style="color: #10B981;">Top {leader_limit}</b> {role_filter} in <b style="color: #38BDF8;">{format_choice}</b>
        </div>
    </div>
    """
)

tab_leaders, tab_faceoff, tab_profile = st.tabs([
    "🏆 Statistical Leaderboards",
    "⚔️ Head-to-Head Player Faceoff",
    "🔎 Holographic Career Dossier"
])

# -------------------------------------------------------------
# TAB 1: STATISTICAL LEADERBOARDS
# -------------------------------------------------------------
with tab_leaders:
    sub_tab1, sub_tab2 = st.tabs(["🏏 Top Run Scorers", "🎯 Top Wicket Takers"])

    with sub_tab1:
        df_bat = player_service.get_top_run_scorers(format_type=format_choice, limit=leader_limit)
        
        # Filter by role if requested
        if role_filter != "All Roles" and not df_bat.empty:
            df_bat = df_bat[df_bat["playing_role"].str.contains(role_filter, case=False, na=False)]

        if not df_bat.empty:
            c1, c2 = st.columns([13, 11])
            with c1:
                render_html(
                    f"""
                    <div style="margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:700; color:#F8FAFC; font-size:1.05rem;">🏏 Batting Masters ({format_choice})</span>
                        <span class="chip active"><span class="dot" style="background:#10B981"></span>{len(df_bat)} Records</span>
                    </div>
                    """
                )
                
                # Format dataframe display
                disp_df = df_bat[[
                    "player_name", "country", "playing_role", "total_runs",
                    "batting_average", "career_strike_rate", "centuries", "highest_score"
                ]].copy()
                disp_df.columns = ["Player", "Nation", "Role", "Runs", "Average", "SR", "100s", "High Score"]
                st.dataframe(disp_df, use_container_width=True, hide_index=True)

            with c2:
                fig_bat = plot_arcade_bar(
                    df_bat.head(8),
                    x_col="player_name",
                    y_col="total_runs",
                    title=f"Top Run Scorers ({format_choice})",
                    color_col="country"
                )
                st.plotly_chart(fig_bat, use_container_width=True)
        else:
            st.info(f"No batting records match format: {format_choice} and role: {role_filter}.")

    with sub_tab2:
        df_bowl = player_service.get_top_wicket_takers(format_type=format_choice, limit=leader_limit)
        if role_filter != "All Roles" and not df_bowl.empty:
            df_bowl = df_bowl[df_bowl["bowling_style"].notna()]

        if not df_bowl.empty:
            c1, c2 = st.columns([13, 11])
            with c1:
                render_html(
                    f"""
                    <div style="margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:700; color:#F8FAFC; font-size:1.05rem;">🎯 Bowling Titans ({format_choice})</span>
                        <span class="chip active"><span class="dot" style="background:#E8A33D"></span>{len(df_bowl)} Records</span>
                    </div>
                    """
                )
                disp_bowl = df_bowl[[
                    "player_name", "country", "bowling_style", "total_wickets",
                    "economy_rate", "bowling_average", "total_overs", "total_maidens"
                ]].copy()
                disp_bowl.columns = ["Player", "Nation", "Style", "Wickets", "Economy", "Average", "Overs", "Maidens"]
                st.dataframe(disp_bowl, use_container_width=True, hide_index=True)

            with c2:
                fig_bowl = plot_arcade_bar(
                    df_bowl.head(8),
                    x_col="player_name",
                    y_col="total_wickets",
                    title=f"Top Wicket Takers ({format_choice})",
                    color_col="country"
                )
                st.plotly_chart(fig_bowl, use_container_width=True)
        else:
            st.info(f"No bowling records match format: {format_choice}.")

# -------------------------------------------------------------
# TAB 2: HEAD-TO-HEAD FACEOFF (ARCADE FEATURE)
# -------------------------------------------------------------
with tab_faceoff:
    st.markdown(
        """
        <div style="font-size:1.1rem; font-weight:700; color:#F8FAFC; margin-bottom:6px;">
            ⚔️ Head-to-Head Player Comparison Matrix
        </div>
        <div style="font-size:0.85rem; color:#8A97AB; margin-bottom:16px;">
            Select two international cricketers to run an arcade stat battle comparing runs, averages, wickets, and strike rates.
        </div>
        """,
        unsafe_allow_html=True
    )

    all_players_df = crud_service.list_players(limit=100)
    player_names = sorted(all_players_df["full_name"].tolist())
    player_id_map = dict(zip(all_players_df["full_name"], all_players_df["player_id"]))

    fcol1, fcol2 = st.columns(2)
    with fcol1:
        p1_name = st.selectbox("Player 1 (Blue Corner):", player_names, index=0)
    with fcol2:
        default_p2_idx = 1 if len(player_names) > 1 else 0
        p2_name = st.selectbox("Player 2 (Gold Corner):", player_names, index=default_p2_idx)

    if p1_name and p2_name:
        p1_sum = player_service.get_player_career_summary(player_id_map[p1_name])
        p2_sum = player_service.get_player_career_summary(player_id_map[p2_name])

        def extract_totals(sum_data):
            bat = sum_data.get("batting", [])
            bowl = sum_data.get("bowling", [])
            total_r = sum(b.get("total_runs", 0) for b in bat)
            avg_sr = sum(b.get("career_strike_rate", 0) for b in bat) / len(bat) if bat else 0
            cents = sum(b.get("centuries", 0) for b in bat)
            total_w = sum(w.get("total_wickets", 0) for w in bowl)
            avg_econ = sum(w.get("economy_rate", 0) for w in bowl) / len(bowl) if bowl else 0
            return total_r, round(avg_sr, 1), cents, total_w, round(avg_econ, 2)

        r1, sr1, c1, w1, ec1 = extract_totals(p1_sum)
        r2, sr2, c2, w2, ec2 = extract_totals(p2_sum)

        card1_html = f"""
        <div class="card" style="border-top: 4px solid #38BDF8;">
            <div style="font-size:0.75rem; color:#38BDF8; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;">CORNER ALPHA</div>
            <div style="font-size:1.3rem; font-weight:800; color:#F8FAFC; margin-top:2px;">{p1_name}</div>
            <div style="font-size:0.85rem; color:#8A97AB; margin-bottom:12px;">{p1_sum.get('profile', {}).get('country', 'N/A')} &middot; {p1_sum.get('profile', {}).get('playing_role', 'N/A')}</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                <div style="background:#182238; padding:8px; border-radius:8px;">
                    <div style="font-size:0.7rem; color:#8A97AB;">CAREER RUNS</div>
                    <div style="font-size:1.2rem; font-weight:800; color:#F8FAFC;">{r1:,}</div>
                </div>
                <div style="background:#182238; padding:8px; border-radius:8px;">
                    <div style="font-size:0.7rem; color:#8A97AB;">CAREER WICKETS</div>
                    <div style="font-size:1.2rem; font-weight:800; color:#F8FAFC;">{w1}</div>
                </div>
                <div style="background:#182238; padding:8px; border-radius:8px;">
                    <div style="font-size:0.7rem; color:#8A97AB;">STRIKE RATE</div>
                    <div style="font-size:1.2rem; font-weight:800; color:#38BDF8;">{sr1}</div>
                </div>
                <div style="background:#182238; padding:8px; border-radius:8px;">
                    <div style="font-size:0.7rem; color:#8A97AB;">CENTURIES (100s)</div>
                    <div style="font-size:1.2rem; font-weight:800; color:#E8A33D;">{c1}</div>
                </div>
            </div>
        </div>
        """

        card2_html = f"""
        <div class="card" style="border-top: 4px solid #E8A33D;">
            <div style="font-size:0.75rem; color:#E8A33D; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;">CORNER BETA</div>
            <div style="font-size:1.3rem; font-weight:800; color:#F8FAFC; margin-top:2px;">{p2_name}</div>
            <div style="font-size:0.85rem; color:#8A97AB; margin-bottom:12px;">{p2_sum.get('profile', {}).get('country', 'N/A')} &middot; {p2_sum.get('profile', {}).get('playing_role', 'N/A')}</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                <div style="background:#182238; padding:8px; border-radius:8px;">
                    <div style="font-size:0.7rem; color:#8A97AB;">CAREER RUNS</div>
                    <div style="font-size:1.2rem; font-weight:800; color:#F8FAFC;">{r2:,}</div>
                </div>
                <div style="background:#182238; padding:8px; border-radius:8px;">
                    <div style="font-size:0.7rem; color:#8A97AB;">CAREER WICKETS</div>
                    <div style="font-size:1.2rem; font-weight:800; color:#F8FAFC;">{w2}</div>
                </div>
                <div style="background:#182238; padding:8px; border-radius:8px;">
                    <div style="font-size:0.7rem; color:#8A97AB;">STRIKE RATE</div>
                    <div style="font-size:1.2rem; font-weight:800; color:#38BDF8;">{sr2}</div>
                </div>
                <div style="background:#182238; padding:8px; border-radius:8px;">
                    <div style="font-size:0.7rem; color:#8A97AB;">CENTURIES (100s)</div>
                    <div style="font-size:1.2rem; font-weight:800; color:#E8A33D;">{c2}</div>
                </div>
            </div>
        </div>
        """

        battle_c1, battle_c2 = st.columns(2)
        with battle_c1:
            render_html(card1_html)
        with battle_c2:
            render_html(card2_html)

# -------------------------------------------------------------
# TAB 3: HOLOGRAPHIC CAREER DOSSIER & SEARCH
# -------------------------------------------------------------
with tab_profile:
    st.markdown(
        """
        <div style="font-size:1.1rem; font-weight:700; color:#F8FAFC; margin-bottom:6px;">
            🔎 Comprehensive Player Dossier Explorer
        </div>
        """,
        unsafe_allow_html=True
    )

    prof_p_name = st.selectbox(
        "Choose Cricketer to Inspect:",
        options=player_names,
        index=0,
        key="prof_select"
    )

    if prof_p_name:
        pid = player_id_map[prof_p_name]
        summary = player_service.get_player_career_summary(pid)

        if summary and summary.get("profile"):
            prof = summary["profile"]
            
            # Holographic dossier header card
            render_html(
                f"""
                <div class="card" style="border-left: 4px solid #008767; margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <div>
                            <div style="display:flex; align-items:center; gap:10px;">
                                <h2 style="color: #F8FAFC; margin: 0; font-size:1.5rem; font-weight:800;">{prof.get('full_name')}</h2>
                                <span class="chip active"><span class="dot" style="background:#008767"></span>VERIFIED PRO</span>
                            </div>
                            <div style="color: #94A3B8; margin-top: 6px; font-size:0.9rem;">
                                🌍 <b>{prof.get('country')}</b> &middot; 🎭 <b>{prof.get('playing_role')}</b> &middot; 🎂 <b>{prof.get('dob', 'N/A')}</b>
                            </div>
                        </div>
                        <div style="text-align: right; color: #8A97AB; font-size: 0.88rem; background:#182238; padding:8px 14px; border-radius:8px; border:1px solid #1F2C42;">
                            Batting Technique: <b style="color: #38BDF8;">{prof.get('batting_style')}</b><br>
                            Bowling Artillery: <b style="color: #E8A33D;">{prof.get('bowling_style')}</b>
                        </div>
                    </div>
                </div>
                """
            )

            col_b, col_w = st.columns(2)
            with col_b:
                st.markdown(
                    """
                    <div style="font-weight:700; color:#F8FAFC; margin-bottom:8px; display:flex; align-items:center; gap:8px;">
                        <span>🏏 Career Batting by Format</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                batting_records = summary.get("batting", [])
                if batting_records:
                    st.dataframe(pd.DataFrame(batting_records), use_container_width=True, hide_index=True)
                else:
                    st.info("No recorded batting innings for this player.")

            with col_w:
                st.markdown(
                    """
                    <div style="font-weight:700; color:#F8FAFC; margin-bottom:8px; display:flex; align-items:center; gap:8px;">
                        <span>🎯 Career Bowling by Format</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                bowling_records = summary.get("bowling", [])
                if bowling_records:
                    st.dataframe(pd.DataFrame(bowling_records), use_container_width=True, hide_index=True)
                else:
                    st.info("No recorded bowling spells for this player.")
