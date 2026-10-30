class TradeCalculator:
def init(self, database=None):
self.db = database

def set_database(self, database):
self.db = database

def calculate_side_value(self, item_list):
if not self.db or not item_list:
return 0
total = 0
for item in item_list:
if item:
total += self.db.get_value(item)
return total

def evaluate_trade(self, my_items, their_items):
my_total = self.calculate_side_value(my_items)
their_total = self.calculate_side_value(their_items)
diff = their_total - my_total

ratio = 0.0
if my_total > 0:
ratio = (their_total / my_total) * 100

status = "EQUAL"
if diff > 0:
status = "WIN"
elif diff < 0:
status = "LOSE"

return {
"my_total": my_total,
"their_total": their_total,
"difference": diff,
"ratio_percentage": round(ratio, 2),
"status": status
}
trade_calc = TradeCalculator()
