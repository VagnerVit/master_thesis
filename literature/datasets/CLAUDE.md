# datasets — Datasety pro plaveckou analýzu

2 papery. Hlavní dataset projektu + nový multimodální projekt SWIM-360.

---

### SwimXYZ_Fiche_2023_SIGGRAPH_MIG.pdf
- **Autoři**: Fiche G. et al., 2023, ACM SIGGRAPH MIG
- **Co to je**: SwimXYZ — syntetický dataset 11,520 videí, 3.4M snímků, 4 styly, SMPL + COCO anotace
- **Přínos pro SwimAth**: **Tvůj primární dataset.** Trénovací data pro style classifier (99.67% accuracy), fine-tuning ViTPose (PCK10: 67→85), referenční šablony pro DTW. Detailně popsat v kapitole 3–4.
- **Kapitola**: 2 (Rešerše — datasety), 3 (Návrh), 4 (Implementace), 5 (Experimenty)

#### Klíčové parametry SwimXYZ:
- 11,520 videí × 300 framů = 3.4M snímků
- 4 styly: freestyle, backstroke, breaststroke, butterfly
- 5 camera views: front, aerial, side underwater, side above water, side water level
- 3 annotation formáty: COCO17, COCO25, Base (48 joints)
- 240 SMPL motion sekvencí
- Generováno: Unity + GANimator + SMPL
- Zenodo: https://zenodo.org/records/8399376

#### Známé limitace (z paperu):
- Malá diverzita subjektů (gender, body shape, plavky)
- Omezená variabilita prostředí (bazén, okolí)
- Chybí segmentace, depth maps
- Chybí starty a obrátky

### SWIM360_Camilleri_2025_multimodal_swimming.pdf
- **Autoři**: Camilleri V. et al., 2025, MDPI Sensors
- **Co to je**: SWIM-360 — probíhající projekt Uni Malta kombinující video PE, IMU (EO SwimBETTER), a NIRS (TrainRed) pro multimodální analýzu plavání. Paper popisuje early findings a proof-of-concept.
- **Přínos pro SwimAth**: Nejbližší probíhající projekt k tvé práci — multimodální analýza plavecké techniky s důrazem na explainability (XAI). Plánují zveřejnit reálný plavecký dataset (nad + pod vodou). Cituj jako concurrent work v rešerši. Klíčový rozdíl: oni kombinují video + IMU + NIRS, ty se soustředíš čistě na video.
- **Kapitola**: 2 (Rešerše — datasety, related work)
- **Web**: https://swim-360.eu/

---

## Viz také
- `swimxyz_refs/` — 21 referencí vytěžených ze SwimXYZ paperu
- CLAUDE.md v hlavním projektu, sekce "Datasety" — přehled všech datasetů (SwimXYZ, Augsburg, SwimmerNET, CADDY)
