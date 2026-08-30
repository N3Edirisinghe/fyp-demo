#!/usr/bin/env bash
# Run the Streamlit app locally for development/testing.
set -e

if [ ! -f .env ]; then
  echo "No .env found — copy .env.example to .env and fill in your API keys first."
  exit 1
fi

export PYTHONPATH="${PYTHONPATH}:$(pwd)"
streamlit run src/app.py
