import random

def spin_slot():
    symbols = ["🍒", "🔔", "💰", "7️⃣"]
    result = [random.choice(symbols) for _ in range(3)]
    return result

def check_win(result):
    if len(set(result)) == 1:
        return True
    return False
