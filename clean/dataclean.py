import pandas as pd
from scipy import stats

def clean_data(df, missing_threshold=0.3, fill_strategy='mean', outlier_removal=False):
    """
    Cleans the dataset by handling missing values, converting data types, and optionally removing outliers.
    
    Parameters:
        df (pd.DataFrame): The DataFrame to be cleaned.
        missing_threshold (float): Threshold (0-1) for dropping columns with excessive missing values.
        fill_strategy (str): Strategy to fill missing values. Options: 'mean', 'median', 'mode', or 'drop'.
        outlier_removal (bool): If True, removes outliers based on Z-score.
        
    Returns:
        pd.DataFrame: Cleaned dataset.
    """
    
    # Drop columns with too many missing values
    df = df.dropna(thresh=int(missing_threshold * len(df)), axis=1)
    
    # Handle remaining missing values based on strategy
    if fill_strategy == 'mean':
        df = df.fillna(df.mean())
    elif fill_strategy == 'median':
        df = df.fillna(df.median())
    elif fill_strategy == 'mode':
        df = df.fillna(df.mode().iloc[0])
    elif fill_strategy == 'drop':
        df = df.dropna()
    
    # Convert data types to best possible types
    df = df.convert_dtypes()

    # Remove outliers based on Z-score if specified
    if outlier_removal:
        z_scores = stats.zscore(df.select_dtypes(include='number'))
        df = df[(abs(z_scores) < 3).all(axis=1)]
    
    print("Data cleaned successfully.")
    return df
