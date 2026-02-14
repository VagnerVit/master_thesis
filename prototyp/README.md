# SwimAth

**Swimming Style Analysis Application using Computer Vision & Machine Learning**

SwimAth je desktopová aplikace pro Windows analyzující plavecký styl ze video záznamů. Využívá pokročilé techniky počítačového vidění a strojového učení k detekci pohybů plavce, porovnání s ideální technikou a poskytnutí personalizovaného feedback.

## Features (Roadmap)

### Phase 1 (MVP)
- ✅ Video processing pipeline (OpenCV)
- ✅ Real-time pose estimation (MediaPipe Pose)
- ✅ Skeleton visualization overlay
- ✅ Basic PySide6 GUI

### Phase 2 (ML Training)
- ⏳ Style classification (YOLOv8-cls: freestyle, backstroke, breaststroke, butterfly)
- ⏳ Stroke analysis (DTW comparison s reference templates)
- ⏳ Feedback generation ("Levé rameno 15° nízko při záběru")

### Phase 3 (Advanced Features)
- ⏳ Underwater refraction correction
- ⏳ Strava integration (OAuth2 sync)
- ⏳ Apple Health import (manual export.zip upload)
- ⏳ Training recommendations

## Tech Stack

- **ML & CV**: MediaPipe Pose, PyTorch, ONNX Runtime, OpenCV
- **GUI**: PySide6 (Qt6)
- **Hardware Acceleration**: DirectML (Windows ML API)
- **Database**: SQLite + SQLAlchemy
- **Integrations**: Strava API (stravalib), Apple Health Parser

## Installation

### Prerequisites
- Windows 10 (64-bit) build 1809+ nebo Windows 11
- Python 3.11+
- GPU doporučeno (NVIDIA RTX 3060+ / AMD RX 6600+ / Intel Arc)
- **Disk space**: 45 GB minimum (annotations + 1 styl), 300 GB pro full dataset

### Quick Start

#### Phase 0: Dataset Setup
```bash
# Windows
scripts\quickstart_phase0.bat

# Linux/Mac
bash scripts/quickstart_phase0.sh
```

Tento skript:
1. Vytvoří virtual environment
2. Nainstaluje Phase 0 dependencies
3. Zobrazí download instrukce

**Detailní instrukce**: Viz [PHASE0_DATASET_SETUP.md](PHASE0_DATASET_SETUP.md)

#### Phase 1: Application Setup
```bash
# Create virtual environment (if not done in Phase 0)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

## Usage

```bash
# Run application
python src/main.py

# Run tests
pytest tests/

# Code formatting
black src/ tests/
```

## Project Structure

```
swimath/
├── src/
│   ├── core/          # Video processing, pose estimation
│   ├── ui/            # PySide6 GUI components
│   ├── models/        # ML model configs
│   ├── analysis/      # Stroke analysis, underwater correction
│   ├── integrations/  # Strava, Apple Health
│   ├── database/      # SQLAlchemy models
│   └── utils/         # Helpers
├── training/          # ML training scripts
├── tests/             # Unit & integration tests
├── data/              # Datasets (gitignored)
└── models/            # Trained model weights (gitignored)
```

## Datasets

Používáme existující open-source datasety:
- **SwimXYZ** (2023): 3.4M framů, 2D/3D joints, SMPL formát
- **Swimmer Pose Estimation Dataset**: 2,500 images, 4 styly, COCO format
- **Sports in the Wild (SVW)**: Underwater freestyle footage

## Performance Targets

- Video Processing: ≥20 FPS (Intel i5-12400 / AMD Ryzen 5 5600)
- ML Inference: <50ms per frame (MediaPipe), <100ms per frame (ONNX)
- UI Responsiveness: 60 FPS

## License

MIT License - see LICENSE file for details

## Contributing

Projekt je v aktivním vývoji. Contributions vítány!

## Contact

Pro otázky nebo feedback otevřete issue na GitHubu.

---

**Status**: 🚧 In Development - Phase 1 (MVP)
