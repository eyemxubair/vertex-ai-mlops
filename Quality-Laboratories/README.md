# Quality & Laboratories – Water Quality Monitoring

This pack contains **sample CSV data** and **ready-to-run Jupyter notebooks** for water quality monitoring and laboratory analysis (chemical & biological).

## Folder Structure
```
Quality-Laboratories/
├─ data/
│  ├─ water_quality_samples.csv         # 60 days × 3-hour readings for 3 stations
│  ├─ lab_thresholds.csv                # Illustrative thresholds (NOT regulatory advice)
│  ├─ qc_blanks_duplicates.csv          # Method blanks + primary/duplicate pairs (RPD, recovery)
│  └─ incidents_log.csv                 # Example incident log
├─ notebooks/
│  ├─ 01_data_overview_and_qc.ipynb     # Load, sanity checks, threshold flags, RPD, blanks/recovery
│  ├─ 02_eda_and_anomaly_detection.ipynb# EDA, z-score flags, IsolationForest anomalies
│  ├─ 03_compliance_and_wqi.ipynb       # Compliance %, simple WQI (illustrative)
│  └─ 04_time_series_forecasting.ipynb  # Daily means + ARIMA forecast for turbidity, nitrate
└─ README.md
```

## Quickstart
1. Open the notebooks in `notebooks/` (Jupyter/Lab/VS Code).
2. Ensure relative paths to `../data/*.csv` remain intact.
3. Run cells top-to-bottom. No internet is required.

## Notes
- Thresholds and WQI formulae are **illustrative** only. Replace with your regulatory standards.
- IsolationForest and ARIMA use default/simple settings for demonstration—tune per your data.
- Extend by adding metals (Pb, As), VOCs, pesticides, and more microbiological markers if needed.
