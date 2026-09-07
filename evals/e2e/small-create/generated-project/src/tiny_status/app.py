import json
import os

def health_response():
    return 200, {"Content-Type":"application/json"}, json.dumps({"status":"ok"}, separators=(",",":"))

def message_response(env=None):
    values=os.environ if env is None else env
    return 200, {"Content-Type":"application/json"}, json.dumps({"message":values.get("STATUS_MESSAGE","Hello")}, separators=(",",":"))
