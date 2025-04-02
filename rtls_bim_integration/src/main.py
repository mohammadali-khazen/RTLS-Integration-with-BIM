from pathlib import Path
import pandas as pd
from .config import Config
from .data_processor import DataProcessor
from .workspace_analyzer import WorkspaceAnalyzer

def main():
    """Main entry point for the RTLS-BIM integration system."""
    try:
        # Initialize configuration
        config = Config()
        
        # Initialize data processor
        processor = DataProcessor(config)
        
        # Load and process data
        print("Loading BIM data...")
        bim_data = processor.load_bim_data()
        
        print("Loading RTLS data...")
        rtls_data = processor.load_rtls_data()
        
        print("Preparing combined dataset...")
        combined_data = processor.prepare_combined_dataset()
        
        # Initialize workspace analyzer
        analyzer = WorkspaceAnalyzer()
        
        print("Analyzing workspace occupancy...")
        occupancy_data = analyzer.analyze_workspace_occupancy(combined_data)
        
        print("Calculating segment distances...")
        distance_data = analyzer.calculate_segment_distances(occupancy_data)
        
        print("Analyzing workspace patterns...")
        patterns = analyzer.analyze_workspace_patterns(distance_data)
        
        # Get workspace statistics
        print("Calculating workspace statistics...")
        stats = processor.get_workspace_statistics()
        
        # Save results
        output_dir = config.DATA_DIR / "output"
        output_dir.mkdir(exist_ok=True)
        
        print("Saving results...")
        distance_data.to_csv(output_dir / "distance_analysis.csv", index=False)
        patterns.to_csv(output_dir / "workspace_patterns.csv")
        stats.to_csv(output_dir / "workspace_statistics.csv")
        
        print("Analysis complete! Results saved to:", output_dir)
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        raise

if __name__ == "__main__":
    main() 