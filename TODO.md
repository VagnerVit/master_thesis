# SwimAth — Diplomová práce TODO

**Last Updated**: 2026-02-21 (datasety aktualizovány)
**Deadline**: ~únor 2027
**Kritická cesta**: A3 → B1 → B2 → C1 → C2 → C3 → D2 → E1

---

## Hotové

### Prototyp (Phase 0-2)

- [x] SwimXYZ dataset stažen (annotations 6.7 GB + freestyle videa 75 GB)
- [x] Dataset loader: sliding window, ~137k train samples
- [x] Style classifier: BiLSTM + Attention, 99.67% accuracy (4 styly)
- [x] ONNX export (`models/style_classifier.onnx`)
- [x] Reference templates: `models/freestyle_template.json`
- [x] Stroke analyzer: DTW comparison, detekce cyklů
- [x] Feedback generator: český text
- [x] PySide6 GUI s video přehrávačem + skeleton overlay
- [x] Export: JSON + PDF reporty
- [x] End-to-end test: video → pose → classifier → feedback → export

### Rešerše (únor 2026)

- [x] DTW rešerše — DTW-D zůstává, Sakoe-Chiba band, DBA pro šablony
- [x] Klasifikace stylu rešerše — BiLSTM + Attention zvolena, experimentální plán navržen
- [x] Rozhodnutí: web aplikace (ne desktop), bez LLM/RAG

---

## A. Rešerše a příprava (4-6 týdnů)

- [ ] **A1. Literární rešerše — biomechanika plavání**
  - Maglischo, Craig & Pendergast, Psycharakis, Chollet, Virag, Barbosa
  - Sepsat do `paper/chapters/02_research.tex`
- [ ] **A2. Literární rešerše — pose estimation a ML**
  - ViTPose, RTMPose, Einfalt, SwimmerNET, DeepLabCut
  - Sepsat do `paper/chapters/02_research.tex`
- [ ] **A3. Získání datasetů** → viz `claude_doc/datasety_kontakty.md`
  - [x] SwimXYZ — staženo (syntetický, 11520 videí)
  - [x] ~~Augsburg Swimming Channel — ZAMÍTNUTO (NDA, data nejsou jejich)~~
  - [ ] SwimmerNET — žádost odeslána, bez odpovědi (pravděpodobně ne)
  - [ ] Oslovit české instituce (VUT CESA Šťastný, FTVS UK, BALUO UPOL)
  - [ ] Oslovit EU zdroje (SWIM-360 Malta, SwimTrack MediaEval, PLOS One HSD)
  - [ ] Oslovit World Aquatics / OTAB pro competition footage
  - [ ] Natočit vlastní reálná data (triatlonový trénink)
- [ ] **A4. Definice metrik a prahů pro 3 úrovně**
  - Začátečník / mírně pokročilý / expert
  - Frekvence záběru, rotace těla, úhel loktu, tolerance odchylek

---

## B. Experimenty s Pose Estimation (4-6 týdnů)

- [ ] **B1. Benchmark: MediaPipe vs RTMPose vs ViTPose na plaveckých datech**
  - Metriky: PCK, AP, inference time
  - SwimXYZ test split
- [ ] **B2. Fine-tuning na SwimXYZ**
  - Side-view freestyle jako první
  - ViTPose nebo RTMPose (podle B1)
- [ ] **B3. Testování na různých pohledech kamery**
  - Side / front / underwater

---

## C. Biomechanická analýza (4-5 týdnů)

- [ ] **C1. Pipeline: keypoints → biomechanické metriky**
  - Úhly kloubů, rotace trupu, symetrie záběru
  - Ragdoll constraints (filtrace nerealistických póz)
- [ ] **C2. Referenční vzory**
  - Min 1 styl × 1 pohled × 3 úrovně
  - DBA (DTW Barycenter Averaging) pro konstrukci šablon
- [ ] **C3. Porovnávací metoda**
  - DTW-D + pravidlový systém + skóre 0-100
  - Benchmark: DTW-D vs Euclidean vs LCSS

---

## D. Webová aplikace (4-6 týdnů)

- [ ] **D1. Backend FastAPI**
  - Upload, PostgreSQL, async processing
  - Celery + Redis pro video processing
  - WebSocket progress
- [ ] **D2. Integrace ML pipeline**
  - PE inference (ONNX)
  - Biomechanická analýza
  - Feedback generátor
- [ ] **D3. Frontend Vue.js**
  - Upload, progress bar, výsledky
  - Video overlay s pózy
  - Historie analýz

---

## E. Vyhodnocení a diplomka (4-6 týdnů)

- [ ] **E1. Testování na reálných videích**
  - Různé úrovně plavců
  - Porovnání s hodnocením trenéra
  - Cross-domain: trénink na SwimXYZ, test na reálných datech
- [ ] **E2. Sepsání textu**
  - Kapitoly 01-06 v `paper/chapters/`
  - Experimenty: BiLSTM vs TCN, ablace, vliv délky sekvence
- [ ] **E3. Příprava na obhajobu**
  - Prezentace, demo

---

## Backlog / Tech debt

- [ ] Stáhnout Butterfly videa (optional, 2 parts na Zenodo)
- [ ] Ragdoll constraints post-processing vrstva
- [ ] Butterworth filtr před DTW (šum)
- [ ] Augmentace šumem při tréninku (domain gap syntetická → reálná data)
- [ ] CI/CD pipeline (GitHub Actions)

---

## Poznámky

- **GPU**: RTX 3060 + školní výkon pro fine-tuning
- **Primární styl**: kraul (freestyle), nejvíc dat i využití
- **Reálná videa**: autor si pořídí sám (aktivní triatlonista)
- **Paralelně**: rešerše (A1, A2) + čekání na datasety (A3) + backend (D1) + frontend (D3)
