"""Configuration and theme settings for the Bond Dashboard."""

import altair as alt

# Thematic Colors (Dark Theme)
BACKGROUND_COLOR = '#0e1117'
TEXT_COLOR = 'white'
ACCENT_BLUE = '#4A90E2'
ACCENT_ORANGE = '#F58518'
ACCENT_GREEN = '#54A24B'
ACCENT_RED = '#DC143C'
ACCENT_GOLD = '#FFD700'
GRID_COLOR = '#2C2C2C'

# Define the set of Canonical Eon Bond Actors
EON_BOND_ACTORS = [
    'Sean Connery', 
    'George Lazenby', 
    'Roger Moore', 
    'Timothy Dalton', 
    'Pierce Brosnan', 
    'Daniel Craig'
]


def get_bond_theme():
    """Defines the dark, elegant style for all charts."""
    return {
        "config": {
            "title": {
                "color": ACCENT_GOLD,
                "fontSize": 18,
                "font": "sans-serif",
                "fontWeight": "bold",
                "anchor": "middle"
            },
            "view": {
                "stroke": "transparent",
                "fill": BACKGROUND_COLOR
            },
            "background": BACKGROUND_COLOR,
            "style": {
                "guide-label": {"fill": TEXT_COLOR},
                "guide-title": {"fill": TEXT_COLOR, "fontWeight": "bold"},
                "group-title": {"fill": TEXT_COLOR},
            },
            "axis": {
                "domainColor": "#444444",
                "gridColor": GRID_COLOR,
                "labelColor": TEXT_COLOR,
                "titleColor": TEXT_COLOR,
                "titleFontWeight": "bold",
                "labelFontSize": 11,
                "titleFontSize": 13,
            },
            "legend": {
                "titleColor": TEXT_COLOR,
                "labelColor": TEXT_COLOR
            },
            "range": {
                "category": [
                    ACCENT_GOLD, ACCENT_RED, ACCENT_BLUE, 
                    ACCENT_GREEN, ACCENT_ORANGE, '#9B59B6', '#95A5A6'
                ]
            },
            "mark": {
                "tooltip": True
            }
        }
    }


def register_theme():
    """Register and enable the Bond theme."""
    alt.themes.register("bond_theme", get_bond_theme)
    alt.themes.enable("bond_theme")
