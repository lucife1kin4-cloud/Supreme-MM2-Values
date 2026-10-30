import time
import requests
from supreme_values import fetch_supreme_values
from database import db

class ValueUpdater:
def init(self, update_interval=3600):
self.update_interval = update_interval
self.last_update_time = 0
self.is_updating = False

def fetch_and_update(self):
if self.is_updating:
return False

self.is_updating = True
try:
new_data = fetch_supreme_values()
if new_data and isinstance(new_data, dict) and len(new_data) > 0:
success = db.update_items(new_data)
if success:
self.last_update_time = time.time()
self.is_updating = False
return True
self.is_updating = False
return False
except requests.exceptions.Timeout:
self.is_updating = False
return False
except requests.exceptions.ConnectionError:
self.is_updating = False
return False
except requests.exceptions.RequestException:
self.is_updating = False
return False
except Exception:
self.is_updating = False
return False

def should_update(self):
if self.last_update_time == 0:
return True
return (time.time() - self.last_update_time) >= self.update_interval

def start_auto_update_loop(self):
while True:
if self.should_update():
self.fetch_and_update()
time.sleep(60)

updater = ValueUpdater()

if name == "main":
result = updater.fetch_and_update()
print("Update status:", result)
