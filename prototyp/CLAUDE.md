# CLAUDE.md - SwimAth Project Instructions

**Project**: SwimAth - Swimming Style Analysis using ML
**Language**: Python 3.11+
**Platform**: Windows (primary), macOS (future)
**Type**: Desktop Application (PySide6)

---

## 🎯 Project Mission

Build a desktop application that analyzes swimming technique from videos using computer vision and machine learning, providing actionable feedback to intermediate-level swimmers in Czech language.

**Core Value**: Privacy-first, local processing, accurate feedback

---

## 🗣️ Communication

### ALWAYS Use Czech Language
- All responses to user in Czech
- Code comments in English (technical terms remain English)
- Commit messages in English (convention)
- User-facing strings in Czech
- Documentation can be Czech or English (user preference)

### User Profile
- **Expertise**: Senior developer, experienced
- **Style**: Direct, action-oriented, dislikes long explanations
- **Preference**: "Chci jít do hloubky" - deep technical implementation
- **Work Mode**: Solo developer, prefers concrete actions over plans

---

## 🏗️ Architecture Principles

### 1. Threading Model (CRITICAL)
```
Main Thread: PySide6 event loop (UI only)
    ↓
Video Decoder Thread: OpenCV frame extraction
    ↓ FrameBuffer (queue.Queue)
Pose Estimator Thread: MediaPipe inference
    ↓ Results Queue
UI Renderer: Display updates
```

**Rules**:
- NEVER block main thread (no heavy compute in UI)
- Use QThread for long-running operations
- Frame buffer max size: 30 frames (backpressure)
- All threads must be joinable on app close

### 2. Performance Targets (NON-NEGOTIABLE)
- Video processing: ≥20 FPS
- ML inference: <50ms per frame (MediaPipe), <100ms (ONNX)
- UI responsiveness: 60 FPS rendering
- Memory: No leaks during extended playback

### 3. Error Handling Strategy
```python
# Pattern 1: Graceful degradation
try:
    result = process_frame(frame)
except Exception as e:
    logger.error(f"Frame processing failed: {e}")
    # Continue with next frame, don't crash

# Pattern 2: User-facing errors
try:
    video = open_video(path)
except VideoError as e:
    QMessageBox.critical(self, "Chyba", f"Nepodařilo se otevřít video:\n{e}")
```

**Never**:
- Silent failures (always log)
- Generic error messages ("Something went wrong")
- Exceptions that crash the app

---

## 💻 Coding Standards

### Type Hints (MANDATORY)
```python
# ✅ Good
def process_frame(
    frame: np.ndarray,
    config: MediaPipeConfig
) -> Optional[PoseResult]:
    ...

# ❌ Bad
def process_frame(frame, config):
    ...
```

### Variable Declaration
```python
# ✅ Good - specific types (from .claude/CLAUDE.md)
frame_count: int = 0
results: List[PoseResult] = []

# ❌ Bad - generic var
var = 0
```

### Primary Constructors (prefer when possible)
```python
# ✅ Good - dataclass
@dataclass
class Frame:
    data: np.ndarray
    frame_number: int
    timestamp: float

# ✅ Also good - explicit __init__
class VideoProcessor:
    def __init__(self, video_path: Path, config: Config):
        self.video_path = video_path
        self.config = config
```

### DateTime Usage
```python
# ✅ Good
from datetime import datetime, timezone
timestamp = datetime.now(timezone.utc)  # or datetime.utcnow()

# ❌ Bad
timestamp = datetime.now()  # Local time, avoid
```

### Comments
```python
# ✅ Good - English, explains WHY
# Use DTW for temporal alignment because stroke cycles vary in duration
result = dtw_compare(user_sequence, reference_sequence)

# ❌ Bad - Czech or obvious
# Porovnáme sekvence
result = dtw_compare(user_sequence, reference_sequence)
```

---

## 🔧 Development Workflow

### 1. Before Making Changes
```bash
# Check current state
git status
git log --oneline -5

# Read relevant docs
cat TODO.md | grep "Phase X"
cat SESSION_HANDOFF.md | grep "What's NOT Done"
```

### 2. Making Changes
```python
# Pattern: Read → Modify → Test → Commit

# Step 1: Read existing code first
# NEVER propose changes without reading the file

# Step 2: Make incremental changes
# Small, logical units (one feature/fix per commit)

# Step 3: Test changes
pytest tests/test_yourmodule.py -v

# Step 4: Commit with meaningful message
git add src/yourmodule.py
git commit -m "Add feature X to module Y

- Implement Z functionality
- Add error handling for edge case W
- Update tests
"
```

### 3. Commit Message Format
```
Short summary (50 chars max)

Detailed description:
- What was changed
- Why it was changed
- Any breaking changes
- Related issue numbers

NO co-author tags (per user preference)
NO mentions of "Claude Code"
```

### 4. Testing Requirements
```bash
# Before every commit
pytest tests/ -v

# Before pushing
pytest tests/ -v --cov=src --cov-report=term-missing

# Target: ≥80% coverage
```

---

## 📦 Dependencies Management

### Adding New Dependencies
```python
# 1. Add to requirements.txt with version
torch>=2.1.0,<3.0.0

# 2. Document why it's needed (comment)
# torch: PyTorch for ML model training and inference

# 3. Test installation
pip install -r requirements.txt

# 4. Commit requirements.txt
git add requirements.txt
git commit -m "Add torch dependency for ML training"
```

### Phase-Specific Dependencies
- `requirements.txt`: Phase 1 (core app)
- `requirements-phase0.txt`: Phase 0 (dataset tools)
- Future: `requirements-dev.txt` (dev tools), `requirements-prod.txt` (minimal)

---

## 🎨 UI/UX Guidelines

### PySide6 Patterns
```python
# Pattern 1: Signals for threading
class Worker(QThread):
    result_ready = Signal(object)

    def run(self):
        result = heavy_computation()
        self.result_ready.emit(result)

# Pattern 2: Progress updates
self.progress_bar.setRange(0, total_frames)
self.progress_bar.setValue(current_frame)

# Pattern 3: Error dialogs
QMessageBox.critical(self, "Chyba", "Popis problému")
QMessageBox.warning(self, "Varování", "Upozornění")
QMessageBox.information(self, "Info", "Informace")
```

### Czech UI Strings
```python
# ✅ Good
self.open_button = QPushButton("Otevřít Video")
self.status_label.setText("Video načteno")

# Use f-strings for dynamic content
self.status_label.setText(f"Zpracováno {count} snímků")
```

---

## 🧪 Testing Strategy

### Test Structure
```python
# tests/test_module.py
import pytest
from src.module import function

def test_basic_functionality():
    """Test basic case"""
    result = function(input)
    assert result == expected

def test_edge_case():
    """Test edge case with explanation"""
    result = function(edge_input)
    assert result == expected_edge

def test_error_handling():
    """Test error handling"""
    with pytest.raises(ValueError):
        function(invalid_input)
```

### What to Test
- ✅ Public APIs (all functions/methods)
- ✅ Edge cases (empty input, None, large values)
- ✅ Error handling (exceptions raised correctly)
- ✅ Threading (no race conditions)
- ❌ Private methods (unless complex)
- ❌ Trivial getters/setters

---

## 📁 File Organization

### Module Structure
```
src/
├── core/          # Core functionality (video, pose, buffer)
├── ui/            # PySide6 GUI components
├── models/        # ML models and configs
├── analysis/      # Stroke analysis, feedback generation
├── integrations/  # External APIs (Strava, Apple Health)
├── database/      # SQLAlchemy models, migrations
├── recommendations/ # Training plans
└── utils/         # Helpers (logging, preprocessing)
```

### Naming Conventions
```python
# Files: snake_case
video_processor.py
stroke_analyzer.py

# Classes: PascalCase
class VideoProcessor:
class StrokeAnalyzer:

# Functions/methods: snake_case
def process_frame():
def calculate_angle():

# Constants: UPPER_SNAKE_CASE
MAX_BUFFER_SIZE = 30
DEFAULT_FPS = 30

# Private: _leading_underscore
def _internal_helper():
self._private_state = 0
```

---

## 🚫 Do NOT

### Code Practices
- ❌ Use `var` keyword (always specific type)
- ❌ Use `# type: ignore` or `# noqa` without explanation
- ❌ Leave `print()` statements (use logger)
- ❌ Hard-code paths (use Path objects, config)
- ❌ Suppress exceptions silently
- ❌ Write code without type hints
- ❌ Create files without reading existing similar files first

### Git Practices
- ❌ Commit without running tests
- ❌ Push broken code
- ❌ Make huge commits (>500 lines without good reason)
- ❌ Commit commented-out code
- ❌ Add co-author tags (user preference)

### Development Practices
- ❌ Over-engineer solutions (KISS principle)
- ❌ Add features not requested
- ❌ Refactor working code without reason
- ❌ Run `update-database` command (user preference)
- ❌ Break existing tests without fixing them

---

## ✅ Do ALWAYS

### Before Coding
1. Read SESSION_HANDOFF.md and TODO.md
2. Check current git status
3. Read existing code in the area you're modifying
4. Understand the threading model for the component

### While Coding
1. Add type hints to all functions
2. Write docstrings for public APIs
3. Log important events (info, warning, error)
4. Handle exceptions gracefully
5. Update TODO.md if tasks change

### After Coding
1. Run unit tests: `pytest tests/ -v`
2. Test manually if UI changes
3. Commit with meaningful message
4. Push to GitHub: `git push origin main`
5. Update documentation if needed

---

## 🏃 Common Tasks Quick Reference

### Start New Session
```bash
# 1. Read context
cat SESSION_HANDOFF.md
cat TODO.md | head -50

# 2. Check git status
git status
git log --oneline -5

# 3. Check dataset status
ls -la data/swimxyz/

# 4. Activate environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### Test Phase 1 MVP
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py  # Should open GUI
pytest tests/ -v    # Should pass 23 tests
```

### Add New Feature
```python
# 1. Create branch (optional but recommended)
git checkout -b feature/new-analysis

# 2. Implement in appropriate module
# src/analysis/new_analyzer.py

# 3. Add tests
# tests/test_new_analyzer.py

# 4. Update TODO.md
# Mark task as completed

# 5. Commit
git add src/analysis/new_analyzer.py tests/test_new_analyzer.py TODO.md
git commit -m "Add new analyzer feature"

# 6. Merge to main
git checkout main
git merge feature/new-analysis
git push origin main
```

### Download Dataset
```bash
# Quick start
scripts\quickstart_phase0.bat

# Annotations only (6.7 GB)
python scripts/download_dataset.py --dataset swimxyz --annotations-only

# Freestyle videos (75 GB)
python scripts/download_dataset.py --dataset swimxyz --style freestyle --all-parts

# Prepare for training
python scripts/prepare_dataset.py --dataset swimxyz --style freestyle

# Verify
python scripts/verify_dataset.py --dataset swimxyz --style freestyle --detailed
```

### Train ML Model (Phase 2)
```bash
# Generate reference template
python -m training.template_generator --style freestyle

# Train multi-style classifier (all 4 styles)
python -m training.train_classifier --multi-style --epochs 50 --no-amp

# Train single-style classifier
python -m training.train_classifier --style freestyle --epochs 50

# Output: models/best_model.pt, models/style_classifier.onnx
```

---

## 🎓 Key Architectural Decisions

### Why MediaPipe for MVP?
- **Pro**: Fast, accurate, runs on CPU, easy integration
- **Con**: Single-person only, not optimized for underwater
- **Future**: Replace with RTMPose (MMPose) in Phase 3

### Why PySide6 over PyQt6?
- **License**: LGPL vs GPL (PySide6 more permissive)
- **Performance**: Identical (both wrap Qt6)
- **Future**: Consider Tauri 2 for modern UI

### Why Windows-first?
- **User base**: Majority on Windows
- **DirectML**: Hardware acceleration via Windows ML API
- **Deployment**: Simpler (no App Store, no signing)
- **Future**: macOS port in Phase 4+ (same Python code, different packaging)

### Why Local-only Processing?
- **Privacy**: Health data stays on device
- **Speed**: No network latency
- **Cost**: No cloud infrastructure
- **GDPR**: Simpler compliance

---

## 📊 Performance Profiling

### If FPS is Low (<20)
```python
# 1. Profile with cProfile
python -m cProfile -o profile.stats src/main.py

# 2. Analyze
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumtime'); p.print_stats(20)"

# 3. Common bottlenecks
# - Frame resizing (use cv2.resize with INTER_LINEAR)
# - Pose inference (check MediaPipe complexity setting)
# - Drawing overlay (optimize cv2.line/circle calls)
# - Queue blocking (increase buffer size?)
```

### If Memory Grows
```python
# 1. Check for leaks
import tracemalloc
tracemalloc.start()
# ... run app for 10 minutes ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)

# 2. Common issues
# - Frames not released (keep weak references)
# - OpenCV Mat not freed (call frame.release())
# - Qt objects not deleted (use deleteLater())
```

---

## 🔍 Debugging Tips

### Video Processing Issues
```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check frame integrity
cv2.imwrite("debug_frame.jpg", frame)

# Verify threading
import threading
print(f"Current thread: {threading.current_thread().name}")
```

### Pose Estimation Issues
```python
# Check MediaPipe installation
import mediapipe
print(mediapipe.__version__)

# Verify frame format
print(f"Frame shape: {frame.shape}, dtype: {frame.dtype}")
# Should be: (H, W, 3), dtype: uint8, RGB order

# Check confidence thresholds
config.min_detection_confidence = 0.5  # Lower if no detections
```

### UI Issues
```python
# Check Qt threading
from PySide6.QtCore import QThread
assert QThread.currentThread() == app.thread(), "Must be main thread!"

# Debug signals
self.signal.connect(lambda x: print(f"Signal emitted: {x}"))
```

---

## 📚 Essential Reading

Before starting work, read these in order:
1. **SESSION_HANDOFF.md** - Complete technical context
2. **TODO.md** - Current task list
3. **PHASE0_DATASET_SETUP.md** - If working with datasets
4. **Plan file** - Original implementation plan (`.claude/plans/tingly-toasting-pearl.md`)

For specific tasks:
- Video processing: Read `src/core/video_processor.py` docstrings
- Pose estimation: Read MediaPipe docs + `src/core/pose_estimator.py`
- UI work: Read PySide6 docs + `src/ui/main_window.py`
- ML training: Read SwimXYZ paper + COCO format docs

---

## 🚀 Project Phases Overview

### Phase 0: Dataset Setup ✅
- Download infrastructure
- SwimXYZ dataset preparation (8,640 sequences, 2.6M frames)
- Verification tools

### Phase 1: MVP Application ✅
- Video processing + MediaPipe
- PySide6 GUI
- Skeleton visualization

### Phase 2: ML Training ✅
- Dataset loader (137k train samples, 4 styles)
- Style classifier (LSTM + Attention, **99.67% accuracy**)
- Stroke analyzer (DTW)
- Feedback generation (Czech)
- **Models**: `models/best_model.pt`, `models/style_classifier.onnx`

### Phase 3: Advanced Features 🔜
- Underwater correction
- Strava/Apple Health integration
- Training recommendations

### Phase 4+: Future 💡
- macOS port
- RTMPose integration
- Cloud sync (optional)

---

## ⚡ Quick Wins (If Stuck)

Low-hanging fruit for immediate progress:
- [ ] Add more unit tests (coverage <80%)
- [ ] Improve error messages (make them more specific)
- [ ] Add keyboard shortcuts (Space = play/pause)
- [ ] Create sample videos for testing
- [ ] Write docstrings for undocumented functions
- [ ] Add progress bar to video processing
- [ ] Implement video seeking/slider
- [ ] Create installer (PyInstaller)

---

## 🤝 Working with User

### User Says This → You Do This
- "MEGATHINK" → Use deep reasoning, comprehensive approach
- "připrav setup" → Create automation scripts + documentation
- "commitni to" → Make git commits immediately
- "potřebuju na jiném zařízení" → Create handoff docs
- "jdi do hloubky" → Deep technical implementation, no shortcuts

### Communication Style
- **Direct answers** (no fluff)
- **Show progress** (use TODO lists)
- **Concrete actions** (less talking, more doing)
- **Czech language** (always!)

---

## 📞 Emergency Contacts

**GitHub Issues**: https://github.com/VagnerVit/SwimAth.git/issues
**Dataset Problems**: Check Zenodo status page
**MediaPipe Issues**: https://github.com/google/mediapipe/issues

---

**Remember**: This is a privacy-first, local-processing, Windows desktop app for helping swimmers improve their technique. Every decision should align with these core values.

---

_Last Updated: 2026-01-13_
_Project Status: Phase 0-2 Complete, Phase 3 Ready_
_Next: End-to-end test, then Phase 3 (Underwater correction, Strava)_
