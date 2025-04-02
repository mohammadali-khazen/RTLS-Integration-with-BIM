# RTLS Integration with BIM

A Python-based system for integrating Real-Time Location System (RTLS) data with Building Information Modeling (BIM) data to analyze workspace occupancy and patterns.

## Overview

This system helps track and analyze the movement of workers within different workspaces defined in a BIM model. It processes both BIM model data (exported from Revit) and RTLS location data to provide insights into workspace occupancy and patterns.

## Key Features

- **BIM Model Integration**: Process workspace definitions and boundaries from Revit exports
- **RTLS Data Analysis**: Track and analyze worker movements in real-time
- **Geometric Analysis**: Calculate distances and workspace occupancy using advanced algorithms
- **Statistical Analysis**: Generate comprehensive workspace statistics and patterns

## Project Structure

```
.
├── data/               # Data directory for input/output files
├── src/               # Source code
│   ├── config.py      # Configuration settings
│   ├── data_processor.py  # Data loading and preprocessing
│   ├── geometry.py    # Geometric calculations
│   ├── workspace_analyzer.py  # Workspace analysis
│   └── main.py        # Main entry point
├── tests/             # Test files
├── requirements.txt   # Project dependencies
└── README.md         # This file
```

## Quick Start

1. **Install Dependencies**:

```bash
pip install -r requirements.txt
```

2. **Prepare Data**:

   - Place your BIM model data CSV file in the `data` directory
   - Place your RTLS location data CSV file in the `data` directory

3. **Run Analysis**:

```bash
python -m src.main
```

4. **View Results**:
   - Check the `data/output` directory for analysis results
   - Review workspace statistics and patterns in the generated CSV files

## Input Data Requirements

### BIM Model Data

- CSV file exported from Revit
- Must include workspace vertices (X1,Y1,Z1 to X4,Y4,Z4)
- Should contain workspace type and description

### RTLS Location Data

- CSV file with timestamp and coordinates
- Format: timestamp, location_X, location_Y