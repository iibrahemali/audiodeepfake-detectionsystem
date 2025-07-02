import pathlib, torch, torchaudio, numpy as np, json

_THIS_DIR = pathlib.Path(__file__).resolve().parent
_AASIST_DIR = _THIS_DIR / "aasist"
_CONFIG_PATH = _AASIST_DIR / "config/AASIST.conf"
_WEIGHTS_PATH = _AASIST_DIR / "models/weights/AASIST.pth"

# Lazy import of the upstream model (keeps local namespace clean)
import sys
sys.path.append(str(_AASIST_DIR))
from models.AASIST import Model as AASISTModel  # type: ignore

_DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# ---------------------------------------------------------------
# Load configuration & model once at module import time.
# This ensures subsequent predict() calls are fast.
# ---------------------------------------------------------------
with open(_CONFIG_PATH, 'r') as f:
    _cfg = json.load(f)
_model = AASISTModel(_cfg["model_config"]).to(_DEVICE)
_state = torch.load(_WEIGHTS_PATH, map_location=_DEVICE)
_model.load_state_dict(_state)
_model.eval()
_nb_samp = _cfg["model_config"]["nb_samp"]  # 64600 (≈4.04 s @ 16 kHz)

# ---------------------------------------------------------------
@torch.no_grad()
def predict_wav(wav_path: str | pathlib.Path) -> dict:
    """Return a dict with spoof probability & label for given WAV/FLAC."""
    wav_path = pathlib.Path(wav_path)
    wav, sr = torchaudio.load(str(wav_path))
    if sr != 16000:
        wav = torchaudio.functional.resample(wav, sr, 16000)
    # mono
    if wav.shape[0] > 1:
        wav = wav.mean(0, keepdim=True)
    # normalise length
    if wav.shape[1] < _nb_samp:
        pad = _nb_samp - wav.shape[1]
        wav = torch.nn.functional.pad(wav, (0, pad))
    wav = wav[:, :_nb_samp]
    # z-norm
    wav = (wav - wav.mean()) / (wav.std() + 1e-9)

    logits = _model(wav.to(_DEVICE))[1]
    prob_fake = torch.softmax(logits, dim=1)[:, 1].item()
    return {
        "score": float(prob_fake),
        "label": "fake" if prob_fake > 0.5 else "real"
    } 