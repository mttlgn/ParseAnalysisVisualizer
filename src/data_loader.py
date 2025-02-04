import pandas as pd
from pathlib import Path
from typing import Dict, List

def load_raid_data(file_path: str) -> pd.DataFrame:
    """
    Load and clean raid composition data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Cleaned DataFrame with raid composition data
    """
    # Read CSV with 'Parses' as string to handle comma-formatted numbers
    df = pd.read_csv(file_path, dtype={'Parses': str})
    
    # Clean the 'Parses' column by removing commas and converting to int
    df['Parses'] = df['Parses'].str.replace(',', '').astype(int)
    
    return df

def calculate_percentages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate percentage shares for each class and spec.
    
    Args:
        df (pd.DataFrame): Input DataFrame with raid composition data
        
    Returns:
        pd.DataFrame: DataFrame with additional percentage columns
    """
    total_parses = df['Parses'].sum()
    
    # Calculate percentages
    df = df.copy()
    df['Percentage'] = (df['Parses'] / total_parses * 100).round(2)
    
    # Add class totals
    class_totals = df.groupby('Class')['Parses'].sum().reset_index()
    class_totals['Class_Percentage'] = (class_totals['Parses'] / total_parses * 100).round(2)
    
    return df, class_totals

def load_all_raids(data_dir: str = 'parse_data') -> Dict[str, pd.DataFrame]:
    """
    Load all raid data files from the specified directory.
    
    Args:
        data_dir (str): Directory containing raid CSV files
        
    Returns:
        Dict[str, pd.DataFrame]: Dictionary mapping raid names to their DataFrames
    """
    # Define raid order (from oldest to newest)
    RAID_ORDER = [
        # Battle for Azeroth (8.x)
        "Uldir (8.1)",
        "Battle of Dazar'alor",
        "Crucible of Storms",
        "Eternal Palace",
        "Nya'lotha (Pre-Nerf)",
        
        # Shadowlands (9.x)
        "Castle Nathria (DF Pre-Patch)",
        "Sanctum of Domination (DF Pre-Patch)",
        "Sepulcher of the First Ones (9.2)",
        
        # Dragonflight (10.x)
        "Vault of the Incarnates",
        "Aberrus, The Shadowed Crucible",
        "Amirdrassil, the Dream's Hope",
        
        # The War Within (11.x)
        "Nerub-ar Palace"
    ]
    
    data_path = Path(data_dir)
    raid_data = {}
    
    # Load all raid data first
    for csv_file in data_path.glob('*.csv'):
        raid_name = csv_file.stem.replace('Parse Counts - ', '')
        raid_data[raid_name] = load_raid_data(str(csv_file))
    
    # Create an ordered dictionary based on RAID_ORDER
    ordered_raid_data = {raid: raid_data[raid] for raid in RAID_ORDER if raid in raid_data}
    
    return ordered_raid_data 