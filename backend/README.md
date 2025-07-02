# AASIST Backend - Deepfake Audio Detection

FastAPI server using the official AASIST model for deepfake audio detection.

## Quick Start

```bash
# Start the server
source venv/bin/activate
python run.py
```

Server runs at: http://localhost:8000

## API Endpoints

- `GET /health` - Health check
- `POST /predict/` - Upload audio file for prediction

## Response Format

```json
{
  "result": "real|fake",
  "score": 0.1234,
  "confidence": 0.8765,
  "threshold": 0.5,
  "model_type": "AASIST"
}
```

## Docker

```bash
docker build -t aasist-backend .
docker run -p 8000:8000 aasist-backend
```

## Testing

```bash
python tests/test_frontend_integration.py
curl http://localhost:8000/health
```

## Requirements

- Python 3.11+
- AASIST model weights (included)
- 4GB RAM minimum 