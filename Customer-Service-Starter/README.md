# Customer Service – Vertex AI Starter Pack

This pack includes sample datasets and notebooks for:
- Intelligent complaint assistant (issue classification)
- Customer satisfaction analysis (CSAT, NPS, sentiment)
- Automated voice support (prototype with STT/TTS skeleton)

## Structure
Customer-Service/
  data/
    complaints_train.csv
    csat_surveys.csv
    intents.csv
    call_transcripts.csv
    knowledge_base.csv
  notebooks/
    00_quickstart_vertex_ai_setup.ipynb
    01_data_exploration_cleansing.ipynb
    02_issue_classification_model.ipynb
    03_csat_sentiment_analysis.ipynb
    04_automated_voice_support_prototype.ipynb
  src/
    utils.py

## How to use
1) Open 00_quickstart_vertex_ai_setup.ipynb and set PROJECT_ID, REGION.
2) Run 01_data_exploration_cleansing.ipynb to create train/val splits.
3) Train baseline or AutoML with 02_issue_classification_model.ipynb.
4) Explore CSAT, sentiment in 03_csat_sentiment_analysis.ipynb.
5) Prototype voice assistant flow in 04_automated_voice_support_prototype.ipynb.
