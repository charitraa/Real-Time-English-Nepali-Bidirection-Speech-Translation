# FYP Translator

**FYP Translator** is an end-to-end speech-to-text translation pipeline
that leverages **Whisper (OpenAI)** for Automatic Speech Recognition
(ASR) and **LangDetect** for language detection. It supports both **CPU
and GPU (CUDA)** inference with automatic fallback, making it suitable
for deployment on various hardware configurations.

This project is designed as a modular, extensible system ideal for
final-year projects (FYP), research prototypes, or production-grade
speech translation applications.

------------------------------------------------------------------------

## Features

-   **Whisper-based ASR** with support for multiple model sizes (`tiny`,
    `base`, `small`, `medium`, `large`)
-   **GPU Acceleration** via PyTorch with CUDA detection and graceful
    CPU fallback
-   **Language Detection** using `langdetect` for input audio
-   **Modular Pipeline Architecture** (`pipeline.py`, `asr.py`,
    `translator.py`, etc.)
-   **Configurable via Environment Variables**
-   **Caching Support** (`__pycache__`, model weights)
-   **Temporary File Management** (`temp_audio/`, `output/`)
-   **Git Version Control Ready**

------------------------------------------------------------------------

## Project Structure

    fyp_translator/
    ├── asr.py              
    ├── translator.py       
    ├── pipeline.py         
    ├── settings.py         
    ├── tts.py              
    ├── urls.py             
    ├── views.py            
    ├── wsgi.py             
    ├── __init__.py
    ├── env/                
    ├── models/             
    ├── temp_audio/         
    ├── output/             
    ├── translator/
    │   └── __pycache__/
    ├── .ipynb_checkpoints/
    ├── requirements.txt    
    └── README.md           

------------------------------------------------------------------------

## Installation

### 1. Clone the Repository

``` bash
git clone https://github.com/yourusername/fyp-translator.git
cd fyp-translator
```

### 2. Set Up Virtual Environment

``` bash
python -m venv env
source env/bin/activate    # Linux/Mac
env\Scripts\activate     # Windows
```

### 3. Install Dependencies

``` bash
pip install -r requirements.txt
```

### 4. (Optional) Enable GPU

``` bash
export USE_GPU=1
```

------------------------------------------------------------------------

## Usage

### Run the Pipeline

``` bash
python pipeline.py --input temp_audio/input.wav --model small
```

### Example in Python

``` python
from pipeline import TranslationPipeline

pipeline = TranslationPipeline(model_size="small", use_gpu=True)
result = pipeline.process("temp_audio/sample.mp3")
print(result)
```

------------------------------------------------------------------------

## Configuration

  Environment Variable   Description                        Default
  ---------------------- ---------------------------------- -------------
  USE_GPU                Force GPU usage (1 or 0)           Auto-detect
  MODEL_SIZE             Whisper model (tiny, base, etc.)   small
  COMPUTE_TYPE           float16 (GPU) or int8 (CPU)        Auto

------------------------------------------------------------------------

## Supported Audio Formats

`.wav, .mp3, .m4a, .flac, .ogg`

------------------------------------------------------------------------

## GPU Support

``` python
if use_gpu and torch.cuda.is_available():
    device = "cuda"
    compute_type = "float16"
else:
    device = "cpu"
    compute_type = "int8"
```

------------------------------------------------------------------------

## Extending the Project

-   Add Translation API in `translator.py`
-   Add TTS Output using `tts.py`
-   Build Web UI
-   Deploy API via `wsgi.py`

------------------------------------------------------------------------

## License

MIT License © 2025 Your Name

------------------------------------------------------------------------

## Contact

Charitra Shrestha\
📧 charitra@example.com\
💻 GitHub: @charitraa
