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

# Thematic Colors
BACKGROUND_COLOR = '#0e1117' # Dark Streamlit background
ACCENT_GOLD = '#FFD700'     # Gold for primary focus/luxury
ACCENT_CRIMSON = '#B22222'  # Crimson for action/danger
TEXT_COLOR = 'white'

# Define the set of Canonical Eon Bond Actors (for the core subset)
EON_BOND_ACTORS = ['Sean Connery', 'George Lazenby', 'Roger Moore', 'Timothy Dalton', 'Pierce Brosnan', 'Daniel Craig']

# --- ALTAIR THEME STYLING ---
def get_bond_theme():
    # Defines the dark, elegant style for all charts
    return {
        "config": {
            "title": {"color": ACCENT_GOLD, "fontSize": 18, "font": "sans-serif", "anchor": "middle"},
            "view": {"stroke": "transparent", "fill": BACKGROUND_COLOR},
            "background": BACKGROUND_COLOR,
            "style": {
                "guide-label": {"fill": TEXT_COLOR},
                "guide-title": {"fill": TEXT_COLOR, "fontWeight": "bold"},
                "group-title": {"fill": TEXT_COLOR},
            },
            "axis": {
                "domainColor": "#444444", 
                "gridColor": "#303030", 
                "labelColor": TEXT_COLOR,
                "titleColor": TEXT_COLOR,
                "titleFontWeight": "bold",
            },
            "legend": {
                "titleColor": TEXT_COLOR, 
                "labelColor": TEXT_COLOR
            },
            "range": {
                # Ensure consistency in color usage
                "category": [ACCENT_GOLD, ACCENT_CRIMSON, '#AAAAAA', '#7CFC00', '#ADD8E6', '#FFA07A'] 
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
data_file = BASE_DIR.parent / 'data' / 'processed' / 'data_final_lead_actor.csv'

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
    st.markdown("A deep dive into the James Bond franchise and lead actor performance across cinematic history.")
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


    # --- KEY METRICS ---
    col1, col2, col3, col4 = st.columns(4)

    total_films = len(df_filtered)
    avg_rating = df_filtered['averageRating'].mean() if total_films > 0 else 0
    avg_runtime = df_filtered['runtimeMinutes'].mean() if total_films > 0 else 0
    highest_voted_film = df_filtered.sort_values(by='numVotes', ascending=False).iloc[0] if total_films > 0 else {'primaryTitle': 'N/A', 'numVotes': 0}

    with col1:
        st.metric("Total Missions (Films)", f"{total_films}")
    with col2:
        st.metric("Avg. Critical Rating (IMDb)", f"{avg_rating:.2f}")
    with col3:
        st.metric("Avg. Mission Duration (Mins)", f"{avg_runtime:.0f} mins")
    with col4:
        st.metric("Top Voted Mission", f"{highest_voted_film['primaryTitle']}")

    st.markdown("---")

    # Only render charts if there is data
    if total_films > 0:

        # --- VISUALIZATIONS (6 Charts) ---

        # --- Row 1: Comparison & Evolution ---
        row1_col1, row1_col2 = st.columns(2)

        with row1_col1:
            st.subheader("Chart 1: Actor Performance Ranking (Avg. Rating)")
            
            # Data prep for Chart 1: Group by actor and calculate mean rating
            actor_ratings = df_filtered.groupby('leadActor').agg(
                averageRating=('averageRating', 'mean'),
                totalFilms=('primaryTitle', 'count')
            ).reset_index()

            # Create the sorted horizontal bar chart
            bar_chart = alt.Chart(actor_ratings).mark_bar().encode(
                y=alt.Y('leadActor:N', sort='-x', title="Lead Actor"),
                x=alt.X('averageRating:Q', title="Average IMDb Rating"),
                color=alt.Color('averageRating', scale=alt.Scale(range=[ACCENT_CRIMSON, ACCENT_GOLD]), legend=None),
                tooltip=[
                    alt.Tooltip('leadActor', title="Actor"),
                    alt.Tooltip('averageRating', title="Avg. Rating", format=".2f"),
                    alt.Tooltip('totalFilms', title="Film Count")
                ]
            ).properties(height=300)

            st.altair_chart(bar_chart, use_container_width=True)

        with row1_col2:
            st.subheader("Chart 2: Rating Trend Over Time (Film Evolution)")
            
            # Define a common selection for interaction
            actor_selection = alt.selection_point(fields=['leadActor'], bind='legend')

            line_chart = alt.Chart(df_filtered).mark_point(filled=True, size=60).encode(
                x=alt.X('releaseYear:O', title="Release Year"),
                y=alt.Y('averageRating:Q', title="IMDb Rating"),
                color=alt.Color('leadActor:N', title="Actor"),
                opacity=alt.condition(actor_selection, alt.value(0.9), alt.value(0.2)),
                tooltip=['primaryTitle', 'releaseYear', alt.Tooltip('averageRating', format=".2f"), 'leadActor']
            ).add_params(
                actor_selection
            ).properties(height=300)
            
            # Add a global trend line (if enough data points exist)
            trend_line = alt.Chart(df_filtered).transform_regression('releaseYear', 'averageRating').mark_line(color=ACCENT_CRIMSON, size=2).encode()
            
            st.altair_chart(line_chart + trend_line, use_container_width=True)

        st.markdown("---")

        # --- Row 2: Runtime, Votes, and Genre Analysis ---
        row2_col1, row2_col2 = st.columns(2)

        with row2_col1:
            st.subheader("Chart 3: Runtime, Rating, and Popularity (4-Variable Scatter)")
            
            # Professional 4-variable scatter plot: X=Runtime, Y=Rating, Color=Actor, Size=Votes
            scatter_chart = alt.Chart(df_filtered).mark_circle().encode(
                x=alt.X('runtimeMinutes:Q', title="Mission Duration (Runtime Mins)"),
                y=alt.Y('averageRating:Q', title="IMDb Rating"),
                size=alt.Size('numVotes:Q', title="Audience Popularity (Num Votes)", scale=alt.Scale(range=[50, 800])),
                color=alt.Color('leadActor:N', title="Actor"),
                tooltip=[
                    'primaryTitle', 'leadActor', 
                    alt.Tooltip('runtimeMinutes', title="Runtime (mins)"), 
                    alt.Tooltip('averageRating', title="Rating", format=".2f"), 
                    alt.Tooltip('numVotes', title="Votes", format=",")
                ]
            ).properties(title="Runtime vs. Rating (Size by Votes)").interactive() # Add zooming/panning (default)

            st.altair_chart(scatter_chart, use_container_width=True)

        with row2_col2:
            st.subheader("Chart 4: Genre Intensity by Decade (Stacked Bar)")
            
            # Prepare Genre data: sum of 0/1 columns
            genre_cols = ['Action', 'Adventure', 'Thriller', 'Romance', 'Sci-Fi', 'Comedy', 'Drama']
            df_genres = df_filtered.groupby('decade')[genre_cols].sum().reset_index()
            
            # Melt the DataFrame for Altair stacking
            df_genres_melted = df_genres.melt('decade', value_vars=genre_cols, var_name='Genre', value_name='Count')

            # Remove decades with zero films after filtering
            df_genres_melted = df_genres_melted[df_genres_melted['Count'] > 0]
            
            genre_chart = alt.Chart(df_genres_melted).mark_bar().encode(
                x=alt.X('decade:O', title="Decade", axis=alt.Axis(labelAngle=-45)),
                y=alt.Y('Count:Q', title="Total Genre Focus (Count)"),
                color=alt.Color('Genre:N', title="Genre Focus"),
                order=alt.Order('decade:O'),
                tooltip=['decade', 'Genre', 'Count']
            ).properties(title="Cinematic Focus Over Time").interactive()

            st.altair_chart(genre_chart, use_container_width=True)

        st.markdown("---")

        # --- Row 3: Distribution and Decadal Count ---
        row3_col1, row3_col2 = st.columns(2)

        with row3_col1:
            st.subheader("Chart 5: Film Rating Distribution (Per Actor Jitter Plot)")
            
            # New Chart 5: Jitter/Strip Plot for detailed distribution of individual film ratings
            strip_chart = alt.Chart(df_filtered).mark_circle(size=70, opacity=0.8).encode(
                x=alt.X('averageRating:Q', title="IMDb Rating"),
                y=alt.Y('leadActor:N', title="Lead Actor"),
                color=alt.Color('leadActor:N', legend=None),
                tooltip=['primaryTitle', 'leadActor', alt.Tooltip('averageRating', title="Rating", format=".2f")]
            ).properties(height=300).interactive() 

            # Add a mean line overlay for clear comparison (Average Rating by Actor)
            mean_line = alt.Chart(df_filtered).mark_rule(color=ACCENT_GOLD, size=2).encode(
                x='mean(averageRating):Q',
                y='leadActor:N'
            )

            st.altair_chart(strip_chart + mean_line, use_container_width=True)


        with row3_col2:
            st.subheader("Chart 6: Decadal Film Production Count")
            
            # Bar chart showing count of films per decade
            decade_chart = alt.Chart(df_filtered).mark_bar(color=ACCENT_GOLD).encode(
                x=alt.X('decade:O', title="Decade", axis=alt.Axis(labelAngle=-45)),
                y=alt.Y('count():Q', title="Number of Films Produced"),
                tooltip=['decade', 'count()']
            ).properties(height=300)

            st.altair_chart(decade_chart, use_container_width=True)
    
    # --- FOOTER ---
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: #555555; font-size: 0.8em;'>
        Data Source: data_final_lead_actor.csv | View: Interactive Dashboard
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# === PAGE 2: STORY MODE (Guided Narrative) ====================================
# ==============================================================================
# ==============================================================================
# === PAGE 3: ACROSS THE 007 VERSE ============================================
# ==============================================================================

def render_best_bond_section(df_full, EON_BOND_ACTORS):
    st.title("Across the 007 Verse")
    st.subheader("Who's the Best Bond?")
    st.markdown("""
    Fans often debate over who's the best **James Bond** — Daniel Craig, George Lazenby, Pierce Brosnan, Roger Moore, Sean Connery, or Timothy Dalton.  
    Within this data story, you have the opportunity to compare their works over the years (1980 onwards).
    """)

    # --- ACTOR SELECTION ---
    selected_actor = st.selectbox("Select a Bond actor:", EON_BOND_ACTORS, index=5)  # Default: Daniel Craig

    # Filter dataset for the chosen actor (post-1980 only)
    df_actor = df_full[(df_full['leadActor'] == selected_actor) & (df_full['releaseYear'] >= 1980)].copy()

    if df_actor.empty:
        st.warning(f"No films found for {selected_actor} after 1980.")
        return

    st.markdown("---")

    # --- CHART 1: GENRE DONUT CHART ---
    st.subheader(f"🎬 Genre Breakdown for {selected_actor}")
    genre_cols = ['Action', 'Adventure', 'Thriller', 'Romance', 'Comedy', 'Drama', 'Sci-Fi']
    df_genre = df_actor[genre_cols].sum().reset_index()
    df_genre.columns = ['Genre', 'Count']
    df_genre = df_genre[df_genre['Count'] > 0]

    donut_chart = (
        alt.Chart(df_genre)
        .mark_arc(innerRadius=80)
        .encode(
            theta=alt.Theta('Count:Q'),
            color=alt.Color('Genre:N', title='Genre'),
            tooltip=['Genre', 'Count']
        )
        .properties(height=350, title=f"{selected_actor}'s Genre Mix")
    )

    st.altair_chart(donut_chart, use_container_width=True)

    # Add the actor name overlay in center (Streamlit markdown hack)
    st.markdown(
        f"<div style='position:relative; top:-280px; text-align:center; font-size:1.5em; color:{ACCENT_GOLD}; font-weight:bold;'>{selected_actor}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # --- CHART 2: SCATTER PLOT (Ratings over Years) ---
    st.subheader(f"📈 IMDb Ratings of {selected_actor}'s Films Over the Years")
    scatter_chart = (
        alt.Chart(df_actor)
        .mark_circle(size=120, opacity=0.8)
        .encode(
            x=alt.X('releaseYear:O', title="Release Year"),
            y=alt.Y('averageRating:Q', title="IMDb Rating"),
            color=alt.value(ACCENT_GOLD),
            tooltip=['primaryTitle', 'releaseYear', alt.Tooltip('averageRating', format=".2f")]
        )
        .properties(height=350, title=f"{selected_actor}: Rating Evolution")
    )

    st.altair_chart(scatter_chart, use_container_width=True)
    st.markdown("---")

    # --- CHART 3: BEST TO WORST MOVIES (Color-Encoded Ratings) ---
    st.subheader(f"🏆 Best to Worst Films of {selected_actor}")

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
                scale=alt.Scale(domain=[5, 10], range=['#B22222', '#FFD700']),
                legend=None
            ),
            tooltip=['primaryTitle', 'releaseYear', alt.Tooltip('averageRating', format=".2f")]
        )
        .properties(height=400, title=f"{selected_actor}'s Films Ranked by IMDb Rating")
    )

    st.altair_chart(rating_chart, use_container_width=True)

def render_story_mode(df_full, EON_BOND_ACTORS):
    st.title("007 Story Mode: The Evolution of Espionage")
    st.markdown("A guided journey through the data, revealing key cinematic shifts in the James Bond franchise.")
    st.markdown("---")

    df_story = df_full[df_full['is_bond_core']].copy()

    # --- NARRATIVE STEP 1: The Golden Age of Connery ---
    st.header("Chapter 1: The Original Blueprint (1960s)")
    st.markdown("""
    The Connery era set the gold standard. His films established the core DNA of the franchise: high-stakes **Adventure** mixed with **Thriller** elements. 
    Notice how the average runtime was relatively shorter and the ratings were consistently high, defining the early, successful formula.
    """)
    
    # Filter data for Connery only
    df_connery = df_story[df_story['leadActor'].isin(['Sean Connery', 'George Lazenby'])]
    
    story_chart_1 = alt.Chart(df_connery).mark_circle(size=150, color=ACCENT_GOLD, opacity=0.8).encode(
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
        color=alt.Color('Genre:N', scale=alt.Scale(range=[ACCENT_CRIMSON, ACCENT_GOLD, '#AAAAAA', '#ADD8E6', '#7CFC00', '#FFA07A']), title="Genre Focus"),
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

    story_chart_3 = alt.Chart(df_craig).mark_bar(color=ACCENT_CRIMSON).encode(
        x=alt.X('primaryTitle:N', sort='-y', title="Film Title", axis=alt.Axis(labelAngle=-45)),
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
