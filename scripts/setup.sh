#!/bin/bash

echo "🚀 Setting up VHACK (Very Hackable AI Chatbot Kit)..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "📦 Poetry not found. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    echo "⚠️  Please restart your terminal or run: source ~/.bashrc"
    echo "   Then run this setup script again."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies with Poetry..."
poetry install

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔧 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OpenRouter API key!"
else
    echo "✅ .env file already exists"
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OpenRouter API key"
echo "2. Run: poetry run python vhack.py"
echo "   Or activate the virtual environment: poetry shell"
echo "   Then run: python vhack.py"
echo ""
echo "Get your API key from: https://openrouter.ai/keys"