# Vertex AI Utilities – Sample Datasets & Notebooks
Generated: 2025-11-01T13:55:07

This package contains **5 domains** with sample CSVs and ready-to-run Jupyter notebooks:
1. Training – Personalized learning analytics and course recommendations.
2. Finance & Procurement – Budget forecasting and automated offer evaluation.
3. Technical Support Services – Ticket analytics, SLA tracking, and breach prediction.
4. Environment & Sustainability – Pollution analysis with anomaly detection alerts.
5. Data & Technology (SCADA + Assets) – Lightweight SCADA assistant demo and asset search.

Open each `*.ipynb` in Jupyter/Colab and run cells top-to-bottom. All notebooks are self-contained and rely only on common Python libraries.


# Custom AI Samples

This folder contains 5 ready-to-run scenarios with sample CSVs and Jupyter notebooks.

## How to run (local)
1) python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
2) pip install -r requirements.txt
3) jupyter lab  # or vscode/colab

> All notebooks assume CSVs are in the same folder as the notebook.

## Folders
- Training/: users.csv, courses.csv, course_interactions.csv, training_notebook.ipynb  
  *KPIs + content-based recommendations.*

- Finance_Procurement/: budget_history.csv, procurement_offers.csv, finance_procurement_notebook.ipynb  
  *Forecasting + multi-criteria supplier scoring.*

- Technical_Support_Services/: tickets.csv, technical_support_notebook.ipynb  
  *SLA KPIs + breach prediction.*

- Environment_Sustainability/: pollution_readings.csv, environment_notebook.ipynb  
  *Daily means + IsolationForest alerts.*

- Data_Technology_SCADA_Assistant/: scada_events.csv, digital_assets.csv, data_technology_notebook.ipynb  
  *SCADA Q&A rules + intent classifier + asset search.*

## (Optional) Run on Vertex AI Workbench
- Create a Workbench instance and open JupyterLab.
- Clone repo and `pip install -r requirements.txt`.

