# 007 Data Dossier: James Bond Film Analysis Dashboard

## Project Overview
An interactive data-visualization dashboard built on a James Bond film dataset. The dashboard provides insights into the franchise's evolution, focusing on actor performance, temporal trends, and genre shifts.

## Theme
"MI6 Mission Briefing" aesthetic: dark mode with Gold (#FFD700) and Crimson (#B22222) accents.

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

## Visualization Breakdown (Thematic Rationale)
The dashboard contains six specialized charts:

### Row 1: Comparison & Evolution
1. **Actor Performance Ranking**: Ranks actors based on critical reception using a Horizontal Bar Chart.
2. **Rating Trend Over Time**: Visualizes evolution of film quality across decades with a Line Chart and Regression line.

### Row 2: Runtime, Votes, and Genre Analysis
3. **Runtime, Rating, and Popularity**: Analyzes relationship between film length, rating, and audience volume using a 4-Variable Scatter Plot.
4. **Genre Intensity by Decade**: Reveals changes in thematic focus over time with a Stacked Bar Chart.

### Row 3: Distribution and Production
5. **Film Rating Distribution**: Shows variability and consistency of ratings for individual films using a Jitter/Strip Plot with Mean Line.
6. **Decadal Film Production Count**: Quantifies activity level and gaps in production over the franchise's history with a Bar Chart.