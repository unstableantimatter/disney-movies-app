import pandas as pd
import numpy as np
from datetime import datetime

def load_and_process_data(file_path):
    """
    Load and process the Disney movies dataset with necessary transformations.
    """
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Convert release_date to datetime
    df['release_date'] = pd.to_datetime(df['release_date'])
    
    # Extract temporal features
    df['year'] = df['release_date'].dt.year
    df['month'] = df['release_date'].dt.month
    df['decade'] = (df['year'] // 10) * 10
    
    # Convert monetary columns to numeric, handling any non-numeric values
    df['total_gross'] = pd.to_numeric(df['total_gross'], errors='coerce')
    df['inflation_adjusted_gross'] = pd.to_numeric(df['inflation_adjusted_gross'], errors='coerce')
    
    # Calculate performance metrics
    df['performance_ratio'] = df['inflation_adjusted_gross'] / df['total_gross']
    
    # Handle missing values
    df['genre'] = df['genre'].fillna('Unknown')
    df['mpaa_rating'] = df['mpaa_rating'].fillna('Not Rated')
    
    # Create success metrics
    avg_gross = df['total_gross'].mean()
    df['success_level'] = np.where(df['total_gross'] > avg_gross, 'Above Average', 'Below Average')
    
    # Create season feature
    df['season'] = df['month'].apply(lambda x: 
        'Winter' if x in [12, 1, 2] else
        'Spring' if x in [3, 4, 5] else
        'Summer' if x in [6, 7, 8] else
        'Fall'
    )
    
    # Create decade ranges for better visualization
    df['decade_range'] = df['decade'].apply(lambda x: f"{x}-{x+9}")
    
    # Calculate year-over-year growth
    df['yoy_growth'] = df.groupby('year')['total_gross'].pct_change() * 100
    
    return df

def get_summary_statistics(df):
    """
    Generate summary statistics for the dataset.
    """
    if df.empty:
        return {
            'total_movies': 0,
            'date_range': 'N/A',
            'total_revenue': 0,
            'avg_revenue': 0,
            'top_genre': 'N/A',
            'most_common_rating': 'N/A'
        }
    return {
        'total_movies': len(df),
        'date_range': f"{df['year'].min()} - {df['year'].max()}",
        'total_revenue': df['total_gross'].sum(),
        'avg_revenue': df['total_gross'].mean(),
        'top_genre': df['genre'].mode()[0],
        'most_common_rating': df['mpaa_rating'].mode()[0]
    }

def get_time_series_data(df):
    """
    Prepare time series data for visualization.
    """
    return df.groupby('year').agg({
        'total_gross': 'sum',
        'inflation_adjusted_gross': 'sum',
        'movie_title': 'count'
    }).reset_index()

def get_genre_distribution(df):
    """
    Prepare genre distribution data for visualization.
    """
    return df['genre'].value_counts().reset_index()

def get_rating_distribution(df):
    """
    Prepare MPAA rating distribution data for visualization.
    """
    return df['mpaa_rating'].value_counts().reset_index()

def get_seasonal_analysis(df):
    """
    Prepare seasonal release analysis data.
    """
    return df.groupby('season').agg({
        'total_gross': 'mean',
        'movie_title': 'count'
    }).reset_index() 