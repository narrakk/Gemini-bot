import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# --- CONFIGURATION ---
# We will set these in the server later
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- SETUP GEMINI ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- BOT FUNCTIONS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am connected to Google Gemini. Ask me anything!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Show "typing..." status while waiting
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # Ask Gemini
        response = model.generate_content(user_text)
        
        # Send the reply back to Telegram
        await update.message.reply_text(response.text)
        
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# --- RUN THE BOT ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler('start', start))
    
    # Messages (Respond to text that isn't a command)
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))
    
    print("Bot is running...")
    app.run_polling()
