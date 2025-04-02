from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """Configuration settings for the RTLS-BIM integration system."""
    
    # Base paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    
    # Input file paths
    BIM_DATA_PATH: Optional[Path] = None
    RTLS_DATA_PATH: Optional[Path] = None
    
    # Processing parameters
    MAX_TIME_DIFF_SECONDS: float = 5.0
    DEFAULT_Z_COORDINATE: float = 0.0
    
    def __post_init__(self):
        """Create necessary directories if they don't exist."""
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        # Set default paths if not provided
        if self.BIM_DATA_PATH is None:
            self.BIM_DATA_PATH = self.DATA_DIR / "model_zone_detection5.csv"
        if self.RTLS_DATA_PATH is None:
            self.RTLS_DATA_PATH = self.DATA_DIR / "Experiment8_zone_detection_pattern6.csv"
