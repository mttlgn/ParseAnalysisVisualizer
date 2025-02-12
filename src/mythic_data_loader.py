import pandas as pd
from pathlib import Path
import os

def load_mythic_scaling_data():
    """Load all Mythic+ scaling data files."""
    # Try multiple possible data directory locations
    possible_paths = [
        Path('mythic_scaling_data'),  # Local development
        Path(__file__).parent.parent / 'mythic_scaling_data',  # Relative to this file
        Path.cwd() / 'mythic_scaling_data'  # Current working directory
    ]
    
    data_dir = None
    for path in possible_paths:
        if path.exists():
            data_dir = path
            break
    
    if data_dir is None:
        raise FileNotFoundError(
            "Could not find mythic_scaling_data directory. "
            f"Tried paths: {[str(p) for p in possible_paths]}"
        )
    
    # Load each CSV file
    try:
        scaling_percentages = pd.read_csv(data_dir / 'M+ Scaling Season 1 vs Season 2 - Scaling Percentages.csv')
        scaling_10_higher = pd.read_csv(data_dir / 'M+ Scaling Season 1 vs Season 2 - Scaling With 10_ Higher Baseline.csv')
        scaling_25_higher = pd.read_csv(data_dir / 'M+ Scaling Season 1 vs Season 2 - Scaling WIth 25_ Higher Baseline.csv')
    except FileNotFoundError as e:
        # List available files in the directory for debugging
        available_files = list(data_dir.glob('*.csv')) if data_dir.exists() else []
        raise FileNotFoundError(
            f"Error loading CSV files from {data_dir}. "
            f"Available files: {[f.name for f in available_files]}"
        ) from e
    
    # Process percentage values in the first file
    for col in scaling_percentages.columns:
        if col != 'Mythic' and col != 'Note':
            scaling_percentages[col] = scaling_percentages[col].str.rstrip('%').astype(float)
    
    # The other files are already in numeric format
    # Just need to ensure consistent column names
    scaling_10_higher = scaling_10_higher.drop(columns=['Notes'], errors='ignore')
    scaling_25_higher = scaling_25_higher.drop(columns=['Notes'], errors='ignore')
    
    return {
        'percentages': scaling_percentages,
        '10_higher': scaling_10_higher,
        '25_higher': scaling_25_higher
    } 