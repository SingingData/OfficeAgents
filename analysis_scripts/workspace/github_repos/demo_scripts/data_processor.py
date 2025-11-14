#!/usr/bin/env python3
import json
from datetime import datetime

print("[DATA] Processing sample data...")

data = {
    "timestamp": datetime.now().isoformat(),
    "items": [i * 2 for i in range(5)],
    "total": sum(i * 2 for i in range(5))
}

print(f"Processed {len(data['items'])} items")
print(f"Total: {data['total']}")
print("✅ Data processing complete!")
