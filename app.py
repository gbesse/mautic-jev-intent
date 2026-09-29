"""Mautic form-submit intent to a contact custom field."""
import base64
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request,urlopen
from jev_core import decide
from webhook import make_app,serve
POLICY=json.loads(Path(__file__).with_name("policy.json").read_text())

def process(event, *, evaluate=decide, update=None):
    results=[]
    for entry in event.get("mautic.form_on_submit",[]):
        submission=entry.get("submission") or {}
        contact=submission.get("lead") or {}
        fields=submission.get("results") or {}
        field=os.environ.get("MAUTIC_MESSAGE_FIELD","message")
        text=fields.get(field,"") if isinstance(fields,dict) else ""
        if not isinstance(contact.get("id"),int) or not isinstance(text,str) or not text.strip(): continue
        result=evaluate(text,POLICY,os.environ["TYPESAFE_API_KEY"])
        (update or update_contact)(contact["id"],result["outcome"])
        results.append({"contactId":contact["id"],"decision":result})
    return results

def update_contact(contact_id,outcome):
    base=os.environ["MAUTIC_URL"].rstrip("/")
    if not base.startswith("https://"): raise ValueError("HTTPS required")
    user=os.environ["MAUTIC_API_USER"]; password=os.environ["MAUTIC_API_PASSWORD"]
    auth=base64.b64encode(f"{user}:{password}".encode()).decode()
    field=os.environ.get("MAUTIC_INTENT_FIELD","jev_intent")
    req=Request(f"{base}/api/contacts/{contact_id}/edit",data=urlencode({field:outcome}).encode(),headers={"Authorization":"Basic "+auth,"Content-Type":"application/x-www-form-urlencoded"},method="PATCH")
    with urlopen(req,timeout=15) as response: response.read()

if __name__=="__main__":
    serve(make_app(process,secret=os.environ["MAUTIC_WEBHOOK_SECRET"],header="HTTP_WEBHOOK_SIGNATURE",scheme="base64-sha256"))
