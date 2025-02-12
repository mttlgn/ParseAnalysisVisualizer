import pandas as pd
from pathlib import Path

def load_mythic_scaling_data():
    """Load all Mythic+ scaling data files."""
    data_dir = Path('mythic_scaling_data')
    
    # Load each CSV file
    scaling_percentages = pd.read_csv(data_dir / 'M+ Scaling Season 1 vs Season 2 - Scaling Percentages.csv')
    scaling_10_higher = pd.read_csv(data_dir / 'M+ Scaling Season 1 vs Season 2 - Scaling With 10_ Higher Baseline.csv')
    scaling_25_higher = pd.read_csv(data_dir / 'M+ Scaling Season 1 vs Season 2 - Scaling With 25_ Higher Baseline.csv')
    
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