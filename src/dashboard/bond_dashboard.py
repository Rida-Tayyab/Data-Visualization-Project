"""
The 007 Data Dossier: James Bond Analysis Dashboard
A comprehensive analysis of the James Bond franchise and lead actor performance.
"""

import streamlit as st
from config import register_theme, EON_BOND_ACTORS
from data_loader import load_and_preprocess_data, get_data_path
from components import render_sidebar_filters
from pages.overview import render_dashboard
from pages.story_mode import render_story_mode
from pages.actor_universe import render_actor_universe
from pages.individual_charts import render_individual_chart


# Page Configuration
st.set_page_config(
    page_title="The 007 Data Dossier: James Bond Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Register theme
register_theme()

# Load data
data_file = get_data_path()
df_full = load_and_preprocess_data(data_file)

# Navigation
st.sidebar.markdown("## 007 Navigation")
page_mode = st.sidebar.radio(
    "",
    ('Bond Overview', 'Individual Charts', 'Story Mode', 'Actor Universe')
)

# Chart selector for Individual Charts page
chart_selection = None
if page_mode == 'Individual Charts':
    st.sidebar.markdown("---")
    st.sidebar.subheader("Select Chart")
    chart_selection = st.sidebar.selectbox(
        "Choose a chart to view:",
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
        ]
    )

st.sidebar.markdown("---")

# Render the selected page
if page_mode == 'Bond Overview':
    df_filtered, _ = render_sidebar_filters(df_full)
    render_dashboard(df_full, df_filtered)

elif page_mode == 'Individual Charts':
    render_individual_chart(df_full, chart_selection)

elif page_mode == 'Story Mode':
    render_story_mode(df_full)

else:  # Actor Universe
    render_actor_universe(df_full, EON_BOND_ACTORS)
