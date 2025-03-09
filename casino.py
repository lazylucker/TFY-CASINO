import random

def spin_slot():
    symbols = ["🍒", "🔔", "💰", "7️⃣"]
    result = [random.choice(symbols) for _ in range(3)]
    return result

def check_win(result):
    if len(set(result)) == 1:
        return True
    return False
def spin_slot_with_bonus(user):
    symbols = ["🍒", "🔔", "💰", "7️⃣"]
    result = [random.choice(symbols) for _ in range(3)]

    # Применение бонуса, если пользователь выиграл, увеличить вероятность выигрыша
    if user.completed_quests > 5:  # пример бонуса на основе квестов
        bonus_multiplier = 2  # Увеличиваем шанс на победу
        if random.random() < 0.5:
            result = [result[0], result[0], result[0]]  # Устанавливаем одинаковые символы
    else:
        bonus_multiplier = 1

    return result, bonus_multiplier

def check_win(result):
    if len(set(result)) == 1:
        return True
    return False
