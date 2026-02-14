# Dataset Download - Rychlý Průvodce

**Aktuální adresář**: `C:\Users\vvagner\source\repos\vitek\swimath`
**Stav datasetu**: ❌ Nestažený (folder `data/` je prázdný)

---

## 📍 Odkud Spouštět Příkazy

**✅ JSI UŽ NA SPRÁVNÉM MÍSTĚ!**

Všechny příkazy spouštíš z **root adresáře projektu** (tam kde už jsi):
```
C:\Users\vvagner\source\repos\vitek\swimath\
```

Zkontroluj:
```bash
pwd
# Mělo by vypsat: /c/Users/vvagner/source/repos/vitek/swimath
```

---

## 📂 Kam Se Stáhnou Datasety

Datasety se stáhnou do **`data/`** folderu v tomto adresáři:

```
C:\Users\vvagner\source\repos\vitek\swimath\data\
├── downloads/           ← Temporary ZIP files (můžeš smazat po extrakci)
└── swimxyz/
    ├── annotations/     ← 6.7 GB (POVINNÉ)
    │   ├── Freestyle_labels/
    │   ├── Backstroke_labels/
    │   ├── Breaststroke_labels/
    │   ├── Butterfly_labels/
    │   └── smpl_swimming_motions/
    ├── videos/          ← 293 GB (OPTIONAL)
    │   ├── freestyle/
    │   │   ├── part1/  (~37.5 GB)
    │   │   └── part2/  (~37.5 GB)
    │   └── ...
    └── processed/       ← Vytvořeno prepare_dataset.py
        └── freestyle/
            ├── train_annotations.json
            ├── val_annotations.json
            ├── test_annotations.json
            └── metadata.json
```

---

## 🚀 Krok za Krokem

### Krok 1: Setup Environment (2 minuty)

**Windows**:
```bash
scripts\quickstart_phase0.bat
```

**Nebo manuálně**:
```bash
# Aktivuj venv (pokud ještě není)
venv\Scripts\activate

# Instaluj Phase 0 dependencies
pip install -r requirements-phase0.txt
```

**Ověř instalaci**:
```bash
python -c "import tqdm, requests; print('OK')"
```

---

### Krok 2: Stáhnout Annotations (15 minut, 6.7 GB)

```bash
python scripts/download_dataset.py --dataset swimxyz --annotations-only
```

**Co to udělá**:
- Stáhne 5 ZIP souborů ze Zenodo
- Extrahuje je do `data/swimxyz/annotations/`
- Temporary ZIPs zůstanou v `data/downloads/`

**Očekávaný output**:
```
INFO: Downloading SwimXYZ annotations (6.7 GB)...
Freestyle_labels.zip: 100%|████| 1.7GB/1.7GB [05:30<00:00, 5.2MB/s]
INFO: Extracting: Freestyle_labels.zip
INFO: Extracted to: data\swimxyz\annotations\Freestyle_labels
...
INFO: Download complete!
```

**Ověř**:
```bash
ls data/swimxyz/annotations/
# Mělo by zobrazit 5 folderů
```

---

### Krok 3: Stáhnout Freestyle Videos Part 1 (1-2 hodiny, 37.5 GB)

```bash
python scripts/download_dataset.py --dataset swimxyz --style freestyle --part 1
```

**Co to udělá**:
- Stáhne Freestyle Part 1 videos ze Zenodo
- Umístí je do `data/swimxyz/videos/freestyle/part1/`

**⚠️ Důležité**:
Tento krok **vyžaduje zenodo_get** pro rychlé stahování.

**Pokud nemáš zenodo_get**:
```bash
pip install zenodo-get
```

**Alternative (manuální download)**:
1. Jdi na: https://zenodo.org/record/8402009
2. Klikni "Download" na každý soubor
3. Ulož do: `data/swimxyz/videos/freestyle/part1/`
4. Extrahuj ZIP soubory

---

### Krok 4: Připravit Dataset (5 minut)

```bash
python scripts/prepare_dataset.py --dataset swimxyz --style freestyle
```

**Co to udělá**:
- Load všechny COCO annotations
- Merge je dohromady
- Vytvoří train/val/test split (70/15/15)
- Uloží do `data/swimxyz/processed/freestyle/`

**Očekávaný output**:
```
INFO: Preparing SwimXYZ freestyle dataset...
INFO: Found 15 annotation files
INFO: Total: 2880 images, 850000 annotations
INFO: Split: train=2016, val=432, test=432
INFO: Saved train annotations: data\swimxyz\processed\freestyle\train_annotations.json
INFO: Saved metadata: data\swimxyz\processed\freestyle\metadata.json
INFO: Dataset prepared: data\swimxyz\processed\freestyle
```

---

### Krok 5: Ověřit Dataset (2 minuty)

```bash
python scripts/verify_dataset.py --dataset swimxyz --style freestyle --detailed
```

**Co to zkontroluje**:
- ✅ Annotations jsou validní JSON
- ✅ Správný počet souborů
- ✅ Train/val/test splits existují
- ⚠️ Videa jsou přítomna (varování pokud nejsou)

**Očekávaný output**:
```
=== SwimXYZ Dataset Verification ===

--- Freestyle ---

✓ Annotations directory: data\swimxyz\annotations\Freestyle_labels
✓ Found 15 annotation files
✓ All annotation files valid

✓ Part 1: Found 576 videos

✓ All processed files present
  Total images: 2880
  Total annotations: 850000
  Keypoints: 33

✓ Dataset verification passed!
```

---

## 📊 Disk Space Přehled

Po každém kroku:

| Krok | Spotřeba | Celkem |
|------|----------|---------|
| 0. Prázdný projekt | 0 GB | 0 GB |
| 1. Annotations only | 6.7 GB | **6.7 GB** |
| 2. + Freestyle Part 1 | 37.5 GB | **44.2 GB** |
| 3. + Processed splits | ~500 MB | **44.7 GB** |

**Optional**:
- Smazat `data/downloads/*.zip` po extrakci: ušetří ~6.5 GB
- Stáhnout i Part 2: další ~37.5 GB
- Stáhnout další styly: 3 × 75 GB = 225 GB

---

## ⚡ Quick Commands

**Zkontrolovat co už je stažené**:
```bash
ls -lh data/swimxyz/annotations/  # Anotace
ls -lh data/swimxyz/videos/        # Videa
ls -lh data/swimxyz/processed/     # Připravené splits
```

**Zjistit velikost**:
```bash
du -sh data/swimxyz/annotations/
du -sh data/swimxyz/videos/
du -sh data/swimxyz/
```

**Smazat temporary ZIPs** (po dokončení):
```bash
rm -rf data/downloads/
```

---

## 🔧 Troubleshooting

### "Command not found: python"
```bash
# Zkus python3
python3 scripts/download_dataset.py --dataset swimxyz --annotations-only

# Nebo aktivuj venv znovu
venv\Scripts\activate
```

### "No module named 'tqdm'"
```bash
pip install -r requirements-phase0.txt
```

### "Download se přerušil"
```bash
# Resume download
python scripts/download_dataset.py --dataset swimxyz --style freestyle --part 1 --resume
```

### "Nedostatek místa na disku"
```bash
# Stáhni jen annotations (6.7 GB)
python scripts/download_dataset.py --dataset swimxyz --annotations-only

# Nebo změň output directory na external disk
python scripts/download_dataset.py --dataset swimxyz --output-dir D:\swimath_data
```

### "zenodo_get not found"
```bash
pip install zenodo-get
```

### "Ověření selhalo"
```bash
# Verbose mode pro detaily
python scripts/verify_dataset.py --dataset swimxyz --style freestyle --detailed

# Zkontroluj pouze annotations (skip videos)
python scripts/verify_dataset.py --dataset swimxyz --style freestyle --no-videos
```

---

## 📝 Příklad Kompletního Workflow

```bash
# 0. JSI UŽ ZDE
pwd
# /c/Users/vvagner/source/repos/vitek/swimath

# 1. Setup (pokud ještě ne)
venv\Scripts\activate
pip install -r requirements-phase0.txt

# 2. Download annotations (6.7 GB, ~15 min)
python scripts/download_dataset.py --dataset swimxyz --annotations-only

# 3. Download Freestyle Part 1 (37.5 GB, ~1-2 hours)
pip install zenodo-get
python scripts/download_dataset.py --dataset swimxyz --style freestyle --part 1

# 4. Prepare dataset (~5 min)
python scripts/prepare_dataset.py --dataset swimxyz --style freestyle

# 5. Verify (~2 min)
python scripts/verify_dataset.py --dataset swimxyz --style freestyle --detailed

# 6. Check results
ls -lh data/swimxyz/processed/freestyle/
```

**Celkový čas**: ~2-3 hodiny (většinou čekání na download)
**Celkový disk**: ~45 GB

---

## ✅ Jak Poznáš Že Jsem Hotový

Dataset je připravený když:
- ✅ `data/swimxyz/annotations/` obsahuje 5 folderů
- ✅ `data/swimxyz/videos/freestyle/part1/` obsahuje ~576 MP4 souborů
- ✅ `data/swimxyz/processed/freestyle/` obsahuje 4 JSON soubory
- ✅ `verify_dataset.py` vypíše "Dataset verification passed!"

**Pak můžeš začít Phase 2 ML training!** 🚀

---

## 📚 Další Info

- **Detailní dokumentace**: `PHASE0_DATASET_SETUP.md`
- **Quick commands**: `PHASE0_QUICKSTART.md`
- **Troubleshooting**: `PHASE0_DATASET_SETUP.md` → Troubleshooting sekce

---

**Shrnutí**: Spouštíš všechno **ODSUD** (root projektu), datasety se stáhnou do `data/` folderu, který už je vytvořený. Easy! 🎯
