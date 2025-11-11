import pandas as pd
import os

# ------------------------------
# Step 0: Define paths
# ------------------------------
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
data_dir = os.path.join(project_dir, "data", "raw")
output_dir = os.path.join(project_dir, "data", "processed")
os.makedirs(output_dir, exist_ok=True)

basics_file = os.path.join(data_dir, "title.basics.tsv.gz")
ratings_file = os.path.join(data_dir, "title.ratings.tsv.gz")

# ------------------------------
# Step 1: Load datasets
# ------------------------------
basics = pd.read_csv(
    basics_file,
    sep="\t",
    compression='gzip',
    na_values="\\N",
    low_memory=False
)

ratings = pd.read_csv(
    ratings_file,
    sep="\t",
    compression='gzip',
    na_values="\\N"
)

# ------------------------------
# Step 2: Filter for movies only
# ------------------------------
movies = basics[basics['titleType'] == 'movie']

# ------------------------------
# Step 3: Merge ratings
# ------------------------------
movies = movies.merge(ratings, on='tconst', how='left')

# ------------------------------
# Step 4: Prepare fields for Tableau
# ------------------------------

# Convert runtimeMinutes to numeric (some values may be missing)
movies['runtimeMinutes'] = pd.to_numeric(movies['runtimeMinutes'], errors='coerce')

# Optional: create decade column for analysis
movies['decade'] = (movies['startYear'] // 10 * 10).astype('Int64')

# Split genres into a list for Tableau filtering
movies['genre_list'] = movies['genres'].str.split(',')

# ------------------------------
# Step 5: Export CSV for Tableau
# ------------------------------
movies.to_csv(os.path.join(output_dir, "movies_clean.csv"), index=False)

print("Movie data preparation complete. CSV ready for Tableau!")
