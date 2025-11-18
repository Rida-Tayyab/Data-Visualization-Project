"""Individual Charts page - focused chart views."""

import streamlit as st
import pandas as pd

try:
    from ..components import render_sidebar_filters
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
    from components import render_sidebar_filters
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


def render_individual_chart(df_full, chart_name):
    """Render a single chart in full view."""
    st.title(f"{chart_name}")
    st.markdown("---")
    
    # Apply filters
    df_filtered, selected_actors = render_sidebar_filters(df_full)
    
    if df_filtered is None or len(df_filtered) == 0:
        st.error("Please select at least one actor")
        return
    
    # Render the selected chart
    if chart_name == "Actor Performance Ranking":
        st.altair_chart(create_actor_performance_chart(df_filtered), use_container_width=True)
    
    elif chart_name == "Rating Trend Over Time":
        st.altair_chart(create_rating_trend_chart(df_filtered), use_container_width=True)
    
    elif chart_name == "Bond vs Other Thriller Films":
        st.markdown("#### James Bond Movies vs Other Thriller Films")
        st.caption("All Bond films compared to thriller movies with trend lines")
        
        chart, bond_data, other_data = create_bond_comparison_chart(df_full)
        st.altair_chart(chart, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            **James Bond Films:**
            - Avg Rating: {bond_data['averageRating'].mean():.2f}
            - Total: {len(bond_data)}
            """)
        with col2:
            st.markdown(f"""
            **Other Thriller Films:**
            - Avg Rating: {other_data['averageRating'].mean():.2f}
            - Total: {len(other_data)}
            """)
    
    elif chart_name == "Runtime vs Rating Analysis":
        st.altair_chart(create_runtime_rating_chart(df_filtered), use_container_width=True)
    
    elif chart_name == "Genre Evolution by Decade":
        st.altair_chart(create_genre_evolution_chart(df_filtered), use_container_width=True)
    
    elif chart_name == "Genre Popularity Trend":
        chart = create_genre_trend_chart(df_filtered)
        if chart:
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Not enough data to show genre trends")
    
    elif chart_name == "Rating Distribution by Actor":
        st.altair_chart(create_rating_distribution_chart(df_filtered), use_container_width=True)
    
    elif chart_name == "Production Volume by Decade":
        st.altair_chart(create_production_volume_chart(df_filtered), use_container_width=True)
    
    elif chart_name == "Performance Heatmap":
        st.altair_chart(create_performance_heatmap(df_filtered), use_container_width=True)
    
    elif chart_name == "Audience Engagement Distribution":
        st.altair_chart(create_engagement_boxplot(df_filtered), use_container_width=True)
    
    elif chart_name == "Complete Film Timeline":
        st.altair_chart(create_film_timeline_chart(df_filtered), use_container_width=True)
