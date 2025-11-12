import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
from pathlib import Path

# --- CONFIGURATION & THEME ---
st.set_page_config(
    page_title="The 007 Data Dossier: James Bond Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Thematic Colors (Dark Theme)
BACKGROUND_COLOR = '#0e1117'      # Dark Streamlit background
TEXT_COLOR = 'white'              # White text
ACCENT_BLUE = '#4A90E2'           # Professional blue
ACCENT_ORANGE = '#F58518'         # Orange accent
ACCENT_GREEN = '#54A24B'          # Green accent
ACCENT_RED = '#DC143C'            # Crimson red
ACCENT_GOLD = '#FFD700'           # Gold for highlights
GRID_COLOR = '#2C2C2C'            # Dark gray grid

# Define the set of Canonical Eon Bond Actors (for the core subset)
EON_BOND_ACTORS = ['Sean Connery', 'George Lazenby', 'Roger Moore', 'Timothy Dalton', 'Pierce Brosnan', 'Daniel Craig']

# --- ALTAIR THEME STYLING (Dark Theme) ---
def get_bond_theme():
    # Defines the dark, elegant style for all charts
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
                # Dark theme color palette
                "category": [ACCENT_GOLD, ACCENT_RED, ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, '#9B59B6', '#95A5A6'] 
            },
            "mark": {
                "tooltip": True
            }
        }
    }

alt.themes.register("bond_theme", get_bond_theme)
alt.themes.enable("bond_theme")

# --- DATA LOADING & PRE-PROCESSING (Loading the full dataset once) ---
@st.cache_data
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)
    
    # 1. Initial Cleaning: Drop rows with missing leadActor, as this is the core of our analysis
    df.dropna(subset=['leadActor'], inplace=True)
    
    # 2. Convert types for cleaner analysis
    df['releaseYear'] = df['releaseYear'].astype(int)
    df['decade'] = (df['releaseYear'] // 10 * 10).astype(int)
    
    # 3. Create the 'Core Bond' subset mask
    is_bond_actor = df['leadActor'].isin(EON_BOND_ACTORS)
    has_bond_title = df['primaryTitle'].str.contains('Bond|007', case=False, na=False) | \
                     df['originalTitle'].str.contains('Bond|007', case=False, na=False)
    
    df['is_bond_core'] = (is_bond_actor | has_bond_title)
    
    # 4. Filter out any remaining garbage entries (e.g., too few votes to matter)
    # Raising the vote threshold to 500 for more robust "General Actor Search"
    df = df[df['numVotes'] >= 500].copy() 
    
    return df

BASE_DIR = Path(__file__).resolve().parent.parent  
data_file = BASE_DIR.parent / 'data' / 'processed' / 'data_final_lead_actor_fixed.csv'

df_full = load_and_preprocess_data(data_file)

# Determine global min/max year for the slider
GLOBAL_YEAR_MIN = int(df_full['releaseYear'].min())
GLOBAL_YEAR_MAX = int(df_full['releaseYear'].max())


# --- PAGE NAVIGATION ---
st.sidebar.header("007 Navigation")
page_mode = st.sidebar.radio(
    "Select View Mode:",
    ('Interactive Dashboard', '007 Story Mode', 'Across the 007 Verse')
)


st.sidebar.markdown("---")

# ==============================================================================
# === PAGE 1: INTERACTIVE DASHBOARD (Existing Logic) =============================
# ==============================================================================

def render_dashboard(df_full, EON_BOND_ACTORS):
    st.title("The 007 Data Dossier: Interactive Dashboard")
    st.markdown("**A comprehensive analysis of the James Bond franchise and lead actor performance across cinematic history.**")
    st.markdown("---")
    
    # --- SIDEBAR FILTERS (Professional Two-Tiered Selection) ---
    st.sidebar.header("Mission Parameters: Data Focus")

    # 1. Data Focus Selection (Tier 1: High-Level Filter)
    data_focus = st.sidebar.radio(
        "1. Select Data Focus:",
        ('James Bond Core Films (EON Actors & 007 Titles)', 'General Actor Search (Full Dataset)'),
        index=0
    )

    # Apply Focus Filter
    if data_focus == 'James Bond Core Films (EON Actors & 007 Titles)':
        df_current = df_full[df_full['is_bond_core']].copy()
        actor_list_options = sorted(list(set(EON_BOND_ACTORS).intersection(df_current['leadActor'].unique())))
        default_actors = EON_BOND_ACTORS
        
    else: # General Actor Search (Full Dataset)
        df_current = df_full.copy()
        
        # Only show actors with at least 5 films and 1000 votes for a cleaner selection list
        top_actors = df_current.groupby('leadActor').filter(lambda x: len(x) >= 5 and x['numVotes'].sum() >= 1000)
        actor_list_options = sorted(top_actors['leadActor'].unique().tolist())
        default_actors = EON_BOND_ACTORS # Defaulting to Bond actors for initial load

    st.sidebar.markdown("---")
    st.sidebar.header("2. Actor Dossier (Vertical Checkbox Filter)")

    # 2. Vertical Checkbox Filter (Tier 2: Granular Filter)
    selected_actors_dict = {}
    for actor in actor_list_options:
        # Use a dictionary to store the selection state
        is_selected = st.sidebar.checkbox(actor, value=(actor in default_actors))
        selected_actors_dict[actor] = is_selected

    selected_actors = [actor for actor, selected in selected_actors_dict.items() if selected]

    st.sidebar.markdown("---")
    st.sidebar.header("3. Temporal Filter")

    # 3. Year Range Slider 
    year_min = int(df_current['releaseYear'].min()) if not df_current.empty else GLOBAL_YEAR_MIN
    year_max = int(df_current['releaseYear'].max()) if not df_current.empty else GLOBAL_YEAR_MAX
        
    # Ensure the range is valid
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


    # Apply ALL Filters
    if selected_actors and not df_current.empty:
        df_filtered = df_current[
            (df_current['leadActor'].isin(selected_actors)) &
            (df_current['releaseYear'] >= selected_years[0]) &
            (df_current['releaseYear'] <= selected_years[1])
        ].copy()
    else:
        # Handle case where no actors are selected or data is empty
        df_filtered = pd.DataFrame(columns=df_current.columns)
        st.error("Please select at least one actor and ensure your filter criteria match available data.")


    # --- KEY METRICS (Tableau-style KPI cards) ---
    col1, col2, col3, col4, col5 = st.columns(5)

    total_films = len(df_filtered)
    avg_rating = df_filtered['averageRating'].mean() if total_films > 0 else 0
    avg_runtime = df_filtered['runtimeMinutes'].mean() if total_films > 0 else 0
    total_votes = df_filtered['numVotes'].sum() if total_films > 0 else 0
    highest_voted_film = df_filtered.sort_values(by='numVotes', ascending=False).iloc[0] if total_films > 0 else {'primaryTitle': 'N/A', 'numVotes': 0}

    with col1:
        st.metric("Total Films", f"{total_films}")
    with col2:
        st.metric("Average Rating", f"{avg_rating:.2f}/10")
    with col3:
        st.metric("Average Runtime", f"{avg_runtime:.0f} min")
    with col4:
        st.metric("Total Votes", f"{total_votes:,.0f}")
    with col5:
        st.metric("Most Popular", f"{highest_voted_film['primaryTitle'][:15]}...")

    st.markdown("---")

    # Only render charts if there is data
    if total_films > 0:

        # --- VISUALIZATIONS ---
        
        # === SECTION 1: PERFORMANCE ANALYSIS ===
        st.markdown("<h2 class='section-header'>Performance Analysis</h2>", unsafe_allow_html=True)
        
        # Chart 1: Actor Performance Ranking
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("#### Actor Performance Ranking")
        st.caption("Average IMDb ratings by lead actor")
        
        # Data prep for Chart 1: Group by actor and calculate mean rating
        actor_ratings = df_filtered.groupby('leadActor').agg(
            averageRating=('averageRating', 'mean'),
            totalFilms=('primaryTitle', 'count')
        ).reset_index()

        # Create the sorted horizontal bar chart
        bar_chart = alt.Chart(actor_ratings).mark_bar().encode(
            y=alt.Y('leadActor:N', sort='-x', title="Lead Actor"),
            x=alt.X('averageRating:Q', title="Average IMDb Rating", scale=alt.Scale(domain=[0, 10])),
            color=alt.Color('averageRating:Q', scale=alt.Scale(range=[ACCENT_ORANGE, ACCENT_BLUE]), legend=None),
            tooltip=[
                alt.Tooltip('leadActor', title="Actor"),
                alt.Tooltip('averageRating', title="Avg. Rating", format=".2f"),
                alt.Tooltip('totalFilms', title="Film Count")
            ]
        ).properties(height=300)

        st.altair_chart(bar_chart, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Chart 2: Rating Trend Over Time
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("#### Rating Trend Over Time")
        st.caption("Film ratings evolution across decades")
        
        # Define a common selection for interaction
        actor_selection = alt.selection_point(fields=['leadActor'], bind='legend')

        line_chart = alt.Chart(df_filtered).mark_point(filled=True, size=60).encode(
            x=alt.X('releaseYear:O', title="Release Year"),
            y=alt.Y('averageRating:Q', title="IMDb Rating", scale=alt.Scale(domain=[5, 10])),
            color=alt.Color('leadActor:N', title="Actor"),
            opacity=alt.condition(actor_selection, alt.value(0.9), alt.value(0.2)),
            tooltip=['primaryTitle', 'releaseYear', alt.Tooltip('averageRating', format=".2f"), 'leadActor']
        ).add_params(
            actor_selection
        ).properties(height=300)
        
        # Add a global trend line
        trend_line = alt.Chart(df_filtered).transform_regression('releaseYear', 'averageRating').mark_line(color=ACCENT_RED, size=2).encode()
        
        st.altair_chart(line_chart + trend_line, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # === NEW CHART: BOND VS OTHER FILMS COMPARISON ===
        st.markdown("<h2 class='section-header'>Bond Film Comparison</h2>", unsafe_allow_html=True)
        
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("#### Select a Bond Film to Compare Against Other Thriller Films")
        
        # Get list of Bond films for dropdown
        bond_films = df_full[df_full['is_bond_core']].sort_values('releaseYear', ascending=False)
        bond_film_options = bond_films['primaryTitle'].unique().tolist()
        
        # Dropdown to select a Bond film
        selected_bond_film = st.selectbox(
            "Choose a James Bond film:",
            bond_film_options,
            index=0
        )
        
        st.caption(f"**{selected_bond_film}** compared to other Thriller films")
        
        # Filter for Thriller films only
        df_comparison = df_full[df_full['Thriller'] == 1].copy()
        
        # Create film type column
        df_comparison['film_type'] = df_comparison['primaryTitle'].apply(
            lambda x: selected_bond_film if x == selected_bond_film else 'Other Thriller Films'
        )
        
        # Create scatter plot with selected film highlighted
        comparison_scatter = alt.Chart(df_comparison).mark_circle(size=100, opacity=0.8).encode(
            x=alt.X('numVotes:Q', title="Number of Votes", scale=alt.Scale(type='log')),
            y=alt.Y('averageRating:Q', title="IMDb Rating", scale=alt.Scale(domain=[4, 10])),
            color=alt.Color('film_type:N', 
                scale=alt.Scale(
                    domain=[selected_bond_film, 'Other Thriller Films'],
                    range=['#E45756', '#4A90E2']  # Red for selected Bond film, Blue for others
                ),
                legend=alt.Legend(title="Film Type")
            ),
            tooltip=[
                'primaryTitle',
                'leadActor',
                alt.Tooltip('averageRating', title="Rating", format=".2f"),
                alt.Tooltip('numVotes', title="Votes", format=","),
                'releaseYear'
            ]
        ).properties(
            height=400, 
            title=f"{selected_bond_film} Compared to Other Thriller Films"
        ).interactive()
        
        # Add reference lines for the selected film
        selected_film_data = df_comparison[df_comparison['primaryTitle'] == selected_bond_film]
        
        # Calculate average rating of all action/thriller films
        avg_rating = df_comparison['averageRating'].mean()
        
        if not selected_film_data.empty:
            selected_rating = selected_film_data.iloc[0]['averageRating']
            selected_votes = selected_film_data.iloc[0]['numVotes']
            
            # Horizontal reference line for selected film
            h_line = alt.Chart(pd.DataFrame({'y': [selected_rating]})).mark_rule(
                color='#E45756', 
                strokeDash=[5, 5],
                size=1
            ).encode(y='y:Q')
            
            # Vertical reference line for selected film
            v_line = alt.Chart(pd.DataFrame({'x': [selected_votes]})).mark_rule(
                color='#E45756', 
                strokeDash=[5, 5],
                size=1
            ).encode(x='x:Q')
            
            # Average rating line (horizontal)
            avg_line = alt.Chart(pd.DataFrame({'avg': [avg_rating]})).mark_rule(
                color=ACCENT_GOLD, 
                strokeDash=[3, 3],
                size=2
            ).encode(
                y='avg:Q'
            )
            
            # Add text annotation for average line
            avg_text = alt.Chart(pd.DataFrame({
                'x': [df_comparison['numVotes'].max() * 0.8],
                'y': [avg_rating],
                'text': [f'Avg Rating: {avg_rating:.2f}']
            })).mark_text(
                align='right',
                baseline='bottom',
                dx=-5,
                dy=-5,
                color=ACCENT_GOLD,
                fontSize=12,
                fontWeight='bold'
            ).encode(
                x='x:Q',
                y='y:Q',
                text='text:N'
            )
            
            final_chart = comparison_scatter + h_line + v_line + avg_line + avg_text
        else:
            # Just show average line if selected film not found
            avg_line = alt.Chart(pd.DataFrame({'avg': [avg_rating]})).mark_rule(
                color=ACCENT_GOLD, 
                strokeDash=[3, 3],
                size=2
            ).encode(y='avg:Q')
            
            final_chart = comparison_scatter + avg_line
        
        st.altair_chart(final_chart, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # === SECTION 2: CONTENT ANALYSIS ===
        st.markdown("<h2 class='section-header'>Content & Genre Analysis</h2>", unsafe_allow_html=True)
        
        # Chart 3: Runtime vs Rating
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("#### Runtime vs Rating Analysis")
        st.caption("Relationship between film length, rating, and popularity")
        
        # Professional 4-variable scatter plot
        scatter_chart = alt.Chart(df_filtered).mark_circle().encode(
            x=alt.X('runtimeMinutes:Q', title="Runtime (Minutes)"),
            y=alt.Y('averageRating:Q', title="IMDb Rating", scale=alt.Scale(domain=[5, 10])),
            size=alt.Size('numVotes:Q', title="Popularity", scale=alt.Scale(range=[50, 800])),
            color=alt.Color('leadActor:N', title="Actor"),
            tooltip=[
                'primaryTitle', 'leadActor', 
                alt.Tooltip('runtimeMinutes', title="Runtime (mins)"), 
                alt.Tooltip('averageRating', title="Rating", format=".2f"), 
                alt.Tooltip('numVotes', title="Votes", format=",")
            ]
        ).properties(height=300).interactive()

        st.altair_chart(scatter_chart, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Chart 4: Genre Evolution
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("#### Genre Evolution by Decade")
        st.caption("Genre distribution across different time periods")
        
        # Prepare Genre data
        genre_cols = ['Action', 'Adventure', 'Thriller', 'Romance', 'Sci-Fi', 'Comedy', 'Drama']
        df_genres = df_filtered.groupby('decade')[genre_cols].sum().reset_index()
        
        # Melt the DataFrame for Altair stacking
        df_genres_melted = df_genres.melt('decade', value_vars=genre_cols, var_name='Genre', value_name='Count')
        df_genres_melted = df_genres_melted[df_genres_melted['Count'] > 0]
        
        genre_chart = alt.Chart(df_genres_melted).mark_bar().encode(
            x=alt.X('decade:O', title="Decade", axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Count:Q', title="Genre Count"),
            color=alt.Color('Genre:N', title="Genre"),
            order=alt.Order('decade:O'),
            tooltip=['decade', 'Genre', 'Count']
        ).properties(height=300).interactive()

        st.altair_chart(genre_chart, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Chart 4b: Genre Popularity Trend Over Time (Area Chart)
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("#### Genre Popularity Trend Over Time")
        st.caption("Film count by genre across decades - showing popularity shifts")
        
        # Use the already prepared melted data
        if not df_genres_melted.empty:
            # Create area chart for better visibility
            area_chart = alt.Chart(df_genres_melted).mark_area(
                opacity=0.7,
                interpolate='monotone'
            ).encode(
                x=alt.X('decade:O', title="Decade", axis=alt.Axis(labelAngle=0)),
                y=alt.Y('Count:Q', title="Number of Films", stack='zero'),
                color=alt.Color('Genre:N', title="Genre"),
                tooltip=[
                    alt.Tooltip('decade:O', title='Decade'),
                    alt.Tooltip('Genre:N', title='Genre'),
                    alt.Tooltip('Count:Q', title='Films')
                ]
            ).properties(height=350, title="Genre Popularity: Stacked Area View")
            
            st.altair_chart(area_chart, use_container_width=True)
        else:
            st.info("Not enough data to show genre trends")
        
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # === SECTION 3: DISTRIBUTION METRICS ===
        st.markdown("<h2 class='section-header'>Distribution & Production Metrics</h2>", unsafe_allow_html=True)
        
        # Chart 5: Rating Distribution
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("#### Rating Distribution by Actor")
        st.caption("Individual film ratings showing distribution patterns")
        
        # Jitter/Strip Plot for rating distribution
        strip_chart = alt.Chart(df_filtered).mark_circle(size=70, opacity=0.7).encode(
            x=alt.X('averageRating:Q', title="IMDb Rating", scale=alt.Scale(domain=[5, 10])),
            y=alt.Y('leadActor:N', title="Lead Actor"),
            color=alt.Color('leadActor:N', legend=None),
            tooltip=['primaryTitle', 'leadActor', alt.Tooltip('averageRating', title="Rating", format=".2f")]
        ).properties(height=300).interactive() 

        # Add mean line overlay
        mean_line = alt.Chart(df_filtered).mark_rule(color=ACCENT_RED, size=2).encode(
            x='mean(averageRating):Q',
            y='leadActor:N'
        )

        st.altair_chart(strip_chart + mean_line, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Chart 6: Production Volume
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("#### Production Volume by Decade")
        st.caption("Number of films produced in each decade")
        
        # Bar chart showing production volume
        decade_data = df_filtered.groupby('decade').size().reset_index(name='count')
        
        decade_chart = alt.Chart(decade_data).mark_bar().encode(
            x=alt.X('decade:O', title="Decade", axis=alt.Axis(labelAngle=0)),
            y=alt.Y('count:Q', title="Number of Films"),
            color=alt.Color('count:Q', scale=alt.Scale(range=[ACCENT_ORANGE, ACCENT_BLUE]), legend=None),
            tooltip=[alt.Tooltip('decade:O', title='Decade'), alt.Tooltip('count:Q', title='Films')]
        ).properties(height=300)

        st.altair_chart(decade_chart, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # === SECTION 4: ADVANCED ANALYTICS ===
        st.markdown("<h2 class='section-header'>Advanced Analytics</h2>", unsafe_allow_html=True)
        
        # Chart 7: Performance Heatmap
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("#### Performance Heatmap: Actor × Decade")
        st.caption("Average ratings across different time periods")
        
        # Create heatmap data
        heatmap_data = df_filtered.groupby(['leadActor', 'decade']).agg(
            avg_rating=('averageRating', 'mean'),
            film_count=('primaryTitle', 'count')
        ).reset_index()
        
        heatmap_data = heatmap_data[heatmap_data['film_count'] > 0]
        
        heatmap = alt.Chart(heatmap_data).mark_rect().encode(
            x=alt.X('decade:O', title="Decade"),
            y=alt.Y('leadActor:N', title="Actor"),
            color=alt.Color('avg_rating:Q', 
                scale=alt.Scale(scheme='blues', domain=[5, 9]),
                title="Avg Rating"
            ),
            tooltip=[
                alt.Tooltip('leadActor:N', title='Actor'),
                alt.Tooltip('decade:O', title='Decade'),
                alt.Tooltip('avg_rating:Q', title='Avg Rating', format='.2f'),
                alt.Tooltip('film_count:Q', title='Films')
            ]
        ).properties(height=300)

        st.altair_chart(heatmap, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Chart 8: Audience Engagement
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("#### Audience Engagement Distribution")
        st.caption("Vote distribution showing audience reach")
        
        # Create box plot with better styling
        box_plot = alt.Chart(df_filtered).mark_boxplot(
            size=50,
            color=ACCENT_BLUE,
            opacity=0.7,
            median={'color': ACCENT_GOLD, 'size': 3},
            outliers={'color': ACCENT_RED, 'size': 30, 'opacity': 0.6}
        ).encode(
            x=alt.X('leadActor:N', title="Actor", axis=alt.Axis(labelAngle=0, labelFontSize=11)),
            y=alt.Y('numVotes:Q', 
                title="Number of Votes (Log Scale)", 
                scale=alt.Scale(type='log'),
                axis=alt.Axis(tickCount=5)
            ),
            tooltip=['leadActor:N', alt.Tooltip('numVotes:Q', format=',')]
        ).properties(height=350)

        st.altair_chart(box_plot, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # === SECTION 5: DETAILED BREAKDOWN ===
        st.markdown("<h2 class='section-header'>Detailed Film Analysis</h2>", unsafe_allow_html=True)
        
        # Chart 9: Film Timeline
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("#### Complete Film Timeline")
        st.caption("Chronological view with rating bands and popularity indicators")
        
        # Create timeline chart
        df_timeline = df_filtered.copy()
        df_timeline['rating_band'] = pd.cut(
            df_timeline['averageRating'], 
            bins=[0, 6, 7, 8, 10], 
            labels=['Below 6', '6-7', '7-8', '8+']
        )
        
        timeline = alt.Chart(df_timeline).mark_circle(size=100).encode(
            x=alt.X('releaseYear:O', title="Release Year"),
            y=alt.Y('leadActor:N', title="Actor"),
            color=alt.Color('rating_band:N', 
                scale=alt.Scale(
                    domain=['Below 6', '6-7', '7-8', '8+'],
                    range=[ACCENT_RED, ACCENT_ORANGE, ACCENT_GREEN, ACCENT_BLUE]
                ),
                title="Rating Band"
            ),
            size=alt.Size('numVotes:Q', scale=alt.Scale(range=[50, 500]), title="Popularity"),
            tooltip=[
                'primaryTitle', 'leadActor', 'releaseYear',
                alt.Tooltip('averageRating:Q', format='.2f'),
                alt.Tooltip('numVotes:Q', format=',')
            ]
        ).properties(height=350)

        st.altair_chart(timeline, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # --- FOOTER ---
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='footer'>Data Source: IMDb via data_final_lead_actor.csv</div>", unsafe_allow_html=True)


# ==============================================================================
# === PAGE 2: STORY MODE (Guided Narrative) ====================================
# ==============================================================================
# ==============================================================================
# === PAGE 3: ACROSS THE 007 VERSE ============================================
# ==============================================================================

def render_best_bond_section(df_full, EON_BOND_ACTORS):
    st.markdown("<h1>Across the 007 Verse</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Comparative Actor Analysis</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("""
    Fans often debate over who's the best **James Bond** — Daniel Craig, George Lazenby, Pierce Brosnan, Roger Moore, Sean Connery, or Timothy Dalton.  
    Within this data story, you have the opportunity to compare their works over the years (1980 onwards).
    """)

    # --- ACTOR SELECTION ---
    selected_actor = st.selectbox("Select a Bond actor:", EON_BOND_ACTORS, index=5)  # Default: Daniel Craig

    # Filter dataset for the chosen actor (ALL films, not just post-1980)
    df_actor = df_full[df_full['leadActor'] == selected_actor].copy()

    if df_actor.empty:
        st.warning(f"No films found for {selected_actor}.")
        return

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- CHART 1: GENRE DONUT CHART ---
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown(f"#### Genre Distribution: {selected_actor}")
    st.caption("Genre breakdown for selected actor's filmography")
    genre_cols = ['Action', 'Adventure', 'Thriller', 'Romance', 'Comedy', 'Drama', 'Sci-Fi']
    df_genre = df_actor[genre_cols].sum().reset_index()
    df_genre.columns = ['Genre', 'Count']
    df_genre = df_genre[df_genre['Count'] > 0]

    # Create the donut chart
    donut_chart = (
        alt.Chart(df_genre)
        .mark_arc(innerRadius=80, outerRadius=140)
        .encode(
            theta=alt.Theta('Count:Q'),
            color=alt.Color('Genre:N', title='Genre'),
            tooltip=['Genre', 'Count']
        )
    )
    
    # Add text in the center - properly centered
    center_text = (
        alt.Chart(pd.DataFrame({'text': [selected_actor]}))
        .mark_text(
            size=22, 
            fontWeight='bold', 
            color=ACCENT_GOLD,
            align='center',
            baseline='middle'
        )
        .encode(text='text:N')
    )
    
    # Combine the charts
    final_chart = alt.layer(donut_chart, center_text).properties(
        height=400, 
        width=400,
        title=f"{selected_actor}'s Genre Distribution"
    ).configure_view(strokeWidth=0)

    # Center the chart
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.altair_chart(final_chart, use_container_width=False)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- CHART 2: SCATTER PLOT (Ratings over Years) ---
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown(f"#### Rating Evolution: {selected_actor}")
    
    # Count Bond vs non-Bond films
    bond_count = df_actor[df_actor['is_bond_core']].shape[0]
    other_count = df_actor[~df_actor['is_bond_core']].shape[0]
    
    st.caption(f"Showing {bond_count} Bond films and {other_count} other films where {selected_actor} is the lead actor")
    
    # Calculate average rating for the actor
    avg_actor_rating = df_actor['averageRating'].mean()
    
    # Add column to indicate if it's a Bond film
    df_actor_viz = df_actor.copy()
    df_actor_viz['film_type'] = df_actor_viz['is_bond_core'].apply(
        lambda x: 'James Bond Films' if x else 'Other Films'
    )
    
    # Create scatter chart with Bond films highlighted
    scatter_chart = (
        alt.Chart(df_actor_viz)
        .mark_circle(size=120, opacity=0.8)
        .encode(
            x=alt.X('releaseYear:O', title="Release Year"),
            y=alt.Y('averageRating:Q', title="IMDb Rating", scale=alt.Scale(domain=[3, 10])),
            color=alt.Color('film_type:N',
                scale=alt.Scale(
                    domain=['James Bond Films', 'Other Films'],
                    range=['#E45756', '#4A90E2']  # Pink for Bond, Blue for others
                ),
                legend=alt.Legend(title="Film Type")
            ),
            tooltip=['primaryTitle', 'releaseYear', alt.Tooltip('averageRating', format=".2f"), 'film_type']
        )
        .properties(height=350)
    )
    
    # Add average rating line
    avg_line = alt.Chart(pd.DataFrame({'avg': [avg_actor_rating]})).mark_rule(
        color=ACCENT_GOLD,
        strokeDash=[5, 5],
        size=2
    ).encode(y='avg:Q')
    
    # Add text annotation for average
    avg_text = alt.Chart(pd.DataFrame({
        'x': [df_actor['releaseYear'].max()],
        'y': [avg_actor_rating],
        'text': [f'Avg: {avg_actor_rating:.2f}']
    })).mark_text(
        align='right',
        baseline='bottom',
        dx=-5,
        dy=-5,
        color=ACCENT_GOLD,
        fontSize=12,
        fontWeight='bold'
    ).encode(
        x='x:O',
        y='y:Q',
        text='text:N'
    )
    
    # Combine charts
    final_evolution_chart = scatter_chart + avg_line + avg_text

    st.altair_chart(final_evolution_chart, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- CHART 3: BEST TO WORST MOVIES (Color-Encoded Ratings) ---
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown(f"#### Film Rankings: {selected_actor}")
    st.caption("Films ranked by IMDb rating")

    # Sort by rating
    df_sorted = df_actor.sort_values(by='averageRating', ascending=False).copy()

    # Add combined label
    df_sorted['Film (Year)'] = df_sorted['primaryTitle'] + " (" + df_sorted['releaseYear'].astype(str) + ")"

    rating_chart = (
        alt.Chart(df_sorted)
        .mark_bar()
        .encode(
            y=alt.Y('Film (Year):N', sort='-x', title=None, axis=alt.Axis(labelLimit=300)),
            x=alt.X('averageRating:Q', title="IMDb Rating"),
            color=alt.Color(
                'averageRating:Q',
                scale=alt.Scale(domain=[5, 10], range=[ACCENT_ORANGE, ACCENT_BLUE]),
                legend=None
            ),
            tooltip=['primaryTitle', 'releaseYear', alt.Tooltip('averageRating', format=".2f")]
        )
        .properties(height=400)
    )

    st.altair_chart(rating_chart, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_story_mode(df_full, EON_BOND_ACTORS):
    st.markdown("<h1>The Evolution of Espionage</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>A data-driven narrative through the James Bond franchise</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    df_story = df_full[df_full['is_bond_core']].copy()

    # --- NARRATIVE STEP 1: The Golden Age of Connery ---
    st.header("Chapter 1: The Original Blueprint (1960s)")
    st.markdown("""
    The Connery era set the gold standard. His films established the core DNA of the franchise: high-stakes **Adventure** mixed with **Thriller** elements. 
    Notice how the average runtime was relatively shorter and the ratings were consistently high, defining the early, successful formula.
    """)
    
    # Filter data for Connery only
    df_connery = df_story[df_story['leadActor'].isin(['Sean Connery', 'George Lazenby'])]
    
    story_chart_1 = alt.Chart(df_connery).mark_circle(size=150, color=ACCENT_BLUE, opacity=0.8).encode(
        x=alt.X('releaseYear:O', title="Release Year"),
        y=alt.Y('averageRating:Q', title="IMDb Rating"),
        size=alt.Size('runtimeMinutes:Q', title="Runtime (Mins)"),
        color=alt.Color('leadActor:N', title="Actor"),
        tooltip=['primaryTitle', 'releaseYear', alt.Tooltip('averageRating', format=".2f"), 'runtimeMinutes', 'leadActor']
    ).properties(
        title="Connery & Lazenby: Defining the Rating and Runtime Benchmark"
    )
    st.altair_chart(story_chart_1, use_container_width=True)
    st.markdown("---")


    # --- NARRATIVE STEP 2: The Action-Comedy Shift of Moore/Brosnan ---
    st.header("Chapter 2: The Camp and the Polish (1970s - 2000s)")
    st.markdown(f"""
    The **Roger Moore** era (1973-1985) introduced campier, more Sci-Fi elements (see *Moonraker*), leading to increased variability in critical ratings. 
    **Pierce Brosnan** (1995-2002) then brought a polished, gadget-heavy approach. This period saw a dramatic rise in the **Action** and **Thriller** count, preparing the franchise for the grittier modern era.
    """)
    
    # Prepare genre data for this era (1970 - 2000)
    df_genre_shift = df_story[(df_story['decade'] >= 1970) & (df_story['decade'] <= 2000)].copy()
    genre_cols = ['Action', 'Adventure', 'Thriller', 'Romance', 'Comedy', 'Sci-Fi']
    df_genres = df_genre_shift.groupby('decade')[genre_cols].sum().reset_index()
    df_genres_melted = df_genres.melt('decade', value_vars=genre_cols, var_name='Genre', value_name='Count')

    story_chart_2 = alt.Chart(df_genres_melted).mark_bar(opacity=0.9).encode(
        x=alt.X('decade:O', title="Decade"),
        y=alt.Y('Count:Q', title="Total Genre Tags per Decade"),
        color=alt.Color('Genre:N', scale=alt.Scale(range=[ACCENT_RED, ACCENT_GOLD, '#AAAAAA', '#ADD8E6', '#7CFC00', '#FFA07A']), title="Genre Focus"),
        order=alt.Order('decade:O'),
        tooltip=['decade', 'Genre', 'Count']
    ).properties(
        title="Genre Emphasis: From Adventure to Action/Thriller"
    ).interactive() # FIXED: Removed invalid 'axis='x'' argument.
    st.altair_chart(story_chart_2, use_container_width=True)
    st.markdown("---")


    # --- NARRATIVE STEP 3: The Craig Reboot ---
    st.header("Chapter 3: The Gritty Modern Agent (Daniel Craig)")
    st.markdown("""
    The **Daniel Craig** era (2006-2021) completely rebooted the narrative, focusing on raw **Thriller** and **Drama** with high budgets and often longer runtimes. The audience response has been highly favorable (high ratings and vote counts). The shift is clearly visible in the data: the latest films maintain high quality but push the boundaries of film length and production scale.
    """)

    # Filter data for Daniel Craig only
    df_craig = df_story[df_story['leadActor'] == 'Daniel Craig']

    story_chart_3 = alt.Chart(df_craig).mark_bar(color=ACCENT_RED).encode(
        x=alt.X('primaryTitle:N', sort='-y', title="Film Title", axis=alt.Axis(labelAngle=0)),
        y=alt.Y('numVotes:Q', title="Total Audience Votes"),
        tooltip=['primaryTitle', alt.Tooltip('numVotes', format=",")]
    ).properties(
        title="Daniel Craig Era: Audience Volume and Popularity"
    )
    st.altair_chart(story_chart_3, use_container_width=True)
    
    # --- FOOTER ---
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: #555555; font-size: 0.8em;'>
        Data Source: data_final_lead_actor.csv | View: 007 Story Mode
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# === MAIN APP LOGIC ===========================================================
# ==============================================================================

if page_mode == 'Interactive Dashboard':
    render_dashboard(df_full, EON_BOND_ACTORS)
elif page_mode == '007 Story Mode':
    render_story_mode(df_full, EON_BOND_ACTORS)
else:
    render_best_bond_section(df_full, EON_BOND_ACTORS)
