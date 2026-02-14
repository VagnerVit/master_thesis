# Session Handoff - SwimAth Project

**Session Date**: 2026-01-13
**Claude Version**: Opus 4.5
**Project Status**: Phase 2.2-2.4 Implementation Complete, Ready for Training

---

## 🎯 Project Overview

**SwimAth** je desktopová aplikace pro Windows analyzující plavecký styl ze video záznamů pomocí ML.

**Cíl**:
1. Nahrát video plavce
2. Detekovat pose (MediaPipe)
3. Klasifikovat styl (LSTM classifier)
4. Analyzovat techniku (DTW comparison s "ideálním" stylem)
5. Poskytnout feedback: "Levý loket příliš ohnutý při záběru (135° místo 160°)"
6. Doporučit cviky na zlepšení

**Target Users**: Plavci se středním výkonem

---

## 📂 Repository Info

**GitHub**: https://github.com/VagnerVit/SwimAth.git
**Branch**: main
**Last Commit**: 2690503 "Add Phase 2.2-2.4 ML training pipeline"
**Language**: Python 3.11+, PySide6, PyTorch, OpenCV, MediaPipe

**Local Path**: `C:\repos\SwimAth`

---

## ✅ What's Done

### Phase 1: MVP Application ✅
- ✅ Video přehrávání + MediaPipe skeleton overlay
- ✅ 22 unit testů prochází
- ✅ PySide6 GUI

### Phase 0: Dataset ✅
- ✅ Annotations (6.7 GB) - všechny styly
- ✅ Freestyle Part 1 + Part 2 (75 GB)
- ✅ Dataset prepared: 8,640 sekvencí, 2.6M framů
- 🔄 Backstroke stahování probíhá

### Phase 2.1: Dataset Loader ✅
- ✅ `training/swimxyz_parser.py` - CSV parser
- ✅ `training/dataset_loader.py` - PyTorch Dataset
- ✅ ~34k training samples

### Phase 2.2: Reference Templates ✅
- ✅ `training/angle_utils.py` - výpočet úhlů kloubů (48 keypointů)
- ✅ `training/template_generator.py` - generování šablon
- ⏳ `models/freestyle_template.json` - čeká na vygenerování

### Phase 2.3: Style Classifier ✅
- ✅ `training/models/style_classifier.py` - LSTM model (4 třídy, attention)
- ✅ `training/train_classifier.py` - training script (CUDA, AMP, early stopping)
- ⏳ `models/style_classifier.onnx` - čeká na trénink

### Phase 2.4: Stroke Analyzer ✅
- ✅ `src/analysis/dtw.py` - Dynamic Time Warping
- ✅ `src/analysis/stroke_analyzer.py` - detekce cyklů, analýza
- ✅ `src/analysis/feedback_generator.py` - český feedback

---

## 📁 Aktuální Struktura

```
SwimAth/
├── src/
│   ├── core/               # video_processor, pose_estimator, frame_buffer
│   ├── ui/                 # main_window, video_player
│   ├── analysis/           # ✅ NOVÉ
│   │   ├── dtw.py          # Dynamic Time Warping
│   │   ├── stroke_analyzer.py   # StrokeAnalyzer class
│   │   └── feedback_generator.py # FeedbackGenerator (Czech)
│   └── models/             # mediapipe_config
├── training/
│   ├── dataset_loader.py   # SwimXYZDataset
│   ├── swimxyz_parser.py   # CSV parser
│   ├── angle_utils.py      # ✅ NOVÉ - joint angle calculations
│   ├── template_generator.py # ✅ NOVÉ - reference templates
│   ├── train_classifier.py # ✅ NOVÉ - training script
│   └── models/
│       └── style_classifier.py # ✅ NOVÉ - LSTM model
├── models/                 # trained models (to be generated)
├── scripts/                # download, prepare, verify scripts
└── data/swimxyz/           # dataset
```

---

## 🔧 Commands

```bash
# Aktivace
cd C:\repos\SwimAth
venv\Scripts\activate

# 1. Vygenerovat freestyle template
python -m training.template_generator --style freestyle

# 2. Trénink modelu (~30 min s CUDA)
python -m training.train_classifier --style freestyle --epochs 50

# 3. Spuštění aplikace
python -m src.main

# 4. Testy
pytest tests/ -v
```

---

## 🏗️ Key Architecture

### Style Classifier (LSTM)
```
Input: [batch, 32, 48, 3]  # seq_len=32, keypoints=48, dims=3
    ↓ Flatten → [batch, 32, 144]
    ↓ LSTM (256 hidden, 2 layers, bidirectional)
    ↓ Attention pooling
    ↓ FC layers → [batch, 4]  # 4 classes
```

### Stroke Analyzer Flow
```
Keypoints → detect_stroke_cycles() → analyze_cycle()
    → compare_with_template() → FeedbackGenerator → Czech text
```

### Joint Definitions (angle_utils.py)
| Joint | Keypoint Indices |
|-------|------------------|
| left_elbow | L_UpperArm(20), L_Forearm(11), L_Hand(12) |
| right_elbow | R_UpperArm(39), R_Forearm(30), R_Hand(31) |
| left_shoulder | Neck(21), L_Clavicle(4), L_UpperArm(20) |
| body_alignment | Head(1), Spine2(41), Pelvis(0) |

---

## 📊 Training Config

```python
StyleClassifierConfig(
    num_keypoints=48,
    keypoint_dims=3,
    sequence_length=32,
    hidden_size=256,
    num_lstm_layers=2,
    num_classes=4,
    dropout=0.3,
    bidirectional=True,
    use_attention=True,
)
```

**Training params:**
- Loss: CrossEntropyLoss
- Optimizer: AdamW (lr=1e-3)
- Scheduler: CosineAnnealing
- Early stopping: patience=10
- Target: ≥85% accuracy

---

## 🔜 Next Steps

1. **Spustit generování template:**
   ```bash
   python -m training.template_generator --style freestyle
   ```

2. **Spustit trénink:**
   ```bash
   python -m training.train_classifier --style freestyle --epochs 50
   ```

3. **Přidat backstroke data** (až se dostahuje)

4. **Integrovat do UI** (Phase 2.5)

---

## 🚦 Current State

**Green Light** ✅: Phase 2.2-2.4 implementace hotová
**Yellow Light** ⚠️: Backstroke stahování probíhá
**Next** 🔜: Spustit trénink, integrovat do UI

---

_Session by: Claude Opus 4.5, 2026-01-13_
_Status: ML pipeline ready, awaiting training run_
