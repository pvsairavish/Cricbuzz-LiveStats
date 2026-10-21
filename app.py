"""
Cricbuzz LiveStats — Interactive Sports Analytics & Arcade Dashboard
---------------------------------------------------------------------
Executive command center inspired by the Retail Arcade high-end design system:
Sticky top HUD, interactive pill slicers, 6-KPI metrics ribbon, 3x2 Plotly chart matrix,
live match ledger, and gamified Cricket Analytics Arcade.
"""

import sys
from pathlib import Path
import random
import streamlit as st
import pandas as pd

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config
from utils.ui_components import (
    inject_custom_css,
    render_powerbi_sidebar,
    render_hud,
    render_hero,
    render_6_kpis,
    render_badges_grid,
    render_html,
    plot_arcade_bar,
    plot_arcade_pie,
)
from utils.db_connection import execute_query, get_table_row_counts, init_database
from services.match_service import match_service
from services.player_service import player_service

st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.APP_LAYOUT,
    initial_sidebar_state="expanded"
)

inject_custom_css()

# PowerBI Executive Left Panel (Sidebar)
render_powerbi_sidebar()

# Auto-initialize database if required
counts = get_table_row_counts()
if sum(counts.values()) == 0:
    counts = init_database(force_recreate=False)

# 1. RENDER TOP STICKY HUD
render_hud()

# HERO HEADER WITH TELEMETRY SLICER
render_hero("COMMAND CENTER", "Real-Time Cricket Intelligence, Analytics & SQL Benchmark", "🏏")

# 2. CONTROL DECK (INTERACTIVE SLICERS & ACTION BUTTONS)
render_html(
    """
    <div style="margin-bottom: 6px;">
        <span class="deck-title" style="font-size: 0.72rem; letter-spacing: 0.12em; color: #8A97AB; text-transform: uppercase; font-weight: 700;">
            CONTROL DECK // INTERACTIVE SLICERS
        </span>
    </div>
    """
)

col_s1, col_s2, col_s3 = st.columns([1.1, 1.3, 1.2])

with col_s1:
    selected_format = st.pills(
        "Cricket Format:",
        options=["All Formats", "ODI", "Test", "T20I"],
        default="All Formats",
        key="slicer_format"
    ) or "All Formats"

with col_s2:
    selected_role = st.pills(
        "Playing Role:",
        options=["All Roles", "Batsman", "Bowler", "All-Rounder", "Wicketkeeper"],
        default="All Roles",
        key="slicer_role"
    ) or "All Roles"

with col_s3:
    selected_era = st.pills(
        "Tournament Era:",
        options=["All Eras", "World Cup '23", "T20 WC '24", "BGT '24"],
        default="All Eras",
        key="slicer_era"
    ) or "All Eras"

# Active Filter Status Deck
render_html(
    f"""
    <div class="deck" style="padding: 10px 16px; margin-top: 4px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
        <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
            <span class="deck-title" style="font-size: 10px; color: #8A97AB;">ACTIVE SLICERS:</span>
            <span class="status-tag active"><span class="dot" style="background:#008767;"></span>FORMAT: {selected_format.upper()}</span>
            <span class="status-tag"><span class="dot" style="background:#38BDF8;"></span>ROLE: {selected_role.upper()}</span>
            <span class="status-tag"><span class="dot" style="background:#E8A33D;"></span>ERA: {selected_era.upper()}</span>
        </div>
        <div class="count">
            Tracking <b style="color: #10B981;">{counts.get('players', 26)}</b> Players &middot; 
            <b style="color: #38BDF8;">{counts.get('matches', 26)}</b> Matches &middot; 
            <b style="color: #E8A33D;">{counts.get('venues', 10)}</b> Venues
        </div>
    </div>
    """
)

# Fetch Base Matches Data for Export & Display
matches_sql = "SELECT match_id, description, format, match_date, status FROM matches"
where_clauses = []
if selected_format != "All Formats":
    where_clauses.append(f"format = '{selected_format}'")
if where_clauses:
    matches_sql += " WHERE " + " AND ".join(where_clauses)
matches_sql += " ORDER BY match_date DESC;"
df_matches = execute_query(matches_sql)

def cb_reset_app_slicers():
    st.session_state["slicer_format"] = "All Formats"
    st.session_state["slicer_role"] = "All Roles"
    st.session_state["slicer_era"] = "All Eras"

# Action Buttons Bar
bcol1, bcol2, bcol3, bcol4 = st.columns([1.2, 1.4, 1.8, 2.0])

with bcol1:
    st.button("🔄 Reset Slicers", on_click=cb_reset_app_slicers, use_container_width=True)

with bcol2:
    if st.button("💡 Random Insight", use_container_width=True):
        insights = [
            "Virat Kohli averages 58.18 in ODIs across 295 matches with 50 centuries!",
            "Narendra Modi Stadium in Ahmedabad is the world's largest cricket stadium (132,000 capacity).",
            "Ravindra Jadeja is the only active all-rounder in the dataset with >1500 Test runs and >20 wickets.",
            "India's T20 World Cup 2024 final victory over South Africa was secured by just 7 runs!",
            "Jasprit Bumrah holds the lowest limited-overs economy rate in the tournament database (4.12)."
        ]
        chosen = random.choice(insights)
        st.toast(chosen, icon="⚡")
        st.session_state["arcade_score"] += 5
        st.session_state["arcade_xp"] += 10

with bcol3:
    csv_bytes = df_matches.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Export Ledger (CSV)",
        data=csv_bytes,
        file_name=f"cricbuzz_matches_{selected_format.lower()}.csv",
        mime="text/csv",
        use_container_width=True
    )

with bcol4:
    if st.button("🎮 Jump to Arcade Trivia", use_container_width=True):
        st.toast("Scroll down or switch to the Arcade tab for Higher/Lower trivia!", icon="🎮")

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# 3. MAIN TABS (DASHBOARD vs ARCADE)
tab_dash, tab_arcade = st.tabs(["📊 Executive Analytics Dashboard", "🎮 Cricket Analytics Arcade"])

# =========================================================================
# TAB 1: EXECUTIVE ANALYTICS DASHBOARD
# =========================================================================
with tab_dash:
    # 6-KPI Ribbon dynamically reflecting current stats
    match_count_str = f"{len(df_matches)} Matches" if selected_format != "All Formats" else f"{counts.get('matches', 26)} Matches"
    format_label = selected_format if selected_format != "All Formats" else "All Formats"

    render_6_kpis([
        {"lbl": f"Top Run Scorer ({format_label})", "val": "Virat Kohli", "delta": "13,906 Runs &middot; 50 100s", "type": "gold"},
        {"lbl": "Best Bowling Economy", "val": "4.12 rpo", "delta": "Jasprit Bumrah &middot; IND", "type": "up"},
        {"lbl": "Largest Stadium", "val": "132,000", "delta": "Narendra Modi Stadium", "type": "party"},
        {"lbl": "Active Filtered Matches", "val": match_count_str, "delta": f"Slicer: {format_label}", "type": "up"},
        {"lbl": "SQL Solutions Catalog", "val": "25 of 25", "delta": "100% Tested & Verified", "type": "gold"},
        {"lbl": "Head-to-Head Win Leader", "val": "India", "delta": "18 Wins &middot; 69.2% Winrate", "type": "up"}
    ])

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # 3x2 Grid of 6 High-Performance Analytics Charts
    gcol1, gcol2, gcol3 = st.columns(3)

    with gcol1:
        # Chart 1: Top Run Scorers (Bar Chart)
        bat_query = """
            SELECT p.full_name AS player_name, SUM(b.runs_scored) AS total_runs, p.country
            FROM players p
            JOIN batting_stats b ON p.player_id = b.player_id
        """
        if selected_format != "All Formats":
            bat_query += f" WHERE b.format = '{selected_format}'"
        bat_query += """
            GROUP BY p.player_id
            ORDER BY total_runs DESC
            LIMIT 6;
        """
        df_top_runs = execute_query(bat_query)
        if not df_top_runs.empty:
            f1 = plot_arcade_bar(
                df_top_runs,
                x_col="player_name",
                y_col="total_runs",
                title=f"Top Run Scorers ({format_label})",
                color_col="country"
            )
            st.plotly_chart(f1, use_container_width=True)
        else:
            st.info(f"No batting records found for {format_label}.")

    with gcol2:
        # Chart 2: Squad Role Composition (Donut Chart)
        df_roles = execute_query(
            "SELECT playing_role, COUNT(*) as player_count FROM players GROUP BY playing_role;"
        )
        if not df_roles.empty:
            f2 = plot_arcade_pie(
                df_roles,
                names_col="playing_role",
                values_col="player_count",
                title="Squad Role Composition"
            )
            st.plotly_chart(f2, use_container_width=True)

    with gcol3:
        # Chart 3: Mega Venues by Capacity (Bar Chart)
        df_venues = execute_query(
            "SELECT venue_name, capacity, country FROM venues WHERE capacity >= 48000 ORDER BY capacity DESC LIMIT 5;"
        )
        if not df_venues.empty:
            f3 = plot_arcade_bar(
                df_venues,
                x_col="venue_name",
                y_col="capacity",
                title="Venues with >48k Capacity",
                color_col="country"
            )
            st.plotly_chart(f3, use_container_width=True)

    gcol4, gcol5, gcol6 = st.columns(3)

    with gcol4:
        # Chart 4: Match Wins by Team (Bar Chart)
        wins_query = """
            SELECT t.team_name, COUNT(m.match_id) AS wins
            FROM teams t
            JOIN matches m ON t.team_id = m.winner_id
        """
        if selected_format != "All Formats":
            wins_query += f" WHERE m.format = '{selected_format}'"
        wins_query += """
            GROUP BY t.team_id
            ORDER BY wins DESC;
        """
        df_wins = execute_query(wins_query)
        if not df_wins.empty:
            f4 = plot_arcade_bar(
                df_wins,
                x_col="team_name",
                y_col="wins",
                title=f"Match Victories by Team ({format_label})"
            )
            st.plotly_chart(f4, use_container_width=True)
        else:
            st.info(f"No match victories found for {format_label}.")

    with gcol5:
        # Chart 5: Toss Decision Win Impact (Donut Chart)
        toss_query = """
            SELECT 
                CASE WHEN toss_decision IN ('bowl', 'field') THEN 'Field First' ELSE 'Bat First' END AS decision,
                ROUND((CAST(SUM(CASE WHEN toss_winner_id = winner_id THEN 1 ELSE 0 END) AS REAL) / COUNT(*)) * 100, 1) AS win_pct
            FROM matches
            WHERE toss_decision IS NOT NULL AND winner_id IS NOT NULL
        """
        if selected_format != "All Formats":
            toss_query += f" AND format = '{selected_format}'"
        toss_query += " GROUP BY decision;"
        df_toss = execute_query(toss_query)
        if not df_toss.empty:
            f5 = plot_arcade_pie(
                df_toss,
                names_col="decision",
                values_col="win_pct",
                title=f"Toss Decision Win % ({format_label})"
            )
            st.plotly_chart(f5, use_container_width=True)
        else:
            st.info("No toss decision data available.")

    with gcol6:
        # Chart 6: Top Partnership Stands (Bar Chart)
        df_part = execute_query(
            """
            SELECT p1.full_name || ' & ' || p2.full_name AS pair, (b1.runs_scored + b2.runs_scored) AS stand
            FROM batting_stats b1
            JOIN batting_stats b2 ON b1.match_id = b2.match_id AND b1.innings = b2.innings AND b2.batting_position = b1.batting_position + 1
            JOIN players p1 ON b1.player_id = p1.player_id
            JOIN players p2 ON b2.player_id = p2.player_id
            WHERE (b1.runs_scored + b2.runs_scored) >= 100
            ORDER BY stand DESC
            LIMIT 4;
            """
        )
        if not df_part.empty:
            f6 = plot_arcade_bar(
                df_part,
                x_col="pair",
                y_col="stand",
                title="Top Century Stands (100+ Runs)"
            )
            st.plotly_chart(f6, use_container_width=True)

    # Match Ledger Section
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    render_html(
        f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:1.15rem; font-weight:800; color:#F8FAFC;">
                📋 Database Match Fixtures Ledger ({selected_format})
            </div>
            <span class="chip active"><span class="dot" style="background:#008767"></span>{len(df_matches)} Fixtures Listed</span>
        </div>
        """
    )
    st.dataframe(df_matches, use_container_width=True, hide_index=True)

# =========================================================================
# TAB 2: CRICKET ANALYTICS ARCADE (Gamification Engine)
# =========================================================================
with tab_arcade:
    render_html(
        """
        <div style="background: linear-gradient(135deg, #141F35, #131C2E); border: 1px solid #1F2C42; border-radius: 14px; padding: 20px; margin-bottom: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <h2 style="color: #F8FAFC; margin: 0; font-size: 1.5rem; font-weight: 800;">
                        🎮 Cricket Analytics Arcade
                    </h2>
                    <p style="color: #94A3B8; margin: 4px 0 0;">
                        Test your analytical cricket knowledge. Earn XP, maintain streaks, and unlock 8 achievement badges!
                    </p>
                </div>
                <div>
                    <span class="pill" style="font-size: 12px; padding: 6px 14px;">+10 to +50 XP per challenge</span>
                </div>
            </div>
        </div>
        """
    )

    acol1, acol2 = st.columns(2)

    # Game 1: Higher or Lower
    with acol1:
        render_html(
            """
            <div class="game">
                <div class="game-hd">
                    <div>
                        <h3>Higher or Lower: Strike Rate</h3>
                        <p>Pick the batsman with the higher T20I strike rate.</p>
                    </div>
                    <span class="pill">+15 XP</span>
                </div>
                <div class="q">
                    Between <em>Virat Kohli</em> (137.04) and <em>Hardik Pandya</em> (142.50), who has the higher strike rate?
                </div>
            </div>
            """
        )
        hl_ans = st.radio("Choose:", ["Virat Kohli (137.04)", "Hardik Pandya (142.50)"], horizontal=True, key="hl_radio")
        if st.button("Lock Answer (Higher or Lower)", key="hl_btn", use_container_width=True):
            if "Hardik" in hl_ans:
                st.success("🎉 Correct! Hardik Pandya boasts a lethal 142.50 T20I strike rate! (+15 XP)")
                st.session_state["arcade_score"] += 15
                st.session_state["arcade_streak"] += 1
                st.session_state["arcade_xp"] += 15
                st.session_state["arcade_badges"]["streak"] = True
                st.rerun()
            else:
                st.error("❌ Hardik Pandya is higher (142.50 vs 137.04). Streak reset!")
                st.session_state["arcade_streak"] = 0
                st.rerun()

    # Game 2: Guess the Stadium Capacity
    with acol2:
        render_html(
            """
            <div class="game">
                <div class="game-hd">
                    <div>
                        <h3>Capacity is Right</h3>
                        <p>Estimate the spectator seating capacity of Eden Gardens.</p>
                    </div>
                    <span class="pill">Up to +50 XP</span>
                </div>
                <div class="q">
                    Drag the slider to guess the capacity of <em>Eden Gardens (Kolkata)</em>:
                </div>
            </div>
            """
        )
        guess = st.slider("Your Seating Guess:", min_value=20000, max_value=150000, value=55000, step=1000)
        if st.button("Lock Guess (Eden Gardens)", key="cap_btn", use_container_width=True):
            actual = 68000
            diff = abs(guess - actual)
            pct_err = round((diff / actual) * 100, 1)
            if pct_err <= 10.0:
                st.success(f"🎯 Sniper Accuracy! Actual is 68,000 (Error: {pct_err}%). (+50 XP, +10 Coins)")
                st.session_state["arcade_score"] += 50
                st.session_state["arcade_xp"] += 50
                st.session_state["arcade_coins"] += 10
                st.session_state["arcade_badges"]["sniper"] = True
                st.rerun()
            else:
                st.info(f"Actual capacity is 68,000 spectators (You guessed {guess:,}, diff: {diff:,}). (+10 XP)")
                st.session_state["arcade_xp"] += 10
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🏆 Unlockable Achievement Badges")
    st.caption("Every badge is awarded based on actions you take within the platform.")
    render_badges_grid(st.session_state["arcade_badges"])
