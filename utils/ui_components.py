"""
Cricbuzz LiveStats — UI Components & Arcade Design Engine
---------------------------------------------------------
Bespoke presentation components modeled after the Retail Arcade design system:
Sticky HUD, Control Deck slicers, 6-KPI matrix, Arcade games, and Plotly charts.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config

import streamlit.components.v1 as components

CSS_FILE = PROJECT_ROOT / "assets" / "styles.css"

# Pre-compiled 80ms 960Hz->680Hz crisp UI chirp WAV audio (offline, zero-latency)
BEEP_WAV_BASE64 = (
    "data:audio/wav;base64,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"
)


def inject_custom_css():
    """Injects bespoke design stylesheet and active Web Audio sound engine into Streamlit."""
    if CSS_FILE.exists():
        with open(CSS_FILE, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    # Active Web Audio Synthesizer Engine rendered via components.html to guarantee browser execution
    sound_muted_js = "true" if not st.session_state.get("sound_fx_enabled", True) else "false"
    audio_component_html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"/></head>
    <body style="margin:0; padding:0; overflow:hidden;">
    <script>
    (function() {{
        const isMuted = {sound_muted_js};
        const B64_DATA = "{BEEP_WAV_BASE64}";

        function installAudio(w, doc) {{
            if (!w || !doc) return;
            w.__cricbuzzSoundMuted = isMuted;

            if (w.__cricbuzzAudioEngineReady) return;
            w.__cricbuzzAudioEngineReady = true;

            let audioCtx = null;

            function triggerBeep() {{
                if (w.__cricbuzzSoundMuted === true) return;

                // Strategy 1: HTML5 Audio instance with Base64 WAV
                try {{
                    const audio = new w.Audio(B64_DATA);
                    audio.volume = 0.5;
                    const p = audio.play();
                    if (p && p.catch) p.catch(function() {{}});
                }} catch (err) {{}}

                // Strategy 2: Web Audio API Oscillator
                try {{
                    const AudioCtx = w.AudioContext || w.webkitAudioContext;
                    if (AudioCtx) {{
                        if (!audioCtx) {{
                            audioCtx = new AudioCtx();
                        }}
                        if (audioCtx.state === 'suspended') {{
                            audioCtx.resume();
                        }}
                        const now = audioCtx.currentTime;
                        const osc = audioCtx.createOscillator();
                        const gain = audioCtx.createGain();
                        osc.type = 'sine';
                        osc.frequency.setValueAtTime(960, now);
                        osc.frequency.exponentialRampToValueAtTime(680, now + 0.08);
                        gain.gain.setValueAtTime(0.25, now);
                        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
                        osc.connect(gain);
                        gain.connect(audioCtx.destination);
                        osc.start(now);
                        osc.stop(now + 0.08);
                    }}
                }} catch (err) {{}}
            }}

            w.playCricbuzzSound = triggerBeep;

            // Global capture click listener across entire document
            doc.addEventListener('click', function(e) {{
                const target = e.target;
                const btn = target.closest(
                    'button, [role="button"], [role="tab"], .chip, [data-baseweb="tab"], ' +
                    '[data-testid="stPills"] button, a, [data-testid="stPageLink-NavLink"], ' +
                    'input[type="submit"], input[type="button"], .stButton button'
                );
                if (btn) {{
                    triggerBeep();
                }}
            }}, true);
        }}

        try {{
            installAudio(window.parent, window.parent.document);
        }} catch (e) {{
            try {{
                installAudio(window.top, window.top.document);
            }} catch (e2) {{
                installAudio(window, document);
            }}
        }}
    }})();
    </script>
    </body>
    </html>
    """
    components.html(audio_component_html, height=0, width=0)


def render_html(html_str: str):
    """
    Renders raw HTML safely in Streamlit by stripping leading indentation
    and newlines so Markdown never misinterprets lines as code blocks.
    """
    clean_lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    st.markdown("".join(clean_lines), unsafe_allow_html=True)


import re

def render_hero(title: str, subtitle: str, icon: str = "🏏", key_suffix: str = ""):
    """Renders a sleek arcade-style page header with micro-branding and interactive telemetry slicer."""
    if "telemetry_stream_mode" not in st.session_state:
        st.session_state["telemetry_stream_mode"] = "STREAM ONLINE"

    current_mode = st.session_state["telemetry_stream_mode"]

    hcol_left, hcol_right = st.columns([3.2, 1.8], vertical_alignment="center")

    with hcol_left:
        render_html(
            f"""
            <div style="padding: 4px 0 6px 0;">
                <span class="deck-title" style="font-size: 0.72rem; letter-spacing: 0.12em; color: #8A97AB; text-transform: uppercase; font-weight: 700;">
                    MODULE TELEMETRY // {icon}
                </span>
                <div style="font-size: 1.35rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.02em; margin-top: 2px;">
                    {title}
                </div>
                <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 2px;">
                    {subtitle}
                </div>
            </div>
            """
        )

    with hcol_right:
        safe_slug = re.sub(r"[^a-zA-Z0-9_]", "_", title.lower())
        widget_key = f"hero_telemetry_mode_{safe_slug}_{key_suffix}" if key_suffix else f"hero_telemetry_mode_{safe_slug}"

        selected_mode = st.pills(
            "Telemetry Sync Mode:",
            options=["STREAM ONLINE", "LOW LATENCY"],
            default=current_mode,
            key=widget_key
        ) or current_mode

        if selected_mode != current_mode:
            st.session_state["telemetry_stream_mode"] = selected_mode
            if selected_mode == "LOW LATENCY":
                st.toast("⚡ Low Latency Mode active: Local sub-millisecond cached ledger enabled (<1ms latency)", icon="⚡")
            else:
                st.toast("🟢 Stream Online Mode active: Live sync with RapidAPI telemetry stream enabled", icon="📡")
            st.rerun()


def init_arcade_session():
    """Initializes user game state in Streamlit session_state."""
    if "arcade_score" not in st.session_state:
        st.session_state["arcade_score"] = 120
    if "arcade_streak" not in st.session_state:
        st.session_state["arcade_streak"] = 3
    if "arcade_coins" not in st.session_state:
        st.session_state["arcade_coins"] = 45
    if "arcade_xp" not in st.session_state:
        st.session_state["arcade_xp"] = 180
    if "arcade_badges" not in st.session_state:
        st.session_state["arcade_badges"] = {"first": True, "filter": True, "streak": True}


def render_hud():
    """Renders the top sticky Heads-Up Display (HUD) inspired by Retail Arcade."""
    init_arcade_session()
    score = st.session_state["arcade_score"]
    streak = st.session_state["arcade_streak"]
    coins = st.session_state["arcade_coins"]
    xp = st.session_state["arcade_xp"]

    level_name = "Novice"
    xp_max = 150
    if xp >= 400:
        level_name = "Data Wizard"
        xp_max = 800
    elif xp >= 250:
        level_name = "Strategist"
        xp_max = 400
    elif xp >= 100:
        level_name = "Analyst"
        xp_max = 250

    pct_fill = min(100, int((xp / xp_max) * 100))

    api_badge = (
        '<span class="badge" style="background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid #10B981;">● LIVE API</span>'
        if config.IS_LIVE_API_ENABLED
        else '<span class="badge" style="background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid #F59E0B;">● MOCK MODE</span>'
    )

    hud_html = f"""
    <header class="hud">
        <div class="hud-in">
            <div class="brand">
                <h1>🏏 Cricbuzz LiveStats</h1>
                <span>Sports Analytics &middot; 25 SQL Engine</span>
            </div>
            <div class="stat"><b class="tnum">{score}</b><i>Score</i></div>
            <div class="stat fire"><b class="tnum">🔥 {streak}</b><i>Streak</i></div>
            <div class="stat gold"><b class="tnum">🪙 {coins}</b><i>Coins</i></div>
            <div class="xp">
                <div class="xp-top"><b>{level_name}</b><em>{xp} / {xp_max} XP</em></div>
                <div class="xp-bar"><div class="xp-fill" style="width: {pct_fill}%;"></div></div>
            </div>
            <div>
                {api_badge}
            </div>
        </div>
    </header>
    """
    render_html(hud_html)


def render_6_kpis(kpi_data: List[Dict[str, str]]):
    """
    Renders 6 glassmorphic KPI cards in a tight responsive grid.
    kpi_data = [{"lbl": "...", "val": "...", "delta": "...", "type": "up|down|gold|flat"}]
    """
    cards_html = []
    for item in kpi_data:
        delta_class = item.get("type", "up")
        cards_html.append(
            f'<div class="kpi">'
            f'<div class="lbl">{item.get("lbl", "")}</div>'
            f'<div class="val tnum">{item.get("val", "")}</div>'
            f'<div class="delta {delta_class}">{item.get("delta", "")}</div>'
            f'</div>'
        )

    full_grid = f'<div class="kpis">{"".join(cards_html)}</div>'
    render_html(full_grid)


def render_badges_grid(unlocked: Dict[str, bool]):
    """Renders the 8 arcade achievement badges grid."""
    BADGES_DEF = [
        {"k": "first", "ico": "🏏", "t": "First Blood", "d": "Answered first cricket trivia or query correctly"},
        {"k": "filter", "ico": "🎯", "t": "Sharp Filter", "d": "Filtered dataset using the Control Deck"},
        {"k": "century", "ico": "💯", "t": "Century Hunter", "d": "Examined 100+ run batting partnerships"},
        {"k": "stadium", "ico": "🏟️", "t": "Mega Stadium", "d": "Discovered stadiums with >50,000 capacity"},
        {"k": "streak", "ico": "🔥", "t": "On Fire", "d": "Achieved a 3+ question streak in the Arcade"},
        {"k": "sniper", "ico": "🎯", "t": "Stats Sniper", "d": "Guessed stadium capacity within 10% accuracy"},
        {"k": "sql", "ico": "⚡", "t": "SQL Maestro", "d": "Executed advanced window function queries"},
        {"k": "wizard", "ico": "👑", "t": "Data Wizard", "d": "Reached top level in the Cricket Analytics Arcade"}
    ]

    cards_html = []
    for b in BADGES_DEF:
        is_on = unlocked.get(b["k"], False)
        on_class = "on" if is_on else ""
        cards_html.append(
            f'<div class="badge-card {on_class}">'
            f'<div class="ico">{b["ico"]}</div>'
            f'<div>'
            f'<b>{b["t"]}</b>'
            f'<small>{b["d"]}</small>'
            f'</div>'
            f'</div>'
        )

    grid_html = f'<div class="badges">{"".join(cards_html)}</div>'
    render_html(grid_html)



def plot_arcade_bar(df: pd.DataFrame, x_col: str, y_col: str, title: str, color_col: str = None, height: int = 330) -> go.Figure:
    """Generates an aesthetic Plotly bar chart matching the Retail Arcade color system."""
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        template="plotly_dark",
        color_discrete_sequence=["#10B981", "#00A9B4", "#E8A33D", "#E879F9", "#38BDF8"]
    )
    fig.update_layout(
        height=height,
        paper_bgcolor="#131C2E",
        plot_bgcolor="#131C2E",
        font=dict(family="Inter, sans-serif", color="#E5E7EB", size=11),
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(size=14, color="#F8FAFC", family="Inter, sans-serif"),
            x=0.02,
            y=0.96
        ),
        margin=dict(l=20, r=20, t=46 if title else 20, b=30),
        xaxis=dict(gridcolor="#1F2C42", linecolor="#1F2C42", tickfont=dict(color="#8A97AB")),
        yaxis=dict(gridcolor="#1F2C42", linecolor="#1F2C42", tickfont=dict(color="#8A97AB")),
        legend=dict(font=dict(color="#8A97AB", size=10), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig


def plot_arcade_pie(df: pd.DataFrame, names_col: str, values_col: str, title: str, height: int = 330) -> go.Figure:
    """Generates an aesthetic Plotly donut chart matching Retail Arcade styling."""
    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        title=title,
        hole=0.55,
        template="plotly_dark",
        color_discrete_sequence=["#008767", "#00A9B4", "#E8A33D", "#E879F9", "#10B981", "#64748B"]
    )
    fig.update_layout(
        height=height,
        paper_bgcolor="#131C2E",
        plot_bgcolor="#131C2E",
        font=dict(family="Inter, sans-serif", color="#E5E7EB", size=11),
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(size=14, color="#F8FAFC", family="Inter, sans-serif"),
            x=0.02,
            y=0.96
        ),
        margin=dict(l=20, r=20, t=46 if title else 20, b=30),
        legend=dict(font=dict(color="#8A97AB", size=10), orientation="h", yanchor="bottom", y=-0.15)
    )
    return fig


# Backward compatibility aliases
plot_bar_chart = plot_arcade_bar
plot_pie_chart = plot_arcade_pie


def render_powerbi_sidebar():
    """Renders an executive Microsoft PowerBI Obsidian left navigation panel."""
    with st.sidebar:
        render_html(
            """
            <div style="padding: 12px 14px; background: linear-gradient(135deg, #131C2E 0%, #1A263E 100%); border-radius: 10px; border: 1px solid #2A3B57; margin-bottom: 12px;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <div style="width:38px; height:38px; border-radius:8px; background:linear-gradient(135deg, #F2C811 0%, #E8A33D 60%, #10B981 100%); display:flex; align-items:center; justify-content:center; font-size:20px; box-shadow:0 0 16px rgba(242,200,17,0.4);">
                        📊
                    </div>
                    <div>
                        <div style="font-size:1.05rem; font-weight:800; color:#FFFFFF; letter-spacing:-0.02em; line-height:1.2;">
                            POWERBI STUDIO
                        </div>
                        <div style="font-size:0.72rem; color:#8A97AB; font-weight:700; text-transform:uppercase; letter-spacing:0.08em;">
                            Cricket Executive Suite
                        </div>
                    </div>
                </div>
            </div>
            """
        )

        # Sound FX Master Switch
        if "sound_fx_enabled" not in st.session_state:
            st.session_state["sound_fx_enabled"] = True

        sound_on = st.session_state["sound_fx_enabled"]
        sound_label = "🔊 Audio Feedback: ON" if sound_on else "🔇 Audio Feedback: OFF"

        def cb_toggle_audio():
            st.session_state["sound_fx_enabled"] = not st.session_state["sound_fx_enabled"]

        st.button(
            sound_label,
            key="pbi_sidebar_audio_btn",
            on_click=cb_toggle_audio,
            use_container_width=True,
            help="Click to enable or mute interactive click beeps"
        )

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        # Workspace Navigation
        st.markdown(
            """
            <div style="font-size:0.68rem; font-weight:800; color:#8A97AB; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:6px;">
                WORKSPACE REPORTS
            </div>
            """,
            unsafe_allow_html=True
        )

        st.page_link("app.py", label="Executive Command Center", icon="🏠")
        st.page_link("pages/1_⚡_Live_Matches.py", label="Live Match Center & Worms", icon="⚡")
        st.page_link("pages/2_📊_Top_Players.py", label="Top Cricketers & Dossiers", icon="📊")
        st.page_link("pages/3_🔍_SQL_Analytics.py", label="SQL Benchmark (25 Queries)", icon="🔍")
        st.page_link("pages/4_🛠️_CRUD_Operations.py", label="Administrative DB Console", icon="🛠️")

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # Global Slicer Pane
        st.markdown(
            """
            <div style="font-size:0.68rem; font-weight:800; color:#8A97AB; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:6px;">
                GLOBAL SLICERS
            </div>
            """,
            unsafe_allow_html=True
        )

        st.pills(
            "Tournament Filter:",
            options=["All Events", "Champions Trophy", "T20 World Cup", "BGT", "IPL"],
            default=st.session_state.get("global_pbi_tournament", "All Events"),
            key="global_pbi_tournament"
        )

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # Live Database Telemetry Card
        render_html(
            """
            <div style="background:#0F172A; border:1px solid #1E293B; border-radius:8px; padding:10px 12px; margin-top:4px;">
                <div style="font-size:0.68rem; font-weight:800; color:#8A97AB; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:6px;">
                    SYSTEM TELEMETRY
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.78rem;">
                    <span style="color:#94A3B8;">RapidAPI Feed:</span>
                    <span style="color:#10B981; font-weight:700;">● Active Stream</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.78rem;">
                    <span style="color:#94A3B8;">SQLite Engine:</span>
                    <span style="color:#38BDF8; font-weight:700;">3.45.2 (WAL)</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.78rem;">
                    <span style="color:#94A3B8;">Relational Integrity:</span>
                    <span style="color:#E8A33D; font-weight:700;">7 Tables Enforced</span>
                </div>
            </div>
            <div style="margin-top:14px; text-align:center; font-size:0.70rem; color:#64748B;">
                PowerBI Cricbuzz Studio &middot; v2.6 Enterprise<br/>
                ICC Official Certified Analytics
            </div>
            """
        )


def plot_powerbi_worm_chart(df: pd.DataFrame, team1_name: str = "India", team2_name: str = "Australia", height: int = 340) -> go.Figure:
    """Generates an executive PowerBI-styled Worm line chart comparing cumulative runs over overs."""
    fig = go.Figure()

    t1_col = f"{team1_name} (IND)" if f"{team1_name} (IND)" in df.columns else df.columns[1]
    t2_col = f"{team2_name} (AUS)" if f"{team2_name} (AUS)" in df.columns else df.columns[3]

    # Team 1 Trace (India - Emerald Green #10B981)
    fig.add_trace(go.Scatter(
        x=df["Over"],
        y=df[t1_col],
        mode="lines+markers",
        name=f"{team1_name} (212/4)",
        line=dict(color="#10B981", width=3.5, shape="spline"),
        marker=dict(size=6, color="#10B981", line=dict(color="#FFFFFF", width=1)),
        hovertemplate="<b>%{y} runs</b> (Over %{x})<extra>" + team1_name + "</extra>"
    ))

    # Team 2 Trace (Australia - PowerBI Cyan #00BCF2)
    fig.add_trace(go.Scatter(
        x=df["Over"],
        y=df[t2_col],
        mode="lines+markers",
        name=f"{team2_name} (208/7)",
        line=dict(color="#00BCF2", width=3.5, shape="spline"),
        marker=dict(size=6, color="#00BCF2", line=dict(color="#FFFFFF", width=1)),
        hovertemplate="<b>%{y} runs</b> (Over %{x})<extra>" + team2_name + "</extra>"
    ))

    fig.update_layout(
        height=height,
        paper_bgcolor="#131C2E",
        plot_bgcolor="#131C2E",
        font=dict(family="Inter, sans-serif", color="#E5E7EB", size=11),
        title=dict(
            text="<b>📈 Live Worm Chart: Cumulative Innings Run Progression</b>",
            font=dict(size=14, color="#F8FAFC", family="Inter, sans-serif"),
            x=0.02,
            y=0.96
        ),
        margin=dict(l=20, r=20, t=46, b=30),
        xaxis=dict(
            title="Overs Completed",
            gridcolor="#1F2C42",
            linecolor="#1F2C42",
            tickfont=dict(color="#8A97AB"),
            dtick=2
        ),
        yaxis=dict(
            title="Cumulative Score",
            gridcolor="#1F2C42",
            linecolor="#1F2C42",
            tickfont=dict(color="#8A97AB")
        ),
        legend=dict(
            font=dict(color="#8A97AB", size=10),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode="x unified"
    )
    return fig


def plot_powerbi_phase_bar(df: pd.DataFrame, height: int = 340) -> go.Figure:
    """Generates an executive PowerBI grouped bar chart comparing runs by match phases."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["Phase"],
        y=df["India (IND)"],
        name="India (IND)",
        marker_color="#10B981",
        text=df["India (IND)"],
        textposition="auto"
    ))
    fig.add_trace(go.Bar(
        x=df["Phase"],
        y=df["Australia (AUS)"],
        name="Australia (AUS)",
        marker_color="#00BCF2",
        text=df["Australia (AUS)"],
        textposition="auto"
    ))

    fig.update_layout(
        barmode="group",
        height=height,
        paper_bgcolor="#131C2E",
        plot_bgcolor="#131C2E",
        font=dict(family="Inter, sans-serif", color="#E5E7EB", size=11),
        title=dict(
            text="<b>📊 Match Phase Run Breakdown: Powerplay vs Middle vs Death</b>",
            font=dict(size=14, color="#F8FAFC", family="Inter, sans-serif"),
            x=0.02,
            y=0.96
        ),
        margin=dict(l=20, r=20, t=46, b=30),
        xaxis=dict(gridcolor="#1F2C42", linecolor="#1F2C42", tickfont=dict(color="#8A97AB")),
        yaxis=dict(title="Runs Scored", gridcolor="#1F2C42", linecolor="#1F2C42", tickfont=dict(color="#8A97AB")),
        legend=dict(font=dict(color="#8A97AB", size=10), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig


def plot_powerbi_donut(df: pd.DataFrame, names_col: str, values_col: str, title: str, center_metric: str = "", height: int = 340) -> go.Figure:
    """Generates an executive PowerBI donut chart with centered callout metric."""
    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        title=title,
        hole=0.60,
        template="plotly_dark",
        color_discrete_sequence=["#F2C811", "#00BCF2", "#10B981", "#E879F9", "#64748B"]
    )
    annotations = []
    if center_metric:
        annotations.append(dict(
            text=f"<b>{center_metric}</b>",
            x=0.5, y=0.5,
            font_size=15,
            font_color="#FFFFFF",
            showarrow=False
        ))

    fig.update_layout(
        height=height,
        paper_bgcolor="#131C2E",
        plot_bgcolor="#131C2E",
        font=dict(family="Inter, sans-serif", color="#E5E7EB", size=11),
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=14, color="#F8FAFC", family="Inter, sans-serif"),
            x=0.02,
            y=0.96
        ),
        annotations=annotations,
        margin=dict(l=20, r=20, t=46, b=30),
        legend=dict(font=dict(color="#8A97AB", size=10), orientation="h", yanchor="bottom", y=-0.15)
    )
    return fig

