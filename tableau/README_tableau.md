# Tableau Dashboards - NYC TLC Trip Duration Analysis

This directory contains Tableau workbooks for visualizing the NYC TLC trip duration prediction project.

## Dashboards Overview

### Dashboard 1: Data Quality & Pipeline Monitoring
**Purpose:** Monitor data quality and preprocessing pipeline performance

**Key Visualizations:**
- Data volume over time (trips per month/day)
- Missing value analysis by column
- Outlier detection (trip distance, fare amount, duration)
- Data distribution histograms
- Geographic distribution of pickups/dropoffs
- Data quality score card

**Metrics:**
- Total records processed
- Records filtered/cleaned
- Null value percentages
- Data size (GB)

### Dashboard 2: Model Performance & Feature Importance
**Purpose:** Compare model performance and understand feature contributions

**Key Visualizations:**
- Model comparison bar charts (RMSE, R², MAE)
- Feature importance horizontal bar chart
- Predictions vs Actual scatter plot
- Residuals distribution
- Error metrics by model type
- Training time comparison

**Metrics:**
- RMSE (Root Mean Squared Error)
- R² Score
- MAE (Mean Absolute Error)
- Training time per model

### Dashboard 3: Business Insights & Recommendations
**Purpose:** Provide actionable insights for taxi operations

**Key Visualizations:**
- Trip duration by time of day (heatmap)
- Average trip duration by day of week
- Trip distance vs duration scatter
- Popular pickup/dropoff locations (map)
- Rush hour impact analysis
- Fare amount distribution
- Tip percentage analysis
- Weekend vs weekday patterns

**Insights:**
- Peak hours identification
- High-demand locations
- Optimal pricing strategies
- Driver allocation recommendations

### Dashboard 4: Scalability & Performance Analysis
**Purpose:** Analyze big data processing performance and costs

**Key Visualizations:**
- Processing time vs data size
- Memory usage over time
- Spark job execution timeline
- Partition distribution
- Strong scaling analysis (speedup chart)
- Weak scaling analysis
- Cost-performance tradeoff

**Metrics:**
- Records processed per second
- Memory utilization (GB)
- CPU utilization (%)
- Execution time by stage
- Cost per million records

## Data Sources

### Primary Data Source
- **Type:** Parquet files
- **Location:** `../data/processed/`
- **Files:**
  - `nyc_tlc_features` - Engineered features
  - `model_comparison.csv` - Model performance metrics
  - `test_results.csv` - Test set evaluation
  - `feature_importance.csv` - Feature importance scores
  - `error_by_distance.csv` - Error analysis by distance
  - `error_by_time.csv` - Error analysis by time

### Connection Setup

#### Option 1: Direct File Connection
1. Open Tableau Desktop
2. Connect to Data → More → Parquet
3. Navigate to `data/processed/` directory
4. Select the parquet files

#### Option 2: CSV Connection (for aggregated results)
1. Open Tableau Desktop
2. Connect to Data → Text File
3. Select CSV files from `data/processed/`

## Creating the Dashboards

### Step 1: Data Preparation
1. Load all data sources into Tableau
2. Create relationships between datasets:
   - Join model results with feature importance
   - Link error analysis tables

### Step 2: Create Calculated Fields

**Prediction Error:**
```
ABS([Trip Duration Minutes] - [Prediction])
```

**Error Percentage:**
```
([Prediction Error] / [Trip Duration Minutes]) * 100
```

**Distance Category:**
```
IF [Trip Distance] < 2 THEN "Short"
ELSEIF [Trip Distance] < 5 THEN "Medium"
ELSEIF [Trip Distance] < 10 THEN "Long"
ELSE "Very Long"
END
```

**Time of Day:**
```
IF [Pickup Hour] >= 6 AND [Pickup Hour] < 12 THEN "Morning"
ELSEIF [Pickup Hour] >= 12 AND [Pickup Hour] < 18 THEN "Afternoon"
ELSEIF [Pickup Hour] >= 18 AND [Pickup Hour] < 22 THEN "Evening"
ELSE "Night"
END
```

### Step 3: Build Visualizations

#### Dashboard 1 - Data Quality
1. Create a line chart for trips over time
2. Add a heat map for missing values
3. Create box plots for outlier detection
4. Add KPI cards for data metrics

#### Dashboard 2 - Model Performance
1. Create bar charts for model comparison
2. Add scatter plot for predictions vs actual
3. Create horizontal bar chart for feature importance
4. Add histogram for residuals

#### Dashboard 3 - Business Insights
1. Create heat map for trip duration by hour/day
2. Add map visualization for pickup/dropoff locations
3. Create line charts for temporal patterns
4. Add comparison charts for weekend vs weekday

#### Dashboard 4 - Scalability
1. Create line chart for processing time vs data size
2. Add area chart for memory usage
3. Create Gantt chart for Spark job timeline
4. Add scatter plot for cost-performance analysis

### Step 4: Add Interactivity
- Add filters for date range, location, time of day
- Create parameter controls for model selection
- Add dashboard actions for drill-down
- Enable tooltips with detailed information

### Step 5: Design & Formatting
- Use consistent color scheme (blue for data, green for good metrics, red for errors)
- Add titles and descriptions
- Include data source information
- Add last updated timestamp
- Ensure mobile responsiveness

## Publishing to Tableau Public

### Step 1: Prepare Workbook
1. Ensure all data sources are embedded or publicly accessible
2. Remove any sensitive information
3. Test all interactivity

### Step 2: Publish
1. File → Save to Tableau Public As...
2. Sign in to Tableau Public account
3. Enter workbook name: "NYC TLC Trip Duration Prediction"
4. Add description and tags
5. Click "Save"

### Step 3: Get Shareable Link
1. After publishing, copy the workbook URL
2. Add this URL to your assignment report
3. Format: `https://public.tableau.com/views/[workbook-name]/[dashboard-name]`

## Best Practices

### Performance Optimization
- Use extracts instead of live connections for large datasets
- Aggregate data where possible
- Limit the number of marks displayed (< 10,000)
- Use context filters to improve performance
- Hide unused fields

### Data Storytelling
- Start with high-level overview (Dashboard 3)
- Provide technical details (Dashboards 1, 2, 4)
- Use annotations to highlight key insights
- Create a logical flow between dashboards
- Add explanatory text where needed

### Accessibility
- Use colorblind-friendly palettes
- Ensure sufficient contrast
- Add alt text to visualizations
- Make dashboards keyboard navigable
- Test on different screen sizes

## Troubleshooting

### Common Issues

**Issue:** Parquet files not loading
- **Solution:** Convert to CSV using pandas: `df.to_csv('output.csv')`

**Issue:** Slow dashboard performance
- **Solution:** Create extracts, reduce data granularity, use aggregations

**Issue:** Visualizations not updating
- **Solution:** Refresh data source, check data connections

**Issue:** Map not showing locations
- **Solution:** Ensure LocationID fields are properly geocoded or use latitude/longitude

## Additional Resources

- [Tableau Public Gallery](https://public.tableau.com/gallery)
- [Tableau Learning Resources](https://www.tableau.com/learn)
- [NYC TLC Data Dictionary](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

## Assignment Submission

Include in your report:
1. Tableau Public workbook URL
2. Screenshots of all 4 dashboards
3. Description of key insights from each dashboard
4. Explanation of design choices
5. Discussion of how visualizations support your analysis

## Contact

For questions about the dashboards, refer to the main project README or contact the module team.
