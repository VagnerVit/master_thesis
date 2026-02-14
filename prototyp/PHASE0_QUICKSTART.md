# Phase 0 Quick Start Cheatsheet

Rychlý přehled příkazů pro stažení a přípravu datasetů.

---

## 🚀 Quick Start (5 minut)

```bash
# 1. Setup environment
scripts\quickstart_phase0.bat  # Windows
bash scripts/quickstart_phase0.sh  # Linux/Mac

# 2. Download annotations (6.7 GB, ~15 min)
python scripts/download_dataset.py --dataset swimxyz --annotations-only

# 3. Download Freestyle Part 1 videos (37.5 GB, ~1-2 hours)
python scripts/download_dataset.py --dataset swimxyz --style freestyle --part 1

# 4. Prepare dataset
python scripts/prepare_dataset.py --dataset swimxyz --style freestyle

# 5. Verify
python scripts/verify_dataset.py --dataset swimxyz --style freestyle --detailed
```

**Total time**: ~2-3 hours (většinou download)
**Total disk**: ~45 GB

---

## 📥 Download Commands

### Minimální Setup (Pouze Annotations)
```bash
# 6.7 GB - rychlé, umožňuje exploraci bez videí
python scripts/download_dataset.py --dataset swimxyz --annotations-only
```

### Jeden Styl (Doporučeno pro testování)
```bash
# Freestyle only (~75 GB)
python scripts/download_dataset.py --dataset swimxyz --style freestyle --all-parts
```

### Všechny Styly (Full Dataset)
```bash
# 300 GB - pro production model
python scripts/download_dataset.py --dataset swimxyz --all-styles --all-parts
```

### Postupné Stahování
```bash
# Stáhnout styly jeden po druhém
python scripts/download_dataset.py --dataset swimxyz --style freestyle --part 1
python scripts/download_dataset.py --dataset swimxyz --style freestyle --part 2
python scripts/download_dataset.py --dataset swimxyz --style backstroke --part 1
# atd.
```

---

## 🛠️ Prepare Commands

### Jeden Styl
```bash
python scripts/prepare_dataset.py --dataset swimxyz --style freestyle
```

### Všechny Styly
```bash
python scripts/prepare_dataset.py --dataset swimxyz --all-styles
```

### Vlastní Split Ratio
```bash
# Default je 0.7/0.15/0.15 (train/val/test)
python scripts/prepare_dataset.py --dataset swimxyz --style freestyle --split 0.8/0.1/0.1
```

---

## ✅ Verify Commands

### Rychlá Verifikace
```bash
python scripts/verify_dataset.py --dataset swimxyz --style freestyle
```

### Detailní Verifikace
```bash
python scripts/verify_dataset.py --dataset swimxyz --style freestyle --detailed
```

### Pouze Annotations (Skip Videos)
```bash
python scripts/verify_dataset.py --dataset swimxyz --style freestyle --no-videos
```

### Ověřit Přehratelnost Videí (Pomalé)
```bash
python scripts/verify_dataset.py --dataset swimxyz --style freestyle --check-playable
```

---

## 📂 Výsledná Struktura

```
data/
├── swimxyz/
│   ├── annotations/              ← 6.7 GB (staženo --annotations-only)
│   │   ├── Freestyle_labels/
│   │   ├── Backstroke_labels/
│   │   ├── Breaststroke_labels/
│   │   ├── Butterfly_labels/
│   │   └── smpl_swimming_motions/
│   ├── videos/                   ← 293 GB (optional)
│   │   ├── freestyle/
│   │   │   ├── part1/  (~37.5 GB)
│   │   │   └── part2/  (~37.5 GB)
│   │   └── ...
│   └── processed/                ← Vytvořeno prepare_dataset.py
│       ├── freestyle/
│       │   ├── train_annotations.json
│       │   ├── val_annotations.json
│       │   ├── test_annotations.json
│       │   └── metadata.json
│       └── ...
└── downloads/  (temporary ZIPs, můžeš smazat po extrakci)
```

---

## 🔧 Troubleshooting

### Download se přerušil
```bash
# Resumable download
python scripts/download_dataset.py --dataset swimxyz --style freestyle --part 1 --resume
```

### Pomalé stahování
```bash
# Použij zenodo_get (rychlejší)
pip install zenodo_get
cd data/downloads
zenodo_get 8399376  # Annotations
zenodo_get 8402009  # Freestyle Part 1
```

### Nedostatek místa na disku
```bash
# Stahuj na external drive
python scripts/download_dataset.py --dataset swimxyz --output-dir /path/to/external/drive
```

### Verify selhalo
```bash
# Znovu stáhni konkrétní soubor
# Annotations
cd data/downloads
wget https://zenodo.org/record/8399376/files/Freestyle_labels.zip

# Manuální extrakce
7z x Freestyle_labels.zip -o../swimxyz/annotations/
```

---

## 📊 Dataset Stats (SwimXYZ)

| Styl | Videa | Annotace | Velikost |
|------|-------|----------|----------|
| **Freestyle** | 2,880 | ~850K snímků | 75 GB |
| **Backstroke** | 2,880 | ~850K snímků | 75 GB |
| **Breaststroke** | 2,880 | ~850K snímků | 75 GB |
| **Butterfly** | 2,880 | ~850K snímků | 75 GB |
| **Celkem** | 11,520 | 3.4M snímků | 300 GB |

**Annotations**: 6.7 GB (všechny styly)
**SMPL Motions**: 240 sekvencí

---

## 📝 Co Dál?

Po dokončení Phase 0:

1. **Exploratory Data Analysis**
   ```bash
   jupyter notebook notebooks/01_swimxyz_eda.ipynb
   ```

2. **Phase 2: ML Training**
   - Trénovat YOLOv8 style classifier
   - Vytvořit reference templates
   - Implementovat stroke analyzer

3. **Test MVP**
   ```bash
   python src/main.py
   # Otevři testovací video z datasetu
   ```

---

## 🔗 Užitečné Linky

- **SwimXYZ Paper**: https://arxiv.org/abs/2310.04360
- **SwimXYZ Website**: https://g-fiche.github.io/research-pages/swimxyz/
- **Zenodo Annotations**: https://zenodo.org/record/8399376
- **Full Documentation**: [PHASE0_DATASET_SETUP.md](PHASE0_DATASET_SETUP.md)

---

**Tip**: Začni s annotations-only a freestyle part1 pro rychlé testování pipeline (45 GB). Stáhni full dataset až když ověříš, že všechno funguje.
