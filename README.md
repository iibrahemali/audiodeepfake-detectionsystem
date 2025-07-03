# Deepfake Audio Detection System

Complete end-to-end system for detecting deepfake audio using the AASIST neural network.

## Features

- 🤖 **AASIST Model**: State-of-the-art neural network for audio anti-spoofing
- ⚡ **FastAPI Backend**: High-performance REST API with real-time processing
- 📱 **Flutter Frontend**: Web app with modern UI (mobile platforms – will do later)
- 🎙️ **Real-time Analysis**: Live audio recording and file upload support
- 📊 **Detailed Results**: Confidence scores and risk assessment
- 🐳 **Docker Ready**: Easy deployment with containerization

## Architecture

```
Flutter App ──HTTP──► FastAPI ──► AASIST Model
    │                    │              │
    ├─ Audio Record      ├─ Processing  ├─ Prediction
    ├─ File Upload       ├─ Validation  ├─ Confidence
    └─ Results Display   └─ Response    └─ Classification
```

## Quick Start

### 1. Backend Setup
```bash
cd backend
source venv/bin/activate
python run.py
```
Backend runs at: http://localhost:8000

### 2. Frontend Setup
```bash
cd frontend
./run_dev.sh
```
Frontend runs at: http://localhost:3000

### 3. Test the System
1. Open the frontend app
2. Record audio or upload a file (WAV, FLAC, MP3, M4A)
3. Click "Analyze" to get AI prediction
4. View results: Real/Fake classification with confidence scores

## API Response Format

```json
{
  "result": "real|fake",
  "score": 0.73,
  "confidence": 0.85,
  "threshold": 0.5,
  "model_type": "AASIST"
}
```

## Docker Deployment

```bash
# Backend only
cd backend
docker build -t aasist-backend .
docker run -p 8000:8000 aasist-backend

# Full system (create docker-compose.yml)
docker-compose up --build
```

## Platform Support

- **Backend**: Linux, macOS, Windows with Python 3.11+
- **Frontend**: Web (Chrome) (Android, iOS, Desktop – will do later)
- **Model**: CPU/GPU inference with 4GB RAM minimum

## Project Structure

```
vocal-biometrics-ai-sys/
├── backend/           # FastAPI + AASIST model
├── frontend/          # Flutter cross-platform app
└── README.md         # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both backend and frontend
5. Submit a pull request

## License

This project uses the official AASIST implementation. See individual directories for specific license terms.

## Research Citation

Based on the AASIST paper:
```
@inproceedings{jung2021aasist,
  title={AASIST: Audio Anti-Spoofing using Integrated Spectro-Temporal Graph Attention Networks},
  author={Jung, Jee-weon and Heo, Hee-Soo and Tak, Hemlata and Shim, Hye-jin and Chung, Joon Son and Lee, Bong-Jin and Yu, Ha-Jin and Evans, Nicholas},
  booktitle={Proc. Interspeech},
  year={2021}
}
```