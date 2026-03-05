# VisionCast-AI

AI-powered live broadcast production system with real-time face recognition, automatic lower-third overlays, and multi-camera management.

## Project Structure

```
visioncast-ai/
├── python/       # AI / face recognition engine (Python)
├── engine/       # Video processing engine (C++)
├── ui/           # User interface / broadcast control (Qt / Electron)
├── sdk/          # Hardware SDK integrations (DeckLink, AJA, Magewell, NDI)
├── overlays/     # Overlay templates and assets
├── talents/      # Talent database (faces, metadata)
├── docs/         # Documentation
└── .gitignore    # Optimized ignore rules
```

## Quick Start

### Prerequisites

- Python 3.11+
- OpenCV
- dlib
- face_recognition

### Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

pip install opencv-python face_recognition numpy Pillow
```

### Run

```bash
cd python
python main.py
```

## Modules

| Directory   | Description                                      |
|-------------|--------------------------------------------------|
| `python/`   | AI face recognition and lower-third generation   |
| `engine/`   | C++ video processing and compositing engine      |
| `ui/`       | Qt-based broadcast control interface              |
| `sdk/`      | DeckLink / AJA / Magewell / NDI SDK integrations |
| `overlays/` | Overlay graphic templates and assets              |
| `talents/`  | Talent face database and metadata                 |
| `docs/`     | Technical documentation and guides                |

## License

Proprietary - All rights reserved.
