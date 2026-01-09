# Telegram Bot Image Generator

This is a Telegram bot that generates images automatically using OpenAI's DALL-E.

## Setup

1. Clone the repository.

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your API keys:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   - To get a Telegram bot token, talk to @BotFather on Telegram.
   - Get an OpenAI API key from https://platform.openai.com/api-keys

4. Run the bot:
   ```
   python src/main.py
   ```

## Usage

- Start a chat with your bot on Telegram.
- Send `/start` to get started.
- Send `/generate <prompt>` to generate an image based on the prompt.

Example: `/generate a beautiful sunset over mountains`

The bot will generate and send the image back to you.