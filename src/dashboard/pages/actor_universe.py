"""Actor Universe page - individual actor analysis with professional design."""

import streamlit as st
import altair as alt
import pandas as pd

try:
    from ..config import ACCENT_GOLD, ACCENT_ORANGE, ACCENT_BLUE, ACCENT_RED
    from ..components import (
        initialize_page_styles, 
        render_page_header, 
        render_section_header,
        render_insight_row
    )
except ImportError:
    from config import ACCENT_GOLD, ACCENT_ORANGE, ACCENT_BLUE, ACCENT_RED
    from components import (
        initialize_page_styles, 
        render_page_header, 
        render_section_header,
        render_insight_row
    )


def render_actor_universe(df_full, EON_BOND_ACTORS):
    """Render the Actor Universe page with professional design system."""
    
    initialize_page_styles()
    
    render_page_header(
        "Across the 007 Verse",
        "Comparative Analysis of All Bond Actors"
    )
    
    st.markdown("""
    Fans often debate over who's the best **James Bond** — Daniel Craig, George Lazenby, 
    Pierce Brosnan, Roger Moore, Sean Connery, or Timothy Dalton.  
    Within this data story, you have the opportunity to compare their works, performance, and legacy.
    """)

    st.markdown("---")

    # ========================================================================
    # ACTOR SELECTION
    # ========================================================================
    render_section_header("Select Your Agent")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        selected_actor = st.selectbox(
            "Choose a Bond actor:",
            EON_BOND_ACTORS,
            index=5,
            label_visibility="collapsed"
        )

    df_actor = df_full[df_full['leadActor'] == selected_actor].copy()

    if df_actor.empty:
        st.warning(f"No films found for {selected_actor}.")
        return

    st.markdown("---")

    # ========================================================================
    # QUICK STATS
    # ========================================================================
    bond_count = df_actor[df_actor['is_bond_core']].shape[0]
    other_count = df_actor[~df_actor['is_bond_core']].shape[0]
    avg_rating = df_actor['averageRating'].mean()
    best_film = df_actor.loc[df_actor['averageRating'].idxmax()]
    worst_film = df_actor.loc[df_actor['averageRating'].idxmin()]

    render_insight_row([
        {
            'label': 'Bond Films',
            'value': str(bond_count),
            'context': f'as lead actor'
        },
        {
            'label': 'Other Films',
            'value': str(other_count),
            'context': f'with this actor'
        },
        {
            'label': 'Avg Rating',
            'value': f'{avg_rating:.2f}/10',
            'context': 'across all films'
        }
    ])

    st.markdown("---")

    # ========================================================================
    # CHART 1: GENRE DISTRIBUTION (DONUT)
    # ========================================================================
    render_section_header(f"Genre Mastery: {selected_actor}")
    
    genre_cols = ['Action', 'Adventure', 'Thriller', 'Romance', 'Comedy', 'Drama', 'Sci-Fi']
    df_genre = df_actor[genre_cols].sum().reset_index()
    df_genre.columns = ['Genre', 'Count']
    df_genre = df_genre[df_genre['Count'] > 0].sort_values('Count', ascending=False)

    donut_chart = alt.Chart(df_genre).mark_arc(innerRadius=80, outerRadius=140).encode(
        theta=alt.Theta('Count:Q'),
        color=alt.Color('Genre:N', 
                       scale=alt.Scale(
                           domain=['Action', 'Adventure', 'Thriller', 'Romance', 'Comedy', 'Drama', 'Sci-Fi'],
                           range=[ACCENT_RED, ACCENT_BLUE, ACCENT_ORANGE, ACCENT_GOLD, '#7CFC00', '#9B59B6', '#95A5A6']
                       ),
                       title='Genre'),
        tooltip=['Genre', 'Count']
    )
    
    center_text = alt.Chart(pd.DataFrame({'text': [selected_actor]})).mark_text(
        size=20, fontWeight='bold', color=ACCENT_GOLD, align='center', baseline='middle'
    ).encode(text='text:N')
    
    final_chart = alt.layer(donut_chart, center_text).properties(
        height=400, width=400, title=f"Genre Distribution in {selected_actor}'s Filmography"
    ).configure_view(strokeWidth=0)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.altair_chart(final_chart, use_container_width=False)

    st.markdown("---")

    # ========================================================================
    # CHART 2: RATING EVOLUTION
    # ========================================================================
    render_section_header(f"Career Arc: {selected_actor}'s Evolution")
    
    avg_actor_rating = df_actor['averageRating'].mean()
    
    df_actor_viz = df_actor.copy()
    df_actor_viz['film_type'] = df_actor_viz['is_bond_core'].apply(
        lambda x: 'James Bond Films' if x else 'Other Films'
    )
    
    scatter_chart = alt.Chart(df_actor_viz).mark_circle(size=120, opacity=0.8).encode(
        x=alt.X('releaseYear:O', title="Release Year", axis=alt.Axis(labelAngle=0)),
        y=alt.Y('averageRating:Q', title="IMDb Rating", scale=alt.Scale(domain=[3, 10])),
        color=alt.Color('film_type:N',
            scale=alt.Scale(domain=['James Bond Films', 'Other Films'], range=[ACCENT_RED, ACCENT_BLUE]),
            legend=alt.Legend(title="Film Type", orient="bottom-right")
        ),
        tooltip=['primaryTitle', 'releaseYear', alt.Tooltip('averageRating', format=".2f"), 'film_type']
    ).properties(height=350)
    
    avg_line = alt.Chart(pd.DataFrame({'avg': [avg_actor_rating]})).mark_rule(
        color=ACCENT_GOLD, strokeDash=[5, 5], size=2
    ).encode(y='avg:Q')
    
    avg_text = alt.Chart(pd.DataFrame({
        'x': [df_actor['releaseYear'].max()],
        'y': [avg_actor_rating],
        'text': [f'Career Avg: {avg_actor_rating:.2f}']
    })).mark_text(
        align='right', baseline='bottom', dx=-5, dy=-5,
        color=ACCENT_GOLD, fontSize=11, fontWeight='bold'
    ).encode(x='x:O', y='y:Q', text='text:N')
    
    st.altair_chart(scatter_chart + avg_line + avg_text, use_container_width=True)

    st.markdown("---")

    # ========================================================================
    # CHART 3: FILM RANKINGS
    # ========================================================================
    render_section_header("⭐", f"Filmography Rankings: {selected_actor}")
    
    df_sorted = df_actor.sort_values(by='averageRating', ascending=False).copy()
    df_sorted['Film (Year)'] = df_sorted['primaryTitle'] + " (" + df_sorted['releaseYear'].astype(str) + ")"
    
    # Show top 15 films
    df_top = df_sorted.head(15)

    rating_chart = alt.Chart(df_top).mark_bar().encode(
        y=alt.Y('Film (Year):N', sort='-x', title=None, axis=alt.Axis(labelLimit=300)),
        x=alt.X('averageRating:Q', title="IMDb Rating", scale=alt.Scale(domain=[0, 10])),
        color=alt.Color('averageRating:Q',
            scale=alt.Scale(domain=[5, 10], range=[ACCENT_ORANGE, ACCENT_BLUE]), 
            legend=None
        ),
        tooltip=['primaryTitle', 'releaseYear', alt.Tooltip('averageRating', format=".2f")]
    ).properties(height=400, title=f"Top 15 Films by Rating")

    st.altair_chart(rating_chart, use_container_width=True)

    # Best and Worst films
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **Best Rated Film**
        
        **{best_film['primaryTitle']}** ({int(best_film['releaseYear'])})
        
        Rating: **{best_film['averageRating']:.2f}/10**
        """)
    
    with col2:
        st.markdown(f"""
        **Lowest Rated Film**
        
        **{worst_film['primaryTitle']}** ({int(worst_film['releaseYear'])})
        
        Rating: **{worst_film['averageRating']:.2f}/10**
        """)

    st.markdown("---")

    # ========================================================================
    # FOOTER
    # ========================================================================
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 40px; padding: 20px; border-top: 1px solid #333;">
        <small>
        <strong>Actor Universe</strong> | Individual Actor Analysis | 007 Data Dossier<br>
        <em>Data Source: IMDb | Analysis: November 2025</em>
        </small>
    </div>
    """, unsafe_allow_html=True)