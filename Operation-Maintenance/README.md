# Operations & Maintenance – Vertex AI MLOps Datasets

This module provides **synthetic datasets** to test end-to-end MLOps workflows on Google Vertex AI for:

| Use Case | Description | Dataset | ML Task |
|-----------|--------------|----------|----------|
| Demand Forecasting | Hourly water demand per zone | `demand_forecasting_timeseries.csv` | Time Series Forecast |
| Leak Detection | Flow/pressure telemetry | `leak_detection_sensors.csv` | Anomaly Detection |
| Predictive Maintenance | Asset vibration/temp/current telemetry | `predictive_maintenance_assets.csv` | Binary Classification |
| Emergency Management | System daily events | `emergency_events_daily.csv` | Multiclass Classification |

### Run Locally

```bash
python Operation-Maintenance/generate_om_datasets.py
```

This creates all CSVs in `Operation-Maintenance/sample_data/`.

### Next Steps
- Upload generated CSVs to your GCS bucket  
- Load into BigQuery (`om_demo` dataset)
- Train and deploy models via Vertex AI (refer to MLOps notebooks)
