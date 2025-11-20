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
    page_title="The 007 Data Dossier: James Bond Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# Register theme
register_theme()

# Initialize design system styles
initialize_page_styles()

# Hide page navigation and remove ALL top spacing
st.markdown("""
    <style>
        /* Hide the page navigation */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        /* AGGRESSIVE: Remove ALL top padding and margins everywhere */
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            margin-top: 0rem !important;
        }
        
        .main .block-container {
            padding-top: 0rem !important;
            margin-top: 0rem !important;
        }
        
        .main {
            padding-top: 0rem !important;
            margin-top: 0rem !important;
        }
        
        .stApp {
            margin-top: 0rem !important;
            padding-top: 0rem !important;
        }
        
        /* Remove sidebar top padding */
        section[data-testid="stSidebar"] {
            padding-top: 0rem !important;
            margin-top: 0rem !important;
        }
        
        section[data-testid="stSidebar"] > div {
            padding-top: 0.5rem !important;
        }
        
        section[data-testid="stSidebar"] .block-container {
            padding-top: 0rem !important;
        }
        
        /* Hide Streamlit branding and header */
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}
        
        .stApp > header {
            display: none !important;
            height: 0rem !important;
        }
        
        /* Force remove any inherited padding */
        div[data-testid="stVerticalBlock"] > div:first-child {
            padding-top: 0rem !important;
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
st.sidebar.markdown("### 007 Navigation")

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
    st.sidebar.markdown("### Select Chart")
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