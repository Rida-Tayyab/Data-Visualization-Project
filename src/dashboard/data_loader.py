"""Data loading and preprocessing utilities."""

import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path

try:
    from .config import EON_BOND_ACTORS
except ImportError:
    from config import EON_BOND_ACTORS


@st.cache_data
def load_and_preprocess_data(file_path):
    """Load and preprocess the Bond film dataset."""
    df = pd.read_csv(file_path)
    
    # 1. Initial Cleaning: Drop rows with missing leadActor
    df.dropna(subset=['leadActor'], inplace=True)
    
    # 2. Clean numeric columns - remove NaN, inf, and invalid values
    numeric_cols = ['averageRating', 'numVotes', 'runtimeMinutes']
    for col in numeric_cols:
        if col in df.columns:
            # Replace inf/-inf with NaN
            df[col] = df[col].replace([np.inf, -np.inf], np.nan)
            # Drop rows with NaN in critical numeric columns
            df = df[df[col].notna()].copy()
            # Ensure positive values for numVotes and runtimeMinutes
            if col in ['numVotes', 'runtimeMinutes']:
                df = df[df[col] > 0].copy()
    
    # 3. Convert types for cleaner analysis
    df['releaseYear'] = df['releaseYear'].astype(int)
    df['decade'] = (df['releaseYear'] // 10 * 10).astype(int)
    
    # 4. Create the 'Core Bond' subset mask
    is_bond_actor = df['leadActor'].isin(EON_BOND_ACTORS)
    has_bond_title = df['primaryTitle'].str.contains('Bond|007', case=False, na=False) | \
                     df['originalTitle'].str.contains('Bond|007', case=False, na=False)
    
    df['is_bond_core'] = (is_bond_actor | has_bond_title)
    
    # 5. Filter out entries with too few votes
    df = df[df['numVotes'] >= 500].copy()
    
    return df


def get_data_path():
    """Get the path to the data file."""
    BASE_DIR = Path(__file__).resolve().parent.parent
    return BASE_DIR.parent / 'data' / 'processed' / 'data_final_lead_actor_fixed.csv'
