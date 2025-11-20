"""
The 007 Data Dossier: James Bond Analysis Dashboard
A comprehensive analysis of the James Bond franchise and lead actor performance.
"""

import streamlit as st
from config import register_theme, EON_BOND_ACTORS, ACCENT_GOLD
from data_loader import load_and_preprocess_data, get_data_path
from components import initialize_page_styles, render_sidebar_filters
from pages.overview import render_dashboard
from pages.story_mode import render_story_mode
from pages.actor_universe import render_actor_universe
from pages.individual_charts import render_individual_chart


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Bond Overview",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# Register theme
register_theme()

# Initialize design system styles
initialize_page_styles()

# Add this CSS to remove top padding
st.markdown("""
    <style>
        .appData {
            margin-top: -80px;
        }
        [data-testid="stVerticalBlock"] {
            padding-top: 0rem;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD DATA
# ============================================================================
data_file = get_data_path()
df_full = load_and_preprocess_data(data_file)


# ============================================================================
# NAVIGATION SIDEBAR
# ============================================================================
st.sidebar.markdown("###  007 Navigation")

page_mode = st.sidebar.radio(
    "Choose your mission:",
    ('Bond Overview', 'Individual Charts', 'Story Mode', 'Actor Universe'),
    index=0
)

# ============================================================================
# CHART SELECTOR (Only shown for Individual Charts page)
# ============================================================================
chart_selection = None
if page_mode == 'Individual Charts':
    st.sidebar.markdown("---")
    st.sidebar.markdown("###  Select Chart")
    chart_selection = st.sidebar.selectbox(
        "Choose a visualization:",
        [
            "Actor Performance Ranking",
            "Rating Trend Over Time",
            "Bond vs Other Thriller Films",
            "Runtime vs Rating Analysis",
            "Genre Evolution by Decade",
            "Genre Popularity Trend",
            "Rating Distribution by Actor",
            "Production Volume by Decade",
            "Performance Heatmap",
            "Audience Engagement Distribution",
            "Complete Film Timeline"
        ],
        label_visibility="collapsed"
    )

st.sidebar.markdown("---")

# Add info section at bottom of sidebar
st.sidebar.markdown("""
---
###  About This Dashboard
**The 007 Data Dossier** provides comprehensive analysis of:
-  James Bond films by lead actor
-  Critical reception trends over decades
-  Genre evolution and audience engagement
-  Comparative actor universe analysis
""")


# ============================================================================
# PAGE ROUTING
# ============================================================================
if page_mode == 'Bond Overview':
    df_filtered, _ = render_sidebar_filters(df_full)
    render_dashboard(df_full, df_filtered)

elif page_mode == 'Individual Charts':
    render_individual_chart(df_full, chart_selection)

elif page_mode == 'Story Mode':
    render_story_mode(df_full)

else:  # Actor Universe
    render_actor_universe(df_full, EON_BOND_ACTORS)