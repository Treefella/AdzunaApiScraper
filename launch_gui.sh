#!/bin/bash
# Launch Adzuna Smart Job Scraper GUI

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Launching Adzuna Smart Job Scraper..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
fi

# Launch the GUI
echo "✓ Starting GUI..."
.venv/bin/python adzuna_smart_gui.py
