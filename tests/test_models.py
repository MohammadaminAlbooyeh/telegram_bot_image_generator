import pytest
from src.models import SessionLocal, User, ImageGeneration, Base, engine


@pytest.fixture(scope="function")
def db_session():
    # Create tables
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    # Drop tables after test
    Base.metadata.drop_all(bind=engine)


def test_create_user(db_session):
    user = User(
        telegram_id=12345,
        username="testuser",
        first_name="Test",
        last_name="User"
    )
    db_session.add(user)
    db_session.commit()

    retrieved = db_session.query(User).filter(User.telegram_id == 12345).first()
    assert retrieved is not None
    assert retrieved.username == "testuser"


def test_create_image_generation(db_session):
    generation = ImageGeneration(
        user_id=12345,
        prompt="test prompt",
        image_url="http://example.com/image.png"
    )
    db_session.add(generation)
    db_session.commit()

    retrieved = db_session.query(ImageGeneration).filter(ImageGeneration.user_id == 12345).first()
    assert retrieved is not None
    assert retrieved.prompt == "test prompt"
    assert retrieved.image_url == "http://example.com/image.png"