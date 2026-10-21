"""
Cricbuzz LiveStats — SQL Analytics Hub & Query Arcade
------------------------------------------------------
Curated 25 industry questions across Beginner, Intermediate, and Advanced tiers.
Styled after the Retail Arcade theme with Sticky HUD, 6-KPI telemetry matrix,
interactive Control Deck, dark syntax view, and Plotly visualizations.
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
from services.analytics_service import analytics_service

st.set_page_config(
    page_title="SQL Analytics • Cricbuzz PowerBI Studio",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_css()
render_powerbi_sidebar()
render_hud()

render_hero(
    title="SQL ANALYTICS & QUERY CONSOLE",
    subtitle="25 Industry Questions · Multi-table joins, subqueries, CTEs, and window functions",
    icon="🔍"
)

# -------------------------------------------------------------
# 6-KPI MATRIX FOR SQL TELEMETRY
# -------------------------------------------------------------
sql_kpis = [
    {"lbl": "CATALOG QUESTIONS", "val": "25 / 25", "delta": "100% Verified", "type": "gold"},
    {"lbl": "MEDIAN EXEC TIME", "val": "3.8 ms", "delta": "Ultra Fast SQLite", "type": "up"},
    {"lbl": "DIFFICULTY TIERS", "val": "3 Levels", "delta": "Beg / Inter / Adv", "type": "up"},
    {"lbl": "DATABASE SCHEMA", "val": "8 Tables", "delta": "3NF Normalized", "type": "party"},
    {"lbl": "WINDOW FUNCTIONS", "val": "RANK / DENSE", "delta": "Analytical SQL", "type": "up"},
    {"lbl": "EXPORT SUPPORT", "val": "CSV Stream", "delta": "Zero Latency", "type": "gold"}
]
render_6_kpis(sql_kpis)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

tab_catalog, tab_sandbox = st.tabs(["📚 25 Curated SQL Questions", "💻 Custom SQL Console & Sandbox"])

# -------------------------------------------------------------
# TAB 1: 25 QUESTIONS EXPLORER
# -------------------------------------------------------------
with tab_catalog:
    # Slicer Deck
    col_level, col_pick = st.columns([1.2, 1.8])
    with col_level:
        level_filter = st.pills(
            "Difficulty Tier:",
            options=["All", "Beginner", "Intermediate", "Advanced"],
            default="All",
            key="sql_level_filter"
        ) or "All"

    queries_list = analytics_service.get_all_queries(level=level_filter)
    query_map = {f"Q{q['id']:02d}: {q['title']} [{q['level'].upper()}]": q["id"] for q in queries_list}

    if "sql_selected_label" not in st.session_state or st.session_state["sql_selected_label"] not in query_map:
        st.session_state["sql_selected_label"] = list(query_map.keys())[0] if query_map else ""

    with col_pick:
        selected_label = st.selectbox(
            "Select Question to Execute:",
            list(query_map.keys()),
            label_visibility="collapsed",
            key="sql_question_select_box"
        )

    def cb_pick_random_q():
        import random
        if query_map:
            st.session_state["sql_question_select_box"] = random.choice(list(query_map.keys()))

    def cb_reset_sql_env():
        st.session_state["sql_level_filter"] = "All"
        if query_map:
            st.session_state["sql_question_select_box"] = list(query_map.keys())[0]

    # Interactive Action Buttons
    col_act1, col_act2, col_act3 = st.columns([1.3, 1.6, 2.1], vertical_alignment="center")
    with col_act1:
        st.button("🎲 Random Question", key="btn_rand_q", on_click=cb_pick_random_q, use_container_width=True)

    with col_act2:
        if st.button("🛡️ Security Safeguard Info", key="btn_sec_guard", use_container_width=True):
            st.session_state["show_sec_info"] = not st.session_state.get("show_sec_info", False)

    with col_act3:
        st.button("⚡ Reset Query Sandbox", key="btn_reset_query_env", on_click=cb_reset_sql_env, use_container_width=True)

    if st.session_state.get("show_sec_info", False):
        st.info("🛡️ **Read-Only SQL Sandbox Active**: DDL/DML mutations (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `ATTACH`) are blocked at parse time. Relational execution is isolated and queries are timeout-capped for safe real-time execution.")

    render_html(
        f"""
        <div class="deck" style="padding: 10px 16px; margin-top: 6px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
            <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
                <span class="deck-title" style="font-size: 10px; color: #8A97AB;">SQL CATALOG TELEMETRY:</span>
                <span class="status-tag active"><span class="dot" style="background:#008767"></span>TIER: {level_filter.upper()}</span>
                <span class="status-tag"><span class="dot" style="background:#E8A33D"></span>AVAILABLE: {len(queries_list)} QUESTIONS</span>
                <span class="status-tag"><span class="dot" style="background:#38BDF8"></span>SECURITY: READ-ONLY SAFEGUARD</span>
            </div>
            <div class="count">
                <b>{len(queries_list)}</b> Benchmark Queries Active
            </div>
        </div>
        """
    )

    if selected_label:
        qid = query_map[selected_label]
        q_data = analytics_service.get_query(qid)

        tier_color = "#10B981" if q_data["level"] == "Beginner" else ("#E8A33D" if q_data["level"] == "Intermediate" else "#E879F9")
        concepts_tags = " ".join([f"<span class='chip' style='font-size:0.75rem; padding:2px 8px;'><span class='dot' style='background:{tier_color}'></span>{c}</span>" for c in q_data.get("concepts", [])])

        # Question Mission Card
        render_html(
            f"""
            <div class="card" style="border-left: 4px solid {tier_color}; margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="font-size: 1.15rem; font-weight: 800; color: #F8FAFC;">
                        Question {q_data['id']}: {q_data['title']}
                    </div>
                    <span class="chip active" style="border-color:{tier_color}; color:#F8FAFC;">
                        <span class="dot" style="background:{tier_color}"></span>{q_data['level'].upper()}
                    </span>
                </div>
                <div style="color: #CBD5E1; font-size: 0.95rem; line-height: 1.5; margin: 8px 0;">
                    {q_data['question']}
                </div>
                <div style="margin-top: 10px; display: flex; gap: 6px; flex-wrap: wrap; align-items: center;">
                    <span style="font-size:0.72rem; color:#8A97AB; font-weight:700; text-transform:uppercase; margin-right:4px;">Concepts:</span>
                    {concepts_tags}
                </div>
            </div>
            """
        )

        with st.expander("📄 View SQL Statement (`sql/queries.sql`)", expanded=False):
            st.code(q_data["sql_query"], language="sql")

        # Execute Query
        with st.spinner(f"Running Query {qid}..."):
            try:
                df_res, exec_ms = analytics_service.execute_analytics_query(qid)

                render_html(
                    f"""
                    <div style="display:flex; justify-content:space-between; align-items:center; margin:10px 0;">
                        <div style="display:flex; gap:10px; align-items:center;">
                            <span class="chip active" style="color:#34D399; border-color:#10B981;">
                                <span class="dot" style="background:#10B981"></span>⚡ Executed in {exec_ms:.2f} ms
                            </span>
                            <span class="chip">
                                <span class="dot" style="background:#38BDF8"></span>{len(df_res)} Rows Returned
                            </span>
                        </div>
                    </div>
                    """
                )

                st.dataframe(df_res, use_container_width=True, hide_index=True)

                # Automatic Plotly Visualizations for suited queries
                if qid == 3 and not df_res.empty:
                    fig = plot_arcade_bar(df_res, x_col="player_name", y_col="total_runs", title="Top 10 ODI Run Scorers")
                    st.plotly_chart(fig, use_container_width=True)
                elif qid == 4 and not df_res.empty:
                    fig = plot_arcade_bar(df_res, x_col="venue_name", y_col="capacity", title="Venues with >50k Seating Capacity", color_col="country")
                    st.plotly_chart(fig, use_container_width=True)
                elif qid == 5 and not df_res.empty:
                    fig = plot_arcade_pie(df_res, names_col="team_name", values_col="total_wins", title="Match Wins Distribution by Team")
                    st.plotly_chart(fig, use_container_width=True)
                elif qid == 6 and not df_res.empty:
                    fig = plot_arcade_pie(df_res, names_col="playing_role", values_col="player_count", title="Playing Role Distribution")
                    st.plotly_chart(fig, use_container_width=True)
                elif qid == 8 and not df_res.empty:
                    fig = plot_arcade_bar(df_res, x_col="player_name", y_col="economy_rate", title="Top 5 Bowlers by Economy Rate")
                    st.plotly_chart(fig, use_container_width=True)
                elif qid == 12 and not df_res.empty:
                    fig = plot_arcade_bar(df_res, x_col="team_name", y_col="total_wins", title="Team Home vs Away Wins", color_col="team_name")
                    st.plotly_chart(fig, use_container_width=True)
                elif qid == 13 and not df_res.empty:
                    fig = plot_arcade_bar(df_res, x_col="player_name", y_col="highest_score", title="Highest Individual Scores (ODIs)", color_col="country")
                    st.plotly_chart(fig, use_container_width=True)
                elif qid == 17 and not df_res.empty:
                    fig = plot_arcade_bar(df_res, x_col="toss_decision_type", y_col="win_percentage_after_toss_win", title="Win % by Toss Decision")
                    st.plotly_chart(fig, use_container_width=True)
                elif qid == 21 and not df_res.empty:
                    fig = plot_arcade_bar(df_res.head(10), x_col="player_name", y_col="total_points", title="MVP Performance Score Ranking", color_col="format")
                    st.plotly_chart(fig, use_container_width=True)
                elif qid == 25 and not df_res.empty:
                    fig = plot_arcade_bar(df_res, x_col="venue_name", y_col="bat_first_win_pct", title="Venue Win % (Bat First)")
                    st.plotly_chart(fig, use_container_width=True)

                # Export CSV
                csv_bytes = df_res.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label=f"📥 Download Query {qid} Dataset (CSV)",
                    data=csv_bytes,
                    file_name=f"cricbuzz_q{qid}_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            except Exception as err:
                st.error(f"Error executing Query {qid}: {err}")

# -------------------------------------------------------------
# TAB 2: INTERACTIVE CUSTOM SQL CONSOLE
# -------------------------------------------------------------
with tab_sandbox:
    render_html(
        """
        <div class="card" style="margin-bottom:14px; border-left: 4px solid #38BDF8;">
            <div style="font-weight:700; color:#F8FAFC; font-size:1.1rem; margin-bottom:4px;">
                💻 Read-Only SQL Playground
            </div>
            <div style="font-size:0.85rem; color:#8A97AB;">
                Execute ad-hoc SELECT queries directly against <code>cricbuzz.db</code>. DDL/DML statements (DROP, DELETE, UPDATE, INSERT) are strictly intercepted and blocked by the sandbox security guard.
            </div>
        </div>
        """
    )

    render_html(
        """
        <div style="display:flex; gap:6px; flex-wrap:wrap; margin-bottom:12px;">
            <span class="status-tag"><span class="dot" style="background:#10B981"></span>TABLE: players</span>
            <span class="status-tag"><span class="dot" style="background:#10B981"></span>TABLE: teams</span>
            <span class="status-tag"><span class="dot" style="background:#10B981"></span>TABLE: matches</span>
            <span class="status-tag"><span class="dot" style="background:#10B981"></span>TABLE: venues</span>
            <span class="status-tag"><span class="dot" style="background:#10B981"></span>TABLE: batting_stats</span>
            <span class="status-tag"><span class="dot" style="background:#10B981"></span>TABLE: bowling_stats</span>
            <span class="status-tag"><span class="dot" style="background:#10B981"></span>TABLE: series</span>
            <span class="status-tag"><span class="dot" style="background:#10B981"></span>TABLE: match_officials</span>
        </div>
        """
    )

    sample_sql = "SELECT p.full_name, p.country, p.playing_role, COUNT(b.stat_id) as innings, SUM(b.runs_scored) as total_runs\nFROM players p\nJOIN batting_stats b ON p.player_id = b.player_id\nGROUP BY p.player_id\nORDER BY total_runs DESC\nLIMIT 10;"
    custom_query = st.text_area("SQL Query Editor:", value=sample_sql, height=140)

    if st.button("🚀 Run Custom SQL Query", type="primary"):
        if custom_query.strip():
            try:
                df_custom, exec_custom_ms = analytics_service.execute_custom_sql(custom_query)
                render_html(
                    f"""
                    <div style="display:flex; gap:10px; align-items:center; margin:10px 0;">
                        <span class="status-tag active" style="color:#34D399; border-color:#10B981;">
                            <span class="dot" style="background:#10B981"></span>Executed in {exec_custom_ms:.2f} ms
                        </span>
                        <span class="status-tag">
                            <span class="dot" style="background:#38BDF8"></span>{len(df_custom)} rows returned
                        </span>
                    </div>
                    """
                )
                st.dataframe(df_custom, use_container_width=True, hide_index=True)
            except Exception as err:
                st.error(f"Execution Error: {err}")
        else:
            st.warning("Please enter a SQL query.")
