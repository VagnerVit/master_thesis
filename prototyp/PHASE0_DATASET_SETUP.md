# Phase 0: Dataset Setup Guide

Tento dokument obsahuje kompletní instrukce pro stažení a přípravu datasetů pro SwimAth projekt.

---

## 📦 Dostupné Datasety

### 1. SwimXYZ Dataset ⭐ **DOPORUČENO**

**Největší a nejkomplexnější veřejný swimming dataset**

**Obsah**:
- 11,520 videí (3.4M snímků)
- Ground truth 2D/3D anotace kloubů
- 240 SMPL sekvencí pohybů
- Všechny 4 styly: Backstroke, Breaststroke, Butterfly, Freestyle
- 3 formáty anotací: COCO17, COCO25, Base (48 kloubů)

**Velikost**: 300GB celkem (6.7GB anotace + ~293GB videa)

**Download Links (Zenodo)**:

#### Anotace (POVINNÉ - 6.7 GB)
```bash
# Všechny label soubory
https://zenodo.org/record/8399376/files/Backstroke_labels.zip      # 1.6 GB
https://zenodo.org/record/8399376/files/Breaststroke_labels.zip    # 1.7 GB
https://zenodo.org/record/8399376/files/Butterfly_labels.zip       # 1.7 GB
https://zenodo.org/record/8399376/files/Freestyle_labels.zip       # 1.7 GB
https://zenodo.org/record/8399376/files/smpl_swimming_motions.zip  # ~100 MB
```

#### Videa - Backstroke (~75GB)
```bash
https://zenodo.org/record/8399837  # Part 1 (frontal/aerial views)
https://zenodo.org/record/8401680  # Part 2 (side views)
```

#### Videa - Breaststroke (~75GB)
```bash
https://zenodo.org/record/8401898  # Part 1
https://zenodo.org/record/8401923  # Part 2
```

#### Videa - Butterfly (~75GB)
```bash
https://zenodo.org/record/8401954  # Part 1
https://zenodo.org/record/8401974  # Part 2
```

#### Videa - Freestyle (~75GB) ⭐ **ZAČNI TADY**
```bash
https://zenodo.org/record/8402009  # Part 1
https://zenodo.org/record/8402031  # Part 2
```

**Dokumentace**: https://g-fiche.github.io/research-pages/swimxyz/
**Licence**: Veřejně přístupné (academic use)
**Formát**: ZIP archivy, videa MP4

---

### 2. Swimming Strokes Detection (Roboflow)

**Malý dataset pro rychlé experimenty**

**Obsah**: 291 anotovaných obrázků plavců

**Download**: https://universe.roboflow.com/gecko-vision/swimming-strokes-detection
**Formát**: YOLO, COCO, Pascal VOC, TFRecord (na výběr)
**Velikost**: ~100 MB
**Použití**: Doplněk pro testování

---

### 3. SwimTrack Dataset (MediaEval 2022)

**HD videa ze závodů (vyžaduje registraci)**

**Registrace**:
1. Vyplnit formulář: https://forms.gle/JcKoa5ycxR2KEiTJ7
2. Podepsat a vrátit smlouvu: https://multimediaeval.github.io/editions/2022/docs/MediaEval2022_UsageAgreement.pdf

**Info**: https://multimediaeval.github.io/editions/2022/tasks/swimtrack/
**GitHub**: https://github.com/centralelyon/swimtrack
**Kontakt**: romain.vuillemot@ec-lyon.fr

---

### 4. Sports Videos in the Wild (SVW)

**Smartphone videa (real-world conditions)**

**Download**: http://cvlab.cse.msu.edu/svw-download.html
**Obsah**: 4,200 videí (30 sportů včetně plavání)
**Poznámka**: Pouze bounding box anotace (ne pose)

---

## 🚀 Quick Start - Minimální Setup

Pro rychlé testování SwimAth pipeline doporučujeme:

### Krok 1: Stáhnout pouze anotace (6.7 GB)
```bash
cd data/
python ../scripts/download_dataset.py --dataset swimxyz --annotations-only
```

### Krok 2: Stáhnout 1 styl videa (Freestyle Part 1, ~37.5 GB)
```bash
python ../scripts/download_dataset.py --dataset swimxyz --style freestyle --part 1
```

### Krok 3: Extrahovat a připravit data
```bash
python ../scripts/prepare_dataset.py --dataset swimxyz --style freestyle
```

**Celkový disk space**: ~45 GB pro minimální setup

---

## 📥 Plný Setup - Všechny Datasety

### Doporučený postup:

#### 1. Nainstalovat download utility
```bash
pip install gdown zenodo_get tqdm
```

#### 2. Stáhnout všechny anotace (6.7 GB)
```bash
python scripts/download_dataset.py --dataset swimxyz --annotations-only
```

#### 3. Stáhnout videa po stylech
```bash
# Freestyle (~75 GB) - nejčastější styl
python scripts/download_dataset.py --dataset swimxyz --style freestyle --all-parts

# Backstroke (~75 GB)
python scripts/download_dataset.py --dataset swimxyz --style backstroke --all-parts

# Breaststroke (~75 GB)
python scripts/download_dataset.py --dataset swimxyz --style breaststroke --all-parts

# Butterfly (~75 GB)
python scripts/download_dataset.py --dataset swimxyz --style butterfly --all-parts
```

#### 4. Připravit datasety pro trénování
```bash
python scripts/prepare_dataset.py --dataset swimxyz --all-styles
```

**Celkový disk space**: ~300 GB pro plný SwimXYZ dataset

---

## 📂 Výsledná Struktura

Po dokončení setupu:

```
data/
├── swimxyz/
│   ├── annotations/
│   │   ├── Backstroke_labels/
│   │   ├── Breaststroke_labels/
│   │   ├── Butterfly_labels/
│   │   ├── Freestyle_labels/
│   │   └── smpl_swimming_motions/
│   ├── videos/
│   │   ├── backstroke/
│   │   │   ├── part1/
│   │   │   └── part2/
│   │   ├── breaststroke/
│   │   │   ├── part1/
│   │   │   └── part2/
│   │   ├── butterfly/
│   │   │   ├── part1/
│   │   │   └── part2/
│   │   └── freestyle/
│   │       ├── part1/
│   │       └── part2/
│   └── processed/
│       ├── train/
│       ├── val/
│       └── test/
├── roboflow/
│   └── swimming_strokes/
└── downloads/  # Temporary ZIP files
```

---

## 🛠️ Použití Download Skriptů

### Základní použití
```bash
# Zobrazit dostupné datasety
python scripts/download_dataset.py --list

# Stáhnout specifický dataset
python scripts/download_dataset.py --dataset swimxyz --style freestyle --part 1

# Resumable download (pokud přerušeno)
python scripts/download_dataset.py --dataset swimxyz --style freestyle --part 1 --resume
```

### Advanced možnosti
```bash
# Paralelní download (rychlejší)
python scripts/download_dataset.py --dataset swimxyz --annotations-only --parallel 4

# Ověřit integritu stažených souborů
python scripts/download_dataset.py --verify-only

# Smazat temporary ZIP soubory po extrakci
python scripts/download_dataset.py --dataset swimxyz --style freestyle --cleanup
```

---

## ✅ Verifikace Datasetu

Po stažení spusť verifikační skript:

```bash
python scripts/verify_dataset.py --dataset swimxyz
```

Zkontroluje:
- ✅ Všechny povinné soubory přítomny
- ✅ ZIP archivy nepoškozené
- ✅ Video soubory přehratelné
- ✅ Anotace ve správném formátu (COCO JSON)
- ✅ Odpovídající počet videí a anotací

---

## 🔧 Troubleshooting

### Problem: Download se přeruší
**Řešení**: Použij `--resume` flag pro pokračování
```bash
python scripts/download_dataset.py --dataset swimxyz --style freestyle --part 1 --resume
```

### Problem: Nedostatek místa na disku
**Řešení 1**: Stáhni pouze jeden styl (Freestyle)
```bash
python scripts/download_dataset.py --dataset swimxyz --style freestyle --all-parts
```

**Řešení 2**: Použij external HDD/SSD
```bash
python scripts/download_dataset.py --dataset swimxyz --output-dir /path/to/external/drive
```

### Problem: Pomalé stahování ze Zenodo
**Řešení**: Použij `zenodo_get` pro paralelní download
```bash
pip install zenodo_get
zenodo_get 8399376  # Pro anotace
```

### Problem: ZIP extrakce selhala
**Řešení**: Manuální extrakce
```bash
cd data/downloads
7z x Freestyle_labels.zip -o../swimxyz/annotations/
```

---

## 📊 Exploratory Data Analysis (EDA)

Po přípravě datasetu spusť EDA notebook:

```bash
jupyter notebook notebooks/01_swimxyz_eda.ipynb
```

Zkontroluje:
- Distribuce stylů plavání
- Kvalita anotací (missing keypoints, confidence scores)
- Video charakteristiky (resolution, FPS, duration)
- Train/val/test split stratifikace

---

## 📝 Poznámky

- **SwimXYZ je priority** - největší a nejkvalitnější dataset
- **Začni s Freestyle** - nejčastější styl, nejvíc dat
- **Anotace nejdřív** - pouhých 6.7 GB umožní exploraci před stažením videí
- **Roboflow jako fallback** - malý dataset pro rychlé experimenty pokud SwimXYZ není dostupný
- **Disk space planning**: 45 GB minimum, 300 GB pro full dataset

---

## 📚 Reference

- SwimXYZ Paper: https://arxiv.org/abs/2310.04360
- SwimXYZ Website: https://g-fiche.github.io/research-pages/swimxyz/
- MediaPipe Pose: https://google.github.io/mediapipe/solutions/pose
- COCO Keypoint Format: https://cocodataset.org/#format-data
