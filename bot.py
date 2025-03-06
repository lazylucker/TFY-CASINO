import logging
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import requests

# Включаем логирование для отладки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота
TOKEN = '7884246690:AAHdoMN0p_T3ZW0WJYfL1ZhBLTlx-KSOdo4'

# Лидерборд (счёт игроков)
leaderboard = {}

# Список доступных квестов
quests = {
    1: {"name": "Пройти слот-игру 5 раз", "completed": False},
    2: {"name": "Победить в игре и выиграть 1000 монет", "completed": False}
}

# Функция старта
async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    leaderboard[user.id] = {"name": user.full_name, "coins": 0}
    await update.message.reply_text(f"Привет, {user.mention_html()}! Добро пожаловать в TFY CASINO! Чтобы начать, нажми кнопку ниже.", parse_mode="HTML", reply_markup=main_menu_keyboard())

# Главное меню
def main_menu_keyboard():
    from telegram import ReplyKeyboardMarkup
    buttons = [
        ["Играть", "Таблица лидеров"],
        ["Квесты", "Помощь"]
    ]
    return ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

# Функция для кнопок "Играть" и "Таблица лидеров"
async def handle_buttons(update: Update, context: CallbackContext):
    text = update.message.text

    if text == "Играть":
        await play_game(update, context)
    elif text == "Таблица лидеров":
        await show_leaderboard(update, context)
    elif text == "Квесты":
        await show_quests(update, context)

# Пример игровой функции
async def play_game(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    # Играем в слот (просто пример)
    game_result = random.choice(["выигрыш", "проигрыш"])
    
    if game_result == "выигрыш":
        reward = random.randint(100, 500)
        leaderboard[user_id]["coins"] += reward
        await update.message.reply_text(f"Поздравляю, ты выиграл! Приз: {reward} монет.")
    else:
        await update.message.reply_text("К сожалению, ты проиграл. Попробуй снова!")

    # Обновляем квесты
    await update_quests(update, context)

# Лидерборд (таблица лидеров)
async def show_leaderboard(update: Update, context: CallbackContext):
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1]["coins"], reverse=True)
    leaderboard_text = "Таблица лидеров:\n"
    
    for index, (user_id, user_info) in enumerate(sorted_leaderboard, 1):
        leaderboard_text += f"{index}. {user_info['name']} - {user_info['coins']} монет\n"
    
    await update.message.reply_text(leaderboard_text)

# Квесты
async def show_quests(update: Update, context: CallbackContext):
    quests_text = "Доступные квесты:\n"
    for quest_id, quest_info in quests.items():
        status = "Завершен" if quest_info["completed"] else "Не завершен"
        quests_text += f"{quest_id}. {quest_info['name']} - {status}\n"
    await update.message.reply_text(quests_text)

# Обновление квестов
async def update_quests(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    # Условие для выполнения квеста 1 (пример)
    if leaderboard[user_id]["coins"] >= 500 and not quests[1]["completed"]:
        quests[1]["completed"] = True
        await update.message.reply_text("Квест 'Пройти слот-игру 5 раз' завершен!")
    
    # Условие для выполнения квеста 2 (пример)
    if leaderboard[user_id]["coins"] >= 1000 and not quests[2]["completed"]:
        quests[2]["completed"] = True
        await update.message.reply_text("Квест 'Победить в игре и выиграть 1000 монет' завершен!")

# Обработчик команд
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Команды:\n/start - Начать\n/leaderboard - Таблица лидеров\n/help - Помощь")

# Основная функция
def main():
    # Создаем объект приложения
    application = Application.builder().token(TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
