# Documentation

Technical documentation and development guides for VisionCast-AI.

## Contents

- [**DOCUMENTATION.md**](DOCUMENTATION.md) — Documentation officielle complète couvrant :
  - Présentation générale et positionnement
  - Architecture globale du système (schémas détaillés)
  - Installation et configuration (Windows, macOS, drivers)
  - Workflow broadcast complet (étape par étape)
  - Module IA Python (détection, reconnaissance, talents.json)
  - Moteur vidéo C++ Vision Engine (pipeline GPU, filtres, overlays)
  - Régie Qt VisionCast Control Room (8 panneaux détaillés)
  - SDK Broadcast (DeckLink, AJA, Magewell, NDI)
  - Sorties vidéo (SDI, HDMI, NDI, SRT, RTMP)
  - Dépannage & FAQ
  - Mentions officielles

- [**USER_MANUAL.md**](USER_MANUAL.md) — Manuel utilisateur complet destiné aux chaînes TV et opérateurs de régie :
  - Introduction et architecture globale (IA + moteur vidéo + régie + SDK broadcast)
  - Installation (Windows, macOS, drivers DeckLink/AJA/Magewell, NDI Tools)
  - Workflow broadcast (caméras → régie → VisionCast‑AI → sortie finale)
  - Utilisation de la régie VisionCast Control Room (7 panneaux détaillés)
  - Gestion des talents (ajout, modification, overlays, thèmes, filtres)
  - Gestion des overlays (templates, thèmes, animations, logos, couleurs)
  - Sorties vidéo (SDI, NDI, SRT, RTMP)
  - Guide de dépannage complet

- [**ARCHITECTURE.md**](ARCHITECTURE.md) — Complete system architecture document covering:
  - System overview and high-level architecture
  - Directory structure and module organization
  - Python AI module (face detection, recognition, IPC)
  - C++ video engine (4K pipeline, overlays, filters)
  - Qt control room (preview, editing, monitoring)
  - SDK abstraction layer (DeckLink, AJA, Magewell, NDI)
  - Data flow, video pipeline, and threading model
  - Python ↔ C++ IPC protocol (ZeroMQ)
  - Configuration and build system
