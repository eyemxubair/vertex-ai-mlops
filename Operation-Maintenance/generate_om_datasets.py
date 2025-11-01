# Operation-Maintenance/generate_om_datasets.py
"""
Generate synthetic datasets for Vertex AI O&M use-cases:
1) Demand Forecasting
2) Leak Detection
3) Predictive Maintenance
4) Emergency Management
"""

from __future__ import annotations
import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path

def generate_demand_forecasting(output_dir: str, start: datetime = datetime(2025, 1, 1),
                                zones=("Z1","Z2","Z3","Z4"), days: int = 60, seed: int = 42) -> str:
    np.random.seed(seed)
    rows_per_zone = 24 * days
    rows = []
    for z in zones:
        base = {"Z1": 120, "Z2": 100, "Z3": 140, "Z4": 90}.get(z, 110)
        for h in range(rows_per_zone):
            ts = start + timedelta(hours=h)
            dow, hour = ts.weekday(), ts.hour
            is_weekend = 1 if dow >= 5 else 0
            temp = 15 + 10*np.sin(2*np.pi*(h/24)/30) + np.random.normal(0, 1.5)
            diurnal = 25*np.exp(-((hour-7)/2.5)**2) + 20*np.exp(-((hour-19)/3.0)**2)
            demand = base + diurnal - 10*is_weekend + 1.2*temp + np.random.normal(0,6)
            rows.append([z, ts, hour, dow, is_weekend, round(temp,2), round(max(0,demand),2)])
    df = pd.DataFrame(rows, columns=["zone_id","timestamp","hour","day_of_week","is_weekend","temp_c","demand_m3"])
    path = os.path.join(output_dir, "demand_forecasting_timeseries.csv")
    df.to_csv(path, index=False)
    return path

def generate_leak_detection(output_dir: str, start: datetime = datetime(2025, 1, 1),
                            n_pipes: int = 50, hours: int = 24*14, seed: int = 42) -> str:
    np.random.seed(seed+1)
    rows = []
    pipes = [f"P{i:03d}" for i in range(1, n_pipes+1)]
    for p in pipes:
        pipe_len = np.random.uniform(0.5, 5.0)
        for h in range(hours):
            ts = start + timedelta(hours=h)
            diurnal = 30*np.exp(-((ts.hour-7)/2.8)**2) + 24*np.exp(-((ts.hour-19)/3.2)**2) + 50
            flow_in = max(10, diurnal + np.random.normal(0, 5))
            normal_loss = np.random.uniform(0.01, 0.03)
            flow_out = flow_in * (1 - normal_loss)
            pressure = max(1.0, 5.0 - 0.1*pipe_len + np.random.normal(0, 0.15))
            leak = 1 if np.random.rand() < 0.01 else 0
            if leak:
                extra = np.random.uniform(0.1, 0.3)
                flow_out = flow_in * (1 - (normal_loss + extra))
                pressure = max(0.5, pressure - np.random.uniform(0.3, 0.8))
            rows.append([p, ts, round(flow_in,2), round(flow_out,2), round(pressure,2), leak, round(pipe_len,2)])
    df = pd.DataFrame(rows, columns=["pipe_id","timestamp","flow_in_lps","flow_out_lps","pressure_bar","leak_label","pipe_length_km"])
    path = os.path.join(output_dir, "leak_detection_sensors.csv")
    df.to_csv(path, index=False)
    return path

def generate_predictive_maintenance(output_dir: str, start: datetime = datetime(2025, 2, 1),
                                    n_assets: int = 200, days: int = 60, seed: int = 42) -> str:
    np.random.seed(seed+2)
    rows = []
    assets = [f"A{i:03d}" for i in range(1, n_assets+1)]
    for a in assets:
        age_days = np.random.randint(100, 1800)
        for d in range(days):
            ts = start + timedelta(days=d)
            vib = np.random.normal(3.0 + 0.001*age_days, 0.4)
            temp = np.random.normal(55 + 0.005*age_days, 2.5)
            current = np.random.normal(50 + 0.002*age_days, 3.0)
            hours_since_maint = np.random.randint(0, 2000)
            risk = 1/(1+np.exp(-(-6 + 0.3*(vib-3.2) + 0.06*(temp-60) + 0.02*(current-52) + 0.0006*hours_since_maint)))
            failure = 1 if np.random.rand() < risk*0.6 else 0
            rows.append([a, ts.date(), round(vib,3), round(temp,2), round(current,2),
                         hours_since_maint, age_days, failure])
    df = pd.DataFrame(rows, columns=[
        "asset_id","date","vibration_mm_s","temperature_c","current_a",
        "hours_since_maintenance","asset_age_days","failure_within_7d"
    ])
    path = os.path.join(output_dir, "predictive_maintenance_assets.csv")
    df.to_csv(path, index=False)
    return path

def generate_emergency_management(output_dir: str, start: datetime = datetime(2025, 1, 1),
                                  days: int = 120, seed: int = 42) -> str:
    np.random.seed(seed+3)
    rows = []
    for d in range(days):
        ts = start + timedelta(days=d)
        rainfall = max(0, np.random.gamma(2, 3) - 2)
        outage = int(np.random.poisson(5 + 0.2*rainfall))
        alarms = int(np.random.poisson(8 + 0.3*outage))
        heat = np.random.normal(32, 4)
        sev_score = 0.2*rainfall + 0.4*outage + 0.5*alarms + 0.1*max(0, heat-35)
        sev = 0 if sev_score < 8 else 1 if sev_score < 16 else 2
        rows.append([ts.date(), round(rainfall,2), outage, alarms, round(heat,1), sev])
    df = pd.DataFrame(rows, columns=["date","rainfall_mm","outage_reports","sensor_alarm_count","heat_index_c","event_severity"])
    path = os.path.join(output_dir, "emergency_events_daily.csv")
    df.to_csv(path, index=False)
    return path

def generate_all(output_root: str = "Operation-Maintenance/sample_data") -> dict:
    output_dir = ensure_dir(output_root)
    return {
        "demand": generate_demand_forecasting(output_dir),
        "leak": generate_leak_detection(output_dir),
        "predictive_maintenance": generate_predictive_maintenance(output_dir),
        "emergency": generate_emergency_management(output_dir),
    }

if __name__ == "__main__":
    paths = generate_all()
    print("✅ Generated files:")
    for k, v in paths.items():
        print(f" - {k}: {v}")
