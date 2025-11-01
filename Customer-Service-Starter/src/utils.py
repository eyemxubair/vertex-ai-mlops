
import re
from typing import List

URL_RE = re.compile(r'https?://\S+')

def basic_clean(text: str) -> str:
    t = text.strip().lower()
    t = URL_RE.sub(' ', t)
    t = re.sub(r'[^a-z0-9\s]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def tokenize(text: str) -> List[str]:
    return basic_clean(text).split()

def simple_keywords_route(text: str) -> str:
    t = basic_clean(text)
    if any(k in t for k in ['cancel','close account']):
        return 'cancel_subscription'
    if any(k in t for k in ['refund','charged twice','double charge']):
        return 'refund_request'
    if any(k in t for k in ['down','outage','no signal']):
        return 'report_outage'
    if any(k in t for k in ['reset password','otp','log in','login']):
        return 'account_help'
    if any(k in t for k in ['plan','price','discount']):
        return 'plans_pricing'
    return 'general_query'
