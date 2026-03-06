# Fine-Tuning Modelů Pose Estimation pro Plaveckou Doménu
## Komplexní Research Report pro Diplomku SwimAth

**Kompilace**: Akademické papery + current best practices (únor 2026)
**Aktualizace**: Březen 2026 — GPU omezení odstraněna (přístup k serveru s více GPU)
**Cíl**: Fine-tuning ViTPose + RTMPose na SwimXYZ datasetu

---

## Stručné Shrnutí

Klíčová zjištění:

- **ViTPose** (NeurIPS 2022): Nejflexibilnější pro domain adaptation. S dostatkem GPU je **ViTPose-L** (307M params, 78.3 AP) optimální volba — víc parametrů = lepší transfer learning.
- **RTMPose** (2023): Lepší inference speed (350+ FPS pro RTMPose-l), lehčí model, production-ready. **RTMPose-l** (27.6M params, 74.8 AP) nabízí nejlepší accuracy/speed trade-off.
- **GPU zdroje**: Server s více GPU → větší modely (ViTPose-H 632M), větší batch sizes, paralelní experimenty.
- **SwimXYZ formát**: COCO17-compatible s expanded keypoint setem (Base48 format), vyžaduje konverzi.
- **Kritická výzva**: Synthetic-to-real domain gap (SwimXYZ syntetický → reálná videa s šumem, refrakcí, okluzí).

---

## Část 1: ViTPose — Fine-Tuning Strategie

### 1.1 Přehled Architektury

**ViTPose** je plain Vision Transformer s:
- Jednoduchým, non-hierarchickým encoder-decoder designem
- Škálovatelnou kapacitou (ViT-B, ViT-L, ViT-H: 20M–1B parametrů)
- Patch embedding (16×16) s MAE pre-training
- Dvěma decoder variantami: Classic (deconvolution) a Simple (bilinear upsampling)

**Klíčová výhoda**: Výborně funguje s omezenými labeled daty díky strong MAE pre-training inicializaci.

### 1.2 Varianty Modelu — Kompletní Porovnání

| Varianta | Params | COCO AP | VRAM (FP16, batch=64) | Training Speed | Domain Adaptation |
|----------|--------|---------|----------------------|----------------|-------------------|
| **ViTPose-S** | 24M | 73.8 | ~8 GB | Velmi rychlý | Dobrá |
| **ViTPose-B** | 86M | 75.8 | ~16 GB | Rychlý | Velmi dobrá |
| **ViTPose-L** | 307M | 78.3 | ~32 GB | Střední | Výborná |
| **ViTPose-H** | 632M | 79.1 | ~48 GB | Pomalý | Nejlepší |

**Doporučení pro diplomku**: **ViTPose-L** jako primární (nejlepší accuracy/compute trade-off se serverovými GPU). ViTPose-H jen pokud je k dispozici multi-GPU trénink.

### 1.3 Fine-Tuning Konfigurace

#### Doporučená Strategie — Tříetapový Přístup

| Etapa | Epochs | LR Schedule | Zmrazené vrstvy | Účel |
|-------|--------|-------------|-----------------|------|
| 1: Decoder | 30 | 5e-4 → 1e-4 | Backbone + Neck | Naučit task-specific features |
| 2: Backbone (pozdní) | 50 | 1e-4 → 1e-5 | Early backbone | Adaptovat high-level reprezentace |
| 3: Joint fine-tuning | 130 | 1e-5 → 1e-6 | Žádné (all unfrozen) | Fine-grained adaptace |

#### Paramwise LR (kritické)

```yaml
paramwise_cfg:
  custom_keys:
    'backbone': dict(lr_mult=0.1)    # 10× pomalejší než decoder
    'neck': dict(lr_mult=0.5)
    'head': dict(lr_mult=1.0)        # Full LR pro task-specific head
```

#### Tréninkové Parametry (Server GPU)

```python
train_cfg = dict(max_epochs=210, val_interval=10)

data_loaders = dict(
    batch_size=64,       # Per GPU — server to zvládne
    num_workers=8,
    persistent_workers=True,
)

# Multi-GPU: DistributedDataParallel
# torchrun --nproc_per_node=4 tools/train.py config.py --launcher pytorch
# Effective batch size = 64 × 4 = 256
```

#### Knowledge Distillation (bonusový experiment)

```python
# ViTPose-H (teacher) → ViTPose-B (student)
loss_token_distill = MSE(student_token, teacher_token)
loss_total = loss_output + α * loss_token_distill  # α ≈ 0.2
```

### 1.4 Data Augmentation pro Plaveckou Doménu

**Kritické pro synthetic→real transfer:**

```python
# Standard augmentation
- RandomFlip (prob=0.5)
- RandomAffine (degrees=30, translate=0.1, scale=0.8-1.2)
- ColorJitter (brightness=0.2, contrast=0.2)

# Underwater-specific
- GaussNoise (p=0.3, var=0.01)           # Image noise
- RandomBlur (p=0.2, sigma=0.5-2.0)      # Simuluj refrakci/bubbles
- WaterArtifacts (occlusion_prob=0.3)     # Vodní linie, reflekce
- AmplitudeSpectrumMixing (alpha=0.5)     # Frequency domain blending
```

---

## Část 2: RTMPose — Fine-Tuning Strategie

### 2.1 Přehled Architektury

**RTMPose** (Real-Time Multi-Person Pose Estimation):
- CSPNeXt backbone
- SimCC head (coordinate classification místo heatmaps) — 2.5× méně parametrů
- **Inference**: 90+ FPS na CPU, 430+ FPS na GPU

### 2.2 Varianty Modelu

| Varianta | Params | COCO AP | Inference (GPU) | VRAM (FP16, batch=64) |
|----------|--------|---------|----------------|----------------------|
| **RTMPose-s** | 5.5M | 68.6 | 600+ FPS | ~4 GB |
| **RTMPose-m** | 13.6M | 72.2 | 430+ FPS | ~8 GB |
| **RTMPose-l** | 27.6M | 74.8 | 350+ FPS | ~12 GB |

**Doporučení**: **RTMPose-l** jako primární (nejlepší accuracy v RTMPose rodině, stále real-time).

### 2.3 Porovnání ViTPose-L vs RTMPose-l

| Kritérium | ViTPose-L | RTMPose-l | Vítěz |
|-----------|-----------|-----------|-------|
| **Inference speed** | ~30 FPS | 350+ FPS | RTMPose |
| **Model size** | 307MB | ~110MB | RTMPose |
| **Fine-tuning na malých datech** | Excellent | Good | ViTPose |
| **Domain adaptation** | Velmi flexibilní | Přímá | ViTPose |
| **Interpretability** | Attention mapy | CNN-based | ViTPose |
| **Production deployment** | Pomalý | Real-time | RTMPose |
| **COCO AP** | 78.3 | 74.8 | ViTPose |

**Doporučení**: Použij **oba** — ViTPose-L pro maximální accuracy, RTMPose-l pro real-time pipeline.

### 2.4 Tréninkový Setup (Server GPU)

```yaml
model:
  backbone:
    type: 'CSPNeXt'
    depth: 'l'  # large varianta
  head:
    type: 'RTMCCHead'
    out_channels: 48  # SwimXYZ Base format
    loss_keypoint:
      type: 'KLDiscretLoss'
      beta: 10.0

train_dataloader:
  batch_size: 128  # RTMPose je velmi memory-efficient
  num_workers: 8

optim_wrapper:
  optimizer:
    type: 'AdamW'
    lr: 0.004
    weight_decay: 0.05
  type: 'AmpOptimWrapper'
  dtype: 'float16'
```

---

## Část 3: Domain Adaptation — Synthetic-to-Real Gap

### 3.1 Challenge SwimXYZ

**SwimXYZ** (syntetický):
- Čisté renderování, perfektní osvětlení
- Žádná water line ambiguity
- 3.4M bezšumových snímků

**Reálný svět** (co musí model zvládat):
- Refrakce u vodní hladiny
- Bubliny, splash, spray
- Variabilní podvodní osvětlení
- Časté okluze (hlava pod vodou)
- Temporal jitter

### 3.2 Strategie Bridging the Gap

#### A: Amplitude Spectrum Augmentation
```python
def amplitude_mixing(synthetic_img, real_img, alpha=0.5):
    """Blend amplitude spectrum pro domain adaptation."""
    synth_fft = np.fft.fft2(synthetic_img)
    real_fft = np.fft.fft2(real_img)
    synth_phase = np.angle(synth_fft)
    mixed_amp = alpha * np.abs(real_fft) + (1 - alpha) * np.abs(synth_fft)
    mixed_fft = mixed_amp * np.exp(1j * synth_phase)
    return np.clip(np.fft.ifft2(mixed_fft).real, 0, 255).astype(np.uint8)
```

#### B: Occlusion-Aware Training
```python
def add_water_artifacts(image, occlusion_prob=0.3):
    """Přidej underwater artifacts — vodní linie, bubliny."""
    # Simuluj water surface occlusion (horizontal band)
    # Přidej bubliny (random bright circles)
    # Gaussian blur v náhodných pásech
```

#### C: Graduated Fine-Tuning

| Fáze | Zmrazené | LR | Epochs | Data | Účel |
|------|----------|-----|--------|------|------|
| 1 | All but head | 1e-4 | 30 | SwimXYZ | Task-specific features |
| 2 | Early layers | 5e-5 | 50 | SwimXYZ + 20% real | Domain adaptation |
| 3 | None | 1e-5 | 130 | Balanced mix | Full fine-tuning |

---

## Část 4: Kompletní Benchmark Plán (Server GPU)

### 5.1 Matice Modelů

| Model | Params | COCO AP | Inference | Batch/GPU (FP16) | Role v Diplomce |
|-------|--------|---------|-----------|------------------|-----------------|
| **ViTPose-H** | 632M | 79.1 | ~20 FPS | 32-48 | Max accuracy (pokud multi-GPU) |
| **ViTPose-L** | 307M | 78.3 | ~30 FPS | 64 | **Primární** — accuracy |
| **ViTPose-B** | 86M | 75.8 | ~50 FPS | 128 | Ablace (vliv velikosti) |
| **RTMPose-l** | 27.6M | 74.8 | 350+ FPS | 256 | **Primární** — real-time |
| **RTMPose-m** | 13.6M | 72.2 | 430+ FPS | 256+ | Speed ablace |

### 5.2 Doporučený Design Benchmarku

**Tier 1 — Povinné pro diplomku:**
1. **ViTPose-L** fine-tuned na SwimXYZ → primární accuracy model
2. **RTMPose-l** fine-tuned na SwimXYZ → primární speed model

**Tier 2 — Ablace:**
4. **ViTPose-B** → vliv velikosti modelu (B vs L)
5. **RTMPose-m** → speed/accuracy trade-off v RTMPose rodině
**Tier 3 — Pokročilé (pokud zbude čas):**
7. **ViTPose-H** → maximální accuracy experiment
8. **Distillation**: ViTPose-H → ViTPose-B
9. **Cross-style generalizace**: trénink na freestyle, test na backstroke

### 5.3 Odhady Tréninku (Server GPU)

Předpoklad: 1× A100 (80GB) nebo ekvivalent.

```
Model          | Batch/GPU | Per-Epoch | Celkem (210 ep) | Poznámka
---------------|-----------|-----------|-----------------|-------
ViTPose-H      | 48        | ~8 min    | ~28 hodin       | Potřebuje 40+ GB VRAM
ViTPose-L      | 64        | ~5 min    | ~18 hodin       | Sweet spot
ViTPose-B      | 128       | ~3 min    | ~10 hodin       | Velmi rychlé
RTMPose-l      | 256       | ~2 min    | ~7 hodin        | Nejrychlejší
RTMPose-m      | 256       | ~1.5 min  | ~5 hodin        | Quick ablation
```

**Multi-GPU scaling** (near-linear):
- 2× GPU ≈ 0.55× čas
- 4× GPU ≈ 0.30× čas

**Implikace**: Se serverovými GPU zvládneš **všechny 4 modely za ~40 GPU-hodin**. Paralelně na 2+ GPU → hotovo za 1-2 dny.

### 5.4 Server GPU Konfigurace

```yaml
# config_swimath_vitpose_l_server.py

train_cfg = dict(max_epochs=210, val_interval=10)

train_dataloader = dict(
    batch_size=64,          # Per GPU
    num_workers=8,
    persistent_workers=True,
)

optim_wrapper = dict(
    type='AmpOptimWrapper',  # Mixed precision stále pro rychlost
    dtype='float16',
    optimizer=dict(type='AdamW', lr=0.001, weight_decay=0.01),
    paramwise_cfg=dict(
        custom_keys={
            'backbone': dict(lr_mult=0.1),
            'neck': dict(lr_mult=0.5),
            'head': dict(lr_mult=1.0),
        }
    ),
)

# Linear LR scaling rule: lr = base_lr × (batch_size × num_gpus / 256)
```

```bash
# Multi-GPU spuštění
torchrun --nproc_per_node=4 tools/train.py config.py --launcher pytorch
```

---

## Část 6: SwimXYZ Dataset Formát & Konverze

### 7.1 Formát Anotací

- **Base format**: 48 keypoints (full body + hands + feet)
- **Poskytované formáty**: COCO17 (subset), COCO25 (extended)
- **Viditelnost**: v=0 (unlabeled), v=1 (occluded), v=2 (visible)

### 7.2 Konverze pro MMPose

```python
# Pokud COCO-compliant → přímé použití
dataset = dict(type='CocoDataset', data_root='data/swimxyz/', ...)

# Jinak → custom dataset class
@DATASETS.register_module(name='SwimXYZDataset')
class SwimXYZDataset(BaseDataset):
    METAINFO = dict(
        dataset_name='swimxyz',
        keypoint_info={...},  # 48 keypoints
        skeleton_info={...},  # connectivity
        joint_weights=[1.0] * 48,
        sigmas=[0.026] * 48,
    )
```

### 7.3 Doporučení

Trénuj na **Base48** (full SwimXYZ format) namísto downsamplingu na COCO17. Extra hand keypoints kritické pro plaveckou analýzu (úhel vstupu ruky, pozice zápěstí).

---

## Část 8: Běžné Chyby & Řešení

| Problem | Příčina | Řešení |
|---------|---------|--------|
| **Špatná accuracy** | LR příliš vysoký | Paramwise LR (backbone 0.1× head) |
| **Overfitting k SwimXYZ** | Syntetická data nse generalizují | Heavy augmentation; freeze early layers déle |
| **Keypoint jitter** | Temporal inconsistency | Butterworth filter post-processing |
| **Water line confuses** | No underwater training data | Synthetic water artifacts augmentace |
| **Left/right swaps** | Side-view ambiguity | Activity-conditioning (swimming style) |
| **Multi-GPU divergence** | LR příliš vysoký pro velký batch | Linear LR scaling rule |
| **OOM na ViTPose-H** | Model příliš velký pro 1 GPU | Gradient checkpointing / model parallelism |
| **Nestabilní trénink** | Velký batch + vysoký LR | Warmup (5 epochs, linear 1e-6 → target) |

---

## Část 9: Doporučení pro SwimAth

### Aktualizovaný Experimentální Plán (Server GPU)

1. **Benchmark Phase (2-3 týdny)**
   - Spusť všechny Tier 1 + Tier 2 experimenty (~80 GPU-hodin, paralelizovatelné)
   - Trénuj ViTPose-L + RTMPose-l na **full** SwimXYZ (ne jen 10% subset)
   - Měř: PCK@0.2, AP, inference FPS, per-joint accuracy
   - Decision point: primární model

2. **Domain Adaptation Phase (2-3 týdny)**
   - Amplitude spectrum augmentation
   - Occlusion-aware training (water line/bubble artifacts)
   - Validace na reálných videích (KRITICKÉ!)
   - Porovnání: s vs. bez domain adaptation

3. **Full Evaluation Phase (2 týdny)**
   - Cross-style generalizace: trénink freestyle, test na všech 4 stylech
   - Cross-domain robustness: syntetický model → reálný freestyle
   - Export finálních modelů do ONNX pro web deployment

### Model Selection — Duální Přístup (Doporučeno)

```
DOPORUČENÍ: Oba jako co-primární modely

→ ViTPose-L pro kvalitu analýzy (offline batch processing)
→ RTMPose-l pro real-time web app pipeline
Diplomka získá:
  1. SOTA accuracy comparison (ViTPose-L)
  2. Praktická deployment cesta (RTMPose-l)
  3. Architektonické srovnání (Transformer vs SimCC)
  4. Vliv velikosti modelu (L vs B, l vs m)
```

### Validační Protokol

```
Fáze 1: Syntetická validace (SwimXYZ test set)
  - Metrika: PCK@0.2
  - Cíl: >95% pro všechny 4 styly
  - Všech 6 modelů, stejný test set

Fáze 2: Reálná validace (pokud dostupná)
  - Metrika: porovnání s expertními anotacemi (trenér)
  - Tolerance: ±5° pro úhly kloubů
  - Klíčové: měřit synthetic→real degradaci

Fáze 3: Cross-domain robustnost
  - Test syntetického modelu na reálném freestyle
  - Měřit pokles accuracy
  - Aplikovat domain adaptation; přeměřit
  - Dokumentovat zlepšení (= přínos diplomky!)
```

---

## Část 10: Literatura & Zdroje

### Pose Estimation Modely
- **ViTPose**: Xu et al. (NeurIPS 2022) — [arXiv:2204.12484](https://arxiv.org/abs/2204.12484)
- **RTMPose**: Jiang et al. (2023) — [arXiv:2303.07399](https://arxiv.org/abs/2303.07399)

### Plavecky-specifická PE
- **Einfalt et al. (WACV 2018)**: Activity-conditioned PE pro plavání — [arXiv:1802.00634](https://arxiv.org/abs/1802.00634)
- **SwimmerNET (Giulietti et al., 2023)**: Underwater 2D swimmer PE — [MDPI Sensors](https://www.mdpi.com/1424-8220/23/4/2364)

### Datasety
- **SwimXYZ**: Fiche et al. (ACM SIGGRAPH MIG 2023) — [arXiv:2310.04360](https://arxiv.org/abs/2310.04360), [Zenodo](https://zenodo.org/records/8399376)

### Domain Adaptation
- **Synthetic-to-Real Gap**: Zhao et al. (CVPR 2025) — [OpenAccess](https://openaccess.thecvf.com/content/CVPR2025/papers/Zhao_Analyzing_the_Synthetic-to-Real_Domain_Gap_in_3D_Hand_Pose_Estimation_CVPR_2025_paper.pdf)
- **FAFA Underwater**: (2024) — [arXiv:2409.16600](https://arxiv.org/html/2409.16600)

### Frameworky
- **MMPose**: [GitHub](https://github.com/open-mmlab/mmpose), [Docs](https://mmpose.readthedocs.io/)
- **DeepLabCut**: [Docs](https://deeplabcut.github.io/DeepLabCut/docs/ModelZoo.html)
- **Linear LR Scaling**: Goyal et al. (2017) — "Accurate, Large Minibatch SGD"

---

## Závěr

**Pro diplomku se serverovými GPU a SwimXYZ daty:**

1. **Primární modely**: **ViTPose-L** (accuracy) + **RTMPose-l** (speed) — duální přístup
2. **Kompletní benchmark**: 4 modely (ViTPose-L/B, RTMPose-l/m)
3. **Key differentiator**: Komplexní swimming domain adaptation se synthetic→real bridge
4. **Timeline**: 6-8 týdnů pro full benchmark + trénink + evaluaci
5. **GPU výhoda**: Všechny experimenty paralelně; žádné kompromisy na velikosti modelu

Se serverovými GPU můžeš natrénovat všechny 4 modely, komplexně porovnat, a demonstrovat jak SOTA accuracy (ViTPose-L) tak praktickou deployment cestu (RTMPose-l).

---

**Dokument vytvořen**: únor 2026
**Aktualizace**: březen 2026 — GPU omezení odstraněna, větší modely přidány
**Status**: Syntéza peer-reviewed literature + MMPose best practices
