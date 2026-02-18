import csv
from collections import defaultdict
from rules import APP_CATEGORIES

INPUT_FILE = "app_log.csv"  # change if using timestamped file
FOCUS_THRESHOLD = 20 * 60   # 20 minutes in seconds
MIN_DURATION = 5            # ignore noise under 5 sec

category_time = defaultdict(int)
unknown_apps = defaultdict(int)

switch_count = 0
total_sessions = 0
longest_block = 0
focus_blocks = 0
total_duration = 0

last_app = None

with open(INPUT_FILE, newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        app = row["app"]
        duration = int(row["duration_seconds"])

        if duration < MIN_DURATION:
            continue

        total_sessions += 1
        total_duration += duration

        # Switch detection
        if last_app is not None and app != last_app:
            switch_count += 1
        last_app = app

        # Longest block
        if duration > longest_block:
            longest_block = duration

        # Focus block detection
        if duration >= FOCUS_THRESHOLD:
            focus_blocks += 1

        # Category aggregation
        category = APP_CATEGORIES.get(app)

        if category:
            category_time[category] += duration
        else:
            unknown_apps[app] += duration
            category_time["neutral"] += duration

# ---- OUTPUT ----

print("\n=== Time by Category ===")
for cat, sec in category_time.items():
    print(f"{cat:12} {sec//60:4} min")

print("\n=== Focus Metrics ===")
print(f"Total sessions:        {total_sessions}")
print(f"Total switches:        {switch_count}")
print(f"Longest block:         {longest_block//60} min")
print(f"Focus blocks >=20min:  {focus_blocks}")

if total_sessions > 0:
    avg_session = total_duration / total_sessions
    print(f"Average session:       {int(avg_session)//60} min")

print("\n=== Unknown Apps ===")
for app, sec in unknown_apps.items():
    print(f"{app:20} {sec//60} min")
