import csv
from collections import defaultdict
from rules import APP_CATEGORIES

INPUT_FILE = "app_log.csv"   # or your session file
MIN_DURATION = 5             # seconds (ignore micro-noise)

category_time = defaultdict(int)
unknown_apps = defaultdict(int)

with open(INPUT_FILE, newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        app = row["app"]
        duration = int(row["duration_seconds"])

        if duration < MIN_DURATION:
            continue

        category = APP_CATEGORIES.get(app)

        if category:
            category_time[category] += duration
        else:
            unknown_apps[app] += duration
            category_time["neutral"] += duration

print("\n=== Time by Category ===")
for cat, sec in category_time.items():
    print(f"{cat:12} {sec//60:4} min")

print("\n=== Unknown Apps (review later) ===")
for app, sec in unknown_apps.items():
    print(f"{app:20} {sec//60} min")
