import objc # type: ignore
from AppKit import NSWorkspace # type: ignore
from Foundation import NSObject, NSRunLoop, NSDate # type: ignore
from datetime import datetime
import csv
import os

LOG_FILE = "app_log.csv"

# Create file with header if not exists
with open(LOG_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["app", "start_time", "end_time", "duration_seconds"])

class AppObserver(NSObject):
    def init(self):
        self = objc.super(AppObserver, self).init()
        if self is None:
            return None

        self.last_app = None
        self.last_time = None
        return self

    def applicationActivated_(self, notification):
        now = datetime.now()
        app = notification.userInfo()["NSWorkspaceApplicationKey"]
        app_name = app.localizedName()

        if self.last_app is not None:
            duration = (now - self.last_time).total_seconds()
            if duration > 2:
                with open(LOG_FILE, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        self.last_app,
                        self.last_time.isoformat(),
                        now.isoformat(),
                        int(duration)
                    ])
            else:
                print(f"Ignored short duration for {self.last_app}: {duration} seconds")

        self.last_app = app_name
        self.last_time = now
        print(f"Switched to {app_name}")

ws = NSWorkspace.sharedWorkspace()
observer = AppObserver()

nc = ws.notificationCenter()
nc.addObserver_selector_name_object_(
    observer,
    "applicationActivated:",
    "NSWorkspaceDidActivateApplicationNotification",
    None
)

print("Logging app usage… (Ctrl+C to stop)")

run_loop = NSRunLoop.currentRunLoop()
while True:
    run_loop.runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(1))
