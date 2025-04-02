from typing import Tuple
import pandas as pd
from pathlib import Path
from datetime import datetime
from .config import Config
import numpy as np

class DataProcessor:
    """Handles data loading and preprocessing for RTLS-BIM integration."""
    
    def __init__(self, config: Config):
        self.config = config
        self.bim_data = None
        self.rtls_data = None
        self.processed_data = None
    
    def load_bim_data(self) -> pd.DataFrame:
        """Load and preprocess BIM model data."""
        try:
            df = pd.read_csv(self.config.BIM_DATA_PATH)
            
            # Separate numeric and categorical columns
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            categorical_cols = ['family_type', 'comment']
            
            # Convert numeric columns to float
            df[numeric_cols] = df[numeric_cols].astype(float)
            
            # Reorder columns
            df = pd.concat([df[categorical_cols], df[numeric_cols]], axis=1)
            
            self.bim_data = df
            return df
            
        except Exception as e:
            raise RuntimeError(f"Error loading BIM data: {str(e)}")
    
    def load_rtls_data(self) -> pd.DataFrame:
        """Load and preprocess RTLS data."""
        try:
            data = pd.read_csv(self.config.RTLS_DATA_PATH)
            
            # Clean timestamp
            data['timestamp'] = pd.to_datetime(
                data['timestamp'].str.replace('@', ''),
                infer_datetime_format=True
            )
            
            # Add z-coordinate
            data['location_Z'] = self.config.DEFAULT_Z_COORDINATE
            
            # Clean and sort data
            data = (data
                   .dropna()
                   .drop_duplicates(subset=['timestamp'])
                   .sort_values('timestamp')
                   .reset_index(drop=True))
            
            self.rtls_data = data
            return data
            
        except Exception as e:
            raise RuntimeError(f"Error loading RTLS data: {str(e)}")
    
    def prepare_combined_dataset(self) -> pd.DataFrame:
        """Prepare the combined dataset for analysis."""
        if self.bim_data is None or self.rtls_data is None:
            raise RuntimeError("BIM and RTLS data must be loaded first")
        
        # Create expanded datasets
        locations = pd.DataFrame(
            np.repeat(self.rtls_data.values, len(self.bim_data.index), axis=0),
            columns=self.rtls_data.columns
        )
        geo = pd.concat([self.bim_data] * len(self.rtls_data.index))
        geo = geo.reset_index(drop=True)
        
        # Combine datasets
        combined = pd.concat([locations, geo], axis=1)
        
        # Calculate time differences
        combined['diff_seconds'] = combined['timestamp'].diff(1).dt.total_seconds()
        
        # Filter out records with large time differences
        combined = combined[
            combined['diff_seconds'] <= self.config.MAX_TIME_DIFF_SECONDS
        ].sort_values('timestamp').reset_index(drop=True)
        
        # Fill missing comments
        combined['comment'].fillna('safe', inplace=True)
        
        self.processed_data = combined
        return combined
    
    def get_workspace_statistics(self) -> pd.DataFrame:
        """Calculate workspace statistics."""
        if self.processed_data is None:
            raise RuntimeError("Processed data must be prepared first")
        
        # Calculate time spent and record counts
        time_spent = self.processed_data.groupby('comment')['diff_seconds'].sum()
        records_number = self.processed_data.groupby('comment')['timestamp'].count()
        
        # Combine statistics
        stats = pd.DataFrame({
            'time_spent': time_spent,
            'records_number': records_number
        })
        
        return stats
