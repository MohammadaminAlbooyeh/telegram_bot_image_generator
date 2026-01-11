import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update, User
from telegram.ext import ContextTypes
from src.main import start, generate_image
from src.models import SessionLocal, User as DBUser, ImageGeneration


@pytest.fixture
def mock_update():
    update = MagicMock(spec=Update)
    user = MagicMock(spec=User)
    user.id = 12345
    user.username = "testuser"
    user.first_name = "Test"
    user.last_name = "User"
    update.effective_user = user
    update.message = MagicMock()
    update.message.reply_text = AsyncMock()
    update.message.reply_photo = AsyncMock()
    return update


@pytest.fixture
def mock_context():
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = ["a", "test", "prompt"]
    return context


@pytest.mark.asyncio
async def test_start(mock_update, mock_context):
    db = SessionLocal()
    try:
        await start(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once_with(
            "Hello! I'm an image generator bot. Use /generate <prompt> to create an image."
        )
        # Check if user was added to DB
        db_user = db.query(DBUser).filter(DBUser.telegram_id == 12345).first()
        assert db_user is not None
        assert db_user.username == "testuser"
    finally:
        db.close()


@pytest.mark.asyncio
@patch('src.main.client')
async def test_generate_image_success(mock_client, mock_update, mock_context):
    # Mock OpenAI response
    mock_response = MagicMock()
    mock_response.data = [MagicMock()]
    mock_response.data[0].url = "http://example.com/image.png"
    mock_client.images.generate.return_value = mock_response

    # Mock requests
    with patch('src.main.requests.get') as mock_get:
        mock_get.return_value.raise_for_status = MagicMock()
        mock_get.return_value.content = b"image data"

        db = SessionLocal()
        try:
            await generate_image(mock_update, mock_context)
            mock_update.message.reply_text.assert_any_call("Generating image... Please wait.")
            mock_update.message.reply_photo.assert_called_once()
            # Check if generation was logged
            generation = db.query(ImageGeneration).filter(ImageGeneration.user_id == 12345).first()
            assert generation is not None
            assert generation.prompt == "a test prompt"
            assert generation.image_url == "http://example.com/image.png"
        finally:
            db.close()


@pytest.mark.asyncio
@patch('src.main.client')
async def test_generate_image_no_args(mock_client, mock_update):
    mock_context = MagicMock()
    mock_context.args = []

    await generate_image(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once_with(
        "Please provide a prompt after /generate. Example: /generate a cat in space"
    )


@pytest.mark.asyncio
@patch('src.main.client')
async def test_generate_image_error(mock_client, mock_update, mock_context):
    mock_client.images.generate.side_effect = Exception("API Error")

    await generate_image(mock_update, mock_context)
    mock_update.message.reply_text.assert_any_call("Generating image... Please wait.")
    mock_update.message.reply_text.assert_any_call(
        "Sorry, I couldn't generate the image. Error: API Error"
    )