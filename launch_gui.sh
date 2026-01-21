#!/bin/bash
# Launch Adzuna Smart Job Scraper GUI
# Forked from: /home/gls/Documents/gmailscraper/run_gui.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Launching Adzuna Smart Job Scraper..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Create it with: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Create it with API credentials:"
    echo "  ADZUNA_APP_ID=your_id"
    echo "  ADZUNA_API_KEY=your_key"
fi

# Launch the GUI
echo "✓ Starting GUI..."
.venv/bin/python adzuna_smart_gui.py

if [ $? -eq 0 ]; then
    echo "✓ Application closed successfully"
else
    echo "✗ Application error occurred"
    exit 1
fi
