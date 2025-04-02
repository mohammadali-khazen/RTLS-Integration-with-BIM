from typing import Tuple, List
import math
import numpy as np
from dataclasses import dataclass

@dataclass
class Point3D:
    """Represents a 3D point with x, y, z coordinates."""
    x: float
    y: float
    z: float
    
    def to_tuple(self) -> Tuple[float, float, float]:
        """Convert point to tuple representation."""
        return (self.x, self.y, self.z)

class GeometryCalculator:
    """Handles geometric calculations for RTLS-BIM integration."""
    
    @staticmethod
    def dot(v: Tuple[float, float, float], w: Tuple[float, float, float]) -> float:
        """Calculate dot product of two 3D vectors."""
        return sum(a * b for a, b in zip(v, w))
    
    @staticmethod
    def length(v: Tuple[float, float, float]) -> float:
        """Calculate length of a 3D vector."""
        return math.sqrt(sum(x * x for x in v))
    
    @staticmethod
    def vector(b: Tuple[float, float, float], e: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """Calculate vector from point b to point e."""
        return tuple(e[i] - b[i] for i in range(3))
    
    @staticmethod
    def unit(v: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """Calculate unit vector of v."""
        mag = GeometryCalculator.length(v)
        return tuple(x / mag for x in v)
    
    @staticmethod
    def distance(p0: Tuple[float, float, float], p1: Tuple[float, float, float]) -> float:
        """Calculate distance between two points."""
        return GeometryCalculator.length(GeometryCalculator.vector(p0, p1))
    
    @staticmethod
    def scale(v: Tuple[float, float, float], sc: float) -> Tuple[float, float, float]:
        """Scale a vector by a scalar."""
        return tuple(x * sc for x in v)
    
    @staticmethod
    def add(v: Tuple[float, float, float], w: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """Add two vectors."""
        return tuple(a + b for a, b in zip(v, w))
    
    @classmethod
    def point_to_line_distance(cls, 
                             point: Tuple[float, float, float],
                             line_start: Tuple[float, float, float],
                             line_end: Tuple[float, float, float]) -> Tuple[float, Tuple[float, float, float]]:
        """
        Calculate the distance from a point to a line segment and the nearest point on the segment.
        
        Args:
            point: The point to calculate distance from
            line_start: Start point of the line segment
            line_end: End point of the line segment
            
        Returns:
            Tuple containing (distance, nearest_point)
        """
        line_vec = cls.vector(line_start, line_end)
        pnt_vec = cls.vector(line_start, point)
        line_len = cls.length(line_vec)
        line_unitvec = cls.unit(line_vec)
        pnt_vec_scaled = cls.scale(pnt_vec, 1.0/line_len)
        t = cls.dot(line_unitvec, pnt_vec_scaled)
        
        # Clamp t to [0,1] to ensure we're on the line segment
        t = max(0.0, min(1.0, t))
        
        nearest = cls.scale(line_vec, t)
        dist = cls.distance(nearest, pnt_vec)
        nearest = cls.add(nearest, line_start)
        
        return dist, nearest
