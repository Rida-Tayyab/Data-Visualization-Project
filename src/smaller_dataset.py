import pandas as pd
import os

# ------------------------------
# Paths
# ------------------------------
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
data_dir = os.path.join(project_dir, "data", "processed")
input_file = os.path.join(data_dir, "movies_merged.csv")
output_file = os.path.join(data_dir, "movies_1990_onwards.csv")

# ------------------------------
# Load CSV
# ------------------------------
movies = pd.read_csv(input_file, na_values="\\N")

# ------------------------------
# Filter for movies from 1990 onwards
# ------------------------------
# Ensure startYear is numeric
movies['startYear'] = pd.to_numeric(movies['startYear'], errors='coerce')

movies_filtered = movies[movies['startYear'] >= 1990]

# ------------------------------
# Save filtered CSV
# ------------------------------
movies_filtered.to_csv(output_file, index=False)

print(f"Filtered movies saved: {output_file}")
print(f"Total movies >=1980: {len(movies_filtered)}")
