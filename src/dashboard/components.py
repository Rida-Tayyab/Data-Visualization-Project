"""Reusable UI components for the dashboard."""

import streamlit as st

try:
    from .config import EON_BOND_ACTORS
except ImportError:
    from config import EON_BOND_ACTORS


def render_key_metrics(df_filtered):
    """Render the key metrics cards."""
    st.markdown("### Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    total_films = len(df_filtered)
    avg_rating = df_filtered['averageRating'].mean() if total_films > 0 else 0
    avg_runtime = df_filtered['runtimeMinutes'].mean() if total_films > 0 else 0
    best_film = df_filtered.loc[df_filtered['averageRating'].idxmax()] if total_films > 0 else {
        'primaryTitle': 'N/A', 
        'averageRating': 0
    }

    with col1:
        st.metric("Total Films", total_films, help="Films analyzed")
    
    with col2:
        st.metric("Average Rating", f"{avg_rating:.1f}/10", help="IMDb score")
    
    with col3:
        st.metric("Avg Runtime", f"{avg_runtime:.0f} min", help="Film length")
    
    with col4:
        best_title = best_film['primaryTitle'][:15] + "..." if len(best_film['primaryTitle']) > 15 else best_film['primaryTitle']
        st.metric("Highest Rated", best_title, f"{best_film['averageRating']:.1f}/10")

    st.markdown("---")


def render_sidebar_filters(df_full):
    """Render sidebar filters and return filtered data."""
    st.sidebar.header("Mission Parameters: Data Focus")

    # 1. Data Focus Selection
    data_focus = st.sidebar.radio(
        "1. Select Data Focus:",
        ('James Bond Core Films (EON Actors & 007 Titles)', 'General Actor Search (Full Dataset)'),
        index=0
    )

    # Apply Focus Filter
    if data_focus == 'James Bond Core Films (EON Actors & 007 Titles)':
        df_current = df_full[df_full['is_bond_core']].copy()
        actor_list_options = sorted(list(set(EON_BOND_ACTORS).intersection(df_current['leadActor'].unique())))
        default_actors = EON_BOND_ACTORS
    else:
        df_current = df_full.copy()
        top_actors = df_current.groupby('leadActor').filter(
            lambda x: len(x) >= 5 and x['numVotes'].sum() >= 1000
        )
        actor_list_options = sorted(top_actors['leadActor'].unique().tolist())
        default_actors = EON_BOND_ACTORS

    st.sidebar.markdown("---")
    st.sidebar.header("2. Actor Dossier (Vertical Checkbox Filter)")

    # 2. Vertical Checkbox Filter
    selected_actors_dict = {}
    for actor in actor_list_options:
        is_selected = st.sidebar.checkbox(actor, value=(actor in default_actors))
        selected_actors_dict[actor] = is_selected

    selected_actors = [actor for actor, selected in selected_actors_dict.items() if selected]

    st.sidebar.markdown("---")
    st.sidebar.header("3. Temporal Filter")

    # 3. Year Range Slider
    year_min = int(df_current['releaseYear'].min()) if not df_current.empty else 1960
    year_max = int(df_current['releaseYear'].max()) if not df_current.empty else 2025

    if year_min < year_max:
        selected_years = st.sidebar.slider(
            'Release Year Range:',
            min_value=year_min,
            max_value=year_max,
            value=(year_min, year_max)
        )
    else:
        st.sidebar.text(f"Single Year Data: {year_min}")
        selected_years = (year_min, year_max)

    # Apply ALL Filters
    if selected_actors and not df_current.empty:
        df_filtered = df_current[
            (df_current['leadActor'].isin(selected_actors)) &
            (df_current['releaseYear'] >= selected_years[0]) &
            (df_current['releaseYear'] <= selected_years[1])
        ].copy()
    else:
        df_filtered = None

    return df_filtered, selected_actors
