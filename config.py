import json
import os

class Config:
def init(self, config_filename="config.json"):
self.config_filename = config_filename
self.default_config = {
"update_interval": 3600,
"data_source_url": "https://supremevalues.com/mm2/",
"db_filename": "values.json",
"auto_update": True,
"ui": {
"theme": "dark",
"show_profit_percentage": True,
"transparency": 0.1
}
}
self.settings = {}
self.load_config()

def load_config(self):
if os.path.exists(self.config_filename):
try:
with open(self.config_filename, "r", encoding="utf-8") as f:
user_settings = json.load(f)
if isinstance(user_settings, dict):
self.settings = {self.default_config, user_settings}
else:
self.settings = self.default_config.copy()
except Exception:
self.settings = self.default_config.copy()
else:
self.settings = self.default_config.copy()
self.save_config()

def save_config(self):
try:
with open(self.config_filename, "w", encoding="utf-8") as f:
json.dump(self.settings, f, ensure_ascii=False, indent=4)
return True
except Exception:
return False

def get(self, key, default=None):
return self.settings.get(key, default)

def set(self, key, value):
self.settings[key] = value
self.save_config()

config = Config()
