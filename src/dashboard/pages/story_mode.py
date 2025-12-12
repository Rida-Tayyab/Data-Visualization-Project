"""Story Mode page - narrative-driven analysis with professional design."""

import streamlit as st
import altair as alt
import pandas as pd

try:
    from ..config import ACCENT_BLUE, ACCENT_RED, ACCENT_GOLD, ACCENT_ORANGE, ACCENT_GREEN
    from ..components import initialize_page_styles, render_page_header, render_section_header
    from ..charts import filter_to_specific_bond_films, create_bond_films_rating_chart, create_actor_performance_chart
except ImportError:
    from config import ACCENT_BLUE, ACCENT_RED, ACCENT_GOLD, ACCENT_ORANGE, ACCENT_GREEN
    from components import initialize_page_styles, render_page_header, render_section_header
    from charts import filter_to_specific_bond_films, create_bond_films_rating_chart, create_actor_performance_chart


def render_story_mode(df_full):
    """Render the Story Mode page with professional design consistency."""
    
    initialize_page_styles()
    
    render_page_header(
        "The Bond Legacy: A Journey Through 40 Years",
        "A data-driven narrative of the modern James Bond era (1981-2021)"
    )

    # Filter to only the 14 specific Bond films
    df_story = filter_to_specific_bond_films(df_full)
    
    if df_story.empty:
        st.error("No Bond films found in the dataset.")
        return
    
    # Sort by release year for chronological narrative
    df_story = df_story.sort_values('releaseYear').reset_index(drop=True)

    # ========================================================================
    # CHAPTER 1: THE COMPLETE JOURNEY
    # ========================================================================
    render_section_header(
        "Chapter 1: The Complete Journey (1981-2021)",
        "Four decades of James Bond: From Roger Moore to Daniel Craig"
    )
    
    st.markdown("""
    Over 40 years, the James Bond franchise has evolved through four distinct eras, each defined by a different actor's 
    interpretation of 007. This journey spans **14 films** from Roger Moore's final outings to Daniel Craig's modern 
    reboot. Let's explore how ratings, popularity, and storytelling have evolved across these four decades.
    """)
    
    # Use the bond films rating chart
    bond_rating_chart = create_bond_films_rating_chart(df_full)
    if bond_rating_chart:
        st.altair_chart(bond_rating_chart, use_container_width=True)
    
    st.markdown("""
    **Key Observations:**
    - The franchise has maintained consistently strong ratings (6.5-8.0 range) across all eras
    - Each actor brought a unique style: Moore's charm, Dalton's intensity, Brosnan's polish, and Craig's grit
    - The average rating line shows the franchise's remarkable consistency in quality
    - Notable peaks include *GoldenEye* (1995) and *Skyfall* (2012), both marking successful actor transitions
    """)
    
    st.markdown("---")

    # ========================================================================
    # CHAPTER 2: THE ACTOR TRANSITIONS
    # ========================================================================
    render_section_header(
        "Chapter 2: The Actor Transitions",
        "How each new Bond shaped the franchise"
    )
    
    st.markdown("""
    Each actor transition marked a new chapter in Bond's evolution. From Roger Moore's suave sophistication to 
    Timothy Dalton's darker interpretation, Pierce Brosnan's modern polish, and finally Daniel Craig's gritty 
    reboot—each brought something unique to the role.
    """)
    
    # Use the existing actor performance chart
    actor_chart = create_actor_performance_chart(df_story)
    if actor_chart:
        st.altair_chart(actor_chart, use_container_width=True)
    else:
        st.warning("No actor statistics available.")
    
    st.markdown("""
    **Key Observations:**
    - **Daniel Craig** leads with the highest average rating (7.4/10), reflecting the success of the modern reboot
    - **Pierce Brosnan** maintained strong ratings (7.0/10) across his four films, bringing Bond into the modern era
    - **Timothy Dalton** had the shortest tenure but delivered intense, critically-acclaimed performances
    - **Roger Moore** closed his era with consistent quality, maintaining the franchise's appeal
    """)
    
    st.markdown("---")

    # ========================================================================
    # CHAPTER 3: THE MODERN REBOOT (CRAIG ERA)
    # ========================================================================
    render_section_header(
        "Chapter 3: The Modern Reboot (2006-2021)",
        "Daniel Craig: Redefining Bond for a new generation"
    )
    
    df_craig = df_story[df_story['leadActor'] == 'Daniel Craig'].sort_values('releaseYear').copy()
    
    st.markdown("""
    The **Daniel Craig** era represents the most significant transformation in Bond's history. Starting with 
    *Casino Royale* (2006), the franchise was completely rebooted with a darker, more realistic tone. This 
    era saw unprecedented audience engagement and critical acclaim, culminating in *Skyfall* (2012), which 
    became the highest-grossing Bond film of all time.
    """)
    
    if not df_craig.empty:
        # Craig films popularity and ratings
        craig_chart = alt.Chart(df_craig).mark_circle(size=200, stroke='white', strokeWidth=2).encode(
            x=alt.X('releaseYear:O', title="Release Year"),
            y=alt.Y('averageRating:Q', title="IMDb Rating", scale=alt.Scale(domain=[6, 8.5])),
            size=alt.Size('numVotes:Q', 
                         scale=alt.Scale(range=[100, 600]),
                         title="Popularity (Votes)",
                         legend=alt.Legend(title="Popularity (Votes)", format=",")),
            color=alt.Color('averageRating:Q',
                          scale=alt.Scale(scheme='reds', domain=[6.5, 8.0]),
                          legend=alt.Legend(title="Rating")),
            tooltip=[
                alt.Tooltip('primaryTitle:N', title="Film"),
                alt.Tooltip('releaseYear:O', title="Year"),
                alt.Tooltip('averageRating:Q', title="Rating", format=".2f"),
                alt.Tooltip('numVotes:Q', title="Votes", format=","),
                alt.Tooltip('runtimeMinutes:Q', title="Runtime (mins)")
            ]
        ).properties(
            height=400,
            title="Daniel Craig Era: Evolution of Ratings and Popularity"
        )
        
        st.altair_chart(craig_chart, use_container_width=True)
    
    st.markdown("""
    **Key Observations:**
    - *Skyfall* (2012) achieved the highest rating (8.0/10) and massive popularity, marking the franchise's 50th anniversary
    - *Casino Royale* (2006) successfully rebooted the series with a fresh, gritty take
    - The Craig era shows increasing audience engagement over time, with *No Time to Die* (2021) reaching new heights
    - Longer runtimes in recent films reflect more complex storytelling and character development
    """)
    
    st.markdown("---")

    # ========================================================================
    # CHAPTER 4: THE EVOLUTION OF POPULARITY
    # ========================================================================
    render_section_header(
        "Chapter 4: The Evolution of Popularity",
        "How audience engagement has grown over four decades"
    )
    
    st.markdown("""
    The franchise's popularity has evolved dramatically over the years. While early films had strong critical 
    reception, modern films have achieved unprecedented audience engagement, reflecting both increased global 
    reach and the franchise's continued relevance.
    """)
    
    # Popularity over time
    popularity_chart = alt.Chart(df_story).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X('releaseYear:O', title="Release Year"),
        y=alt.Y('numVotes:Q', title="Number of Votes (Popularity)", 
               scale=alt.Scale(type='log'),
               axis=alt.Axis(format=".0s")),
        color=alt.Color('leadActor:N', title="Bond Actor"),
        tooltip=[
            alt.Tooltip('primaryTitle:N', title="Film"),
            alt.Tooltip('releaseYear:O', title="Year"),
            alt.Tooltip('numVotes:Q', title="Votes", format=","),
            alt.Tooltip('leadActor:N', title="Actor")
        ]
    ).properties(
        height=400,
        title="Audience Engagement Over Time (Log Scale)"
    )
    
    st.altair_chart(popularity_chart, use_container_width=True)
    
    st.markdown("""
    **Key Observations:**
    - Audience engagement has grown exponentially, especially in the Craig era
    - *Skyfall* and *No Time to Die* show the highest engagement, reflecting modern global reach
    - The Brosnan era marked a significant increase in popularity, bringing Bond to a new generation
    - Even older films maintain strong engagement, showing the franchise's enduring appeal
    """)
    
    st.markdown("---")

    # ========================================================================
    # CONCLUSION
    # ========================================================================
    render_section_header(
        "The Legacy Continues",
        "What 40 years of data tells us about Bond's future"
    )
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Films", len(df_story))
    
    with col2:
        avg_rating = df_story['averageRating'].mean()
        st.metric("Average Rating", f"{avg_rating:.2f}/10")
    
    with col3:
        total_votes = df_story['numVotes'].sum()
        st.metric("Total Votes", f"{total_votes:,.0f}")
    
    with col4:
        avg_runtime = df_story['runtimeMinutes'].mean()
        st.metric("Avg Runtime", f"{avg_runtime:.0f} min")
    
    st.markdown("""
    Over 40 years and 14 films, the James Bond franchise has demonstrated remarkable resilience and evolution:
    
    1. **Consistent Quality**: Despite changing actors and styles, the franchise has maintained an average rating 
       of **{:.2f}/10**, showing consistent quality across decades.
    
    2. **Growing Popularity**: Modern films achieve unprecedented audience engagement, with the Craig era 
       reaching millions more viewers than earlier films.
    
    3. **Successful Transitions**: Each actor transition has been successful, with new Bonds bringing fresh 
       perspectives while maintaining the core appeal.
    
    4. **Evolutionary Adaptation**: The franchise has evolved from Moore's charm to Craig's grit, proving its 
       ability to adapt to changing audience expectations while maintaining its essential identity.
    
    The next Bond actor will inherit a franchise that has proven its ability to evolve while staying true to 
    its core—a formula that has worked for over 60 years and will continue into the future.
    """.format(avg_rating))
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 40px; padding: 20px; border-top: 1px solid #333;">
        <small>
        <strong>Story Mode</strong> | Data-Driven Narrative | 007 Data Dossier<br>
        <em>Data Source: IMDb | Analysis: November 2025 | Films Analyzed: 14 Bond Films (1981-2021)</em>
        </small>
    </div>
    """, unsafe_allow_html=True)