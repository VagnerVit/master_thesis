# CVAT Annotation Pipeline — Semi-automatická anotace pro fine-tuning ViTPose

**Autor:** Vit Vagner | **Datum:** 2026-03-05 | **Status:** Rozhodnutí a návrh pipeline
**Scope:** Anotace plaveckých videí keypointy pro fine-tuning ViTPose na freestyle side-view.
**Navazuje na:** `pozadavky_video_data.md` (zdroje videí), `SwimAth_v2_architektura (1).md` (ViTPose jako cílový PE model)

---

## 1. Rozhodnutí: Anotační nástroj

**Zvoleno: CVAT** (Computer Vision Annotation Tool, Intel, open-source)

### Důvody volby

| Kritérium | CVAT | DeepLabCut | Label Studio |
|---|---|---|---|
| **COCO Keypoints export** | Nativní podpora | Vlastní formát (nutná konverze) | Plugin, méně robustní |
| **Auto-anotace** | Vestavěný backend (model-agnostický) | Iterativní trénink od nuly | Omezená podpora |
| **Video mód** | Anotace N-tého framu + interpolace | Ano | Omezený |
| **Citovatelnost** | Ano (Sekachev et al., 2020) | Ano (Mathis et al., 2018) | Méně akademických citací |
| **Deploy** | `docker compose up` lokálně | Python package | Docker / cloud |
| **Keypoint podpora** | Plná (skeleton definice, occlusion flagy) | Primární use case | Obecnější, horší UX |

### Odmítnuté alternativy

- **DeepLabCut** — Silný nástroj pro markerless PE, ale orientovaný na iterativní trénink vlastního modelu od nuly. My chceme fine-tunovat existující ViTPose, ne trénovat nový model v DLC ekosystému. Zbytečná složitost.
- **Label Studio** — Obecnější anotační platforma. Keypoint anotace méně propracovaná než CVAT (chybí skeleton vizualizace, interpolace mezi framy horší). Pro 2D keypoints na videu je CVAT lepší volba.

---

## 2. Rozhodnutí: Self-training pipeline

Místo jednorázové ruční anotace použijeme **iterativní self-training loop**:

1. ViTPose (pretrained na COCO) automaticky předanotuje plavecká videa
2. Člověk opraví chyby v CVAT (fokus na problematické framy)
3. Fine-tuned model předanotuje další videa přesněji
4. Opakovat dokud kvalita nestačí

### Proč self-training

- **Efektivita** — ruční anotace 17 keypointů na frame trvá ~1-2 min. S předanotací stačí opravit chyby (~10-20 s/frame).
- **Metodologická čistota** — v diplomce jasně popsatelný a reprodukovatelný postup.
- **Škálovatelnost** — každá iterace snižuje množství ruční práce na dalších videích.

---

## 3. Pipeline workflow

```
┌─────────────────────────────────────────────────────────┐
│  Iterace 0                                              │
│                                                         │
│  ViTPose (COCO pretrained)                              │
│       │                                                 │
│       ▼                                                 │
│  Předanotace plaveckých videí                           │
│       │                                                 │
│       ▼                                                 │
│  CVAT: ruční korekce (okluze, podvodní, reflexe)        │
│       │                                                 │
│       ▼                                                 │
│  Export COCO Keypoints JSON                             │
│       │                                                 │
│       ▼                                                 │
│  Fine-tuning ViTPose na opravených datech               │
│       │                                                 │
│       ▼                                                 │
│  Vyhodnocení (AP na held-out setu)                      │
└───────┬─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  Iterace 1+                                             │
│                                                         │
│  Fine-tuned ViTPose předanotuje nová videa přesněji     │
│       │                                                 │
│       ▼                                                 │
│  CVAT: méně korekcí potřeba                             │
│       │                                                 │
│       ▼                                                 │
│  Export + fine-tuning na rozšířeném datasetu             │
└─────────────────────────────────────────────────────────┘
```

### Kroky detailně

1. **Předanotace** — ViTPose-B (pretrained COCO, 17 keypointů) zpracuje videa. Výstup: COCO JSON s predikovanými keypointy a confidence scores.
2. **Import do CVAT** — Video + předanotace se nahrají do CVAT projektu. Skeleton definovaný podle COCO 17-keypoint topologie.
3. **Ruční korekce** — Anotátor (autor) opravuje framy s nízkou confidence nebo viditelnými chybami. CVAT video mód: anotuj každý N-tý frame (např. každý 5.), zbytek interpoluje. Fokus na problematické situace:
   - Okluze (ruka pod vodou)
   - Reflexe vodní hladiny
   - Podvodní záběry (refrakce)
   - Boční rotace trupu (záměna L/R)
4. **Export** — COCO Keypoints formát (JSON). Kompatibilní s MMPose/ViTPose training pipeline.
5. **Fine-tuning** — ViTPose fine-tuning na opraveném datasetu (SwimXYZ + reálná anotovaná data).
6. **Evaluace** — AP (Average Precision) na held-out setu reálných plaveckých framů.

---

## 4. Zdroje videí pro anotaci

| Zdroj | Právní status | Poznámky |
|---|---|---|
| **Vlastní videa autora** | Bezproblémové | Nejbezpečnější právně. Autor aktivně plave — reálná data. |
| **YouTube — edukační kanály** | Fair use / souhlas nutný | Race Club, Skills NT, Swim Smooth, World Aquatics. Pro akademický výzkum argumentovatelné fair use, ale ideálně kontaktovat autory. |
| **SwimXYZ syntetická videa** | Veřejný dataset (Zenodo) | Už máme. Perfektní anotace, ale syntetická — domain gap. |

### Právní poznámka

- **Videa z YouTube**: Pro trénink modelu v rámci diplomky (nekomerční výzkum) je argumentovatelné fair use. Bezpečnější je kontaktovat autory kanálů.
- **Extrahované keypointy nejsou chráněné autorským právem** — jsou to odvozená numerická data (pozice kloubů), ne kopie díla. Model natrénovaný na keypointech lze distribuovat bez omezení.
- **Vlastní videa** jsou právně nejčistší volba a měla by tvořit jádro validačního setu.

---

## 5. Technické poznámky

### CVAT deploy

```bash
# Lokální instalace
git clone https://github.com/cvat-ai/cvat
cd cvat
docker compose up -d
# UI na http://localhost:8080
```

### Auto-annotation backend

CVAT podporuje napojení vlastních modelů přes Nuclio serverless framework nebo CVAT SDK. ViTPose lze napojit jako auto-annotation backend:

1. Zabalit ViTPose inference do Nuclio funkce
2. Registrovat v CVAT jako auto-annotation model
3. Spustit předanotaci přímo z CVAT UI

Alternativně: předanotaci spustit offline (Python skript) a importovat výsledky do CVAT jako COCO JSON.

### Video mód — strategie anotace

- **Keyframe interval**: Každý 5. frame (při 30 FPS = 6 anotací/s videa)
- **Interpolace**: CVAT lineárně interpoluje keypointy mezi keyframy
- **Occlusion flagy**: CVAT podporuje `visibility` flag per keypoint (visible / occluded / out-of-frame) — mapuje se na COCO `v` flag (0/1/2)

### Výstupní formát (COCO Keypoints)

```json
{
  "annotations": [{
    "id": 1,
    "image_id": 100,
    "category_id": 1,
    "keypoints": [x1, y1, v1, x2, y2, v2, ...],
    "num_keypoints": 17,
    "bbox": [x, y, w, h]
  }],
  "categories": [{
    "id": 1,
    "name": "swimmer",
    "keypoints": ["nose", "left_eye", "right_eye", ...],
    "skeleton": [[0,1], [0,2], ...]
  }]
}
```

---

## 6. Očekávaný rozsah anotací

| Fáze | Počet framů | Zdroj | Účel |
|---|---|---|---|
| Iterace 0 | ~200-500 ručně opravených | Vlastní videa + YouTube | Prvotní fine-tuning |
| Iterace 1+ | ~500-1000 dalších | Nová videa s lepší předanotací | Rozšíření datasetu |
| Validační set | ~100-200 | Vlastní videa (held-out) | Evaluace AP |

Celkový cíl: **~1000-2000 anotovaných framů** reálných plaveckých dat pro fine-tuning. V kombinaci se SwimXYZ syntetickými daty (3.4M framů) by to mělo stačit pro doménovou adaptaci.

---

## 7. Citace

- **CVAT**: Sekachev, B. et al. (2020). *OpenCV/CVAT: Computer Vision Annotation Tool*. GitHub. https://github.com/cvat-ai/cvat
- **ViTPose**: Xu, Y. et al. (2022). *ViTPose: Simple Vision Transformer Baselines for Human Pose Estimation*. NeurIPS 2022. arXiv:2204.12484
- **COCO**: Lin, T.-Y. et al. (2014). *Microsoft COCO: Common Objects in Context*. ECCV 2014. arXiv:1405.0312

---

_Last Updated: 2026-03-05_
