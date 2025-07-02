#!/bin/bash

echo "🚀 Starting Flutter Web App - Deepfake Audio Detector"
echo "================================================================"

# Check if Flutter is installed
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter is not installed or not in PATH"
    echo "Please install Flutter: https://flutter.dev/docs/get-started/install"
    exit 1
fi

# Check Flutter doctor for web
echo "🔍 Checking Flutter setup..."
flutter doctor | grep -E "(Flutter|Chrome)"

echo ""
echo "📦 Installing dependencies..."
flutter pub get

echo ""
echo "🔧 Building web version..."
flutter build web

echo ""
echo "🌐 Starting web server..."
echo ""
echo "📍 App will be available at: http://localhost:3000"
echo "🔗 Make sure your backend is running at: http://localhost:8000"
echo ""
echo "💡 Tips:"
echo "  • Backend: cd ../backend && python run.py"
echo "  • Use Chrome for best compatibility"
echo "  • File upload works on web (recording is disabled)"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================================================"

# Start the web server
python3 -m http.server 3000 -d build/web 