.PHONY: install run chat query web tools-chat clean test format lint help docker-build docker-run docker-chat docker-query docker-stop docker-clean docker-web

# Default target
help:
	@echo "Available commands:"
	@echo ""
	@echo "Local Development:"
	@echo "  install    - Install dependencies using Poetry"
	@echo "  run        - Run the AI agent in interactive mode (auto-detect)"
	@echo "  chat       - Alias for run"
	@echo "  tools-chat - Force tools mode with LangChain"
	@echo "  web        - Start web interface (auto-detect mode)"
	@echo "  query      - Run a single query (use QUERY='your question')"
	@echo "  test       - Run tests"
	@echo "  format     - Format code with black"
	@echo "  lint       - Lint code with flake8"
	@echo "  clean      - Clean up cache files"
	@echo ""
	@echo "Docker Commands:"
	@echo "  docker-build  - Build Docker image"
	@echo "  docker-run    - Run with Docker Compose in background"
	@echo "  docker-web    - Start web interface with Docker"
	@echo "  docker-chat   - Run interactive chat with Docker"
	@echo "  docker-query  - Run single query with Docker (use QUERY='question')"
	@echo "  docker-stop   - Stop Docker containers"
	@echo "  docker-clean  - Clean up Docker containers and images"
	@echo ""
	@echo "Examples:"
	@echo "  make install"
	@echo "  make web"
	@echo "  make run"
	@echo "  make query QUERY='What is Python?'"
	@echo "  make docker-web"

# Install dependencies
install:
	chmod +x scripts/setup.sh
	./scripts/setup.sh

# Run interactive mode
run:
	poetry run python main_launcher.py

# Alias for run
chat: run

# Force tools mode with LangChain
tools-chat:
	@echo "🛠️  Starting agent with LangChain tools enabled"
	@echo "⚠️  Agent will have access to actual system tools"
	poetry run python main_launcher.py --mode tools

# Start web interface
web:
	@echo "Starting VHACK web interface at http://localhost:5000"
	@echo "⚠️  WARNING: This is a vulnerable application for educational purposes!"
	chmod +x scripts/start_web.sh
	./scripts/start_web.sh

# Run a single query
query:
	@if [ -z "$(QUERY)" ]; then \
		echo "Usage: make query QUERY='your question here'"; \
		exit 1; \
	fi
	poetry run python main_launcher.py --query "$(QUERY)"

# Run tests
test:
	poetry run pytest

# Format code
format:
	poetry run black .

# Lint code
lint:
	poetry run flake8 .

# Clean up
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete

# Docker commands
docker-build:
	docker compose build

docker-run:
	@echo "Starting Docker container in background..."
	docker compose up -d

docker-chat:
	@echo "Starting interactive chat with Docker..."
	docker compose run --rm vhack poetry run python main_launcher.py

docker-web:
	@echo "Starting VHACK web interface with Docker at http://localhost:5000"
	@echo "⚠️  WARNING: This is a vulnerable application for educational purposes!"
	docker compose --profile web up --build vhack-web

docker-query:
	@if [ -z "$(QUERY)" ]; then \
		echo "Usage: make docker-query QUERY='your question here'"; \
		exit 1; \
	fi
	docker compose run --rm vhack poetry run python main_launcher.py --query "$(QUERY)"

docker-stop:
	docker compose down

docker-clean:
	docker compose down --rmi all --volumes --remove-orphans