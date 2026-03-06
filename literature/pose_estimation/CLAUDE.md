# pose_estimation — Modely pro odhad pózy

5 paperů (+MediaPipe ze swimxyz_refs/). Jádro ML pipeline SwimAth — kandidáti na fine-tuning a benchmark.
Viz také swimxyz_refs/ pro další swimming-specific PE papery (Einfalt doplňky: Zecha 2012, Zecha 2017, Ascenso 2021 PhD, Ceseracciu 2011, Greif 2009).

---

### ViTPose_Xu_2022_NeurIPS.pdf
- **Autoři**: Xu Y. et al., 2022, NeurIPS
- **Co to je**: ViTPose — Vision Transformer pro PE, škálovatelný 20M–1B params, SOTA 80.9 AP na COCO
- **Přínos pro SwimAth**: **Kandidát #1 na fine-tuning.** Tvůj hlavní PE model. SwimXYZ paper ukazuje, že fine-tuned ViTPose zlepšuje PCK z 67→85 (PCK10). Backbone = ViT (viz swimxyz_refs/).
- **Kapitola**: 2 (Rešerše — PE), 3 (Návrh), 4 (Implementace), 5 (Benchmark B1–B2)

### RTMPose_Jiang_2023.pdf
- **Autoři**: Jiang T. et al., 2023, arXiv
- **Co to je**: RTMPose — 75.8% AP COCO, 90+ FPS CPU, 430+ FPS GPU, real-time
- **Přínos pro SwimAth**: **Kandidát #2 na fine-tuning.** Real-time alternativa k ViTPose. Porovnáváš oba v benchmarku. Výhoda: nižší latence pro webovou aplikaci.
- **Kapitola**: 2, 3, 5 (Benchmark)

### Einfalt_WACV_2018_swimming_pose.pdf
- **Autoři**: Einfalt M., Zecha D., Lienhart R., 2018, WACV
- **Co to je**: Activity-conditioned continuous PE pro plavání — Augsburg skupina
- **Přínos pro SwimAth**: **Jediný swimming-specific PE paper.** Řeší temporální vyhlazení (+16% zlepšení), refrakci, vodní prostředí. Autoři = tvůrci Augsburg datasetu. Klíčová reference pro domain-specific PE výzvy.
- **Kapitola**: 2 (Rešerše — PE v plavání), 3 (Návrh — ragdoll constraints)

### SwimmerNET_Giulietti_2023.pdf
- **Autoři**: Giulietti N. et al., 2023, MDPI Sensors
- **Co to je**: SwimmerNET — CNN pro underwater 2D PE plavců, wide-angle kamera, chyba ~1–10 mm
- **Přínos pro SwimAth**: Relevantní pro underwater view. Ukazuje specifické výzvy podvodního PE (refrakce, bubliny, deformace). Dataset na žádost (2,021 snímků kraulu).
- **Kapitola**: 2 (Rešerše — podvodní PE)

### DeepLabCut_Mathis_2018_PMC.pdf
- **Autoři**: Mathis A. et al., 2018, Nature Neuroscience
- **Co to je**: DeepLabCut — markerless PE z ~200 anotovaných snímků, transfer learning
- **Přínos pro SwimAth**: Alternativní přístup (few-shot PE). Cituj jako metodu, kterou jsi zvažoval. Výhoda: málo anotací potřeba. Nevýhoda: single-animal/person, ne tak škálovatelný jako ViTPose.
- **Kapitola**: 2 (Rešerše — PE architektury)

---

## Viz také
- `swimxyz_refs/MediaPipe_Lugaresi_2019.pdf` — framework používaný v prototypu
- `swimxyz_refs/Dosovitskiy_2020_ViT.pdf` — ViT backbone pro ViTPose
- `swimxyz_refs/Cao_2017_OpenPose.pdf` — baseline PE metoda
