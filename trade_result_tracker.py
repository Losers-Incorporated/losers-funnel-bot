import json
import os
import pandas as pd
from datetime import datetime
from collections import defaultdict

LOG_DIR = "logs"
WEIGHTS_FILE = "engine_weights.json"

# Decay settings
DECAY_RATE = 0.95  # older trades are worth 95% per day older
FAILURE_PENALTY = 0.9  # failed trades reduce importance of their indicators

# Buckets to score (slope, RSI, volume)
metrics = ["slope", "rsi", "volume"]

# Initialize score storage
weighted_scores = defaultdict(float)
count_weights = defaultdict(float)

# Process all logs
for filename in os.listdir(LOG_DIR):
    if not filename.endswith(".json"):
        continue
    path = os.path.join(LOG_DIR, filename)
    with open(path, "r") as f:
        entries = json.load(f)

    for entry in entries:
        result = entry.get("result", "unknown")
        if result not in ["success", "failure"]:
            continue

        # Calculate time decay
        try:
            days_old = (datetime.now() - datetime.fromisoformat(entry["timestamp"])).days
        except:
            days_old = 0

        decay = DECAY_RATE ** days_old
        multiplier = decay * (1 if result == "success" else FAILURE_PENALTY)

        for metric in metrics:
            value = float(entry.get(metric, 0))
            weighted_scores[metric] += value * multiplier
            count_weights[metric] += multiplier

# Compute weighted averages
updated_weights = {
    f"{metric}_weight": round(weighted_scores[metric] / count_weights[metric], 4)
    if count_weights[metric] else 1.0
    for metric in metrics
}

# Save weights to JSON
with open(WEIGHTS_FILE, "w") as f:
    json.dump(updated_weights, f, indent=2)

print("✅ Updated engine weights with decay + penalty logic:")
print(updated_weights)
