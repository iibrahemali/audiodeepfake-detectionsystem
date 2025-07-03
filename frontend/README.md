# Flutter Frontend - Deepfake Audio Detector

Web-only Flutter app for deepfake audio detection using the AASIST backend (mobile platforms – will do later).

## Quick Start

```bash
# Development mode (with hot reload)
./run_dev.sh

# Or manually
flutter pub get
flutter run -d chrome --web-port=3000
```

App runs at: http://localhost:3000

## Features

- ✅ **Web**: Works on Chrome (mobile platforms – will do later)
- ✅ **File Upload**: WAV, FLAC, MP3, M4A support
- ✅ **Audio Playback**: Play selected files
- ✅ **Real-time Results**: Instant AI predictions
- ✅ **Material Design 3**: Modern UI with dark/light themes

## Platform Support

- **Web**: File upload + playback (recording disabled)
- **Mobile**: (will do later)
- **Desktop**: (will do later)

## Backend Integration

Connects to backend at `http://localhost:8000`:
- Automatic health checking
- Perfect API response matching
- Comprehensive error handling

## Build

```bash
# Web production build
flutter build web

# Production server
./run_web.sh
```

## Testing

```bash
flutter test                    # Unit tests
dart test_integration.dart      # Backend integration test
```

## Requirements

- Flutter SDK 3.0+
- Chrome browser (for web)
- Backend running on port 8000 