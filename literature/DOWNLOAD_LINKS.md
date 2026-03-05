# Chybějící literatura — download linky

_Vygenerováno: 2026-03-05_

Sandbox neumožňuje přímé stahování. Stáhni ručně a ulož do příslušných složek.

---

## DTW papery → `literature/dtw/`

| # | Paper | URL | Název souboru |
|---|-------|-----|---------------|
| 1 | **Sakoe & Chiba (1978)** — DTW originál | [PDF (UIUC)](http://jeffe.cs.illinois.edu/teaching/compgeom/refs/Sakoe-Chiba-DTW.pdf) | `Sakoe_Chiba_1978_DTW_original.pdf` |
| 2 | **Keogh (2004)** — Exact indexing of DTW, LB_Keogh | [PDF (UCR)](https://www.cs.ucr.edu/~eamonn/KAIS_2004_warping.pdf) | `Keogh_2004_exact_indexing_DTW.pdf` |
| 3 | **Keogh** — "Everything you know about DTW is wrong" | [PDF (UCR)](https://www.cs.ucr.edu/~eamonn/DTW_myths.pdf) | `Keogh_DTW_myths.pdf` |
| 4 | **Shokoohi-Yekta et al. (2017)** — DTW-D vs DTW-I, multivariate | [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC5668684/) nebo [Springer](https://link.springer.com/article/10.1007/s10618-016-0455-0) | `Shokoohi-Yekta_2017_DTW_multivariate.pdf` |
| 5 | **S-WFDTW (2025)** — Fitness scoring s BlazePose, improved DTW | [Nature Scientific Reports](https://www.nature.com/articles/s41598-025-02535-5) | `S-WFDTW_2025_fitness_scoring.pdf` |

## Pose estimation → `literature/pose_estimation/`

| # | Paper | URL | Název souboru |
|---|-------|-----|---------------|
| 6 | **MediaPipe — Lugaresi et al. (2019)** | [arXiv PDF](https://arxiv.org/pdf/1906.08172) | `MediaPipe_Lugaresi_2019.pdf` |

## General CV → `literature/general_cv/`

| # | Paper | URL | Název souboru |
|---|-------|-----|---------------|
| 7 | **MS COCO — Lin et al. (2014)** | [arXiv PDF](https://arxiv.org/pdf/1405.0312) | `COCO_Lin_2014.pdf` |

## Kniha → `literature/biomechanics/`

| # | Paper | Kde sehnat | Název souboru |
|---|-------|------------|---------------|
| 8 | **Maglischo (2003) — Swimming Fastest** | [Internet Archive](https://archive.org/details/swimmingfastest0000magl) (borrow) nebo [Open Library](https://openlibrary.org/books/OL3554622M/Swimming_fastest) | `Maglischo_2003_Swimming_Fastest.pdf` |

---

## Quick download (bash — spusť lokálně na svém PC)

```bash
# DTW
mkdir -p literature/dtw literature/general_cv

curl -L -o "literature/dtw/Sakoe_Chiba_1978_DTW_original.pdf" \
  "http://jeffe.cs.illinois.edu/teaching/compgeom/refs/Sakoe-Chiba-DTW.pdf"

curl -L -o "literature/dtw/Keogh_2004_exact_indexing_DTW.pdf" \
  "https://www.cs.ucr.edu/~eamonn/KAIS_2004_warping.pdf"

curl -L -o "literature/dtw/Keogh_DTW_myths.pdf" \
  "https://www.cs.ucr.edu/~eamonn/DTW_myths.pdf"

# Pose estimation
curl -L -o "literature/pose_estimation/MediaPipe_Lugaresi_2019.pdf" \
  "https://arxiv.org/pdf/1906.08172"

# General CV
curl -L -o "literature/general_cv/COCO_Lin_2014.pdf" \
  "https://arxiv.org/pdf/1405.0312"
```

Papery #4, #5 a #8 vyžadují buď institucionální přístup nebo registraci (PMC/Springer/Internet Archive).
