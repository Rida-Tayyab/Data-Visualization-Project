"""Actor Universe page - individual actor analysis."""

import streamlit as st
import altair as alt
import pandas as pd

try:
    from ..config import ACCENT_GOLD, ACCENT_ORANGE, ACCENT_BLUE
except ImportError:
    from config import ACCENT_GOLD, ACCENT_ORANGE, ACCENT_BLUE


def render_actor_universe(df_full, EON_BOND_ACTORS):
    """Render the Actor Universe page."""
    st.markdown("# Across the 007 Verse")
    st.markdown("**Comparative Actor Analysis**")
    st.markdown("---")
    
    st.markdown("""
    Fans often debate over who's the best **James Bond** — Daniel Craig, George Lazenby, 
    Pierce Brosnan, Roger Moore, Sean Connery, or Timothy Dalton.  
    Within this data story, you have the opportunity to compare their works over the years.
    """)

    # Actor Selection
    selected_actor = st.selectbox("Select a Bond actor:", EON_BOND_ACTORS, index=5)

    df_actor = df_full[df_full['leadActor'] == selected_actor].copy()

    if df_actor.empty:
        st.warning(f"No films found for {selected_actor}.")
        return

    st.markdown("---")

    # Chart 1: Genre Donut Chart
    st.markdown(f"#### Genre Distribution: {selected_actor}")
    st.caption("Genre breakdown for selected actor's filmography")
    
    genre_cols = ['Action', 'Adventure', 'Thriller', 'Romance', 'Comedy', 'Drama', 'Sci-Fi']
    df_genre = df_actor[genre_cols].sum().reset_index()
    df_genre.columns = ['Genre', 'Count']
    df_genre = df_genre[df_genre['Count'] > 0]

    donut_chart = alt.Chart(df_genre).mark_arc(innerRadius=80, outerRadius=140).encode(
        theta=alt.Theta('Count:Q'),
        color=alt.Color('Genre:N', title='Genre'),
        tooltip=['Genre', 'Count']
    )
    
    center_text = alt.Chart(pd.DataFrame({'text': [selected_actor]})).mark_text(
        size=22, fontWeight='bold', color=ACCENT_GOLD, align='center', baseline='middle'
    ).encode(text='text:N')
    
    final_chart = alt.layer(donut_chart, center_text).properties(
        height=400, width=400, title=f"{selected_actor}'s Genre Distribution"
    ).configure_view(strokeWidth=0)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.altair_chart(final_chart, use_container_width=False)

    # Chart 2: Rating Evolution
    st.markdown(f"#### Rating Evolution: {selected_actor}")
    
    bond_count = df_actor[df_actor['is_bond_core']].shape[0]
    other_count = df_actor[~df_actor['is_bond_core']].shape[0]
    
    st.caption(f"Showing {bond_count} Bond films and {other_count} other films where {selected_actor} is the lead actor")
    
    avg_actor_rating = df_actor['averageRating'].mean()
    
    df_actor_viz = df_actor.copy()
    df_actor_viz['film_type'] = df_actor_viz['is_bond_core'].apply(
        lambda x: 'James Bond Films' if x else 'Other Films'
    )
    
    scatter_chart = alt.Chart(df_actor_viz).mark_circle(size=120, opacity=0.8).encode(
        x=alt.X('releaseYear:O', title="Release Year"),
        y=alt.Y('averageRating:Q', title="IMDb Rating", scale=alt.Scale(domain=[3, 10])),
        color=alt.Color('film_type:N',
            scale=alt.Scale(domain=['James Bond Films', 'Other Films'], range=['#E45756', '#4A90E2']),
            legend=alt.Legend(title="Film Type")
        ),
        tooltip=['primaryTitle', 'releaseYear', alt.Tooltip('averageRating', format=".2f"), 'film_type']
    ).properties(height=350)
    
    avg_line = alt.Chart(pd.DataFrame({'avg': [avg_actor_rating]})).mark_rule(
        color=ACCENT_GOLD, strokeDash=[5, 5], size=2
    ).encode(y='avg:Q')
    
    avg_text = alt.Chart(pd.DataFrame({
        'x': [df_actor['releaseYear'].max()],
        'y': [avg_actor_rating],
        'text': [f'Avg: {avg_actor_rating:.2f}']
    })).mark_text(
        align='right', baseline='bottom', dx=-5, dy=-5,
        color=ACCENT_GOLD, fontSize=12, fontWeight='bold'
    ).encode(x='x:O', y='y:Q', text='text:N')
    
    st.altair_chart(scatter_chart + avg_line + avg_text, use_container_width=True)

    # Chart 3: Film Rankings
    st.markdown(f"#### Film Rankings: {selected_actor}")
    st.caption("Films ranked by IMDb rating")

    df_sorted = df_actor.sort_values(by='averageRating', ascending=False).copy()
    df_sorted['Film (Year)'] = df_sorted['primaryTitle'] + " (" + df_sorted['releaseYear'].astype(str) + ")"

    rating_chart = alt.Chart(df_sorted).mark_bar().encode(
        y=alt.Y('Film (Year):N', sort='-x', title=None, axis=alt.Axis(labelLimit=300)),
        x=alt.X('averageRating:Q', title="IMDb Rating"),
        color=alt.Color('averageRating:Q',
            scale=alt.Scale(domain=[5, 10], range=[ACCENT_ORANGE, ACCENT_BLUE]), legend=None
        ),
        tooltip=['primaryTitle', 'releaseYear', alt.Tooltip('averageRating', format=".2f")]
    ).properties(height=400)

    st.altair_chart(rating_chart, use_container_width=True)
