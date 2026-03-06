# Reference vytěžené ze SwimXYZ paperu (Fiche et al., 2023)

_70 referencí celkem, níže 23 relevantních pro SwimAth._
_Aktualizováno: 2026-03-05_

---

## Plavecky-specifické PE a analýza

| # | Ref | Autoři & rok | Název | Složka | Status |
|---|-----|-------------|-------|--------|--------|
| 1 | [38] | Ascenso G., 2021 | *Development of a non-invasive motion capture system for swimming biomechanics* | swimxyz_refs/ | ✅ |
| 2 | [41] | Zecha D., Eggert C., Lienhart R., 2017 | *Pose estimation for deriving kinematic parameters of competitive swimmers* | swimxyz_refs/ | ✅ |
| 3 | [42] | Zecha D., Greif T., Lienhart R., 2012 | *Swimmer detection and PE for continuous stroke-rate determination* | swimxyz_refs/ | ✅ |
| 4 | [44] | Kirmizibayrak C. et al., 2011 | *Digital analysis and visualization of swimming motion* | swimxyz_refs/ | ✅ |
| 5 | [45] | Ceseracciu E. et al., 2011 | *Markerless analysis of front crawl swimming* | swimxyz_refs/ | ✅ |
| 6 | [61] | Greif T. & Lienhart R., 2009 | *An annotated data set for pose estimation of swimmers* | swimxyz_refs/ | ✅ |
| 7 | [62] | Woinoski T., 2020 | *Towards automated swimming analytics using deep neural networks* | swimxyz_refs/ | ✅ |
| 8 | [68] | Delhaye E. et al., 2022 | *Automatic swimming activity recognition and lap time assessment based on a single IMU* | swimxyz_refs/ | ✅ |
| 9 | [8] | Wang J. et al., 2019 | *AI Coach: Deep human PE and analysis for personalized athletic training* | swimxyz_refs/ | ✅ |

## 3D Pose & Shape Estimation

| # | Ref | Autoři & rok | Název | Složka | Status |
|---|-----|-------------|-------|--------|--------|
| 10 | [21] | Loper M. et al., 2015 | *SMPL: A skinned multi-person linear model* | swimxyz_refs/ | ✅ |
| 11 | [32] | Cao Z. et al., 2017 | *Realtime multi-person 2D PE using part affinity fields* | swimxyz_refs/ | ✅ |
| 12 | [33] | Bogo F. et al., 2016 | *Keep it SMPL: Automatic estimation of 3D human pose and shape* | swimxyz_refs/ | ✅ |
| 13 | [70] | Dosovitskiy A. et al., 2020 | *An image is worth 16×16 words: Transformers for image recognition at scale* | swimxyz_refs/ | ✅ |

## Sportovní datasety

| # | Ref | Autoři & rok | Název | Složka | Status |
|---|-----|-------------|-------|--------|--------|
| 14 | [43] | Safdarnejad S.M. et al., 2015 | *Sports videos in the wild (SVW)* | — | ❌ Nestaženo (nízká priorita) |
| 15 | [53] | Johnson S. & Everingham M., 2010 | *LSP: Clustered pose and nonlinear appearance models for HPE* | — | ❌ Nestaženo (nízká priorita) |
| 16 | [54] | Nibali A. et al., 2021 | *ASPset: An outdoor sports pose video dataset with 3D keypoint annotations* | — | ❌ Nestaženo (nízká priorita) |
| 17 | [56] | Tang Y. et al., 2023 | *Flag3D: A 3D fitness activity dataset with language instruction* | swimxyz_refs/ | ✅ |
| 18 | [57] | Fieraru M. et al., 2021 | *AIFit: Automatic 3D human-interpretable feedback models for fitness training* | swimxyz_refs/ | ✅ |

## Syntetická data pro PE

| # | Ref | Autoři & rok | Název | Složka | Status |
|---|-----|-------------|-------|--------|--------|
| 19 | [19] | Black M.J. et al., 2023 | *BEDLAM* | swimxyz_refs/ | ✅ |
| 20 | [20] | Varol G. et al., 2017 | *Learning from synthetic humans* | swimxyz_refs/ | ✅ |
| 21 | [52] | Mahmood N. et al., 2019 | *AMASS: Archive of motion capture as surface shapes* | swimxyz_refs/ | ✅ |

## Generativní modely pohybu

| # | Ref | Autoři & rok | Název | Složka | Status |
|---|-----|-------------|-------|--------|--------|
| 22 | [22] | Li P. et al., 2022 | *GANimator: Neural motion synthesis from a single sequence* | swimxyz_refs/ | ✅ |
| 23 | [2] | Starke S. et al., 2022 | *DeepPhase: Periodic autoencoders for learning motion phase manifolds* | swimxyz_refs/ | ✅ |

---

## Souhrn: 20/23 staženo

- ✅ Staženo: 20 paperů (vše v swimxyz_refs/)
- ❌ Nestaženo: 3 (SVW, LSP, ASPset — nízká priorita, obecné sportovní datasety)

---

## Vzdělávací zdroje (kurzy)

### ÚFAL NPFL138 — Deep Learning (MFF UK)
- **URL**: https://ufal.mff.cuni.cz/courses/npfl138/2526-summer
- **Garant**: Milan Straka
- **Formát**: 8 ECTS, přednášky + cvičení, Python + PyTorch
- **GitHub**: https://github.com/ufal/npfl138
- **Relevantní témata**: CNNs, Vision Transformers, attention mechanismy, generativní modely
- **Využití**: Teoretický základ pro PE architektury (ViT, attention), training pipeline

### FIT ČVUT NIE-PDL — Practical Deep Learning
- **URL**: https://courses.fit.cvut.cz/NIE-PDL/index.html
- **Formát**: Magisterský předmět, PyTorch
- **Relevantní témata**: Praktický DL, computer vision, trénink modelů
- **Využití**: Praktické aspekty fine-tuningu, deployment

---

## Open-source projekty

### Swimming-Stroke-Rate-Analysis
- **URL**: https://github.com/agvdndor/Swimming-Stroke-Rate-Analysis
- **Co to je**: Analýza stroke rate plavců z videa pomocí human pose estimation
- **Využití**: Referenční implementace pro porovnání přístupů, inspirace pro stroke rate detekci v SwimAth pipeline
