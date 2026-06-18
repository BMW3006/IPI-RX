#!/bin/bash
# run.sh - Quick launcher for the link tracker

echo "🔗 LINK TRACKER LAUNCHER"
echo "========================"
echo ""
echo "1) Start Server"
echo "2) Start Viewer (Track clicks)"
echo "3) Generate New Link"
echo "4) View Dashboard (in browser)"
echo ""

read -p "Choose an option (1-4): " choice

case $choice in
    1)
        echo "🚀 Starting server..."
        python server.py
        ;;
    2)
        echo "👀 Starting viewer..."
        python tracker.py
        ;;
    3)
        echo "🔗 Generating link..."
        python create_link.py
        ;;
    4)
        echo "🌐 Opening dashboard..."
        echo "Open http://localhost:5000/dashboard in your browser"
        ;;
    *)
        echo "❌ Invalid option"
        ;;
esac
