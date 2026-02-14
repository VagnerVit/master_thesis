# SwimAth - TODO List

**Last Updated**: 2026-01-14
**Current Phase**: Phase 2 Complete - Ready for Phase 3

---

## ✅ Completed Tasks

### Phase 0: Dataset Preparation
- [x] Create comprehensive dataset documentation (PHASE0_DATASET_SETUP.md)
- [x] Create quick reference cheatsheet (PHASE0_QUICKSTART.md)
- [x] Implement download/prepare/verify scripts
- [x] Download SwimXYZ annotations (6.7 GB) - all styles
- [x] Download Freestyle videos Part 1 + Part 2 (75 GB)
- [x] Run prepare_dataset.py → 8,640 sekvencí, 2.6M framů
- [x] Verify dataset integrity

### Phase 1: MVP Application
- [x] Video processing + MediaPipe pose estimation
- [x] PySide6 GUI with skeleton overlay
- [x] Unit tests (22 passing)

### Phase 2.1: Dataset Loader
- [x] `training/swimxyz_parser.py` - CSV parser pro SwimXYZ formát
- [x] `training/dataset_loader.py` - PyTorch Dataset class
- [x] Sliding window sampling (seq_len=32, stride=16) → ~34k samples
- [x] Support pro 48 keypoints (base formát)

### Phase 2.2: Reference Templates
- [x] `training/angle_utils.py` - výpočet úhlů kloubů
- [x] `training/template_generator.py` - generování šablon
- [x] `models/freestyle_template.json` - vygenerováno (18k samples, 11 kloubů)

### Phase 2.3: Style Classifier
- [x] `training/models/style_classifier.py` - LSTM model (4 třídy)
- [x] `training/train_classifier.py` - training script
- [x] Multi-style trénink (všechny 4 styly, 137k train samples)
- [x] **Test accuracy: 99.67%** (cíl ≥85% ✅)
  - Freestyle: 99.79%
  - Backstroke: 100.00%
  - Breaststroke: 99.75%
  - Butterfly: 99.15%
- [x] ONNX export (`models/style_classifier.onnx`)

### Phase 2.4: Stroke Analyzer
- [x] `src/analysis/dtw.py` - Dynamic Time Warping
- [x] `src/analysis/stroke_analyzer.py` - hlavní analyzátor
- [x] `src/analysis/feedback_generator.py` - český feedback

### Phase 2.5: UI Integration & Export
- [x] FeedbackWidget pro zobrazení analýzy
- [x] AnalysisWorker pro background processing
- [x] Integrace do MainWindow (QSplitter layout)
- [x] Export výsledků (JSON/PDF)
  - `src/export/json_exporter.py` - JSON export
  - `src/export/pdf_exporter.py` - PDF report s reportlab
  - Menu: Analysis → Export JSON/PDF (Ctrl+E, Ctrl+Shift+E)

---

## 🔄 In Progress

### End-to-End Testing
- [x] Manuální test: video → pose → classifier → feedback → export ✅

---

## 📋 Backlog

### UI Improvements
- [ ] Zobrazit počet detekovaných cyklů ve feedbacku
- [ ] Přidat lepší progress indikátor při full video analysis (% zpracovaných framů)
- [ ] Vizualizace detekovaných cyklů na timeline

### Dataset Expansion
- [x] Stáhnout Backstroke - HOTOVO (anotace)
- [x] Stáhnout Breaststroke - HOTOVO (anotace)
- [x] Stáhnout Butterfly - HOTOVO (anotace)
- [ ] Stáhnout Butterfly videa (part1 + part2) - OPTIONAL:
  - https://zenodo.org/record/8401954 (Part 1)
  - https://zenodo.org/record/8401974 (Part 2)
- [x] Multi-style classifier trénink - **HOTOVO (99.67% accuracy)**

---

### Phase 3: Advanced Features (AFTER PHASE 2)

#### 3.1 Underwater Correction
- [ ] Research refraction correction models (40%+ improvement)
- [ ] Implement src/analysis/underwater_correction.py
- [ ] Water surface detection (edge detection)
- [ ] Spatial coordinate transformation
- [ ] Test on underwater footage from SwimXYZ

#### 3.2 Strava Integration
- [ ] Implement src/integrations/strava_oauth.py
  - [ ] OAuth2 flow (localhost:8080 callback)
  - [ ] Token storage with encryption (Fernet)
  - [ ] Token refresh logic
- [ ] Implement src/integrations/strava_sync.py
  - [ ] Sync swimming activities
  - [ ] Rate limiting (100 req/15min)
  - [ ] Background sync job
- [ ] Create UI for Strava connection
- [ ] Store workouts in SQLite

#### 3.3 Apple Health Integration (OPTIONAL)
- [ ] Implement src/integrations/apple_health_importer.py
- [ ] Parse XML from export.zip
- [ ] Extract swimming workouts
- [ ] Handle stroke count metadata
- [ ] Create upload UI

#### 3.4 Training Recommendations
- [ ] Implement src/recommendations/training_planner.py
- [ ] Analyze historical data patterns
- [ ] Match video feedback with workout metrics
- [ ] Generate weekly training plans
- [ ] Create exercise database JSON

---

## 🐛 Known Issues / Tech Debt

- [ ] Add error handling for corrupted video files
- [ ] Implement proper logging rotation
- [ ] Add configuration file (YAML/TOML) instead of hardcoded values
- [ ] Create installer/packaging (PyInstaller for Windows .exe)
- [ ] Add progress bar for video processing
- [ ] Implement video seeking/slider
- [ ] Add keyboard shortcuts (Space = play/pause, etc.)
- [ ] Write integration tests (end-to-end video processing)
- [ ] Add CI/CD pipeline (GitHub Actions)
- [ ] Create user documentation / help dialog

---

## 🎯 Success Criteria

### Phase 1 MVP ✅
- [x] Video opens and plays
- [x] Pose estimation runs at ≥20 FPS
- [x] Skeleton overlay visible with confidence colors
- [x] No memory leaks during extended playback
- [x] Unit tests pass

### Phase 2 ML Training
- [ ] Style classifier ≥85% accuracy on test set
- [ ] Stroke analyzer generates meaningful feedback
- [ ] Inference <100ms per frame
- [ ] Czech language feedback

### Phase 3 Advanced
- [ ] Strava sync working with real account
- [ ] Training recommendations make sense (validated by coach)
- [ ] Underwater correction improves accuracy

---

## 📚 Documentation To Create

- [ ] API documentation (docstrings + Sphinx)
- [ ] User manual (CZ)
- [ ] Developer guide (contribution guidelines)
- [ ] Architecture diagram (system overview)
- [ ] Training manual (how to retrain models)
- [ ] Deployment guide (PyInstaller setup)

---

## 🔬 Research / Exploration

- [ ] Investigate RTMPose (MMPose) as MediaPipe replacement
- [ ] Explore DirectML NPU acceleration (Lunar Lake/Strix Point)
- [ ] Test ONNX Runtime DirectML provider performance
- [ ] Research SWOLF score calculation
- [ ] Investigate temporal consistency improvements
- [ ] Explore 3D pose estimation (depth from video)

---

## 💡 Future Ideas (Backlog)

- [ ] macOS port (Phase 4+)
- [ ] Web version (React + Python backend)
- [ ] Mobile companion app (iOS/Android)
- [ ] Cloud sync for workouts
- [ ] Social features (share analysis with coach)
- [ ] Garmin/Fitbit integration
- [ ] Live camera analysis (real-time feedback)
- [ ] VR training mode
- [ ] Multi-swimmer tracking
- [ ] Competition mode (compare with friends)

---

## 📊 Current Status Summary

**Phase 0**: ✅ Complete (Dataset ready)
**Phase 1**: ✅ MVP Complete
**Phase 2**: ✅ Complete (Style Classifier 99.67% accuracy)
**Phase 3**: 🔜 Planned

**Git**: https://github.com/VagnerVit/SwimAth.git
**Branch**: main

---

**Next Steps**:
1. End-to-end test: video → pose → classifier → feedback
2. Export výsledků (JSON/PDF)
3. Phase 3: Underwater correction, Strava integration
