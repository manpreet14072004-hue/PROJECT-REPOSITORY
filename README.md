# NYC TLC Trip Duration Prediction - Big Data ML Project

This project implements a complete machine learning pipeline using PySpark to predict NYC taxi trip durations from the TLC Trip Record dataset.

## Project Overview

**Dataset:** NYC Taxi and Limousine Commission (TLC) Trip Record Data  
**Problem Type:** Regression (predicting trip duration in minutes)  
**Dataset Size:** 1.16 GB (24 months: 2022-2023 data)  
**Features:** 18+ original columns, 25+ engineered features  
**Models:** Linear Regression, Decision Tree, Random Forest, Gradient Boosted Trees

## Directory Structure

```
project/
├── notebooks/              # Jupyter notebooks for analysis
│   ├── 1_data_ingestion.ipynb
│   ├── 2_feature_engineering.ipynb
│   ├── 3_model_training.ipynb
│   └── 4_evaluation.ipynb
├── tableau/               # Tableau dashboards
│   ├── dashboard1.twbx
│   ├── dashboard2.twbx
│   └── README_tableau.md
├── scripts/               # Executable Python scripts
│   ├── setup_environment.sh
│   ├── run_pipeline.py
│   └── performance_profiler.py
├── config/                # Configuration files
│   ├── spark_config.yaml
│   └── tableau_config.json
├── data/                  # Data storage
│   ├── schemas/
│   └── samples/
├── tests/                 # Unit tests
│   └── test_pipeline.py
├── .gitignore
├── environment.yml        # Conda dependencies
├── Dockerfile
└── README.md
```

## Dataset Information

**Source:** NYC Taxi and Limousine Commission (TLC)  
**URL:** https://registry.opendata.aws/nyc-tlc-trip-records-pds/  
**Alternative:** https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

### Dataset Requirements (Met)
- Size: >1GB (multiple parquet files)
- Columns: 18+ original features + engineered features
- Records: Millions of taxi trips
- Not from Kaggle
- Real-world problem

### Data Download Instructions

1. **Option 1: Automated Download (Recommended)**
   ```bash
   python scripts/download_data.py
   ```
   This will download 24 months of data (2022-2023) totaling ~1.16 GB

2. **Option 2: Manual Download**
   - Visit: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
   - Download Yellow Taxi Trip Records (Parquet format)
   - Download 2022-01 through 2023-12 (24 files)
   - Place files in `data/raw/` directory

3. **Option 3: AWS CLI**
   ```bash
   aws s3 cp s3://nyc-tlc/trip data/yellow_tripdata_2022-01.parquet data/raw/ --no-sign-request
   aws s3 cp s3://nyc-tlc/trip data/yellow_tripdata_2022-02.parquet data/raw/ --no-sign-request
   # Continue for all months...
   ```

## Setup Instructions

### Using Conda (Recommended)

1. **Create environment:**
   ```bash
   conda env create -f environment.yml
   ```

2. **Activate environment:**
   ```bash
   conda activate project-env
   ```

3. **Download data** (see Dataset Information above)

4. **Run setup script (Linux/Mac):**
   ```bash
   bash scripts/setup_environment.sh
   ```

   **Windows:**
   ```cmd
   conda activate project-env
   ```

### Using Docker

```bash
docker build -t nyc-tlc-ml .
docker run nyc-tlc-ml
```

## Running the Pipeline

### Complete Pipeline
Execute the complete pipeline:

```bash
python scripts/run_pipeline.py
```

### Step-by-Step Execution

Run notebooks in sequence:

1. **Data Ingestion** (`notebooks/1_data_ingestion.ipynb`)
   - Loads NYC TLC parquet files
   - Performs initial data validation
   - Filters invalid records
   - Saves cleaned data

2. **Feature Engineering** (`notebooks/2_feature_engineering.ipynb`)
   - Creates temporal features (hour, day, month, rush hour)
   - Calculates speed and distance features
   - Engineers location-based features
   - Handles missing values
   - Saves engineered features

3. **Model Training** (`notebooks/3_model_training.ipynb`)
   - Trains 4+ regression models
   - Performs hyperparameter tuning
   - Compares model performance
   - Saves trained models

4. **Evaluation** (`notebooks/4_evaluation.ipynb`)
   - Evaluates models on test set
   - Generates visualizations
   - Analyzes errors
   - Exports results for Tableau

## Project Structure

```
project/
├── notebooks/              # Jupyter notebooks for analysis
│   ├── 1_data_ingestion.ipynb       # Load and clean NYC TLC data
│   ├── 2_feature_engineering.ipynb  # Create features
│   ├── 3_model_training.ipynb       # Train ML models
│   └── 4_evaluation.ipynb           # Evaluate and visualize
├── tableau/               # Tableau dashboards
│   ├── dashboard1.twbx              # Data Quality Dashboard
│   ├── dashboard2.twbx              # Model Performance Dashboard
│   └── README_tableau.md            # Tableau documentation
├── scripts/               # Executable Python scripts
│   ├── setup_environment.sh         # Environment setup
│   ├── run_pipeline.py              # Pipeline orchestration
│   └── performance_profiler.py      # Performance monitoring
├── config/                # Configuration files
│   ├── spark_config.yaml            # Spark settings
│   └── tableau_config.json          # Tableau settings
├── data/                  # Data storage
│   ├── raw/                         # Original parquet files
│   ├── processed/                   # Cleaned and engineered data
│   ├── schemas/                     # Data schemas
│   └── samples/                     # Sample datasets
├── models/                # Trained models (created during training)
├── tests/                 # Unit tests
│   └── test_pipeline.py
├── .gitignore
├── environment.yml        # Conda dependencies
├── Dockerfile
└── README.md
```

## Machine Learning Models

This project implements 4 regression algorithms using PySpark MLlib:

1. **Linear Regression**
   - Baseline model
   - Fast training
   - Interpretable coefficients

2. **Decision Tree Regressor**
   - Non-linear relationships
   - Feature importance
   - No feature scaling required

3. **Random Forest Regressor**
   - Ensemble method
   - Robust to overfitting
   - Feature importance ranking

4. **Gradient Boosted Trees (GBT)**
   - Sequential ensemble
   - High accuracy
   - Handles complex patterns

### Model Evaluation Metrics
- RMSE (Root Mean Squared Error)
- R² Score (Coefficient of Determination)
- MAE (Mean Absolute Error)

## Features

### Original Features (18)
- VendorID, pickup/dropoff datetime, passenger count
- Trip distance, fare amount, payment type
- Pickup/dropoff location IDs
- Rate code, store and forward flag
- Extra charges, tolls, tips, surcharges

### Engineered Features (25+)
- **Temporal:** hour, day, month, year, time_of_day, is_weekend, is_rush_hour
- **Distance/Speed:** avg_speed_mph, distance_category, fare_per_mile
- **Location:** same_location, is_popular_pickup, is_popular_dropoff
- **Payment:** total_extras, tip_percentage, is_high_tipper
- **Target:** trip_duration_minutes

## Tableau Dashboards

Four interactive dashboards are created:

1. **Data Quality & Pipeline Monitoring**
   - Data volume trends
   - Missing value analysis
   - Outlier detection
   - Geographic distribution

2. **Model Performance & Feature Importance**
   - Model comparison charts
   - Feature importance rankings
   - Predictions vs actual
   - Residual analysis

3. **Business Insights & Recommendations**
   - Trip patterns by time/location
   - Peak hour analysis
   - Fare and tip analysis
   - Operational recommendations

4. **Scalability & Performance Analysis**
   - Processing time metrics
   - Memory utilization
   - Spark job performance
   - Cost-performance tradeoffs

See [tableau/README_tableau.md](tableau/README_tableau.md) for detailed dashboard documentation.

## Running Tests

```bash
pytest tests/
```

## Jupyter Notebooks

Start Jupyter Lab:

```bash
jupyter lab
```

Navigate to the `notebooks/` directory and open notebooks in sequence.

## Performance Monitoring

Profile pipeline performance:

```bash
python scripts/performance_profiler.py
```

## Configuration

- **Spark Configuration:** `config/spark_config.yaml`
  - Memory settings
  - Executor configuration
  - Shuffle partitions
  
- **Tableau Configuration:** `config/tableau_config.json`
  - Server connection
  - Data sources
  - Refresh schedule

Update these files according to your environment and requirements.

## Assignment Requirements Checklist

### Big Data Requirements
- Dataset size >1GB
- 18+ columns/features
- Not from Kaggle
- Real-world problem

### Technical Requirements
- PySpark data engineering (ingestion, partitioning, optimization)
- 4+ MLlib algorithms implemented
- Distributed training & hyperparameter tuning
- Scalability analysis
- 4 Tableau dashboards
- Comprehensive model evaluation

### Deliverables
- Project repository with proper structure
- Jupyter notebooks (4 notebooks)
- Tableau workbooks (4 dashboards)
- Configuration files
- Documentation (README files)
- Test suite

## Key Results

Expected outcomes after running the pipeline:

- **Data Processing:** Millions of records processed efficiently
- **Model Performance:** R² > 0.7, RMSE < 5 minutes
- **Feature Importance:** Trip distance, time of day, location most important
- **Business Insights:** Rush hour significantly impacts trip duration
- **Scalability:** Linear scaling with data size up to 10GB

## Troubleshooting

### Common Issues

**Issue:** Out of memory errors
- **Solution:** Increase `spark.driver.memory` and `spark.executor.memory` in config
- Reduce `spark.sql.shuffle.partitions`
- Process data in smaller batches

**Issue:** Slow data loading
- **Solution:** Use Parquet format (already implemented)
- Increase number of partitions
- Enable Spark adaptive execution (already enabled)

**Issue:** Model training takes too long
- **Solution:** Reduce hyperparameter grid size
- Use smaller sample for initial testing
- Increase parallelism in CrossValidator

**Issue:** Tableau can't connect to data
- **Solution:** Export to CSV format
- Use Tableau extracts instead of live connection
- Check file paths are correct

## Requirements

- Python 3.9+
- Apache Spark 3.1+
- Tableau Desktop/Public (for dashboards)
- 8GB+ RAM recommended
- 10GB+ disk space for data

## Documentation

- [Tableau Dashboards Guide](tableau/README_tableau.md)
- [NYC TLC Data Dictionary](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

## License

This project is for educational purposes as part of the 7006SCN Machine Learning and Big Data module at Coventry University.

## Acknowledgments

- NYC Taxi and Limousine Commission for providing the dataset
- Apache Spark community
- Coventry University Module Team

## Contact

For questions about this project, contact the module team or refer to the assignment brief.
