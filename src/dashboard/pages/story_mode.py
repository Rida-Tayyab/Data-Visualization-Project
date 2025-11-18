"""Story Mode page - narrative-driven analysis."""

import streamlit as st
import altair as alt

try:
    from ..config import ACCENT_BLUE, ACCENT_RED, ACCENT_GOLD
except ImportError:
    from config import ACCENT_BLUE, ACCENT_RED, ACCENT_GOLD


def render_story_mode(df_full):
    """Render the Story Mode page."""
    st.markdown("# The Evolution of Espionage")
    st.markdown("**A data-driven narrative through the James Bond franchise**")
    st.markdown("---")

    df_story = df_full[df_full['is_bond_core']].copy()

    # Chapter 1: The Golden Age of Connery
    st.header("Chapter 1: The Original Blueprint (1960s)")
    st.markdown("""
    The Connery era set the gold standard. His films established the core DNA of the franchise: 
    high-stakes **Adventure** mixed with **Thriller** elements. Notice how the average runtime was 
    relatively shorter and the ratings were consistently high, defining the early, successful formula.
    """)
    
    df_connery = df_story[df_story['leadActor'].isin(['Sean Connery', 'George Lazenby'])]
    
    story_chart_1 = alt.Chart(df_connery).mark_circle(size=150, color=ACCENT_BLUE, opacity=0.8).encode(
        x=alt.X('releaseYear:O', title="Release Year"),
        y=alt.Y('averageRating:Q', title="IMDb Rating"),
        size=alt.Size('runtimeMinutes:Q', title="Runtime (Mins)"),
        color=alt.Color('leadActor:N', title="Actor"),
        tooltip=['primaryTitle', 'releaseYear', alt.Tooltip('averageRating', format=".2f"), 
                'runtimeMinutes', 'leadActor']
    ).properties(title="Connery & Lazenby: Defining the Rating and Runtime Benchmark")
    
    st.altair_chart(story_chart_1, use_container_width=True)
    st.markdown("---")

    # Chapter 2: The Action-Comedy Shift
    st.header("Chapter 2: The Camp and the Polish (1970s - 2000s)")
    st.markdown("""
    The **Roger Moore** era (1973-1985) introduced campier, more Sci-Fi elements (see *Moonraker*), 
    leading to increased variability in critical ratings. **Pierce Brosnan** (1995-2002) then brought 
    a polished, gadget-heavy approach. This period saw a dramatic rise in the **Action** and **Thriller** 
    count, preparing the franchise for the grittier modern era.
    """)
    
    df_genre_shift = df_story[(df_story['decade'] >= 1970) & (df_story['decade'] <= 2000)].copy()
    genre_cols = ['Action', 'Adventure', 'Thriller', 'Romance', 'Comedy', 'Sci-Fi']
    df_genres = df_genre_shift.groupby('decade')[genre_cols].sum().reset_index()
    df_genres_melted = df_genres.melt('decade', value_vars=genre_cols, var_name='Genre', value_name='Count')

    story_chart_2 = alt.Chart(df_genres_melted).mark_bar(opacity=0.9).encode(
        x=alt.X('decade:O', title="Decade"),
        y=alt.Y('Count:Q', title="Total Genre Tags per Decade"),
        color=alt.Color('Genre:N', 
            scale=alt.Scale(range=[ACCENT_RED, ACCENT_GOLD, '#AAAAAA', '#ADD8E6', '#7CFC00', '#FFA07A']), 
            title="Genre Focus"
        ),
        order=alt.Order('decade:O'),
        tooltip=['decade', 'Genre', 'Count']
    ).properties(title="Genre Emphasis: From Adventure to Action/Thriller").interactive()
    
    st.altair_chart(story_chart_2, use_container_width=True)
    st.markdown("---")

    # Chapter 3: The Craig Reboot
    st.header("Chapter 3: The Gritty Modern Agent (Daniel Craig)")
    st.markdown("""
    The **Daniel Craig** era (2006-2021) completely rebooted the narrative, focusing on raw **Thriller** 
    and **Drama** with high budgets and often longer runtimes. The audience response has been highly 
    favorable (high ratings and vote counts). The shift is clearly visible in the data: the latest films 
    maintain high quality but push the boundaries of film length and production scale.
    """)

    df_craig = df_story[df_story['leadActor'] == 'Daniel Craig']

    story_chart_3 = alt.Chart(df_craig).mark_bar(color=ACCENT_RED).encode(
        x=alt.X('primaryTitle:N', sort='-y', title="Film Title", axis=alt.Axis(labelAngle=0)),
        y=alt.Y('numVotes:Q', title="Total Audience Votes"),
        tooltip=['primaryTitle', alt.Tooltip('numVotes', format=",")]
    ).properties(title="Daniel Craig Era: Audience Volume and Popularity")
    
    st.altair_chart(story_chart_3, use_container_width=True)
    
    st.markdown("---")
    st.markdown("Data Source: data_final_lead_actor.csv | View: 007 Story Mode")
