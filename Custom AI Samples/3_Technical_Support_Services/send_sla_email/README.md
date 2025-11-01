# send_sla_email – Cloud Function (Pub/Sub → Email)

## Deploy
```
gcloud functions deploy send_sla_email \
  --runtime python311 \
  --trigger-topic=sla-email-events \
  --entry-point=sla_email_trigger \
  --region=us-central1 \
  --set-env-vars="EMAIL_SMTP_HOST=smtp.gmail.com,EMAIL_SMTP_PORT=587,EMAIL_SMTP_USER=<your_user>,EMAIL_SMTP_PASS=<your_pass>,EMAIL_FROM=support@yourdomain.com"
```

## Payload (example)
Published by your Vertex AI notebook to Pub/Sub topic `sla-email-events`:
```json
{
  "complaint_id": 1234,
  "email": "user@example.com",
  "customer_name": "Ahmed",
  "label": "billing_issue",
  "channel": "email",
  "priority": "high",
  "first_response_minutes": 160,
  "sla_minutes": 120,
  "sla_breached": true
}
```

## Security
- Prefer Secret Manager for SMTP creds:
```
gcloud secrets create smtp-user --data-file=<(echo -n '<your_user>')
gcloud secrets create smtp-pass --data-file=<(echo -n '<your_pass>')
gcloud functions deploy send_sla_email \
  --runtime python311 \
  --trigger-topic=sla-email-events \
  --entry-point=sla_email_trigger \
  --region=us-central1 \
  --set-env-vars="EMAIL_SMTP_HOST=smtp.gmail.com,EMAIL_SMTP_PORT=587,EMAIL_FROM=support@yourdomain.com" \
  --set-secrets="EMAIL_SMTP_USER=smtp-user:latest,EMAIL_SMTP_PASS=smtp-pass:latest"
```



## Hook from your Vertex AI notebook

- Hook from your Vertex AI notebook
```

from google.cloud import pubsub_v1
import json, os

PROJECT_ID = os.environ.get("PROJECT_ID","your-gcp-project-id")
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, "sla-email-events")

def publish_sla_event(row):
    payload = {
        "complaint_id": int(row["complaint_id"]),
        "email": row.get("email","unknown@example.com"),
        "customer_name": row.get("customer_name","Customer"),
        "label": row["label"],
        "channel": row["channel"],
        "priority": row["priority"],
        "first_response_minutes": int(row["first_response_minutes"]),
        "sla_minutes": int(row["sla_minutes"]),
        "sla_breached": bool(row["sla_breached"])
    }
    future = publisher.publish(topic_path, data=json.dumps(payload).encode("utf-8"))
    _ = future.result()

for _, r in df.iterrows():
    publish_sla_event(r)


```


