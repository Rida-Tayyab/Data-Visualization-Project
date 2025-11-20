"""
Professional UI components with consistent design system.
All components aligned to design_system.py specifications.
"""

import streamlit as st

try:
    from .config import EON_BOND_ACTORS
    from .design_system import (
        inject_global_styles,
        get_section_header_style,
        get_insight_card_style,
        get_chart_wrapper_style,
        NAV_ITEMS,
        SPACING_MD,
        SPACING_LG
    )
except ImportError:
    from config import EON_BOND_ACTORS
    from design_system import (
        inject_global_styles,
        get_section_header_style,
        get_insight_card_style,
        get_chart_wrapper_style,
        NAV_ITEMS,
        SPACING_MD,
        SPACING_LG
    )


# Note: Page configuration should be done in main bond_dashboard.py file
# This file only contains reusable components


def initialize_page_styles():
    """Initialize all design system styles - CALL THIS AT TOP OF EVERY PAGE"""
    inject_global_styles()


def render_page_header(title, subtitle=""):
    """
    Render professional page header with consistent styling.
    
    Args:
        title: Main page title (e.g., "Bond Overview")
        subtitle: Optional subtitle with more context
    """
    st.markdown(f"""
    <div style="text-align: center; margin-top: 0; margin-bottom: 20px; padding-top: 0;">
        <h1 style="font-size: 48px; font-weight: bold; color: white; margin: 0; padding: 0; letter-spacing: 1px;">
            {title}
        </h1>
        {f'<p style="font-size: 16px; color: #FFD700; margin: 8px 0 0 0; padding: 0;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")


def render_section_header(title, description=""):
    """
    Render consistent section header with title and optional description.
    
    Args:
        title: Section title (required)
        description: Optional descriptive text (optional)
    """
    st.markdown(f"""
    <div style="margin-bottom: 16px;">
        <h2 style="
            font-size: 28px;
            font-weight: bold;
            color: white;
            margin: 0 0 8px 0;
        ">
            {title}
        </h2>
        {f'<p style="font-size: 14px; color: #999; margin: 0; padding: 0;">{description}</p>' if description else ''}
    </div>
    <div style="height: 2px; background: linear-gradient(90deg, #FFD700, transparent); margin: 12px 0 20px 0;"></div>
    """, unsafe_allow_html=True)


def render_metric_card(label, value, context="", width=None):
    """
    Render a single consistent metric card.
    
    Args:
        label: Metric label (e.g., "Total Films")
        value: Metric value (e.g., "25")
        context: Optional context text
        width: Optional width (for use in columns)
    """
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {f'<small style="color: #999; margin-top: 8px;">{context}</small>' if context else ''}
    </div>
    """, unsafe_allow_html=True)


def render_metrics_row(metrics_list):
    """
    Render 4 metric cards in a consistent row.
    
    Args:
        metrics_list: List of dicts with keys: label, value, context
        Example: [
            {'label': 'Total Films', 'value': '25', 'context': 'analyzed'},
            ...
        ]
    """
    cols = st.columns(4)
    for idx, col in enumerate(cols):
        if idx < len(metrics_list):
            with col:
                metric = metrics_list[idx]
                render_metric_card(
                    metric['label'],
                    metric['value'],
                    metric.get('context', '')
                )


def render_insight_card(label, value, context=""):
    """
    Render a single insight card with gold gradient.
    
    Args:
        label: Insight label
        value: Main insight value/finding
        context: Optional additional context
    """
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-label">{label}</div>
        <div class="insight-value">{value}</div>
        {f'<div class="insight-context">{context}</div>' if context else ''}
    </div>
    """, unsafe_allow_html=True)


def render_insight_row(insights_list):
    """
    Render insight cards in a flexible row (2-3 columns depending on content).
    
    Args:
        insights_list: List of dicts with keys: label, value, context
    """
    num_insights = len(insights_list)
    if num_insights == 0:
        return
    
    # Determine columns: 2-3 insights per row
    num_cols = min(3, num_insights)
    cols = st.columns(num_cols)
    
    for idx, col in enumerate(cols):
        if idx < num_insights:
            with col:
                insight = insights_list[idx]
                render_insight_card(
                    insight['label'],
                    insight['value'],
                    insight.get('context', '')
                )


def render_chart_with_description(
    title,
    description,
    key_insight,
    chart_element,
    interaction_tip="",
    use_container_width=True
):
    """
    Render a chart with professional wrapper, description, and guidance.
    
    Args:
        title: Chart title
        description: 2-3 sentence explanation of what chart shows
        key_insight: What pattern/trend to notice
        chart_element: The Altair chart object or st.altair_chart call result
        interaction_tip: Optional interaction guidance
        use_container_width: Whether chart uses full width
    """
    st.markdown("""
    <div class="chart-wrapper">
    """, unsafe_allow_html=True)
    
    # Title and description
    st.markdown(f"<div class='chart-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chart-description'>{description}</div>", unsafe_allow_html=True)
    
    # Chart itself
    st.altair_chart(chart_element, use_container_width=use_container_width)
    
    # Insights and tips footer
    col1, col2 = st.columns([3, 1]) if interaction_tip else (st.columns([1]), None)
    
    with col1:
        st.markdown(
            f"<small><strong>Key Insight:</strong> {key_insight}</small>",
            unsafe_allow_html=True
        )
    
    if col2 and interaction_tip:
        with col2:
            st.markdown(
                f"<small>{interaction_tip}</small>",
                unsafe_allow_html=True
            )
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_two_column_charts(
    left_chart_config,
    right_chart_config
):
    """
    Render two charts side-by-side with consistent styling.
    
    Args:
        left_chart_config: Dict with keys: title, description, key_insight, chart, interaction_tip
        right_chart_config: Dict with keys: title, description, key_insight, chart, interaction_tip
    """
    col_left, col_right = st.columns(2)
    
    with col_left:
        render_chart_with_description(
            title=left_chart_config['title'],
            description=left_chart_config['description'],
            key_insight=left_chart_config['key_insight'],
            chart_element=left_chart_config['chart'],
            interaction_tip=left_chart_config.get('interaction_tip', ''),
            use_container_width=True
        )
    
    with col_right:
        render_chart_with_description(
            title=right_chart_config['title'],
            description=right_chart_config['description'],
            key_insight=right_chart_config['key_insight'],
            chart_element=right_chart_config['chart'],
            interaction_tip=right_chart_config.get('interaction_tip', ''),
            use_container_width=True
        )


def render_key_metrics(df_filtered):
    """
    Render the key metrics section - USED IN OVERVIEW PAGE.
    Now uses consistent metric cards.
    """
    st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #FFD700;
        margin-bottom: 10px;
        text-align: center;
        min-height: 100px;
    }
    .metric-label {
        font-size: 12px;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)
    
    render_section_header("Executive Metrics")
    
    total_films = len(df_filtered)
    avg_rating = df_filtered['averageRating'].mean() if total_films > 0 else 0
    avg_runtime = df_filtered['runtimeMinutes'].mean() if total_films > 0 else 0
    best_film = df_filtered.loc[df_filtered['averageRating'].idxmax()] if total_films > 0 else {
        'primaryTitle': 'N/A',
        'averageRating': 0
    }
    
    metrics = [
        {
            'label': 'Total Films Analyzed',
            'value': str(total_films),
            'context': 'in selection'
        },
        {
            'label': 'Average IMDb Rating',
            'value': f'{avg_rating:.2f}/10',
            'context': 'mean score'
        },
        {
            'label': 'Average Runtime',
            'value': f'{avg_runtime:.0f} min',
            'context': 'film length'
        },
        {
            'label': 'Highest Rated Film',
            'value': f'{best_film["averageRating"]:.2f}/10',
            'context': best_film['primaryTitle'][:20] + '...' if len(best_film['primaryTitle']) > 20 else best_film['primaryTitle']
        }
    ]
    
    render_metrics_row(metrics)
    st.markdown("---")


def render_sidebar_filters(df_full):
    """
    Render sidebar filters and return filtered data.
    Enhanced with better organization and icons.
    """
    st.sidebar.markdown("### Mission Parameters")

    # 1. Data Focus Selection
    data_focus = st.sidebar.radio(
        "Select Data Focus:",
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
    st.sidebar.markdown("### Actor Dossier")

    # 2. Vertical Checkbox Filter
    selected_actors_dict = {}
    for actor in actor_list_options:
        is_selected = st.sidebar.checkbox(actor, value=(actor in default_actors))
        selected_actors_dict[actor] = is_selected

    selected_actors = [actor for actor, selected in selected_actors_dict.items() if selected]

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Temporal Filter")

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

    st.sidebar.markdown("---")
    
    # Reset filters button
    if st.sidebar.button("Reset All Filters", use_container_width=True):
        st.rerun()

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


def get_page_container_style():
    """CSS for main page container - consistent page layout"""
    return """
    <style>
    .page-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 20px;
        margin-top: -60px;
    }
    .page-title {
        font-size: 36px;
        font-weight: bold;
        color: white;
        margin-bottom: 8px;
        text-align: center;
        margin-top: 0;
    }
    .page-subtitle {
        font-size: 16px;
        color: #FFD700;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """