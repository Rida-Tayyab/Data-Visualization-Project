"""Story Mode page - narrative-driven analysis with professional design."""

import streamlit as st
import altair as alt
import pandas as pd

try:
    from ..config import ACCENT_BLUE, ACCENT_RED, ACCENT_GOLD
    from ..components import initialize_page_styles, render_page_header, render_section_header
except ImportError:
    from config import ACCENT_BLUE, ACCENT_RED, ACCENT_GOLD
    from components import initialize_page_styles, render_page_header, render_section_header


def render_story_mode(df_full):
    """Render the Story Mode page with professional design consistency."""
    
    initialize_page_styles()
    
    render_page_header(
        "The Evolution of Espionage",
        "A data-driven narrative through the James Bond franchise"
    )

    df_story = df_full[df_full['is_bond_core']].copy()

    # ========================================================================
    # CHAPTER 1: THE GOLDEN AGE OF CONNERY
    # ========================================================================
    render_section_header(
        "Chapter 1: The Original Blueprint (1960s)",
        "Where it all began: Connery and Lazenby set the standard"
    )
    
    st.markdown("""
    The Connery era set the gold standard. His films established the core DNA of the franchise: 
    high-stakes **Adventure** mixed with **Thriller** elements. Notice how the average runtime was 
    relatively shorter and the ratings were consistently high, defining the early, successful formula.
    """)
    
    df_connery = df_story[df_story['leadActor'].isin(['Sean Connery', 'George Lazenby'])]
    
    story_chart_1 = alt.Chart(df_connery).mark_circle(size=150, opacity=0.8).encode(
        x=alt.X('releaseYear:O', title="Release Year"),
        y=alt.Y('averageRating:Q', title="IMDb Rating", scale=alt.Scale(domain=[5, 10])),
        size=alt.Size('runtimeMinutes:Q', title="Runtime (Mins)", scale=alt.Scale(range=[50, 400])),
        color=alt.Color('leadActor:N', title="Actor", scale=alt.Scale(range=[ACCENT_BLUE, ACCENT_RED])),
        tooltip=['primaryTitle', 'releaseYear', alt.Tooltip('averageRating', format=".2f"), 
                'runtimeMinutes', 'leadActor']
    ).properties(
        height=350,
        title="Connery & Lazenby: Defining the Rating and Runtime Benchmark"
    ).interactive()
    
    st.altair_chart(story_chart_1, use_container_width=True)
    
    st.markdown("""
    **Key Observations:**
    - Early Bond films maintained high ratings (7.0+)
    - Runtime remained consistent around 100-120 minutes
    - Formula proved successful from the start
    """)
    
    st.markdown("---")

    # ========================================================================
    # CHAPTER 2: THE ACTION-COMEDY SHIFT
    # ========================================================================
    render_section_header(
        "Chapter 2: The Camp and the Polish (1970s - 2000s)",
        "Experiment, innovation, and the search for reinvention"
    )
    
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
        x=alt.X('decade:O', title="Decade", axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Count:Q', title="Total Genre Tags per Decade"),
        color=alt.Color('Genre:N', 
            scale=alt.Scale(range=[ACCENT_RED, ACCENT_GOLD, '#AAAAAA', '#ADD8E6', '#7CFC00', '#FFA07A']), 
            title="Genre Focus"
        ),
        order=alt.Order('decade:O'),
        tooltip=['decade', 'Genre', 'Count']
    ).properties(
        height=350,
        title="Genre Emphasis: From Adventure to Action/Thriller"
    ).interactive()
    
    st.altair_chart(story_chart_2, use_container_width=True)
    
    st.markdown("""
    **Key Observations:**
    - Action and Thriller tags increased significantly in the 1990s-2000s
    - Comedy elements were more prominent in Moore era (1980s)
    - Adventure (the original DNA) remained consistent
    - Clear shift toward modern, grittier storytelling by 2000s
    """)
    
    st.markdown("---")

    # ========================================================================
    # CHAPTER 3: THE CRAIG REBOOT
    # ========================================================================
    render_section_header(
        "Chapter 3: The Gritty Modern Agent (Daniel Craig)",
        "The reboot that changed everything (2006-2021)"
    )
    
    st.markdown("""
    The **Daniel Craig** era (2006-2021) completely rebooted the narrative, focusing on raw **Thriller** 
    and **Drama** with high budgets and often longer runtimes. The audience response has been highly 
    favorable (high ratings and vote counts). The shift is clearly visible in the data: the latest films 
    maintain high quality but push the boundaries of film length and production scale.
    """)

    df_craig = df_story[df_story['leadActor'] == 'Daniel Craig'].sort_values('numVotes', ascending=True).copy()

    if not df_craig.empty:
        story_chart_3 = alt.Chart(df_craig).mark_bar().encode(
            y=alt.Y('primaryTitle:N', title="Film Title", sort='-x', axis=alt.Axis(labelLimit=200)),
            x=alt.X('numVotes:Q', title="Total Audience Votes"),
            color=alt.Color('averageRating:Q', 
                           scale=alt.Scale(scheme='reds', domain=[5, 10]),
                           title="IMDb Rating"),
            tooltip=['primaryTitle', alt.Tooltip('numVotes', format=","), 
                    alt.Tooltip('averageRating', format=".2f")]
        ).properties(
            height=400,
            title="Daniel Craig Era: Audience Volume and Popularity"
        )
        
        st.altair_chart(story_chart_3, use_container_width=True)
    else:
        st.info("No Daniel Craig films found in the data.")
    
    st.markdown("""
    **Key Observations:**
    - Craig films achieved record audience engagement (highest vote counts)
    - Ratings remained consistently high (7.0+) despite increased controversy
    - *Skyfall* emerged as the most popular Bond film
    - Production budgets increased, reflected in higher viewer counts
    """)
    
    st.markdown("---")

    # ========================================================================
    # CONCLUSION
    # ========================================================================
    render_section_header(
        "The Future of Bond",
        "What the data tells us about the franchise"
    )
    
    st.markdown("""
    From Connery's elegant simplicity to Craig's explosive intensity, the Bond franchise has continuously 
    evolved while maintaining its core appeal. The data shows:
    
    1. **Quality over Quantity**: Fewer films, but consistently higher ratings in recent years
    2. **Audience Growth**: Modern films attract significantly more viewer engagement
    3. **Genre Evolution**: From pure adventure to complex thriller-drama hybrids
    4. **Actor Cyclicity**: Each new actor brings fresh interpretation, maintaining franchise vitality
    
    The next Bond actor will inherit a franchise that has proven its ability to adapt while maintaining 
    its essential identity—a crucial balance for longevity.
    """)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 40px; padding: 20px; border-top: 1px solid #333;">
        <small>
        <strong>Story Mode</strong> | Data-Driven Narrative | 007 Data Dossier<br>
        <em>Data Source: IMDb | Analysis: November 2025</em>
        </small>
    </div>
    """, unsafe_allow_html=True)