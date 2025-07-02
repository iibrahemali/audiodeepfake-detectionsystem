#!/bin/bash

echo "🔥 Starting Flutter Development Server - Deepfake Audio Detector"
echo "================================================================"

# Check if Flutter is installed
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter is not installed or not in PATH"
    echo "Please install Flutter: https://flutter.dev/docs/get-started/install"
    exit 1
fi

echo "🔍 Checking Flutter setup..."
flutter doctor | grep -E "(Flutter|Chrome)"

echo ""
echo "📦 Installing dependencies..."
flutter pub get

echo ""
echo "🔥 Starting development server with hot reload..."
echo ""
echo "📍 App will be available at: http://localhost:3000"
echo "🔗 Make sure your backend is running at: http://localhost:8000"
echo ""
echo "💡 Development Mode Features:"
echo "  • Hot reload enabled (press 'r' to reload)"
echo "  • Debug information available"
echo "  • Console logging enabled"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================================================"

# Start Flutter development server
flutter run -d chrome --web-port=3000 