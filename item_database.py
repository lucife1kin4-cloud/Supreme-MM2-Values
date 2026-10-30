import json
import os

class ItemDatabase:
def init(self, filename="values.json"):
self.filename = filename
self.items = {}
self.load_database()

def load_database(self):
if os.path.exists(self.filename):
try:
with open(self.filename, "r", encoding="utf-8") as file:
data = json.load(file)
if isinstance(data, dict):
self.items = data
else:
self.items = {}
except json.JSONDecodeError:
self.items = {}
except Exception:
self.items = {}
else:
self.items = {}

def save_database(self):
try:
with open(self.filename, "w", encoding="utf-8") as file:
json.dump(self.items, file, ensure_ascii=False, indent=4)
except Exception:
pass

def update_items(self, raw_data):
if not raw_data or not isinstance(raw_data, dict):
return False

processed_data = {}
for name, value in raw_data.items():
clean_name = str(name).strip()
try:
clean_value = int(value)
except (ValueError, TypeError):
clean_value = 0

processed_data[clean_name] = clean_value

self.items = processed_data
self.save_database()
return True

def get_value(self, item_name):
clean_name = str(item_name).strip()
if clean_name in self.items:
return self.items[clean_name]

for name, value in self.items.items():
if name.lower() == clean_name.lower():
return value

return 0

def search_items(self, query):
query = str(query).strip().lower()
results = {}
for name, value in self.items.items():
if query in name.lower():
results[name] = value
return results

def calculate_trade(self, my_items, their_items):
my_total = sum(self.get_value(item) for item in my_items)
their_total = sum(self.get_value(item) for item in their_items)
diff = their_total - my_total
percentage = ((their_total - my_total) / my_total * 100) if my_total > 0 else 0
return {
"my_total": my_total,
"their_total": their_total,
"difference": diff,
"win_percentage": round(percentage, 2)
}

db = ItemDatabase()
