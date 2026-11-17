import logging
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Mengambil token dan API key secara aman dari sistem Cloud
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY_AI = os.getenv("API_KEY_AI")
AI_URL = "https://api.deepseek.com/chat/completions"

logging.basicConfig(level=logging.INFO)

def tanya_ai(pesan_user):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY_AI}"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Kamu adalah asisten AI yang ramah dan siap membantu di Telegram."},
            {"role": "user", "content": pesan_user}
        ],
        "stream": False
    }
    try:
        response = requests.post(AI_URL, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Maaf, terjadi kendala pada server AI (Kode: {response.status_code})."
    except Exception as e:
        return f"Kesalahan koneksi: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Bot AI Cloud Anda sudah aktif 24 jam.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pesan_masuk = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    jawaban = tanya_ai(pesan_masuk)
    await update.message.reply_text(jawaban)

if __name__ == '__main__':
    # Mengambil port otomatis dari cloud, atau default ke 8080
    port = int(os.environ.get("PORT", 8080))
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot cloud berjalan...")
    app.run_polling()
