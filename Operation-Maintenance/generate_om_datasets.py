import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

OUTPUT_DIR = "Operation-Maintenance/sample_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)
np.random.seed(42)

# 1️⃣ Demand Forecasting
start = datetime(2025, 1, 1)
zones = ["Z1", "Z2", "Z3", "Z4"]
records = []
for z in zones:
    for h in range(24 * 60):
        ts = start + timedelta(hours=h)
        dow = ts.weekday()
        hour = ts.hour
        is_weekend = 1 if dow >= 5 else 0
        temp = 15 + 10 * np.sin(2 * np.pi * (h / 24) / 30) + np.random.normal(0, 1.5)
        base = {"Z1": 120, "Z2": 100, "Z3": 140, "Z4": 90}[z]
        diurnal = 25 * np.exp(-((hour - 7) / 2.5)**2) + 20 * np.exp(-((hour - 19) / 3.0)**2)
        demand = base + diurnal + (-10 * is_weekend) + 1.2 * temp + np.random.normal(0, 6)
        records.append([z, ts, hour, dow, is_weekend, round(temp,2), round(demand,2)])
df = pd.DataFrame(records, columns=["zone_id","timestamp","hour","day_of_week","is_weekend","temp_c","demand_m3"])
df.to_csv(f"{OUTPUT_DIR}/demand_forecasting_timeseries.csv", index=False)

# 2️⃣ Leak Detection
pipes = [f"P{i:03d}" for i in range(1, 51)]
records = []
for p in pipes:
    pipe_len = np.random.uniform(0.5, 5.0)
    for h in range(24 * 14):
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
            pressure -= np.random.uniform(0.3, 0.8)
        records.append([p, ts, round(flow_in,2), round(flow_out,2), round(pressure,2), leak, round(pipe_len,2)])
df = pd.DataFrame(records, columns=["pipe_id","timestamp","flow_in_lps","flow_out_lps","pressure_bar","leak_label","pipe_length_km"])
df.to_csv(f"{OUTPUT_DIR}/leak_detection_sensors.csv", index=False)

# 3️⃣ Predictive Maintenance
assets = [f"A{i:03d}" for i in range(1, 201)]
records = []
for a in assets:
    age_days = np.random.randint(100, 1800)
    for d in range(60):
        ts = start + timedelta(days=d)
        vib = np.random.normal(3.0 + 0.001*age_days, 0.4)
        temp = np.random.normal(55 + 0.005*age_days, 2.5)
        current = np.random.normal(50 + 0.002*age_days, 3.0)
        hours_since_maint = np.random.randint(0, 2000)
        risk = 1/(1+np.exp(-(-6 + 0.3*(vib-3.2) + 0.06*(temp-60) + 0.02*(current-52) + 0.0006*hours_since_maint)))
        failure = 1 if np.random.rand() < risk*0.6 else 0
        records.append([a, ts.date(), round(vib,3), round(temp,2), round(current,2), hours_since_maint, age_days, failure])
df = pd.DataFrame(records, columns=["asset_id","date","vibration_mm_s","temperature_c","current_a","hours_since_maintenance","asset_age_days","failure_within_7d"])
df.to_csv(f"{OUTPUT_DIR}/predictive_maintenance_assets.csv", index=False)

# 4️⃣ Emergency Management
records = []
for d in range(120):
    ts = start + timedelta(days=d)
    rain = max(0, np.random.gamma(2,3) - 2)
    outage = np.random.poisson(5 + 0.2*rain)
    alarms = np.random.poisson(8 + 0.3*outage)
    heat = np.random.normal(32, 4)
    sev_score = 0.2*rain + 0.4*outage + 0.5*alarms + 0.1*max(0, heat-35)
    sev = 0 if sev_score < 8 else 1 if sev_score < 16 else 2
    records.append([ts.date(), round(rain,2), outage, alarms, round(heat,1), sev])
df = pd.DataFrame(records, columns=["date","rainfall_mm","outage_reports","sensor_alarm_count","heat_index_c","event_severity"])
df.to_csv(f"{OUTPUT_DIR}/emergency_events_daily.csv", index=False)

print("✅ All O&M CSVs generated in:", OUTPUT_DIR)
