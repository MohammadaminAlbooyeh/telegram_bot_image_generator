# Telegram Bot Image Generator

A simple Telegram bot that generates images using OpenAI's DALL-E API. Send a text prompt, and the bot will create and send back a custom image.

## Features

- Generate images from text prompts using DALL-E 3
- Easy setup with environment variables
- Docker support for containerized deployment
- Asynchronous image generation with user feedback
- Database integration for storing user data and generation history

## Requirements

- Python 3.8 or higher
- Telegram Bot Token (from @BotFather)
- OpenAI API Key (from OpenAI Platform)
- SQLite (built-in with Python)
- (Optional) Docker and Docker Compose for containerized running

## Installation

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/telegram_bot_image_generator.git
   cd telegram_bot_image_generator
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   - **Telegram Bot Token:** Talk to [@BotFather](https://t.me/botfather) on Telegram to create a new bot and get your token.
   - **OpenAI API Key:** Obtain from [OpenAI Platform](https://platform.openai.com/api-keys).

5. **Run the bot:**
   ```bash
   python src/main.py
   ```

   The database (`bot.db`) will be created automatically on first run.

### Running with Docker

1. Ensure Docker and Docker Compose are installed.

2. Build and run the bot:
   ```bash
   docker-compose up --build
   ```

3. To run in the background:
   ```bash
   docker-compose up -d --build
   ```

4. To stop the bot:
   ```bash
   docker-compose down
   ```

## Usage

1. Start a chat with your bot on Telegram.
2. Send `/start` to receive a welcome message.
3. Send `/generate <prompt>` to create an image.

   **Example:**
   ```
   /generate a futuristic cityscape at sunset
   ```

4. The bot will respond with the generated image and a caption.

## Testing

1. Install development dependencies:
   ```bash
   pip install pytest pytest-asyncio
   ```

2. Run tests:
   ```bash
   pytest tests/
   ```

   Or use the Makefile:
   ```bash
   make test
   ```

## Troubleshooting

- **Bot not responding:** Ensure your `.env` file has correct API keys and the bot is running.
- **Image generation fails:** Check OpenAI API key validity and quota. Errors are logged in the console.
- **Docker issues:** Ensure ports are not conflicting and Docker is running.
- **Permission errors:** Make sure the bot has necessary permissions on Telegram.

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.