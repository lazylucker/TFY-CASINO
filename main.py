from telegram.ext import Application, CallbackQueryHandler, MessageHandler, filters
from handlers import start, select_character, quest, casino
from config import TOKEN

app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))
app.add_handler(CallbackQueryHandler(select_character))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Квест"), quest))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Казино"), casino))

app.run_polling()
