"""Chart generation functions for the dashboard."""

import altair as alt
import pandas as pd

try:
    from .config import (
        ACCENT_BLUE, ACCENT_ORANGE, ACCENT_RED, ACCENT_GOLD, 
        ACCENT_GREEN, GRID_COLOR
    )
except ImportError:
    from config import (
        ACCENT_BLUE, ACCENT_ORANGE, ACCENT_RED, ACCENT_GOLD, 
        ACCENT_GREEN, GRID_COLOR
    )


def filter_to_specific_bond_films(df):
    """Filter dataframe to only include the specific 14 Bond films."""
    # Define the specific Bond films to include (year and title keywords for matching)
    target_films = [
        (1981, 'for your eyes only', 'Roger Moore'),
        (1983, 'octopussy', 'Roger Moore'),
        (1985, 'view to a kill', 'Roger Moore'),
        (1987, 'living daylights', 'Timothy Dalton'),
        (1989, 'licence to kill', 'Timothy Dalton'),
        (1995, 'goldeneye', 'Pierce Brosnan'),
        (1997, 'tomorrow never dies', 'Pierce Brosnan'),
        (1999, 'world is not enough', 'Pierce Brosnan'),
        (2002, 'die another day', 'Pierce Brosnan'),
        (2006, 'casino royale', 'Daniel Craig'),
        (2008, 'quantum of solace', 'Daniel Craig'),
        (2012, 'skyfall', 'Daniel Craig'),
        (2015, 'spectre', 'Daniel Craig'),
        (2021, 'no time to die', 'Daniel Craig')
    ]
    
    # Filter to only the specific films
    filtered_films = []
    for year, title_keywords, actor in target_films:
        # Match by year and title keywords (case-insensitive)
        matches = df[
            (df['releaseYear'] == year) &
            (df['primaryTitle'].str.lower().str.contains(title_keywords, case=False, na=False))
        ]
        if not matches.empty:
            # If multiple matches, prefer the one with matching actor if available
            if actor in matches['leadActor'].values:
                matches = matches[matches['leadActor'] == actor]
            filtered_films.append(matches.iloc[0])
    
    if not filtered_films:
        return pd.DataFrame()
    
    # Convert to DataFrame
    return pd.DataFrame(filtered_films)


def create_actor_performance_chart(df_filtered):
    """Create actor performance ranking bar chart."""
    actor_ratings = df_filtered.groupby('leadActor').agg(
        averageRating=('averageRating', 'mean'),
        totalFilms=('primaryTitle', 'count')
    ).reset_index()

    chart = alt.Chart(actor_ratings).mark_bar().encode(
        y=alt.Y('leadActor:N', sort='-x', title="Lead Actor"),
        x=alt.X('averageRating:Q', title="Average IMDb Rating", scale=alt.Scale(domain=[0, 10])),
        color=alt.Color('averageRating:Q', scale=alt.Scale(range=[ACCENT_ORANGE, ACCENT_BLUE]), legend=None),
        tooltip=[
            alt.Tooltip('leadActor', title="Actor"),
            alt.Tooltip('averageRating', title="Avg. Rating", format=".2f"),
            alt.Tooltip('totalFilms', title="Film Count")
        ]
    ).properties(height=300)
    
    return chart


def create_rating_trend_chart(df_filtered):
    """Create rating trend over time chart."""
    actor_selection = alt.selection_point(fields=['leadActor'], bind='legend')

    line_chart = alt.Chart(df_filtered).mark_point(filled=True, size=60).encode(
        x=alt.X('releaseYear:O', title="Release Year"),
        y=alt.Y('averageRating:Q', title="IMDb Rating", scale=alt.Scale(domain=[5, 10])),
        color=alt.Color('leadActor:N', title="Actor"),
        opacity=alt.condition(actor_selection, alt.value(0.9), alt.value(0.2)),
        tooltip=['primaryTitle', 'releaseYear', alt.Tooltip('averageRating', format=".2f"), 'leadActor']
    ).add_params(actor_selection).properties(height=300)

    # Add trend line only if enough data
    if len(df_filtered) >= 3:
        trend_line = alt.Chart(df_filtered).transform_regression(
            'releaseYear', 'averageRating'
        ).mark_line(color=ACCENT_RED, size=2).encode()
        return line_chart + trend_line
    
    return line_chart


def create_bond_films_rating_chart(df_full):
    """Create chart showing IMDb ratings for specific James Bond films only, color-coded by actor."""
    # Define the specific Bond films to include (year and title keywords for matching)
    target_films = [
        (1981, 'for your eyes only', 'Roger Moore'),
        (1983, 'octopussy', 'Roger Moore'),
        (1985, 'view to a kill', 'Roger Moore'),
        (1987, 'living daylights', 'Timothy Dalton'),
        (1989, 'licence to kill', 'Timothy Dalton'),
        (1995, 'goldeneye', 'Pierce Brosnan'),
        (1997, 'tomorrow never dies', 'Pierce Brosnan'),
        (1999, 'world is not enough', 'Pierce Brosnan'),
        (2002, 'die another day', 'Pierce Brosnan'),
        (2006, 'casino royale', 'Daniel Craig'),
        (2008, 'quantum of solace', 'Daniel Craig'),
        (2012, 'skyfall', 'Daniel Craig'),
        (2015, 'spectre', 'Daniel Craig'),
        (2021, 'no time to die', 'Daniel Craig')
    ]
    
    # Filter to only James Bond films first
    bond_films = df_full[df_full['is_bond_core'] == True].copy()
    
    if bond_films.empty:
        return None
    
    # Filter to only the specific films
    filtered_films = []
    for year, title_keywords, actor in target_films:
        # Match by year and title keywords (case-insensitive)
        matches = bond_films[
            (bond_films['releaseYear'] == year) &
            (bond_films['primaryTitle'].str.lower().str.contains(title_keywords, case=False, na=False))
        ]
        if not matches.empty:
            # If multiple matches, prefer the one with matching actor if available
            if actor in matches['leadActor'].values:
                matches = matches[matches['leadActor'] == actor]
            filtered_films.append(matches.iloc[0])
    
    if not filtered_films:
        return None
    
    # Convert to DataFrame
    bond_films = pd.DataFrame(filtered_films)
    
    # Sort by release year to ensure chronological order
    bond_films = bond_films.sort_values('releaseYear').reset_index(drop=True)
    
    # Create titles with year for x-axis labels (use full title, not abbreviated)
    bond_films['title_short'] = bond_films['primaryTitle'] + ' (' + bond_films['releaseYear'].astype(str) + ')'
    
    # Calculate average rating for the average line
    avg_rating = bond_films['averageRating'].mean()
    
    # Add actor selection (same as create_rating_trend_chart)
    actor_selection = alt.selection_point(fields=['leadActor'], bind='legend')
    
    # Main chart with points (removed white stroke)
    point_chart = alt.Chart(bond_films).mark_point(filled=True, size=120).encode(
        x=alt.X(
            'title_short:N',
            title="James Bond Films",
            sort=alt.SortField('releaseYear', order='ascending'),
            axis=alt.Axis(labelAngle=-45, labelLimit=0, labelOverlap=False)
        ),
        y=alt.Y('averageRating:Q', title="IMDb Rating", scale=alt.Scale(domain=[5, 10])),
        color=alt.Color('leadActor:N', title="Bond Actor", legend=alt.Legend(title="Actor")),
        opacity=alt.condition(actor_selection, alt.value(0.9), alt.value(0.2)),
        tooltip=[
            alt.Tooltip('primaryTitle:N', title="Film"),
            alt.Tooltip('releaseYear:O', title="Year"),
            alt.Tooltip('averageRating:Q', title="Rating", format=".2f"),
            alt.Tooltip('leadActor:N', title="Actor"),
            alt.Tooltip('numVotes:Q', title="Votes", format=",")
        ]
    ).add_params(actor_selection).properties(
        height=400,
        width=1200
    )
    
    # Add average line (same color as trend line in create_rating_trend_chart)
    avg_line = alt.Chart(pd.DataFrame({'avg_rating': [avg_rating]})).mark_rule(
        color=ACCENT_RED,
        size=2,
        strokeDash=[5, 5]
    ).encode(
        y=alt.Y('avg_rating:Q', title="IMDb Rating")
    )
    
    # Combine point chart with average line
    chart = point_chart + avg_line
    
    return chart


def create_bond_comparison_chart(df_full):
    """Create Bond vs Other Thriller Films comparison chart."""
    # Define the specific Bond films to include (year and title keywords for matching)
    target_films = [
        (1981, 'for your eyes only', 'Roger Moore'),
        (1983, 'octopussy', 'Roger Moore'),
        (1985, 'view to a kill', 'Roger Moore'),
        (1987, 'living daylights', 'Timothy Dalton'),
        (1989, 'licence to kill', 'Timothy Dalton'),
        (1995, 'goldeneye', 'Pierce Brosnan'),
        (1997, 'tomorrow never dies', 'Pierce Brosnan'),
        (1999, 'world is not enough', 'Pierce Brosnan'),
        (2002, 'die another day', 'Pierce Brosnan'),
        (2006, 'casino royale', 'Daniel Craig'),
        (2008, 'quantum of solace', 'Daniel Craig'),
        (2012, 'skyfall', 'Daniel Craig'),
        (2015, 'spectre', 'Daniel Craig'),
        (2021, 'no time to die', 'Daniel Craig')
    ]
    
    df_comparison = df_full[df_full['Thriller'] == 1].copy()
    
    # Filter to only the specific Bond films and track their indices
    bond_films_list = []
    bond_indices = set()
    
    for year, title_keywords, actor in target_films:
        # Match by year and title keywords (case-insensitive)
        matches = df_comparison[
            (df_comparison['releaseYear'] == year) &
            (df_comparison['primaryTitle'].str.lower().str.contains(title_keywords, case=False, na=False))
        ]
        if not matches.empty:
            # If multiple matches, prefer the one with matching actor if available
            if actor in matches['leadActor'].values:
                matches = matches[matches['leadActor'] == actor]
            selected_match = matches.iloc[0]
            bond_films_list.append(selected_match)
            bond_indices.add(selected_match.name)  # Track the original index
    
    # Create bond_films_data DataFrame
    if bond_films_list:
        bond_films_data = pd.DataFrame(bond_films_list)
    else:
        bond_films_data = pd.DataFrame()
    
    # All other thriller films (excluding the specific Bond films)
    other_films_data = df_comparison[~df_comparison.index.isin(bond_indices)].copy()
    
    # Other thriller films scatter
    other_scatter = alt.Chart(other_films_data).mark_circle(size=60, opacity=0.4, color='#9CA3AF').encode(
        x=alt.X('numVotes:Q', title="Number of Votes", scale=alt.Scale(type='log', domain=[100, 10000000])),
        y=alt.Y('averageRating:Q', title="IMDb Rating", scale=alt.Scale(domain=[4, 10])),
        tooltip=[
            'primaryTitle', 'leadActor', alt.Tooltip('averageRating', format=".2f"),
            alt.Tooltip('numVotes', format=","), 'releaseYear'
        ]
    )
    
    # Bond films scatter
    bond_scatter = alt.Chart(bond_films_data).mark_circle(size=150, opacity=0.9, color=ACCENT_RED).encode(
        x=alt.X('numVotes:Q'),
        y=alt.Y('averageRating:Q'),
        tooltip=[
            'primaryTitle', 'leadActor', alt.Tooltip('averageRating', format=".2f"),
            alt.Tooltip('numVotes', format=","), 'releaseYear'
        ]
    )
    
    # Build layers dynamically
    layers = [other_scatter, bond_scatter]
    
    if len(other_films_data) >= 3:
        other_trend = alt.Chart(other_films_data).transform_regression(
            'numVotes', 'averageRating', method='log'
        ).mark_line(color='#9CA3AF', size=3, strokeDash=[5, 5]).encode(
            x=alt.X('numVotes:Q'), y=alt.Y('averageRating:Q')
        )
        layers.insert(1, other_trend)
    
    if len(bond_films_data) >= 3:
        bond_trend = alt.Chart(bond_films_data).transform_regression(
            'numVotes', 'averageRating', method='log'
        ).mark_line(color=ACCENT_GOLD, size=4).encode(
            x=alt.X('numVotes:Q'), y=alt.Y('averageRating:Q')
        )
        layers.append(bond_trend)
    
    chart = alt.layer(*layers).properties(
        height=450,
        title="James Bond Films vs Other Thriller Films (with Best-Fit Lines)"
    ).interactive()
    
    return chart, bond_films_data, other_films_data


def create_runtime_rating_chart(df_filtered):
    """Create runtime vs rating scatter chart."""
    # Filter to only specific Bond films
    df_filtered = filter_to_specific_bond_films(df_filtered)
    
    if df_filtered.empty:
        return None
    
    chart = alt.Chart(df_filtered).mark_circle(stroke='white', strokeWidth=1).encode(
        x=alt.X('runtimeMinutes:Q', title="Runtime (Minutes)"),
        y=alt.Y('averageRating:Q', title="IMDb Rating", scale=alt.Scale(domain=[5, 10])),
        size=alt.Size('numVotes:Q', 
                     title="Popularity",
                     scale=alt.Scale(range=[50, 800]),
                     legend=alt.Legend(title="Popularity (Number of Votes)", 
                                      format=",",
                                      labelFontSize=11,
                                      symbolFillColor='white',
                                      symbolStrokeColor='white',
                                      symbolStrokeWidth=1)),
        color=alt.Color('leadActor:N', title="Actor"),
        tooltip=[
            'primaryTitle', 'leadActor',
            alt.Tooltip('runtimeMinutes', title="Runtime (mins)"),
            alt.Tooltip('averageRating', title="Rating", format=".2f"),
            alt.Tooltip('numVotes', title="Votes", format=",")
        ]
    ).properties(height=300).interactive()
    
    return chart


def create_genre_evolution_chart(df_filtered):
    """Create genre evolution by decade chart."""
    # Filter to only specific Bond films
    df_filtered = filter_to_specific_bond_films(df_filtered)
    
    if df_filtered.empty:
        return None
    
    genre_cols = ['Action', 'Adventure', 'Thriller', 'Romance', 'Sci-Fi', 'Comedy', 'Drama']
    df_genres = df_filtered.groupby('decade')[genre_cols].sum().reset_index()
    df_genres_melted = df_genres.melt('decade', value_vars=genre_cols, var_name='Genre', value_name='Count')
    df_genres_melted = df_genres_melted[df_genres_melted['Count'] > 0]
    
    chart = alt.Chart(df_genres_melted).mark_bar().encode(
        x=alt.X('decade:O', title="Decade", axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Count:Q', title="Genre Count"),
        color=alt.Color('Genre:N', title="Genre"),
        order=alt.Order('decade:O'),
        tooltip=['decade', 'Genre', 'Count']
    ).properties(height=300).interactive()
    
    return chart


def create_genre_trend_chart(df_filtered):
    """Create genre popularity trend area chart."""
    # Filter to only specific Bond films
    df_filtered = filter_to_specific_bond_films(df_filtered)
    
    if df_filtered.empty:
        return None
    
    genre_cols = ['Action', 'Adventure', 'Thriller', 'Romance', 'Sci-Fi', 'Comedy', 'Drama']
    df_genres = df_filtered.groupby('decade')[genre_cols].sum().reset_index()
    df_genres_melted = df_genres.melt('decade', value_vars=genre_cols, var_name='Genre', value_name='Count')
    df_genres_melted = df_genres_melted[df_genres_melted['Count'] > 0]
    
    if df_genres_melted.empty:
        return None
    
    chart = alt.Chart(df_genres_melted).mark_area(opacity=0.7, interpolate='monotone').encode(
        x=alt.X('decade:O', title="Decade", axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Count:Q', title="Number of Films", stack='zero'),
        color=alt.Color('Genre:N', title="Genre"),
        tooltip=[
            alt.Tooltip('decade:O', title='Decade'),
            alt.Tooltip('Genre:N', title='Genre'),
            alt.Tooltip('Count:Q', title='Films')
        ]
    ).properties(height=350, title="Genre Popularity: Stacked Area View")
    
    return chart


def create_rating_distribution_chart(df_filtered):
    """Create rating distribution strip chart."""
    strip_chart = alt.Chart(df_filtered).mark_circle(size=70, opacity=0.7).encode(
        x=alt.X('averageRating:Q', title="IMDb Rating", scale=alt.Scale(domain=[5, 10])),
        y=alt.Y('leadActor:N', title="Lead Actor"),
        color=alt.Color('leadActor:N', legend=None),
        tooltip=['primaryTitle', 'leadActor', alt.Tooltip('averageRating', title="Rating", format=".2f")]
    ).properties(height=300).interactive()

    mean_line = alt.Chart(df_filtered).mark_rule(color=ACCENT_RED, size=2).encode(
        x='mean(averageRating):Q',
        y='leadActor:N'
    )

    return strip_chart + mean_line


def create_production_volume_chart(df_filtered):
    """Create production volume by decade chart."""
    # Filter to only specific Bond films
    df_filtered = filter_to_specific_bond_films(df_filtered)
    
    if df_filtered.empty:
        return None
    
    decade_data = df_filtered.groupby('decade').size().reset_index(name='count')
    
    chart = alt.Chart(decade_data).mark_bar().encode(
        x=alt.X('decade:O', title="Decade", axis=alt.Axis(labelAngle=0)),
        y=alt.Y('count:Q', title="Number of Films"),
        color=alt.Color('count:Q', scale=alt.Scale(range=[ACCENT_ORANGE, ACCENT_BLUE]), legend=None),
        tooltip=[alt.Tooltip('decade:O', title='Decade'), alt.Tooltip('count:Q', title='Films')]
    ).properties(height=300)
    
    return chart


def create_performance_heatmap(df_filtered):
    """Create performance heatmap by actor and decade."""
    heatmap_data = df_filtered.groupby(['leadActor', 'decade']).agg(
        avg_rating=('averageRating', 'mean'),
        film_count=('primaryTitle', 'count')
    ).reset_index()
    
    heatmap_data = heatmap_data[heatmap_data['film_count'] > 0]
    
    chart = alt.Chart(heatmap_data).mark_rect().encode(
        x=alt.X('decade:O', title="Decade"),
        y=alt.Y('leadActor:N', title="Actor"),
        color=alt.Color('avg_rating:Q', scale=alt.Scale(scheme='blues', domain=[5, 9]), title="Avg Rating"),
        tooltip=[
            alt.Tooltip('leadActor:N', title='Actor'),
            alt.Tooltip('decade:O', title='Decade'),
            alt.Tooltip('avg_rating:Q', title='Avg Rating', format='.2f'),
            alt.Tooltip('film_count:Q', title='Films')
        ]
    ).properties(height=300)
    
    return chart


def create_engagement_boxplot(df_filtered):
    """Create audience engagement distribution boxplot."""
    chart = alt.Chart(df_filtered).mark_boxplot(
        size=50,
        color=ACCENT_BLUE,
        opacity=0.7,
        median={'color': ACCENT_GOLD, 'size': 3},
        outliers={'color': ACCENT_RED, 'size': 30, 'opacity': 0.6}
    ).encode(
        x=alt.X('leadActor:N', title="Actor", axis=alt.Axis(labelAngle=0, labelFontSize=11)),
        y=alt.Y('numVotes:Q', title="Number of Votes (Log Scale)", 
                scale=alt.Scale(type='log'), axis=alt.Axis(tickCount=5)),
        tooltip=['leadActor:N', alt.Tooltip('numVotes:Q', format=',')]
    ).properties(height=350)
    
    return chart


def create_film_timeline_chart(df_filtered):
    """Create complete film timeline chart."""
    df_timeline = df_filtered.copy()
    df_timeline['rating_band'] = pd.cut(
        df_timeline['averageRating'],
        bins=[0, 6, 7, 8, 10],
        labels=['Below 6', '6-7', '7-8', '8+']
    )
    
    chart = alt.Chart(df_timeline).mark_circle(size=100, stroke='white', strokeWidth=1).encode(
        x=alt.X('releaseYear:O', title="Release Year"),
        y=alt.Y('leadActor:N', title="Actor"),
        color=alt.Color('rating_band:N',
            scale=alt.Scale(
                domain=['Below 6', '6-7', '7-8', '8+'],
                range=[ACCENT_RED, ACCENT_ORANGE, ACCENT_GREEN, ACCENT_BLUE]
            ),
            title="Rating Band"
        ),
        size=alt.Size('numVotes:Q', 
                     scale=alt.Scale(range=[50, 500]), 
                     title="Popularity",
                     legend=alt.Legend(title="Popularity (Number of Votes)",
                                      format=",",
                                      labelFontSize=11,
                                      symbolFillColor='white',
                                      symbolStrokeColor='white',
                                      symbolStrokeWidth=1)),
        tooltip=[
            'primaryTitle', 'leadActor', 'releaseYear',
            alt.Tooltip('averageRating:Q', format='.2f'),
            alt.Tooltip('numVotes:Q', format=',')
        ]
    ).properties(height=350)
    
    return chart
