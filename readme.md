# 007 Data Dossier: James Bond Film Analysis Dashboard

## Project Overview
An interactive data-visualization dashboard built on a James Bond film dataset. The dashboard provides insights into the franchise's evolution, focusing on actor performance, temporal trends, and genre shifts.

## Theme
"MI6 Mission Briefing" aesthetic: dark mode with Tableau-inspired professional styling
- Gold (#FFD700) for primary highlights
- Crimson (#DC143C) for action/danger elements
- Professional Blue (#4A90E2) and Teal (#1ABC9C) accents
- Clean, modern layout with enhanced visual hierarchy

## Technology Stack
- Framework: Python (Streamlit)
- Visualization: Altair
- Data: `data_final_lead_actor.csv`

## Prerequisites
- Python 3.8+

## Installation
Install required packages:
```bash
pip install pandas streamlit altair
```

## File Setup
Ensure these files are in the same directory:
- `bond_dashboard.py` (main Python code file)
- `data_final_lead_actor.csv` (original dataset file)

## Run the Dashboard
In the project directory, run:
```bash
streamlit run bond_dashboard.py
```

This opens the interactive dashboard in your web browser.

## Dashboard Functionality and Filtering
The dashboard has a three-tiered filtering system:

1. **Data Focus (Tier 1 - Radio Button):**
   - "James Bond Core Films (EON Actors & 007 Titles)": Focuses on officially relevant Bond films.
   - "General Actor Search (Full Dataset)": Expands to include movies with any actor having 5+ films and 1000+ votes.

2. **Actor Dossier (Tier 2 - Vertical Checkbox):**
   - Granular selection of specific actors for comparison.

3. **Temporal Filter (Tier 3 - Slider):**
   - Narrows analysis to a specific range of release years.

## Visualization Breakdown (Tableau-Inspired Design)
The dashboard now contains 10 specialized charts with enhanced Tableau-style formatting:

### KPI Metrics Row
- 5 key performance indicators with icons: Total Films, Avg Rating, Avg Runtime, Total Votes, Top Film

### Row 1: Comparison & Evolution
1. **Actor Performance Ranking**: Horizontal bar chart with gradient coloring based on ratings
2. **Rating Trend Over Time**: Interactive scatter plot with regression line and legend-based filtering

### Row 2: Runtime, Votes, and Genre Analysis
3. **Runtime, Rating, and Popularity**: 4-variable scatter plot with zoom/pan interactivity
4. **Genre Intensity by Decade**: Stacked bar chart showing genre evolution

### Row 3: Distribution and Production
5. **Film Rating Distribution**: Jitter plot with mean line overlay for distribution analysis
6. **Decadal Film Production Count**: Gradient-colored bar chart showing production trends

### Row 4: Advanced Analytics (NEW - Tableau-Inspired)
7. **Actor-Decade Performance Heatmap**: Color-coded heatmap showing rating performance across time periods
8. **Box Office Appeal**: Box plot visualization showing vote distribution by actor (log scale)

### Row 5: Detailed Breakdown (NEW)
9. **Film Timeline with Rating Bands**: Bubble chart with color-coded rating categories and size-based popularity
10. **Top 10 Highest Rated Films**: Horizontal bar chart showcasing the hall of fame films

## Enhanced Features
- **Custom CSS Styling**: Tableau-inspired metric cards, typography, and color schemes
- **Interactive Elements**: Legend-based filtering, zoom/pan capabilities, hover tooltips
- **Professional Color Palette**: Extended color range for better data distinction
- **Improved Visual Hierarchy**: Clear section headers, consistent spacing, enhanced readability