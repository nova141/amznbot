import json
from datetime import datetime

def structured_log(event, context=None, level="INFO"):
    print(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "event": event,
        "context": context or {}
    }))
    