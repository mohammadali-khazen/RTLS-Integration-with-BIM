from typing import List, Tuple
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon
from .geometry import GeometryCalculator

class WorkspaceAnalyzer:
    """Analyzes workspace occupancy and target locations."""
    
    def __init__(self):
        self.geometry_calculator = GeometryCalculator()
    
    def check_point_in_polygon(self, 
                             point: Tuple[float, float],
                             polygon_points: List[Tuple[float, float]]) -> bool:
        """
        Check if a point is inside a polygon using Shapely.
        
        Args:
            point: (x, y) coordinates of the point
            polygon_points: List of (x, y) coordinates defining the polygon vertices
            
        Returns:
            bool: True if point is inside polygon, False otherwise
        """
        polygon = Polygon(polygon_points)
        point_obj = Point(point)
        return polygon.contains(point_obj)
    
    def analyze_workspace_occupancy(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze which workspace each target point belongs to.
        
        Args:
            data: DataFrame containing target locations and workspace vertices
            
        Returns:
            DataFrame with workspace occupancy information
        """
        # Extract polygon vertices for each workspace
        vertices = []
        for i in range(1, 5):
            vertices.append(data[[f'X{i}', f'Y{i}']].values.tolist())
        
        # Check each point against each workspace
        results = []
        for _, row in data.iterrows():
            point = (row['location_X'], row['location_Y'])
            for workspace_vertices in vertices:
                is_inside = self.check_point_in_polygon(point, workspace_vertices)
                results.append(is_inside)
        
        # Add results to dataframe
        data['in_workspace'] = results
        return data
    
    def calculate_segment_distances(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate distances from target points to workspace segments.
        
        Args:
            data: DataFrame containing target locations and workspace vertices
            
        Returns:
            DataFrame with segment distance information
        """
        results = []
        
        for _, row in data.iterrows():
            point = (row['location_X'], row['location_Y'], row['location_Z'])
            
            # Calculate distances to each segment
            segment_distances = []
            for i in range(1, 5):
                start_idx = i
                end_idx = (i % 4) + 1
                
                start = (row[f'X{start_idx}'], row[f'Y{start_idx}'], row[f'Z{start_idx}'])
                end = (row[f'X{end_idx}'], row[f'Y{end_idx}'], row[f'Z{end_idx}'])
                
                distance, nearest_point = self.geometry_calculator.point_to_line_distance(
                    point, start, end
                )
                
                segment_distances.append({
                    f'distance_{i}': distance,
                    f'nearest_point_{i}': nearest_point
                })
            
            results.append(segment_distances)
        
        # Convert results to DataFrame
        distance_df = pd.DataFrame([
            {k: v for d in r for k, v in d.items()}
            for r in results
        ])
        
        return pd.concat([data, distance_df], axis=1)
    
    def analyze_workspace_patterns(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze patterns in workspace occupancy.
        
        Args:
            data: DataFrame containing workspace occupancy information
            
        Returns:
            DataFrame with workspace pattern analysis
        """
        # Group by workspace and calculate statistics
        patterns = data.groupby('comment').agg({
            'in_workspace': ['count', 'sum', 'mean'],
            'diff_seconds': ['sum', 'mean']
        })
        
        # Flatten column names
        patterns.columns = ['_'.join(col).strip() for col in patterns.columns.values]
        
        return patterns
