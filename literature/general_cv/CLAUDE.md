# general_cv — Obecné computer vision reference

1 paper. Základní benchmark dataset pro pose estimation.

---

### COCO_Lin_2014.pdf
- **Autoři**: Lin T.Y. et al., 2014, ECCV (Microsoft COCO)
- **Co to je**: MS COCO dataset — standardní benchmark pro detekci objektů, segmentaci a pose estimation (330k obrázků, 200k anotovaných, 17 keypointů pro osoby)
- **Přínos pro SwimAth**: Referenční benchmark pro všechny PE modely (ViTPose, RTMPose, OpenPose). Metriky AP (Average Precision) na COCO jsou standard pro porovnání PE modelů v kapitole 2 a benchmarku B1. SwimXYZ používá COCO keypoint formát pro anotace.
- **Kapitola**: 2 (Rešerše — PE metriky a benchmarky), 5 (Benchmark B1)
