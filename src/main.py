import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
from dotenv import load_dotenv
from models import SessionLocal, User, ImageGeneration

# Load environment variables
load_dotenv()

# Get API keys from environment
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Please set TELEGRAM_BOT_TOKEN and OPENAI_API_KEY in your .env file")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a prompt after /generate. Example: /generate a cat in space")
        return

    prompt = ' '.join(context.args)
    await update.message.reply_text("Generating image... Please wait.")

    db = SessionLocal()
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url

        # Log to database
        user_id = update.effective_user.id
        generation = ImageGeneration(user_id=user_id, prompt=prompt, image_url=image_url)
        db.add(generation)
        db.commit()

        # Download the image
        image_response = requests.get(image_url)
        image_response.raise_for_status()

        # Send the image
        await update.message.reply_photo(photo=image_response.content, caption=f"Generated image for: {prompt}")

    except Exception as e:
        await update.message.reply_text(f"Sorry, I couldn't generate the image. Error: {str(e)}")
    finally:
        db.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    try:
        user = update.effective_user
        db_user = db.query(User).filter(User.telegram_id == user.id).first()
        if not db_user:
            db_user = User(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            db.add(db_user)
            db.commit()
        await update.message.reply_text("Hello! I'm an image generator bot. Use /generate <prompt> to create an image.")
    finally:
        db.close()

def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("generate", generate_image))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()