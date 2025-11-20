"""
Professional Design System for Bond Dashboard
Ensures consistency across all pages and components
"""

# ============================================================================
# COLOR PALETTE (Keep existing + Enhanced)
# ============================================================================
BACKGROUND_COLOR = '#0e1117'
TEXT_COLOR = 'white'
ACCENT_BLUE = '#4A90E2'
ACCENT_ORANGE = '#F58518'
ACCENT_GREEN = '#54A24B'
ACCENT_RED = '#DC143C'
ACCENT_GOLD = '#FFD700'
GRID_COLOR = '#2C2C2C'
CARD_BG = '#1a1a2e'
CARD_BORDER = '#FFD700'

# ============================================================================
# SPACING SYSTEM (Consistent margins & padding)
# ============================================================================
SPACING_XS = 8
SPACING_SM = 12
SPACING_MD = 16
SPACING_LG = 24
SPACING_XL = 32
SPACING_XXL = 48

# ============================================================================
# TYPOGRAPHY SIZES (Consistent heading hierarchy)
# ============================================================================
HEADING_SIZE_L = 48      # Main page title
HEADING_SIZE_M = 24      # Section headers
HEADING_SIZE_S = 18      # Subsection headers
TEXT_SIZE_NORMAL = 14
TEXT_SIZE_SMALL = 12
TEXT_SIZE_CAPTION = 10

# ============================================================================
# COMPONENT SIZING
# ============================================================================
METRIC_CARD_HEIGHT = 100
INSIGHT_CARD_HEIGHT = 120
CHART_HEIGHT_SM = 300
CHART_HEIGHT_MD = 350
CHART_HEIGHT_LG = 450
CHART_HEIGHT_XL = 500

# ============================================================================
# STANDARDIZED CSS FOR CONSISTENT COMPONENTS
# ============================================================================

def get_metric_card_style():
    """CSS for metric cards - consistent sizing and alignment"""
    return """
    <style>
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #FFD700;
        margin-bottom: 10px;
        text-align: center;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
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
    """


def get_section_header_style():
    """CSS for section headers - consistent hierarchy"""
    return """
    <style>
    .section-header {
        font-size: 28px;
        font-weight: bold;
        color: white;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, #FFD700, transparent);
        margin: 10px 0 20px 0;
    }
    .section-subtitle {
        font-size: 14px;
        color: #999;
        margin-bottom: 16px;
    }
    </style>
    """


def get_insight_card_style():
    """CSS for insight cards - gold gradient with consistency"""
    return """
    <style>
    .insight-card {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #000;
        padding: 16px;
        border-radius: 8px;
        margin: 8px 0;
        text-align: center;
        min-height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .insight-label {
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
        opacity: 0.8;
        margin-bottom: 8px;
    }
    .insight-value {
        font-size: 24px;
        font-weight: bold;
    }
    .insight-context {
        font-size: 11px;
        margin-top: 8px;
        opacity: 0.7;
    }
    </style>
    """


def get_chart_wrapper_style():
    """CSS for chart wrappers - consistent borders and spacing"""
    return """
    <style>
    .chart-wrapper {
        background: transparent;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 20px;
    }
    .chart-title {
        font-size: 18px;
        font-weight: bold;
        color: #FFD700;
        margin-bottom: 8px;
    }
    .chart-description {
        font-size: 12px;
        color: #999;
        margin-bottom: 12px;
        line-height: 1.5;
    }
    .chart-insights {
        display: flex;
        gap: 12px;
        font-size: 11px;
        color: #999;
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid #333;
    }
    .chart-insight-item {
        flex: 1;
    }
    </style>
    """


def get_page_container_style():
    """CSS for main page container - consistent page layout"""
    return """
    <style>
    .page-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0px 20px;
    }
    .page-title {
        font-size: 48px;
        font-weight: bold;
        color: white;
        margin: 0;
        padding: 0;
        text-align: center;
    }
    .page-subtitle {
        font-size: 16px;
        color: #FFD700;
        text-align: center;
        margin: 8px 0 20px 0;
        padding: 0;
    }
    
    /* Remove all top spacing */
    .block-container {
        padding-top: 0rem !important;
    }
    </style>
    """


# ============================================================================
# INJECTION FUNCTIONS - Use these to ensure consistency
# ============================================================================

def inject_global_styles():
    """Inject ALL design system styles into page"""
    import streamlit as st
    st.markdown(get_metric_card_style(), unsafe_allow_html=True)
    st.markdown(get_section_header_style(), unsafe_allow_html=True)
    st.markdown(get_insight_card_style(), unsafe_allow_html=True)
    st.markdown(get_chart_wrapper_style(), unsafe_allow_html=True)
    st.markdown(get_page_container_style(), unsafe_allow_html=True)


# ============================================================================
# COLOR MAPS FOR CONSISTENCY
# ============================================================================
GENRE_COLORS = {
    'Action': '#DC143C',
    'Adventure': '#4A90E2',
    'Thriller': '#F58518',
    'Romance': '#FFD700',
    'Comedy': '#54A24B',
    'Drama': '#9B59B6',
    'Sci-Fi': '#95A5A6'
}

RATING_BAND_COLORS = {
    'Below 6': '#DC143C',
    '6-7': '#F58518',
    '7-8': '#54A24B',
    '8+': '#4A90E2'
}

# ============================================================================
# NAVIGATION ICONS & LABELS
# ============================================================================
NAV_ITEMS = {
    'Bond Overview': '',
    'Individual Charts': '',
    'Story Mode': '',
    'Actor Universe': ''
}