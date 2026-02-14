# SwimAth - Výzkumný Deník

**Projekt**: SwimAth - Analýza plaveckého stylu pomocí strojového učení
**Autor**: [Jméno autora]
**Vedoucí práce**: [Jméno vedoucího]
**Instituce**: [Název školy]
**Rok**: 2026

---

## 1. Abstrakt

SwimAth je desktopová aplikace pro Windows určená k analýze plavecké techniky z video záznamů. Využívá počítačové vidění a strojové učení k detekci pózy plavce, klasifikaci plaveckého stylu a generování zpětné vazby pro zlepšení techniky.

**Klíčová slova**: pose estimation, swimming analysis, computer vision, MediaPipe, machine learning

---

## 2. Motivace a Cíle

### 2.1 Motivace

Analýza plavecké techniky tradičně vyžaduje přítomnost kvalifikovaného trenéra, který vizuálně hodnotí pohyby plavce. Tento přístup má několik omezení:

1. **Subjektivita**: Hodnocení závisí na zkušenostech a pozornosti trenéra
2. **Dostupnost**: Ne všichni plavci mají přístup k profesionálnímu trenérovi
3. **Kvantifikace**: Obtížné objektivně měřit pokrok v čase
4. **Zpětná vazba**: Okamžitá zpětná vazba během tréninku je omezená

### 2.2 Cíle projektu

1. Automatická detekce pózy plavce z video záznamu
2. Klasifikace plaveckého stylu (kraul, znak, prsa, motýlek)
3. Analýza techniky a porovnání s "ideálním" stylem
4. Generování konkrétní zpětné vazby v českém jazyce
5. Doporučení cvičení pro zlepšení identifikovaných nedostatků

### 2.3 Cílová skupina

Plavci střední úrovně (intermediate) - ne úplní začátečníci, ne profesionální sportovci. Tato skupina má největší potenciál pro zlepšení prostřednictvím technické analýzy.

---

## 3. Related Work (Rešerše)

### 3.1 Existující řešení pro analýzu plavání

| Řešení | Typ | Výhody | Nevýhody |
|--------|-----|--------|----------|
| Coach's Eye | Mobilní app | Zpomalené video, kreslení | Žádná automatická analýza |
| Swimbot | Wearable | Real-time feedback | Vyžaduje speciální hardware |
| TritonWear | Wearable | Profesionální metriky | Drahé, pro týmy |
| Acadiana | Desktop | Podrobná analýza | Manuální anotace |

**Závěr**: Existující řešení buď vyžadují speciální hardware (wearables), nebo neposkytují automatickou analýzu. Prostor pro desktop aplikaci s ML-based automatickou analýzou.

### 3.2 Pose Estimation Technologie

#### 3.2.1 Přehled technologií

| Technologie | Architektura | Keypoints | Rychlost | GPU Required |
|-------------|--------------|-----------|----------|--------------|
| **MediaPipe Pose** | BlazePose | 33 | ~30 FPS (CPU) | Ne |
| OpenPose | Multi-stage CNN | 25 | ~8 FPS | Ano |
| RTMPose (MMPose) | RTMDet + SimCC | 17-133 | ~50 FPS | Doporučeno |
| AlphaPose | SPPE | 17 | ~20 FPS | Ano |
| HRNet | High-Resolution Net | 17 | ~15 FPS | Ano |

#### 3.2.2 Rozhodnutí: MediaPipe Pose pro MVP

**Důvody volby**:
1. Běží na CPU bez GPU - dostupnější pro koncové uživatele
2. Dostatečná rychlost (~30 FPS) pro real-time zobrazení
3. 33 keypointů včetně prstů - detailnější než COCO 17
4. Jednoduchá integrace přes Python API
5. Aktivně udržovaný Google projektem

**Nevýhody** (akceptované pro MVP):
- Single-person detection (OK pro analýzu jednoho plavce)
- Není optimalizovaný pro underwater scény
- Méně přesný než state-of-the-art (HRNet, RTMPose)

**Plán**: RTMPose jako vylepšení v Phase 3 pro vyšší přesnost.

#### 3.2.3 Reference
- Bazarevsky et al., "BlazePose: On-device Real-time Body Pose tracking", CVPR 2020 Workshop
- Cao et al., "OpenPose: Realtime Multi-Person 2D Pose Estimation", IEEE TPAMI 2019
- Jiang et al., "RTMPose: Real-Time Multi-Person Pose Estimation", arXiv 2023

### 3.3 Dostupné Datasety

#### 3.3.1 Přehled datasetů pro plavání

| Dataset | Velikost | Styly | Anotace | Dostupnost | Rok |
|---------|----------|-------|---------|------------|-----|
| **SwimXYZ** | 300 GB | 4 | 2D/3D keypoints | Veřejný (Zenodo) | 2023 |
| SwimTrack | ? | ? | Bounding boxes | Registrace | 2022 |
| SVW | ~10 GB | 4 | Labels | Veřejný | 2017 |
| Roboflow Swimming | 100 MB | 4 | Class labels | Veřejný | 2023 |

#### 3.3.2 Rozhodnutí: SwimXYZ Dataset

**Zvoleno**: SwimXYZ (Fiche et al., 2023)

**Důvody**:
1. **Velikost**: 11,520 videí, 3.4M framů - dostatečné pro trénink ML modelu
2. **Anotace**: 2D i 3D keypoints - umožňuje trénink pose estimation
3. **Všechny styly**: Freestyle, Backstroke, Breaststroke, Butterfly
4. **Kvalita**: Syntetická data s ground truth - perfektní anotace
5. **Dostupnost**: Veřejně na Zenodo, akademická licence
6. **Dokumentace**: Publikovaný paper s detailním popisem

**Nevýhody** (akceptované):
- Syntetická data (ne reální plavci) - může být domain gap
- Velká velikost (300 GB) - náročné na úložiště

**Alternativy zamítnuty**:
- Roboflow: Příliš malý (291 obrázků) pro ML trénink
- SwimTrack: Vyžaduje registraci a schválení, nejistá dostupnost
- SVW: Starší dataset, méně dat, zastaralý formát

#### 3.3.3 SwimXYZ - Technické detaily

**Formát anotací** (zjištěno empiricky - není v dokumentaci):
- **NE** standardní COCO JSON formát
- Vlastní CSV formát se středníky jako oddělovačem
- Evropský desetinný formát (čárka místo tečky)

**Soubory na sekvenci**:
```
2D_cam.txt    - 2D keypoints v pixelových souřadnicích kamery
2D_pelvis.txt - 2D keypoints relativně k pánvi (normalizované)
3D_cam.txt    - 3D keypoints v souřadnicích kamery
3D_pelvis.txt - 3D keypoints relativně k pánvi (normalizované)
```

**Struktura hlavičky**:
```
Pelvis.x;Pelvis.y;Pelvis.z;Head.x;Head.y;Head.z;...
```

**48 keypointů**:
Pelvis, Head, HeadNub, Neck, Spine, Spine1, Spine2,
L/R Clavicle, L/R UpperArm, L/R Forearm, L/R Hand,
L/R Finger0-4, L/R Thigh, L/R Calf, L/R Foot, L/R Heel,
L/R Toe0-4, Ear_L, Ear_R, Eye_L, Eye_R, Nose

#### 3.3.4 Reference
- Fiche et al., "SwimXYZ: A Large-Scale Dataset for Swimming Motion Capture", arXiv:2310.04360, 2023
- Dataset: https://zenodo.org/record/8399376

### 3.4 Metody Analýzy Pohybu

#### 3.4.1 Dynamic Time Warping (DTW)

Pro porovnání plaveckého stylu s "ideálním" vzorem bude použit DTW algoritmus.

**Proč DTW**:
1. Tolerance k rozdílné rychlosti pohybu
2. Umožňuje porovnání sekvencí různé délky
3. Dobře zdokumentovaný a osvědčený pro analýzu pohybu

**Alternativy**:
- Euclidean distance: Příliš rigidní, neumí kompenzovat rychlost
- LSTM/Transformer: Komplexnější, vyžaduje více dat pro trénink

#### 3.4.2 Reference
- Müller, "Information Retrieval for Music and Motion", Springer 2007

---

## 4. Metodologie

### 4.1 Architektura Systému

```
┌─────────────────────────────────────────────────────────┐
│                    SwimAth Architecture                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │   Video     │    │   Frame     │    │    Pose     │ │
│  │  Processor  │───▶│   Buffer    │───▶│  Estimator  │ │
│  │  (OpenCV)   │    │  (Queue)    │    │ (MediaPipe) │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│        │                                      │         │
│        │              ┌─────────────┐         │         │
│        │              │    Style    │         │         │
│        └─────────────▶│ Classifier  │◀────────┘         │
│                       │  (YOLOv8)   │                   │
│                       └─────────────┘                   │
│                              │                          │
│                       ┌─────────────┐                   │
│                       │   Stroke    │                   │
│                       │  Analyzer   │                   │
│                       │   (DTW)     │                   │
│                       └─────────────┘                   │
│                              │                          │
│                       ┌─────────────┐                   │
│                       │  Feedback   │                   │
│                       │ Generator   │                   │
│                       └─────────────┘                   │
│                              │                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │              PySide6 GUI (Main Thread)            │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Threading Model

```
Main Thread (PySide6 Event Loop)
    │
    ├──▶ Video Decoder Thread (OpenCV)
    │         │
    │         ▼
    │    FrameBuffer (queue.Queue, maxsize=30)
    │         │
    │         ▼
    ├──▶ Pose Estimator Thread (MediaPipe)
    │         │
    │         ▼
    │    Results Queue
    │         │
    │         ▼
    └──▶ UI Renderer (QLabel + QPixmap)
```

**Důvody pro multi-threading**:
1. UI responsiveness - hlavní vlákno nesmí být blokované
2. Paralelní zpracování - dekódování a inference současně
3. Backpressure handling - frame buffer jako brzda při přetížení

### 4.3 Volba Technologií

| Komponenta | Technologie | Zdůvodnění |
|------------|-------------|------------|
| GUI Framework | PySide6 | LGPL licence, Qt ekosystém, cross-platform |
| Video Processing | OpenCV | De-facto standard, rychlý, dobře dokumentovaný |
| Pose Estimation | MediaPipe | CPU inference, 33 keypoints, jednoduchá integrace |
| Style Classifier | YOLOv8-cls | State-of-the-art, rychlý, transfer learning |
| ML Framework | PyTorch | Flexibilita, komunita, ONNX export |
| Inference | ONNX Runtime | Optimalizovaný, DirectML pro Windows |

### 4.4 Datový Pipeline

```
Video File (.mp4, .webm)
    │
    ▼
OpenCV VideoCapture
    │
    ▼
Frame Preprocessing
├── Resize (640x480)
├── Color conversion (BGR → RGB)
└── Normalization (optional)
    │
    ▼
MediaPipe Pose
    │
    ▼
Keypoint Extraction (33 points)
    │
    ▼
Style Classification (YOLOv8)
    │
    ▼
Stroke Analysis (DTW)
    │
    ▼
Feedback Generation (Czech)
```

---

## 5. Implementační Deník

### 5.1 Chronologický Záznam

#### Session 1: 2026-01-12 (Opus 4.5)

**Cíl**: Test MVP, stažení datasetu, příprava pro Phase 2

**Provedeno**:
1. ✅ Otestována MVP aplikace
   - Video přehrávání funguje
   - Skeleton overlay zobrazuje keypointy
   - Zelené body = vysoká confidence detekce

2. ✅ Opraveny runtime chyby
   - `pyqtSignal` → `Signal` (PySide6 kompatibilita)
   - `mp.solutions` type hint → `Any` (MediaPipe API)
   - Frame buffer timeout handling
   - Play/Pause threading logika

3. ✅ Stažen SwimXYZ dataset
   - Annotations: 6.7 GB (všechny styly)
   - Freestyle Part 1: 40.3 GB (590 .webm videí)

4. ✅ Přepsán prepare_dataset.py
   - Původní kód očekával COCO JSON
   - SwimXYZ používá vlastní CSV formát
   - Implementován parser pro středníkový CSV

5. ✅ Přidána podpora .webm formátu v GUI

6. ✅ **Phase 2.1: Dataset Loader implementován**
   - `training/swimxyz_parser.py` - CSV parser pro SwimXYZ formát
   - `training/dataset_loader.py` - PyTorch Dataset class
   - Sliding window sampling (seq_len=32, stride=16)
   - Auto-detekce dimenzí z CSV hlavičky
   - Lazy loading s volitelným cachingem

**Dataset Loader stats**:
- Train batches: 1,076 (base formát)
- Val batches: 219
- Test batches: 235
- Keypoints shape: `[batch=32, seq_len=32, keypoints=48, dims=3]`

**Zjištěné problémy**:
| Problém | Řešení |
|---------|--------|
| MediaPipe 0.10.31 nemá `solutions` | Downgrade na 0.10.14 |
| SwimXYZ není COCO formát | Vlastní CSV parser |
| Desetinná čárka v datech | `replace(',', '.')` |
| File dialog nevidí .webm | Přidán do filtru |
| COCO formát má data mismatch | Default filtr na "base" formát |
| "2D" soubory mají x,y,z | Auto-detekce dims z hlavičky |

**Zjištěné formáty keypointů v SwimXYZ**:
- **base** (48 kpts) - ✅ Funguje, použito jako default
- **body25** (25 kpts) - OpenPose formát
- **COCO** (25 kpts) - ⚠️ Data mismatch (header 75 cols, data 54 cols)

### 5.2 Problémy a Jejich Řešení

#### P1: MediaPipe API změna (KRITICKÉ)

**Symptom**: `AttributeError: module 'mediapipe' has no attribute 'solutions'`

**Příčina**: MediaPipe 0.10.31 změnil veřejné API

**Řešení**:
```bash
pip install mediapipe==0.10.14
```

**Poučení**: Vždy specifikovat přesnou verzi závislostí v requirements.txt

---

#### P2: SwimXYZ formát anotací

**Symptom**: `No annotation JSON files found`

**Příčina**: Dokumentace SwimXYZ nespecifikuje formát, předpokládali jsme COCO JSON

**Zjištění** (empirické):
- Soubory jsou `.txt`, ne `.json`
- CSV formát se středníky
- Evropský desetinný formát (čárka)

**Řešení**: Vlastní parser `parse_swimxyz_csv()`:
```python
def parse_swimxyz_csv(file_path: Path) -> Tuple[List[str], List[List[float]]]:
    # Handle semicolon separator
    values = line.split(';')
    # Handle European decimal format
    float(val.replace(',', '.'))
```

---

#### P3: PySide6 vs PyQt6 signály

**Symptom**: `ImportError: cannot import name 'pyqtSignal'`

**Příčina**: Kód používal PyQt syntaxi v PySide6 projektu

**Řešení**:
```python
# Špatně (PyQt6)
from PySide6.QtCore import pyqtSignal

# Správně (PySide6)
from PySide6.QtCore import Signal
```

---

## 6. Evaluace

*Bude doplněno po implementaci Phase 2*

### 6.1 Metriky
- Přesnost klasifikace stylu (accuracy, F1-score)
- Rychlost inference (FPS)
- Uživatelská spokojenost (dotazník)

### 6.2 Testovací data
- SwimXYZ test split
- Reálná videa plavců (budoucí sběr)

---

## 7. Reference

### Datasety
1. Fiche, G. et al. "SwimXYZ: A Large-Scale Dataset for Swimming Motion Capture." arXiv:2310.04360, 2023.
   - Dataset: https://zenodo.org/record/8399376

### Pose Estimation
2. Bazarevsky, V. et al. "BlazePose: On-device Real-time Body Pose tracking." CVPR Workshop, 2020.
   - https://google.github.io/mediapipe/solutions/pose

3. Cao, Z. et al. "OpenPose: Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields." IEEE TPAMI, 2019.

4. Jiang, T. et al. "RTMPose: Real-Time Multi-Person Pose Estimation based on MMPose." arXiv, 2023.

### Analýza pohybu
5. Müller, M. "Information Retrieval for Music and Motion." Springer, 2007.

### Technologie
6. PySide6 Documentation: https://doc.qt.io/qtforpython-6/
7. OpenCV Documentation: https://docs.opencv.org/
8. PyTorch Documentation: https://pytorch.org/docs/

---

*Poslední aktualizace: 2026-01-12*
