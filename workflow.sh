#!/bin/bash
# Install the required Python packages (commented out, uncomment if needed)
# pip install -r requirements.txt

# Export your Notion integration token (replace with your actual token)
export NOTION_TOKEN=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

# Export the Notion database ID (replace with your actual database ID)
export NOTION_DATABASE_ID=14fe1921c162800ba7a7f40e024f1111

# Set the directory where downloaded files will be saved
export DOWNLOAD_DIR=/Users/eaguerov/Library/CloudStorage/GoogleDrive-elvisavfc65@gmail.com/My\ Drive/Reading\ Bibliography/Academic\ Readings/papers/

# Export your Semantic Scholar API key (optional, uncomment and replace if available)
export SS_KEY=Hg3W2wCtsEyjvsc5cdJi8QyjcBTgyrh8aXkQ3QPe

# Set the sleep interval for Semantic Scholar API requests (optional, uncomment and adjust if needed)
export SS_SLEEP_INTERVAL=3

# Run the Python UI script
cd ~/Documents/Github/arxiv-workflow/
python UI.py

# Uncomment the line below to run the FastAPI server script instead of the UI
# fastapi run server.py
