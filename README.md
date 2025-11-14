# Real Time English Nepali Bidirection Speech Translation Translator  
### **Speech-to-Speech Translation (English ↔ Nepali)**  
*Powered by Whisper, Fine-tuned mBART50, and Coqui/gTTS*

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

**Real Time English Nepali Bidirection Speech Translation Translator** is a **real-time, end-to-end speech-to-speech translation system** designed for **English ↔ Nepali** communication. It combines state-of-the-art models into a **modular, GPU-accelerated pipeline**:

| Component         | Model / Library               |
|------------------|-------------------------------|
| **ASR**           | OpenAI **Whisper** (tiny → large) |
| **Translation**   | **Fine-tuned mBART50** (EN ↔ NE) |
| **TTS**           | **gTTS** or **Coqui TTS**       |
| **Lang Detect**   | `langdetect`                  |
| **Backend**       | PyTorch, CUDA, Fast Inference |

Perfect for **Final Year Projects**, **research prototypes**, or **production deployment**.

---

## Features

| Feature | Description |
|-------|-------------|
| **Speech-to-Speech** | Full audio in → translated audio out |
| **Nepali ↔ English** | Bidirectional, culturally aware translation |
| **GPU Auto Detection** | GPU auto-detect + fallback to CPU |
| **Modular Design** | `asr.py`, `translator.py`, `tts.py`, `pipeline.py` |
| **Model Caching** | Whisper + mBART weights stored locally |
| **Configurable** | Via environment vars or CLI |
| **Production Ready** | WSGI, API endpoints, logging |

---

## Project Structure

```bash
Real Time English Nepali Bidirection Speech Translation_translator/
├── asr.py              # Whisper ASR
├── translator.py       # mBART50 translation (EN↔NE)
├── tts.py              # Text-to-Speech (gTTS / Coqui)
├── pipeline.py         # End-to-end S2S pipeline
├── settings.py         # Config & constants
├── urls.py             # API routes
├── views.py            # Web views (optional UI)
├── wsgi.py             # Production entry
│
├── models/
│   ├── whisper/
│   └── mbart/
│       ├── config.json
│       ├── pytorch_model.bin
│       ├── tokenizer.json
│       └── sentencepiece.bpe.model
│
├── temp_audio/
├── output/
├── env/
└── requirements.txt
```

---

## Installation

### 1. Clone
```bash
git clone https://github.com/charitraa/fyp_translator.git
cd fyp_translator
```

### 2. Virtual Environment
```bash
python -m venv env
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### GPU Users
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Force GPU
```bash
export USE_GPU=1
```

---

## Usage

### Run Full Pipeline
```bash
python pipeline.py \
  --input temp_audio/hello_nepali.wav \
  --asr-model small \
  --use-mbart \
  --use-tts \
  --tts-engine gtts
```

## mBART Translation Example

```python
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

model = MBartForConditionalGeneration.from_pretrained("models/mbart")
tok = MBart50TokenizerFast.from_pretrained("models/mbart")

text = "My name is Ravi."
tok.src_lang = "en_XX"
inputs = tok(text, return_tensors="pt")
generated = model.generate(**inputs, forced_bos_token_id=tok.lang_code_to_id["ne_NP"])
print(tok.decode(generated[0], skip_special_tokens=True))
```

---

## TTS Example

```python
from tts import TextToSpeech

tts = TextToSpeech(engine="gtts")
tts.speak("नमस्ते, तपाईंलाई कस्तो छ?", lang="ne", output_path="output/greeting_ne.mp3")
```

---

## Supported Formats
```
.wav | .mp3 | .m4a | .flac | .ogg
```

---

## GPU / CPU Logic

```python
if use_gpu and torch.cuda.is_available():
    device = "cuda"
    compute_type = "float16"
    print("Using GPU for Whisper & mBART")
else:
    device = "cpu"
    compute_type = "int8"
    print("GPU failed → Using CPU (int8)")
```

---

## Configuration

| Env Var | Values | Default |
|--------|--------|---------|
| USE_GPU | 1 / 0 | Auto |
| ASR_MODEL | tiny, small, base | small |
| USE_MBART | True / False | True |
| USE_TTS | True / False | True |
| TTS_ENGINE | gtts, coqui | gtts |

---

## Extending

- Add FastAPI UI  
- Deploy with Nginx + Gunicorn  
- Add real-time streaming  
- Train Nepali TTS model  
- Add Hindi, Tamil, Bengali support  

---

## License  
MIT License © 2025 Charitra Shrestha

---

## Contact
**Charitra Shrestha**  
📧 stharabi9862187405@gmail.com  
🐙 GitHub: **@charitraa**  
🚀 Demo coming soon!

"Breaking language barriers, one voice at a time."
