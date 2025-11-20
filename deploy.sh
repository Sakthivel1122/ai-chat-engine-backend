#!/bin/bash

echo "Pulling latest code..."
git pull origin main

echo "Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo "Restarting Django service..."
sudo systemctl restart ai_chat_engine.service
