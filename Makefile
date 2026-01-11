.PHONY: test install dev-install lint clean

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt
	pip install pytest pytest-asyncio

test:
	pytest tests/ -v

lint:
	flake8 src/ tests/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -f bot.db