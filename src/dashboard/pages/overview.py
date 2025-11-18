"""Bond Overview dashboard page."""

import streamlit as st

try:
    from ..components import render_key_metrics
    from ..charts import (
        create_actor_performance_chart,
        create_rating_trend_chart,
        create_bond_comparison_chart,
        create_runtime_rating_chart,
        create_genre_evolution_chart,
        create_genre_trend_chart,
        create_rating_distribution_chart,
        create_production_volume_chart,
        create_performance_heatmap,
        create_engagement_boxplot,
        create_film_timeline_chart
    )
except ImportError:
    from components import render_key_metrics
    from charts import (
        create_actor_performance_chart,
        create_rating_trend_chart,
        create_bond_comparison_chart,
        create_runtime_rating_chart,
        create_genre_evolution_chart,
        create_genre_trend_chart,
        create_rating_distribution_chart,
        create_production_volume_chart,
        create_performance_heatmap,
        create_engagement_boxplot,
        create_film_timeline_chart
    )


def render_dashboard(df_full, df_filtered):
    """Render the main Bond Overview dashboard."""
    st.title("The 007 Data Dossier: Interactive Dashboard")
    st.markdown("**A comprehensive analysis of the James Bond franchise and lead actor performance across cinematic history.**")
    st.markdown("---")
    
    if df_filtered is None or len(df_filtered) == 0:
        st.error("Please select at least one actor and ensure your filter criteria match available data.")
        return
    
    # Key Metrics
    render_key_metrics(df_filtered)
    
    # === SECTION 1: PERFORMANCE ANALYSIS ===
    st.markdown("## Performance Analysis")
    
    st.markdown("#### Actor Performance Ranking")
    st.caption("Average IMDb ratings by lead actor")
    st.altair_chart(create_actor_performance_chart(df_filtered), use_container_width=True)
    
    st.markdown("#### Rating Trend Over Time")
    st.caption("Film ratings evolution across decades")
    st.altair_chart(create_rating_trend_chart(df_filtered), use_container_width=True)
    
    st.markdown("---")
    
    # === SECTION 2: BOND VS OTHER FILMS ===
    st.markdown("## Bond Film Comparison")
    
    st.markdown("#### James Bond Movies vs Other Thriller Films")
    st.caption("All Bond films compared to thriller movies with trend lines")
    
    chart, bond_data, other_data = create_bond_comparison_chart(df_full)
    st.altair_chart(chart, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        **James Bond Films:**
        - Average Rating: {bond_data['averageRating'].mean():.2f}
        - Total Films: {len(bond_data)}
        """)
    with col2:
        st.markdown(f"""
        **Other Thriller Films:**
        - Average Rating: {other_data['averageRating'].mean():.2f}
        - Total Films: {len(other_data)}
        """)
    
    st.markdown("---")
    
    # === SECTION 3: CONTENT ANALYSIS ===
    st.markdown("## Content & Genre Analysis")
    
    st.markdown("#### Runtime vs Rating Analysis")
    st.caption("Relationship between film length, rating, and popularity")
    st.altair_chart(create_runtime_rating_chart(df_filtered), use_container_width=True)
    
    st.markdown("#### Genre Evolution by Decade")
    st.caption("Genre distribution across different time periods")
    st.altair_chart(create_genre_evolution_chart(df_filtered), use_container_width=True)
    
    st.markdown("#### Genre Popularity Trend Over Time")
    st.caption("Film count by genre across decades - showing popularity shifts")
    genre_trend = create_genre_trend_chart(df_filtered)
    if genre_trend:
        st.altair_chart(genre_trend, use_container_width=True)
    else:
        st.info("Not enough data to show genre trends")
    
    st.markdown("---")
    
    # === SECTION 4: DISTRIBUTION METRICS ===
    st.markdown("## Distribution & Production Metrics")
    
    st.markdown("#### Rating Distribution by Actor")
    st.caption("Individual film ratings showing distribution patterns")
    st.altair_chart(create_rating_distribution_chart(df_filtered), use_container_width=True)
    
    st.markdown("#### Production Volume by Decade")
    st.caption("Number of films produced in each decade")
    st.altair_chart(create_production_volume_chart(df_filtered), use_container_width=True)
    
    st.markdown("---")
    
    # === SECTION 5: ADVANCED ANALYTICS ===
    st.markdown("## Advanced Analytics")
    
    st.markdown("#### Performance Heatmap: Actor × Decade")
    st.caption("Average ratings across different time periods")
    st.altair_chart(create_performance_heatmap(df_filtered), use_container_width=True)
    
    st.markdown("#### Audience Engagement Distribution")
    st.caption("Vote distribution showing audience reach")
    st.altair_chart(create_engagement_boxplot(df_filtered), use_container_width=True)
    
    st.markdown("---")
    
    # === SECTION 6: DETAILED BREAKDOWN ===
    st.markdown("## Detailed Film Analysis")
    
    st.markdown("#### Complete Film Timeline")
    st.caption("Chronological view with rating bands and popularity indicators")
    st.altair_chart(create_film_timeline_chart(df_filtered), use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("Data Source: IMDb via data_final_lead_actor.csv")
