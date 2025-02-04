import pandas as pd
from typing import Dict, Tuple, List

def compare_raids(raid1_df: pd.DataFrame, raid2_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compare spec/class distributions between two raids.
    
    Args:
        raid1_df (pd.DataFrame): First raid's data
        raid2_df (pd.DataFrame): Second raid's data
        
    Returns:
        pd.DataFrame: Comparison DataFrame with changes in percentages
    """
    # Calculate percentages for both raids
    raid1_total = raid1_df['Parses'].sum()
    raid2_total = raid2_df['Parses'].sum()
    
    raid1_df = raid1_df.copy()
    raid2_df = raid2_df.copy()
    
    raid1_df['Percentage'] = (raid1_df['Parses'] / raid1_total * 100).round(2)
    raid2_df['Percentage'] = (raid2_df['Parses'] / raid2_total * 100).round(2)
    
    # Merge the dataframes
    comparison = pd.merge(
        raid1_df[['Class', 'Spec', 'Percentage']],
        raid2_df[['Class', 'Spec', 'Percentage']],
        on=['Class', 'Spec'],
        suffixes=('_raid1', '_raid2')
    )
    
    # Calculate changes
    comparison['Percentage_Change'] = (
        comparison['Percentage_raid2'] - comparison['Percentage_raid1']
    ).round(2)
    
    return comparison

def identify_trends(raid_data: Dict[str, pd.DataFrame], exclude_raids: List[str] = None) -> pd.DataFrame:
    """
    Identify trends across all raids.
    
    Args:
        raid_data (Dict[str, pd.DataFrame]): Dictionary of raid data
        exclude_raids (List[str], optional): List of raid names to exclude from analysis
        
    Returns:
        pd.DataFrame: Trend analysis DataFrame
    """
    trend_data = []
    exclude_raids = exclude_raids or []  # Convert None to empty list
    
    # Filter out excluded raids
    filtered_raids = {name: df for name, df in raid_data.items() if name not in exclude_raids}
    
    for raid_name, df in filtered_raids.items():
        total_parses = df['Parses'].sum()
        
        for _, row in df.iterrows():
            trend_data.append({
                'Raid': raid_name,
                'Class': row['Class'],
                'Spec': row['Spec'],
                'Percentage': (row['Parses'] / total_parses * 100).round(2)
            })
    
    return pd.DataFrame(trend_data)

def get_top_specs(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """
    Get the top N specs by parse count.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        n (int): Number of top specs to return
        
    Returns:
        pd.DataFrame: Top N specs
    """
    return df.nlargest(n, 'Parses')

def identify_class_trends(raid_data: Dict[str, pd.DataFrame], exclude_raids: List[str] = None) -> pd.DataFrame:
    """
    Identify class-level trends across all raids.
    
    Args:
        raid_data (Dict[str, pd.DataFrame]): Dictionary of raid data
        exclude_raids (List[str], optional): List of raid names to exclude from analysis
        
    Returns:
        pd.DataFrame: Class trend analysis DataFrame
    """
    trend_data = []
    exclude_raids = exclude_raids or []
    
    # Filter out excluded raids
    filtered_raids = {name: df for name, df in raid_data.items() if name not in exclude_raids}
    
    for raid_name, df in filtered_raids.items():
        total_parses = df['Parses'].sum()
        class_totals = df.groupby('Class')['Parses'].sum()
        
        for class_name, parses in class_totals.items():
            trend_data.append({
                'Raid': raid_name,
                'Class': class_name,
                'Percentage': (parses / total_parses * 100).round(2)
            })
    
    return pd.DataFrame(trend_data)

def analyze_class_changes(raid_data: Dict[str, pd.DataFrame], class_name: str, exclude_raids: List[str] = None) -> pd.DataFrame:
    """
    Analyze how a specific class's representation has changed between raids.
    
    Args:
        raid_data (Dict[str, pd.DataFrame]): Dictionary of raid data
        class_name (str): Name of the class to analyze
        exclude_raids (List[str], optional): List of raid names to exclude from analysis
        
    Returns:
        pd.DataFrame: DataFrame with class percentage changes between raids
    """
    exclude_raids = exclude_raids or []
    filtered_raids = {name: df for name, df in raid_data.items() if name not in exclude_raids}
    
    changes = []
    previous_percentage = None
    previous_raid = None
    
    for raid_name, df in filtered_raids.items():
        total_parses = df['Parses'].sum()
        class_parses = df[df['Class'] == class_name]['Parses'].sum()
        current_percentage = (class_parses / total_parses * 100).round(2)
        
        if previous_percentage is not None:
            change = current_percentage - previous_percentage
            changes.append({
                'From Raid': previous_raid,
                'To Raid': raid_name,
                'From Percentage': previous_percentage,
                'To Percentage': current_percentage,
                'Change': change.round(2)
            })
        
        previous_percentage = current_percentage
        previous_raid = raid_name
    
    return pd.DataFrame(changes) 