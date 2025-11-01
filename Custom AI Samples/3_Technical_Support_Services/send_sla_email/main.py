import base64, json, os, smtplib, ssl
from email.message import EmailMessage
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent / "templates"

def parse_subject_and_body(text: str):
    first_newline = text.find("\n")
    header = text[:first_newline].strip()
    subject = header.replace("Subject:", "").strip() if header.lower().startswith("subject:") else "Notification"
    body = text[first_newline+1:].lstrip()
    return subject, body

def render_template(template_name: str, ctx: dict) -> str:
    path = TEMPLATE_DIR / template_name
    text = path.read_text(encoding="utf-8")
    for k, v in ctx.items():
        text = text.replace(f"{{{{{k}}}}}", str(v))
    return text

def send_email(to_addr: str, subject: str, body: str):
    host = os.getenv("EMAIL_SMTP_HOST")
    port = int(os.getenv("EMAIL_SMTP_PORT", "587"))
    user = os.getenv("EMAIL_SMTP_USER")
    pwd  = os.getenv("EMAIL_SMTP_PASS")
    sender = os.getenv("EMAIL_FROM", "no-reply@example.com")

    if not host or not user or not pwd:
        raise RuntimeError("SMTP env vars missing: EMAIL_SMTP_HOST/USER/PASS (and optional EMAIL_FROM/PORT)")

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP(host, port) as server:
        server.starttls(context=context)
        server.login(user, pwd)
        server.send_message(msg)

def sla_email_trigger(event, context):
    """Cloud Function entry point. Trigger: Pub/Sub (topic: sla-email-events).
    Expects a JSON payload with:
      complaint_id, email, customer_name, label, channel, priority,
      first_response_minutes, sla_minutes, sla_breached (bool)
    """
    if "data" not in event:
        print("No data in event")
        return

    data = json.loads(base64.b64decode(event["data"]).decode("utf-8"))
    print("Received SLA event:", data)

    ctx = {
        "complaint_id": data.get("complaint_id"),
        "customer_name": data.get("customer_name", "Customer"),
        "label": data.get("label"),
        "channel": data.get("channel"),
        "priority": data.get("priority"),
        "first_response_minutes": data.get("first_response_minutes"),
        "sla_minutes": data.get("sla_minutes"),
    }

    breached = bool(data.get("sla_breached", False))
    template = "apology_email.txt" if breached else "success_email.txt"

    rendered = render_template(template, ctx)
    subject, body = parse_subject_and_body(rendered)

    to_addr = data.get("email")
    if not to_addr:
        print("Missing destination email address in payload; skipping.")
        return

    send_email(to_addr, subject, body)
    print(f"Email sent to {to_addr} ({'Apology' if breached else 'Success'})")
