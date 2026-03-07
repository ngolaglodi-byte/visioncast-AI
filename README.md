# VisionCast-AI

AI-powered live broadcast production system with real-time face recognition, automatic lower-third overlays, and multi-camera management.

> **VisionCast-AI — Licence officielle Prestige Technologie Company, développée par Glody Dimputu Ngola.**

## ⚠ Security Notice

**Ne jamais exposer la clé API Supabase dans le code public.**

All sensitive credentials (API URLs, API keys) must be provided via
environment variables.  See the [Environment Variables](#environment-variables)
section below.

## Project Structure

```
visioncast-ai/
├── python/           # AI / face recognition engine (Python)
│   ├── ai/           # Face detection, matching, talent DB
│   └── ipc/          # ZeroMQ metadata protocol
├── engine/           # Video processing engine (C++)
│   ├── include/      # Public headers
│   └── src/          # Implementation
├── ui/               # Broadcast control room (Qt)
│   ├── include/      # UI headers
│   └── src/          # Implementation
├── sdk/              # Hardware SDK abstraction (DeckLink, AJA, Magewell, NDI)
│   ├── include/      # Device interface headers
│   └── src/          # Device implementations
├── overlays/         # Overlay templates and assets
├── talents/          # Talent database (faces, metadata)
├── config/           # System configuration
├── docs/             # Documentation (architecture, guides)
├── CMakeLists.txt    # Top-level CMake build
└── .gitignore        # Ignore rules
```

## Quick Start

### Prerequisites

- Python 3.11+
- CMake 3.20+
- OpenCV 4.8+
- Qt 5.15+ or Qt 6.x
- dlib / face_recognition

### Environment Variables

Before running VisionCast-AI, set the following environment variables.
Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
# Edit .env with your real values
```

| Variable          | Description                         |
|-------------------|-------------------------------------|
| `LICENSE_API_URL` | URL of the license validation API   |
| `LICENSE_API_KEY` | API key (bearer/anon) for the API   |

> ⚠ **Never commit `.env` or real credentials to version control.**

### Installation

```bash
# Python AI module
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r python/requirements.txt

# C++ engine + Qt UI
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --parallel
```

### Run

```bash
# Start the C++ engine
./build/bin/visioncast_engine &

# Start the AI module
python python/main.py &

# Start the control room
./build/bin/visioncast_ui
```

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the complete system architecture.

## Modules

| Directory   | Description                                          |
|-------------|------------------------------------------------------|
| `python/`   | AI face recognition, matching, and metadata IPC      |
| `engine/`   | C++ 4K video processing, compositing, and pipeline   |
| `ui/`       | Qt broadcast control room and monitoring              |
| `sdk/`      | DeckLink / AJA / Magewell / NDI device abstraction   |
| `overlays/` | Overlay graphic templates (JSON definitions)          |
| `talents/`  | Talent face database and metadata                     |
| `config/`   | System configuration files                            |
| `docs/`     | Technical documentation and architecture              |

## License

Proprietary - All rights reserved.
