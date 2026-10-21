"""
Cricbuzz LiveStats — PowerBI Executive Match Center & Visual Dashboard
-----------------------------------------------------------------------
Real-time Cricbuzz match center with PowerBI Obsidian sidebar, Worm line charts,
phase-by-phase grouped bar charts, scoring distribution donut charts, and live scorecards.
"""

import sys
from pathlib import Path
import streamlit as st
import pandas as pd

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config
from utils.ui_components import (
    inject_custom_css,
    render_powerbi_sidebar,
    render_hud,
    render_hero,
    render_html,
    plot_powerbi_worm_chart,
    plot_powerbi_phase_bar,
    plot_powerbi_donut,
)
from services.match_service import match_service

st.set_page_config(
    page_title="Live Matches • Cricbuzz PowerBI Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_css()

# PowerBI Executive Left Panel (Sidebar)
render_powerbi_sidebar()

# Top Sticky HUD
render_hud()

# Hero Header with Telemetry Sync Toggle
render_hero("MATCH TELEMETRY CENTER", "Live Ball-by-Ball Feed, RapidAPI Telemetry & PowerBI Visualizations", "⚡")

# -------------------------------------------------------------
# 1. POWERBI LIVE MATCH EXECUTIVE SCOREBOARD & KPIS
# -------------------------------------------------------------
render_html(
    """
    <div class="card" style="border-left: 4px solid #10B981; background: #131C2E; margin-bottom: 16px; padding: 16px 20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
            <div style="display:flex; align-items:center; gap:8px;">
                <span class="live-pulse"></span>
                <span style="font-weight:800; color:#F8FAFC; font-size:1.15rem; letter-spacing:-0.01em;">
                    ICC CHAMPIONS TROPHY 2025 &middot; GRAND FINAL
                </span>
                <span class="status-tag active" style="font-size:0.72rem; padding:2px 8px; border-color:#10B981; color:#34D399;">
                    LIVE &middot; OVER 19.4
                </span>
            </div>
            <div style="color:#94A3B8; font-size:0.82rem;">
                📍 <b>Narendra Modi Stadium</b>, Ahmedabad &middot; Pitch: Dry & Flat
            </div>
        </div>

        <div style="display:grid; grid-template-columns: repeat(5, 1fr); gap:12px; padding:12px 0; border-top:1px solid #1F2C42; border-bottom:1px solid #1F2C42;">
            <div>
                <div style="font-size:0.70rem; color:#8A97AB; text-transform:uppercase; font-weight:700;">1st Innings (IND)</div>
                <div style="font-size:1.45rem; font-weight:900; color:#10B981;" class="tnum">212/4 <span style="font-size:0.85rem; color:#8A97AB;">(20.0)</span></div>
                <div style="font-size:0.75rem; color:#64748B;">Kohli 82* &middot; Rohit 48</div>
            </div>
            <div>
                <div style="font-size:0.70rem; color:#8A97AB; text-transform:uppercase; font-weight:700;">Chasing (AUS)</div>
                <div style="font-size:1.45rem; font-weight:900; color:#00BCF2;" class="tnum">208/7 <span style="font-size:0.85rem; color:#8A97AB;">(19.4)</span></div>
                <div style="font-size:0.75rem; color:#64748B;">Head 64 &middot; Maxwell 54</div>
            </div>
            <div>
                <div style="font-size:0.70rem; color:#8A97AB; text-transform:uppercase; font-weight:700;">Current Run Rate</div>
                <div style="font-size:1.45rem; font-weight:900; color:#F8FAFC;" class="tnum">10.57 <span style="font-size:0.85rem; color:#8A97AB;">rpo</span></div>
                <div style="font-size:0.75rem; color:#34D399;">Projected: 215</div>
            </div>
            <div>
                <div style="font-size:0.70rem; color:#8A97AB; text-transform:uppercase; font-weight:700;">Required Run Rate</div>
                <div style="font-size:1.45rem; font-weight:900; color:#E8A33D;" class="tnum">15.00 <span style="font-size:0.85rem; color:#8A97AB;">rpo</span></div>
                <div style="font-size:0.75rem; color:#E8A33D;">Need 5 runs in 2 balls</div>
            </div>
            <div>
                <div style="font-size:0.70rem; color:#8A97AB; text-transform:uppercase; font-weight:700;">Win Probability</div>
                <div style="font-size:1.45rem; font-weight:900; color:#38BDF8;" class="tnum">IND 58%</div>
                <div style="font-size:0.75rem; color:#64748B;">AUS 42%</div>
            </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px; flex-wrap:wrap; gap:8px;">
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:0.78rem; font-weight:700; color:#8A97AB; text-transform:uppercase;">Over 20 Deliveries:</span>
                <span class="status-tag" style="background:#0F172A; color:#34D399; font-weight:800;">4</span>
                <span class="status-tag" style="background:#0F172A; color:#94A3B8; font-weight:800;">1</span>
                <span class="status-tag" style="background:#0F172A; color:#E8A33D; font-weight:800;">6</span>
                <span class="status-tag" style="background:#0F172A; color:#F43F5E; font-weight:800;">W</span>
                <span class="status-tag active" style="background:rgba(16,185,129,0.15); color:#10B981; font-weight:800;">Ball 5 (Live)</span>
            </div>
            <div style="font-size:0.88rem; font-weight:800; color:#FBBF24;">
                ⚡ THRILLER: Australia need a boundary off the remaining 2 deliveries!
            </div>
        </div>
    </div>
    """
)

# -------------------------------------------------------------
# 2. POWERBI VISUALIZATIONS GRID (LINE, BAR, DONUT CHARTS)
# -------------------------------------------------------------
render_html(
    """
    <div style="margin-bottom: 8px;">
        <span class="deck-title" style="font-size: 0.72rem; letter-spacing: 0.12em; color: #8A97AB; text-transform: uppercase; font-weight: 700;">
            POWERBI ANALYTICS CANVAS // INNINGS TRAJECTORY & RUN COMPOSITION
        </span>
    </div>
    """
)

chart_col1, chart_col2 = st.columns([1.5, 1.0])

# Prepare Visual Datasets
df_worm = match_service.get_match_worm_data(90101)
df_phases = match_service.get_match_phase_data(90101)
df_scoring = match_service.get_match_scoring_distribution(90101)
df_wickets = match_service.get_bowling_wicket_distribution(90101)

with chart_col1:
    fig_worm = plot_powerbi_worm_chart(df_worm, team1_name="India", team2_name="Australia", height=320)
    st.plotly_chart(fig_worm, use_container_width=True)

with chart_col2:
    fig_donut_runs = plot_powerbi_donut(df_scoring, names_col="Score_Type", values_col="Runs", title="🎯 Scoring Breakdown (IND 212)", center_metric="212 Runs", height=320)
    st.plotly_chart(fig_donut_runs, use_container_width=True)

chart_col3, chart_col4 = st.columns([1.3, 1.0])

with chart_col3:
    fig_phase = plot_powerbi_phase_bar(df_phases, height=300)
    st.plotly_chart(fig_phase, use_container_width=True)

with chart_col4:
    fig_donut_bowl = plot_powerbi_donut(df_wickets, names_col="Bowling_Type", values_col="Wickets", title="🎳 Wickets by Bowling Style", center_metric="11 Wkts", height=300)
    st.plotly_chart(fig_donut_bowl, use_container_width=True)

# -------------------------------------------------------------
# 3. MATCH FEED CONTROLS & SCORECARD ARCHIVE
# -------------------------------------------------------------
st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

col_feed, col_btn = st.columns([3.5, 1.2], vertical_alignment="center")
with col_feed:
    view_mode = st.pills(
        "Match Center Feed:",
        options=["🔴 Live In-Progress Matches", "🏁 Recently Completed Matches", "🗄️ Database Match History"],
        default="🔴 Live In-Progress Matches",
        key="live_feed_mode"
    ) or "🔴 Live In-Progress Matches"
with col_btn:
    if st.button("🔄 Refresh Live Stream", key="refresh_live_btn", use_container_width=True):
        st.cache_data.clear()
        st.toast("Real-time live feed refreshed!", icon="⚡")
        st.rerun()

render_html(
    f"""
    <div class="deck" style="padding: 10px 16px; margin-top: 4px; margin-bottom: 14px; display:flex; justify-content:space-between; align-items:center;">
        <span class="status-tag active"><span class="dot" style="background:#10B981;"></span>ACTIVE FEED: {view_mode}</span>
        <span class="status-tag"><span class="dot" style="background:#38BDF8;"></span>TELEMETRY REFRESH: REAL-TIME (SUB-SECOND)</span>
    </div>
    """
)


def render_match_card(m: dict):
    """Renders a high-end Cricbuzz match card matching the Retail Arcade theme."""
    is_live = "live" in m.get("state", "").lower() or "progress" in m.get("state", "").lower()
    pulse_dot = '<span class="live-pulse"></span>' if is_live else ""
    status_color = "#34D399" if is_live else "#FBBF24"

    card_html = f"""
    <div class="card" style="border-left: 4px solid #008767; background: #131C2E; margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap;">
            <span style="color: #94A3B8; font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">
                {m.get('series_name', 'International Series')} &middot; <span style="color: #38BDF8;">{m.get('format', 'T20')}</span>
            </span>
            <span class="pill" style="background: rgba(0, 135, 103, 0.18); border-color: #008767; color: #34D399;">
                {pulse_dot}{m.get('description', 'Fixture')}
            </span>
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-top: 1px solid #1F2C42; border-bottom: 1px solid #1F2C42;">
            <div style="flex: 1;">
                <div style="font-size: 1.35rem; font-weight: 800; color: #F8FAFC;">
                    {m.get('team1_name', 'Team 1')}
                </div>
                <div style="font-size: 1.15rem; font-weight: 700; color: #38BDF8; font-variant-numeric: tabular-nums;">
                    {m.get('team1_score', 'Yet to bat')}
                </div>
            </div>
            
            <div style="padding: 0 20px; color: #64748B; font-weight: 900; font-size: 1.1rem;">
                VS
            </div>
            
            <div style="flex: 1; text-align: right;">
                <div style="font-size: 1.35rem; font-weight: 800; color: #F8FAFC;">
                    {m.get('team2_name', 'Team 2')}
                </div>
                <div style="font-size: 1.15rem; font-weight: 700; color: #38BDF8; font-variant-numeric: tabular-nums;">
                    {m.get('team2_score', 'Yet to bat')}
                </div>
            </div>
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px; font-size: 0.85rem; color: #94A3B8; flex-wrap: wrap; gap: 8px;">
            <div>📍 <b>{m.get('venue_name', 'Stadium')}</b> &middot; {m.get('venue_city', '')}</div>
            <div style="font-weight: 700; color: {status_color}; font-size: 0.9rem;">
                📢 {m.get('status', 'Match in progress')}
            </div>
        </div>
    </div>
    """
    render_html(card_html)


if view_mode == "🔴 Live In-Progress Matches":
    with st.spinner("Streaming real-time matches from Cricbuzz API..."):
        matches = match_service.get_live_matches()

    if not matches:
        st.info("No active international matches live at this moment.")
    else:
        st.caption(f"Showing **{len(matches)}** real-time international fixture(s) via Cricbuzz REST API.")
        for match in matches:
            render_match_card(match)
            mid = match.get("match_id")
            if mid:
                with st.expander(f"📋 Expand Scorecard: {match['team1_name']} vs {match['team2_name']} ({match['description']})"):
                    scorecard = match_service.get_detailed_scorecard(mid)
                    innings = scorecard.get("innings", [])
                    if innings:
                        for inn in innings:
                            render_html(
                                f"""
                                <div style="display: flex; justify-content: space-between; align-items: center; background: #182238; padding: 10px 14px; border-radius: 8px; margin: 12px 0 8px;">
                                    <b style="color: #38BDF8; font-size: 1.1rem;">🏏 {inn['team_name']}</b>
                                    <b style="color: #F8FAFC; font-size: 1.15rem;" class="tnum">{inn['runs']}/{inn['wickets']} in {inn['overs']} ov (RR: {inn['run_rate']})</b>
                                </div>
                                """
                            )
                            c_bat, c_bowl = st.columns([3, 2])
                            with c_bat:
                                st.caption("Innings Batting Performance")
                                if inn.get("batsmen"):
                                    df_bat = pd.DataFrame(inn["batsmen"])
                                    st.dataframe(
                                        df_bat[["name", "runs", "balls", "fours", "sixes", "strike_rate", "dismissal"]],
                                        use_container_width=True,
                                        hide_index=True
                                    )
                            with c_bowl:
                                st.caption("Innings Bowling Figures")
                                if inn.get("bowlers"):
                                    df_bowl = pd.DataFrame(inn["bowlers"])
                                    st.dataframe(
                                        df_bowl[["name", "overs", "maidens", "runs", "wickets", "economy"]],
                                        use_container_width=True,
                                        hide_index=True
                                    )
                    else:
                        st.info("Detailed scorecard will populate as balls are bowled.")

elif view_mode == "🏁 Recently Completed Matches":
    with st.spinner("Fetching recently completed matches..."):
        matches = match_service.get_recent_matches()

    if not matches:
        st.info("No recent matches found.")
    else:
        st.caption(f"Displaying **{len(matches)}** recently concluded fixtures.")
        for match in matches:
            render_match_card(match)

elif view_mode == "🗄️ Database Match History":
    st.caption("Historical fixtures stored and archived in local SQLite database.")
    db_matches = match_service.get_db_matches(limit=25)
    if db_matches:
        df_db = pd.DataFrame(db_matches)
        st.dataframe(
            df_db[[
                "description", "format", "match_date", "team1_name",
                "team2_name", "winner_name", "victory_margin", "victory_type", "venue_name"
            ]],
            use_container_width=True,
            hide_index=True
        )
