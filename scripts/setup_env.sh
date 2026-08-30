#!/usr/bin/env bash
# One-time local environment setup.
set -e

echo "Creating virtual environment..."
python -m venv .venv
source .venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f .env ]; then
  echo "Creating .env from .env.example — fill in your API keys before running the app."
  cp .env.example .env
fi

mkdir -p data/processed data/raw

echo "Setup complete. Activate the environment with: source .venv/bin/activate"
echo "Then run the app with: bash scripts/run_local.sh"
