"""Bond Overview Page - Main Dashboard with Professional Design System."""

import streamlit as st
from charts import (
    create_actor_performance_chart,
    create_rating_distribution_chart,
    create_bond_comparison_chart,
    create_runtime_rating_chart,
    create_genre_evolution_chart,
    create_production_volume_chart,
    create_genre_trend_chart,
    create_rating_trend_chart,
    create_performance_heatmap,
    create_engagement_boxplot,
    create_film_timeline_chart
)
from components import (
    initialize_page_styles,
    render_page_header,
    render_section_header,
    render_key_metrics,
    render_insight_row,
    render_chart_with_description,
    render_two_column_charts
)

try:
    from ..config import ACCENT_GOLD, ACCENT_ORANGE, ACCENT_BLUE, ACCENT_RED
except ImportError:
    from config import ACCENT_GOLD, ACCENT_ORANGE, ACCENT_BLUE, ACCENT_RED


def render_dashboard(df_full, df_filtered):
    """
    Render the main Bond Overview dashboard with professional design system.
    All components aligned to consistent sizing, spacing, and styling.
    """
    
    # Initialize design system styles
    initialize_page_styles()
    
    if df_filtered is None or df_filtered.empty:
        st.warning("No data matches your filters. Please adjust your selection.")
        return
    
    # ========================================================================
    # SECTION 1: PAGE HEADER
    # ========================================================================
    render_page_header(
        "Bond Overview",
        "Comprehensive Analysis of James Bond Films & Actor Performance"
    )
    
    # ========================================================================
    # SECTION 2: EXECUTIVE METRICS
    # ========================================================================
    render_key_metrics(df_filtered)
    
    # ========================================================================
    # SECTION 3: ACTOR PERFORMANCE (2-COLUMN)
    # ========================================================================
    render_section_header(
        "Actor Performance Analysis",
        "Compare critical reception across all Bond actors"
    )
    
    render_two_column_charts(
        left_chart_config={
            'title': 'Actor Performance Ranking',
            'description': 'Ranks each Bond actor by their average IMDb rating across all films. '
                          'Higher ratings indicate stronger critical reception.',
            'key_insight': 'Which actor has the highest critical reception? Notice correlations between film count and ratings.',
            'chart': create_actor_performance_chart(df_filtered),
            'interaction_tip': 'Hover to see film counts'
        },
        right_chart_config={
            'title': 'Rating Distribution by Actor',
            'description': 'Visualizes the spread of ratings for each actor\'s films. '
                          'The red line shows the average rating.',
            'key_insight': 'Which actors have the most consistent ratings? Are there outliers?',
            'chart': create_rating_distribution_chart(df_filtered),
            'interaction_tip': 'Hover for film titles'
        }
    )
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 4: RATING TRENDS (FULL WIDTH)
    # ========================================================================
    render_section_header(
        "Rating Trends Over Time",
        "Track how IMDb ratings have evolved across decades"
    )
    
    render_chart_with_description(
        title='Rating Evolution Analysis',
        description='Track how IMDb ratings for Bond films have evolved across decades and individual actors. '
                   'Use the legend to toggle actors on/off, revealing trends across different eras.',
        key_insight='Is there a consistent trend in film quality over decades? How do actor eras compare?',
        chart_element=create_rating_trend_chart(df_filtered),
        interaction_tip='Click legend items to filter actors'
    )
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 5: BOND VS COMPETITION (FULL WIDTH)
    # ========================================================================
    # Compare Bond films with other thriller movies
    render_section_header(
        "James Bond vs. The Competition",
        "How do Bond films compare to other thriller movies?"
    )
    
    render_chart_with_description(
        title='Bond Films vs Other Thrillers',
        description='Compare James Bond films with other thriller films using popularity (votes) on X-axis '
                   'and IMDb rating on Y-axis. Red circles are Bond films, gray circles are other thrillers.',
        key_insight='Do Bond films consistently outperform other thrillers in both rating and popularity?',
        chart_element=create_bond_comparison_chart(df_full)[0],
        interaction_tip='Hover for detailed film information'
    )
    
    # Quick comparison insights
    bond_comp_chart, bond_df, other_df = create_bond_comparison_chart(df_full)
    if not bond_df.empty and not other_df.empty:
        bond_avg = bond_df['averageRating'].mean()
        other_avg = other_df['averageRating'].mean()
        bond_votes = bond_df['numVotes'].mean()
        other_votes = other_df['numVotes'].mean()
        
        render_insight_row([
            {
                'label': 'Bond Avg Rating',
                'value': f'{bond_avg:.2f}/10',
                'context': f'{len(bond_df)} films'
            },
            {
                'label': 'Thriller Avg Rating',
                'value': f'{other_avg:.2f}/10',
                'context': f'{len(other_df)} films'
            },
            {
                'label': 'Bond Premium',
                'value': f'↑ {abs(bond_avg - other_avg):.2f}',
                'context': 'points higher'
            }
        ])
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 6: FILM CHARACTERISTICS (2-COLUMN)
    # ========================================================================
    render_section_header(
        "Film Characteristics & Popularity",
        "Explore runtime, production volume, and audience engagement"
    )
    
    render_two_column_charts(
        left_chart_config={
            'title': 'Runtime vs Rating Analysis',
            'description': 'Explore the relationship between film length and critical reception. '
                          'Bubble size represents popularity (number of votes).',
            'key_insight': 'Is there an optimal runtime for Bond films? Do longer films get better ratings?',
            'chart': create_runtime_rating_chart(df_filtered),
            'interaction_tip': 'Hover for film details'
        },
        right_chart_config={
            'title': 'Production Volume by Decade',
            'description': 'Shows how many Bond films were produced in each decade. '
                          'Reveals the frequency and intensity of franchise activity.',
            'key_insight': 'In which decade were most Bond films released? Are there gaps in production?',
            'chart': create_production_volume_chart(df_filtered),
            'interaction_tip': 'Hover for exact counts'
        }
    )
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 7: GENRE ANALYSIS (2-COLUMN)
    # ========================================================================
    render_section_header(
        "Genre Evolution & Trends",
        "How have genres shifted across Bond film eras?"
    )
    
    render_two_column_charts(
        left_chart_config={
            'title': 'Genre Evolution by Decade',
            'description': 'Track which genres appear in Bond films across different decades. '
                          'Shows the count of films in each genre per decade.',
            'key_insight': 'Which genres are most common? How has genre diversity changed over time?',
            'chart': create_genre_evolution_chart(df_filtered),
            'interaction_tip': 'Hover for genre breakdown'
        },
        right_chart_config={
            'title': 'Genre Popularity Trend',
            'description': 'Stacked area chart showing genre distribution across decades. '
                          'Each colored area represents a genre over time.',
            'key_insight': 'Is Action still dominant? How have Romance and Sci-Fi evolved?',
            'chart': create_genre_trend_chart(df_filtered) or st.info("Not enough data"),
            'interaction_tip': 'Hover for detailed breakdown'
        }
    )
    
    st.markdown("---")
    
    # ========================================================================
    # SECTION 8: ADVANCED ANALYTICS (COLLAPSIBLE)
    # ========================================================================
    render_section_header(
        "Advanced Analytics",
        "Explore detailed performance heatmaps and engagement metrics"
    )
    
    # Performance Heatmap
    with st.expander("Performance Heatmap - Actor Performance by Decade", expanded=False):
        render_chart_with_description(
            title='Performance Heatmap',
            description='Heatmap showing average ratings for each actor in each decade they were active. '
                       'Darker blue indicates higher ratings.',
            key_insight='Which actor-decade combinations had the best critical reception? Any performance dips?',
            chart_element=create_performance_heatmap(df_filtered),
            interaction_tip='Hover for exact ratings and film counts'
        )
    
    # Audience Engagement
    with st.expander("Audience Engagement Distribution", expanded=False):
        render_chart_with_description(
            title='Audience Engagement Boxplot',
            description='Box plot showing the distribution of audience votes (popularity) for each actor. '
                       'The box shows the middle 50% of data.',
            key_insight='Which actors have the most engaged audiences? Which films are outliers?',
            chart_element=create_engagement_boxplot(df_filtered),
            interaction_tip='Hover for detailed statistics'
        )
    
    # Complete Timeline
    with st.expander("Complete Film Timeline", expanded=False):
        render_chart_with_description(
            title='Film Timeline Analysis',
            description='Comprehensive view of all films plotted by release year and actor. '
                       'Circle size represents popularity, color represents rating band.',
            key_insight='Can you spot patterns in film quality over time? Which periods were most prolific?',
            chart_element=create_film_timeline_chart(df_filtered),
            interaction_tip='Hover for film titles and ratings'
        )
    
    st.markdown("---")
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.markdown("""
    <div style="
        text-align: center;
        color: #666;
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid #333;
    ">
        <small>
         <strong>The 007 Data Dossier</strong> | Advanced Analysis of James Bond Films & Actor Performance<br>
        <em>Data Source: IMDb | Last Updated: November 2025</em>
        </small>
    </div>
    """, unsafe_allow_html=True)