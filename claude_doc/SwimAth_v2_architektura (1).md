# SwimAth v2 — Architektura aplikace

## Přehled

Webová aplikace pro ML-based analýzu plavecké techniky. Uživatel (trenér/plavec) nahraje video natočené telefonem u bazénu, zvolí úroveň plavce a pohled kamery. Server video zpracuje, extrahuje pózu, porovná ji s referenčním modelem pro danou úroveň a vrátí zpětnou vazbu.

---

## Technologický stack

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND                         │
│              Vue.js 3 + Vite                        │
│         Tailwind CSS · Pinia · Axios                │
│                                                     │
│  Upload videa · Výběr úrovně/pohledu · Výsledky     │
│  Vizualizace pózy · Porovnání s referencí           │
└──────────────────────┬──────────────────────────────┘
                       │ REST API (JSON)
                       │ + WebSocket (progress)
┌──────────────────────▼──────────────────────────────┐
│                    BACKEND                          │
│              FastAPI (Python 3.11+)                  │
│                                                     │
│  ┌─────────────┐ ┌──────────────┐ ┌──────────────┐ │
│  │ API Router  │ │ Video Worker │ │ ML Pipeline  │ │
│  │ (endpoints) │ │ (Celery/bg)  │ │ (inference)  │ │
│  └─────────────┘ └──────────────┘ └──────────────┘ │
│                                                     │
│  ┌─────────────┐ ┌──────────────┐ ┌──────────────┐ │
│  │ Pose Est.   │ │ Biomech.     │ │ Comparator   │ │
│  │ ViTPose/    │ │ Extractor    │ │ (DTW/ML)     │ │
│  │ RTMPose     │ │              │ │              │ │
│  └─────────────┘ └──────────────┘ └──────────────┘ │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                   STORAGE                           │
│                                                     │
│  PostgreSQL        Redis          File Storage      │
│  (uživatelé,       (task queue,   (videa,           │
│   výsledky,        cache,         referenční        │
│   reference)       sessions)      modely)           │
└─────────────────────────────────────────────────────┘
```

---

## Detailní popis komponent

### 1. Frontend (Vue.js 3)

**Framework:** Vue 3 + Composition API + Vite (build tool)
**Styling:** Tailwind CSS
**State management:** Pinia
**HTTP klient:** Axios
**Vizualizace:** Canvas API nebo Three.js (pro overlay pózy na video)

#### Hlavní stránky / views:

```
/                   → Landing page
/upload             → Upload videa + nastavení parametrů
/analysis/:id       → Výsledky analýzy (po dokončení)
/history            → Historie analýz uživatele
/references         → Prohlížení referenčních vzorů (volitelné)
```

#### Upload flow:

```
┌──────────────────────────────────────────────────┐
│                  UPLOAD VIEW                      │
│                                                   │
│  1. Drag & drop / výběr video souboru             │
│                                                   │
│  2. Výběr parametrů:                              │
│     ┌─────────────────────────────────────────┐   │
│     │ Úroveň plavce:                         │   │
│     │   ○ Děti / začátečníci                  │   │
│     │   ○ Mírně pokročilí                     │   │
│     │   ○ Expert / závodní                    │   │
│     ├─────────────────────────────────────────┤   │
│     │ Pohled kamery:                          │   │
│     │   ○ Z boku (side-view)                  │   │
│     │   ○ Zepředu (front-view)                │   │
│     │   ○ Pod vodou (underwater)              │   │
│     ├─────────────────────────────────────────┤   │
│     │ Plavecký styl:                          │   │
│     │   ○ Kraul  ○ Znak  ○ Prsa  ○ Motýlek   │   │
│     └─────────────────────────────────────────┘   │
│                                                   │
│  3. [Analyzovat] → upload + start processing      │
│                                                   │
│  4. Progress bar (WebSocket real-time updates)     │
│     ████████░░░░░░░░ 52% — Extrakce pózy...       │
│                                                   │
│  5. Redirect na /analysis/:id po dokončení        │
└──────────────────────────────────────────────────┘
```

#### Výsledková stránka:

```
┌──────────────────────────────────────────────────┐
│              ANALYSIS VIEW                        │
│                                                   │
│  ┌─────────────────┐  ┌───────────────────────┐   │
│  │ Video přehrávač │  │ Biomechanické metriky │   │
│  │ s overlay pózy  │  │                       │   │
│  │                 │  │ Frekvence záběru: 42/m│   │
│  │  [▶] ──●────── │  │ Délka záběru: 1.8m    │   │
│  │                 │  │ Rotace těla: 38°      │   │
│  └─────────────────┘  │ Poloha hlavy: OK ✓    │   │
│                        │ Úhel loktu: 12° nízko│   │
│  ┌─────────────────┐  └───────────────────────┘   │
│  │ Srovnání        │                              │
│  │ s referencí     │  ┌───────────────────────┐   │
│  │                 │  │ Doporučení            │   │
│  │ Tvůj záběr  Ref│  │                       │   │
│  │   ╭╮    vs  ╭╮ │  │ • Loket o 12° výš     │   │
│  │  ╭╯╰╮      ╭╯╰╮│  │   při záběru          │   │
│  │  │  │      │  ││  │ • Rotace OK pro tvou  │   │
│  │  ╯  ╰      ╯  ╰│  │   úroveň              │   │
│  └─────────────────┘  └───────────────────────┘   │
└──────────────────────────────────────────────────┘
```

---

### 2. Backend (FastAPI)

#### Struktura projektu:

```
swimath-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app, CORS, lifecycle
│   ├── config.py               # Settings (Pydantic BaseSettings)
│   │
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   ├── router.py           # Hlavní router
│   │   ├── upload.py           # POST /api/upload
│   │   ├── analysis.py         # GET /api/analysis/{id}
│   │   ├── history.py          # GET /api/history
│   │   └── websocket.py        # WS /ws/progress/{task_id}
│   │
│   ├── ml/                     # ML pipeline
│   │   ├── __init__.py
│   │   ├── pose_estimator.py   # ViTPose / RTMPose wrapper
│   │   ├── biomechanics.py     # Výpočet metrik z keypoints
│   │   ├── comparator.py       # Porovnání s referencí (DTW/ML)
│   │   ├── feedback.py         # Generování zpětné vazby
│   │   └── models/             # Model weights (gitignored)
│   │       ├── vitpose_swim.pth
│   │       └── rtmpose_swim.onnx
│   │
│   ├── processing/             # Video zpracování
│   │   ├── __init__.py
│   │   ├── video_handler.py    # Upload, validace, ffmpeg
│   │   ├── frame_extractor.py  # Extrakce framů z videa
│   │   └── pipeline.py         # Orchestrace celého procesu
│   │
│   ├── references/             # Referenční databáze
│   │   ├── __init__.py
│   │   ├── manager.py          # CRUD pro reference
│   │   └── templates/          # Předpočítané referenční pózy
│   │       ├── beginner/
│   │       │   ├── freestyle_side.npy
│   │       │   ├── freestyle_front.npy
│   │       │   └── ...
│   │       ├── intermediate/
│   │       └── expert/
│   │
│   ├── db/                     # Databáze
│   │   ├── __init__.py
│   │   ├── database.py         # SQLAlchemy engine/session
│   │   ├── models.py           # ORM modely
│   │   └── migrations/         # Alembic migrace
│   │
│   └── utils/
│       ├── __init__.py
│       └── video_utils.py
│
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env
```

#### Klíčové API endpointy:

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SwimAth API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
)
```

```python
# app/api/upload.py
from fastapi import APIRouter, UploadFile, Form
from enum import Enum

class SkillLevel(str, Enum):
    beginner = "beginner"       # Děti / začátečníci
    intermediate = "intermediate"  # Mírně pokročilí
    expert = "expert"           # Expert / závodní

class CameraView(str, Enum):
    side = "side"               # Z boku
    front = "front"             # Zepředu
    underwater = "underwater"   # Pod vodou

class SwimStyle(str, Enum):
    freestyle = "freestyle"     # Kraul
    backstroke = "backstroke"   # Znak
    breaststroke = "breaststroke"  # Prsa
    butterfly = "butterfly"     # Motýlek

router = APIRouter()

@router.post("/api/upload")
async def upload_video(
    video: UploadFile,
    skill_level: SkillLevel = Form(...),
    camera_view: CameraView = Form(...),
    swim_style: SwimStyle = Form(...),
):
    # 1. Validace videa (formát, velikost, délka)
    # 2. Uložení na disk / object storage
    # 3. Vytvoření záznamu v DB
    # 4. Spuštění async tasku (Celery / BackgroundTasks)
    # 5. Vrácení task_id pro sledování progressu
    return {"task_id": task_id, "status": "processing"}
```

```python
# app/api/analysis.py
@router.get("/api/analysis/{analysis_id}")
async def get_analysis(analysis_id: int):
    # Vrátí kompletní výsledky analýzy
    return {
        "id": analysis_id,
        "status": "completed",
        "skill_level": "intermediate",
        "camera_view": "side",
        "swim_style": "freestyle",
        "metrics": {
            "stroke_rate": 42,          # záběrů/min
            "stroke_length": 1.8,       # metry
            "body_rotation": 38,        # stupně
            "head_position": "ok",
            "elbow_angle_deviation": -12,  # stupně od reference
            "kick_frequency": 6,        # kopů na cyklus
        },
        "comparison": {
            "reference_level": "intermediate",
            "overall_score": 72,        # 0-100
            "deviations": [
                {
                    "body_part": "left_elbow",
                    "metric": "catch_angle",
                    "actual": 142,
                    "reference": 155,
                    "severity": "moderate",
                    "feedback_cs": "Levý loket o 13° níže při záběru než reference"
                }
            ]
        },
        "pose_data": { ... },  # Keypoints pro vizualizaci
        "video_url": "/media/analyses/123/overlay.mp4"
    }
```

```python
# app/api/websocket.py
from fastapi import WebSocket

@router.websocket("/ws/progress/{task_id}")
async def progress_websocket(websocket: WebSocket, task_id: str):
    await websocket.accept()
    while True:
        progress = get_task_progress(task_id)
        await websocket.send_json({
            "progress": progress.percent,   # 0-100
            "stage": progress.stage,        # "uploading" / "extracting" / "pose_estimation" / "comparing" / "done"
            "message": progress.message     # "Extrakce pózy... snímek 145/300"
        })
        if progress.stage == "done":
            break
        await asyncio.sleep(0.5)
```

---

### 3. ML Pipeline — zpracování videa krok za krokem

```
Video input (MP4/MOV)
       │
       ▼
┌──────────────┐
│ 1. VALIDACE  │  Formát, rozlišení, délka (max 60s?), velikost
│    & PŘÍPRAV │  Normalizace FPS (např. na 30), resize
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ 2. EXTRAKCE  │  OpenCV VideoCapture
│    FRAMŮ     │  Každý N-tý frame nebo klíčové momenty
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ 3. DETEKCE   │  YOLOv8 nebo jednoduchý background subtraction
│    PLAVCE    │  Bounding box kolem plavce v každém framu
└──────┬───────┘
       │
       ▼
┌──────────────────────────────┐
│ 4. ODHAD PÓZY               │
│                              │
│  ViTPose-B / RTMPose-L       │
│  (fine-tuned na SwimXYZ      │
│   + reálná plavecká data)    │
│                              │
│  Input: crop framu           │
│  Output: 17 keypoints (COCO) │
│          + confidence scores  │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ 5. EXTRAKCE BIOMECH. METRIK │
│                              │
│  Z keypoints sekvence:       │
│  • Frekvence záběru (SR)     │
│  • Délka záběru (SL)         │
│  • Rotace těla               │
│  • Poloha hlavy              │
│  • Úhly kloubů (loket, rame)│
│  • Fáze záběru (catch, pull, │
│    push, recovery)           │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ 6. POROVNÁNÍ S REFERENCÍ    │
│                              │
│  Výběr referenčního vzoru:   │
│  skill_level × camera_view   │
│  × swim_style                │
│                              │
│  Metody:                     │
│  • DTW (Dynamic Time Warping)│
│    pro temporální sekvence   │
│  • Euklidovská vzdálenost    │
│    pro statické úhly         │
│  • Natrénovaný klasifikátor  │
│    pro detekci chyb          │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│ 7. GENEROVÁNÍ ZPĚTNÉ VAZBY  │
│                              │
│  Na základě odchylek:        │
│  deviation → pravidlo →      │
│  → text v češtině/angličtině │
│                              │
│  Příklady:                   │
│  • elbow_angle < ref - 10°   │
│    → "Loket o X° níž při     │
│       záběru"                │
│  • head_rotation > ref + 15° │
│    → "Přílišná rotace hlavy  │
│       při nádechu"           │
└──────────────────────────────┘
```

---

### 4. Referenční databáze — 3 úrovně

```
references/
├── beginner/               # Děti / začátečníci
│   ├── freestyle/
│   │   ├── side_view/
│   │   │   ├── pose_sequence.npy     # Sekvence keypoints
│   │   │   ├── metrics.json          # Očekávané rozsahy metrik
│   │   │   └── error_thresholds.json # Prahy pro chyby
│   │   ├── front_view/
│   │   └── underwater/
│   ├── backstroke/
│   ├── breaststroke/
│   └── butterfly/
│
├── intermediate/           # Mírně pokročilí
│   └── ... (stejná struktura)
│
└── expert/                 # Expert / závodní
    └── ... (stejná struktura)
```

#### Co obsahuje reference pro každou kombinaci:

```json
// references/intermediate/freestyle/side_view/metrics.json
{
  "stroke_rate": {
    "optimal_range": [35, 50],
    "unit": "strokes/min"
  },
  "body_rotation": {
    "optimal_range": [35, 55],
    "unit": "degrees"
  },
  "elbow_angle_catch": {
    "optimal_range": [145, 170],
    "unit": "degrees"
  },
  "head_position": {
    "description": "Hlava v neutrální pozici, oči dolů",
    "max_lateral_rotation": 45
  }
}
```

```json
// references/intermediate/freestyle/side_view/error_thresholds.json
{
  "errors": [
    {
      "id": "dropped_elbow",
      "condition": "elbow_angle_catch < 135",
      "severity": "moderate",
      "feedback_cs": "Padající loket při záběru — zkus držet loket výš",
      "feedback_en": "Dropped elbow during catch — try to keep elbow higher"
    },
    {
      "id": "excessive_head_rotation",
      "condition": "head_lateral_rotation > 60",
      "severity": "minor",
      "feedback_cs": "Přílišná rotace hlavy při nádechu",
      "feedback_en": "Excessive head rotation during breathing"
    },
    {
      "id": "insufficient_body_roll",
      "condition": "body_rotation < 25",
      "severity": "moderate",
      "feedback_cs": "Nedostatečná rotace těla — zkus rotovat víc z boků",
      "feedback_en": "Insufficient body rotation — try rotating more from hips"
    }
  ]
}
```

#### Jak se liší prahy podle úrovně:

| Metrika | Začátečník | Mírně pokročilý | Expert |
|---|---|---|---|
| Frekvence záběru | 25–40/min | 35–50/min | 45–65/min |
| Rotace těla | 20–45° | 35–55° | 45–60° |
| Úhel loktu (catch) | >120° OK | >140° OK | >150° OK |
| Tolerance odchylek | ±25° | ±15° | ±8° |

Začátečníkům se toleruje víc a feedback se zaměřuje na základy (poloha hlavy, dýchání, kopání). Expertům se hodnotí jemné detaily (EVF úhel, timing koordinace).

---

### 5. Databázový model

```python
# app/db/models.py
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, Enum
from sqlalchemy.orm import DeclarativeBase
import datetime

class Base(DeclarativeBase):
    pass

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Upload parametry
    video_path = Column(String, nullable=False)
    skill_level = Column(String, nullable=False)    # beginner/intermediate/expert
    camera_view = Column(String, nullable=False)     # side/front/underwater
    swim_style = Column(String, nullable=False)      # freestyle/backstroke/...

    # Status
    status = Column(String, default="processing")    # processing/completed/failed
    progress = Column(Integer, default=0)            # 0-100

    # Výsledky
    metrics = Column(JSON, nullable=True)            # biomechanické metriky
    deviations = Column(JSON, nullable=True)         # odchylky od reference
    feedback = Column(JSON, nullable=True)           # textová zpětná vazba
    pose_data_path = Column(String, nullable=True)   # cesta k .npy s keypoints
    overlay_video_path = Column(String, nullable=True)  # video s overlay

    overall_score = Column(Float, nullable=True)     # 0-100 celkové skóre
```

---

### 6. Deployment

```yaml
# docker-compose.yml
version: "3.9"

services:
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - api

  api:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./data/videos:/app/media/videos
      - ./data/models:/app/ml/models
    environment:
      - DATABASE_URL=postgresql://swimath:pass@db:5432/swimath
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  worker:
    build: ./backend
    command: celery -A app.worker worker --loglevel=info
    volumes:
      - ./data/videos:/app/media/videos
      - ./data/models:/app/ml/models
    environment:
      - DATABASE_URL=postgresql://swimath:pass@db:5432/swimath
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]   # pro ML inference

  db:
    image: postgres:16
    environment:
      - POSTGRES_DB=swimath
      - POSTGRES_USER=swimath
      - POSTGRES_PASSWORD=pass
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  pgdata:
```

---

### 7. Fáze vývoje

#### Fáze 1 — Základ (2–3 týdny)
- [ ] FastAPI projekt + základní endpointy (upload, status, výsledek)
- [ ] Vue.js projekt + upload formulář + progress bar
- [ ] Video upload + uložení + základní validace
- [ ] PostgreSQL + SQLAlchemy model
- [ ] Docker compose pro lokální dev

#### Fáze 2 — ML Pipeline (3–4 týdny)
- [ ] Integrace ViTPose/RTMPose (ONNX Runtime)
- [ ] Fine-tuning na SwimXYZ datasetu (side-view freestyle jako první)
- [ ] Extrakce keypoints z videa → .npy sekvence
- [ ] Výpočet biomechanických metrik z keypoints
- [ ] Video overlay s vizualizací pózy (OpenCV)

#### Fáze 3 — Referenční systém (2–3 týdny)
- [ ] Vytvoření referenčních vzorů pro 1. styl + 1. pohled + 3 úrovně
- [ ] DTW porovnávání sekvencí
- [ ] Pravidlový systém pro detekci chyb (error_thresholds.json)
- [ ] Generování textové zpětné vazby (CZ + EN)
- [ ] Skórovací systém (overall_score)

#### Fáze 4 — Frontend vizualizace (2 týdny)
- [ ] Výsledková stránka s metrikami
- [ ] Video přehrávač s overlay pózy (Canvas)
- [ ] Side-by-side porovnání s referencí
- [ ] Historie analýz
- [ ] Responsive design (mobil-friendly)

#### Fáze 5 — Rozšíření (průběžně)
- [ ] Další styly a pohledy kamery
- [ ] Front-view + underwater modely
- [ ] Vylepšení feedbacku na základě testování s reálnými plavci
- [ ] Uživatelské účty (volitelné)

---

### 8. Klíčová rozhodnutí k doladění

| Otázka | Doporučení | Alternativa |
|---|---|---|
| Async zpracování videa | Celery + Redis | FastAPI BackgroundTasks (jednodušší, ale méně škálovatelné) |
| Pose estimation model | RTMPose-L (rychlejší) | ViTPose-B (přesnější) |
| Porovnávací metoda | DTW + pravidlový systém | Natrénovaný klasifikátor chyb |
| Storage videí | Lokální filesystem | S3/MinIO (škálovatelnější) |
| Auth | Zatím žádný (MVP) | JWT + OAuth2 (později) |
| Max délka videa | 60 sekund | Delší = delší zpracování |
