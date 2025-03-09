from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import session, User
from quests import characters, assign_quest

async def start(update, context):
    user_id = update.effective_user.id
    user = session.query(User).filter_by(telegram_id=user_id).first()
    
    if not user:
        keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in characters.keys()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Выбери персонажа:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Ты уже выбрал персонажа!")

async def select_character(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    character = query.data

    user = User(telegram_id=user_id, character=character)
    session.add(user)
    session.commit()

    await query.answer(f"Ты выбрал {character}!")
    await query.message.reply_text(f"Теперь ты можешь получать квесты!")

async def quest(update, context):
    user_id = update.effective_user.id
    user = session.query(User).filter_by(telegram_id=user_id).first()

    if user:
        quest_name = assign_quest(user)
        await update.message.reply_text(f"Твой квест: {quest_name}")
    else:
        await update.message.reply_text("Сначала выбери персонажа через /start")
