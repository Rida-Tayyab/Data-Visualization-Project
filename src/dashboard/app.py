# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.set_page_config(page_title="F1 Analytics Dashboard", layout="wide")
    
    st.title("🏎️ Formula 1 Performance Analytics")
    st.markdown("Interactive analysis of F1 historical data (1950-2023)")
    
    # Load data
    datasets = load_and_explore_data()
    cleaned_data = clean_f1_data(datasets)
    analytical_df = create_analytical_dataset(cleaned_data)
    
    # Sidebar filters
    st.sidebar.header("Filters")
    selected_years = st.sidebar.slider(
        "Season Years", 
        min_value=int(analytical_df['year'].min()),
        max_value=int(analytical_df['year'].max()),
        value=(2010, 2023)
    )
    
    selected_constructors = st.sidebar.multiselect(
        "Constructors",
        options=analytical_df['name_y'].unique(),
        default=['Mercedes', 'Ferrari', 'Red Bull']
    )
    
    # Filter data
    filtered_df = analytical_df[
        (analytical_df['year'] >= selected_years[0]) & 
        (analytical_df['year'] <= selected_years[1]) &
        (analytical_df['name_y'].isin(selected_constructors))
    ]
    
    # Dashboard layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_position_analysis(filtered_df), use_container_width=True)
        st.plotly_chart(create_pit_stop_analysis(filtered_df, cleaned_data['pit_stops']), 
                       use_container_width=True)
    
    with col2:
        st.plotly_chart(create_team_performance_timeline(filtered_df), use_container_width=True)
        st.plotly_chart(create_circuit_heatmap(filtered_df), use_container_width=True)
    
    # Interactive section
    st.header("Driver Head-to-Head Comparison")
    selected_drivers = st.multiselect(
        "Select drivers to compare:",
        options=filtered_df['full_name'].unique()[:15],
        default=[filtered_df['full_name'].iloc[0], filtered_df['full_name'].iloc[1]]
    )
    
    if len(selected_drivers) >= 2:
        comparison_data = filtered_df[filtered_df['full_name'].isin(selected_drivers)]
        fig = px.line(
            comparison_data.groupby(['year', 'full_name'])['points'].sum().reset_index(),
            x='year', y='points', color='full_name',
            title=f"Championship Points Comparison: {' vs '.join(selected_drivers)}"
        )
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()