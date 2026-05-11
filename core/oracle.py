#!/usr/bin/env python3
import json, time, os, random
from datetime import datetime

DATA_FILE = os.path.expanduser("~/cortex/data/state.json")

def get_reality():
    return {
        "timestamp": datetime.now().isoformat(),
        "world": {
            "h_index": round(random.uniform(2.0, 4.5), 2),
            "crisis_level": random.randint(60, 90)
        },
        "economy": {
            "gold": 2355.40,
            "btc": 64100.00
        }
    }

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    while True:
        with open(DATA_FILE, 'w') as f:
            json.dump(get_reality(), f, indent=2)
        time.sleep(10)
