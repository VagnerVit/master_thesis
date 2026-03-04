# CLAUDE.md — SwimAth: Diplomová práce

**Projekt**: SwimAth — Analýza plavecké techniky z videa s využitím pose estimation a ML
**Autor**: Vít Vagner (vit.vagner@memos.cz)
**Typ**: Diplomová práce (master thesis)
**Jazyk kódu**: Python 3.11+
**GitHub**: https://github.com/VagnerVit/SwimAth.git

---

## Mise projektu

Uživatel nahraje video svého plavání → pose estimation extrahuje klíčové body těla → aplikace vypočítá biomechanické metriky (úhly kloubů, rotace trupu, symetrie záběru) → ML pipeline (pravidlový systém + natrénované modely) vygeneruje personalizovanou zpětnou vazbu a doporučení cviků → druhá součást aplikace generuje personalizované tréninkové plány na základě zjištěných slabých stránek a úrovně plavce.

**Proč to existuje**: Na trhu je velmi málo dostupných nástrojů pro analýzu plavecké techniky z videa a ty které existují jsou drahé. Autor aktivně závodí v triatlonu — reálná data pro testování.

**Výzkumná mezera**: Neexistuje veřejně dostupný end-to-end systém pro automatickou analýzu plavecké techniky z videa, který by kombinoval moderní pose estimation (ViTPose/RTMPose) fine-tuned na plaveckých datech s biomechanickou analýzou a personalizovaným feedbackem podle úrovně plavce. Existující práce řeší dílčí problémy (detekce pózy, klasifikace stylu), ale chybí ucelený pipeline video → metriky → detekce chyb → zpětná vazba.

---

## Komunikace

- **Veškerá komunikace s uživatelem ČESKY**
- Komentáře v kódu anglicky
- Commit messages anglicky
- User-facing stringy v aplikaci česky
- Uživatel je senior developer — přímý, action-oriented, preferuje hloubku ("chci jít do hloubky")
- Styl: konkrétní akce > dlouhé vysvětlování
- **Rešerše**: nejprve hledej v `@literature/` (stažené PDF), teprve pak na webu

---

## Struktura repozitáře

```
master_thesis/
├── CLAUDE.md              ← tento soubor
├── claude_doc/            ← dokumenty z předchozích chatů (rešerše, plány, architektura)
│   ├── AI_analyza_plavani_datasety_literatura.md   ← kompletní rešerše datasetů a literatury
│   ├── SwimAth_plan_diplomky.md                    ← plán diplomky s TODO balíky A-E
│   ├── SwimAth_v2_architektura (1).md              ← architektura webové aplikace (v2)
│   └── moje poznamky.txt                           ← autorovy poznámky a nápady
├── literature/            ← stažená literatura (15/16 PDF)
│   ├── biomechanics/      ← 5 PDF (Barbosa, Barden, Chollet, Craig, Psycharakis)
│   ├── pose_estimation/   ← 5 PDF (ViTPose, RTMPose, Einfalt, SwimmerNET, DeepLabCut)
│   ├── rag_llm_sport/     ← 4 PDF (RAG Lewis, Comendant, Talking Tennis, BoxingPro)
│   └── datasets/          ← 1 PDF (SwimXYZ Fiche 2023)
├── paper/                 ← text diplomky (LaTeX, XeLaTeX + natbib)
│   ├── main.tex           ← hlavní soubor
│   ├── references.bib     ← bibliografie (15 záznamů)
│   ├── chapters/          ← kapitoly (01-06 + appendix)
│   ├── figures/           ← obrázky a diagramy
│   └── tables/            ← tabulky
└── prototyp/              ← funkční prototyp (desktop app, PySide6)
    ├── src/               ← zdrojový kód aplikace
    ├── training/          ← ML trénovací pipeline
    ├── models/            ← natrénované modely
    ├── data/swimxyz/      ← dataset (gitignored)
    ├── scripts/           ← download/prepare/verify skripty
    └── tests/             ← unit testy
```

---

## Dvě verze architektury

### v1 — Prototyp (HOTOVÝ, v `prototyp/`)

- **Desktop app**: PySide6 (Qt6) na Windows
- **Pose estimation**: MediaPipe Pose
- **ML**: PyTorch LSTM style classifier (99.67% accuracy na 4 styly)
- **Analýza**: DTW porovnání s referenčními šablonami
- **Feedback**: Pravidlový systém v češtině
- **Export**: JSON + PDF reporty
- **Fáze 0-2 kompletní**, Phase 3 (underwater correction, Strava) plánovaná

### v2 — Cílová architektura pro diplomku (v `claude_doc/SwimAth_v2_architektura`)

- **Web app**: Vue.js 3 + FastAPI + PostgreSQL + Redis + Celery
- **Pose estimation**: ViTPose/RTMPose (fine-tuned na SwimXYZ)
- **Analýza**: DTW + pravidlový systém (bez LLM/RAG — viz Rozhodnuté otázky)
- **2 úrovně plavců**: Dítě (8–14) / Pokročilý (15+). Profesionál jako budoucí rozšíření.
- **3 pohledy kamery**: side / front / underwater
- **4 styly**: kraul / znak / prsa / motýlek

---

## Prototyp — technický stav

### Hotové (Phase 0-2)

- Video processing + MediaPipe skeleton overlay (≥20 FPS)
- PySide6 GUI s QSplitter layoutem
- SwimXYZ dataset: 8,640 sekvencí, 2.6M framů (annotations 6.7 GB + freestyle videa 75 GB)
- Dataset loader: sliding window (seq_len=32, stride=16), ~137k train samples
- Style classifier: LSTM + Attention, bidirectional, 256 hidden, 2 layers → **99.67% test accuracy**
  - Freestyle: 99.79%, Backstroke: 100%, Breaststroke: 99.75%, Butterfly: 99.15%
  - Export: `models/style_classifier.onnx`
- Reference templates: `models/freestyle_template.json` (18k samples, 11 kloubů)
- Stroke analyzer: DTW comparison, detekce cyklů
- Feedback generator: český text ("Levý loket o 13° níže při záběru než reference")
- Export: JSON + PDF (reportlab)

### Klíčové soubory prototypu

```
src/
├── core/
│   ├── video_processor.py      # OpenCV VideoCapture, frame extraction
│   ├── pose_estimator.py       # MediaPipe wrapper
│   └── frame_buffer.py         # Queue-based frame buffer (max 30)
├── analysis/
│   ├── dtw.py                  # Dynamic Time Warping
│   ├── stroke_analyzer.py      # StrokeAnalyzer (detekce cyklů, analýza)
│   ├── feedback_generator.py   # FeedbackGenerator (CZ text)
│   ├── keypoint_mapper.py      # Mapování keypoints
│   └── mediapipe_angles.py     # Výpočet úhlů z MediaPipe
├── ui/
│   ├── main_window.py          # Hlavní okno (QSplitter)
│   ├── video_player.py         # Video přehrávač s overlay
│   ├── feedback_widget.py      # Widget pro zobrazení analýzy
│   ├── analysis_worker.py      # QThread pro background processing
│   ├── full_video_worker.py    # Worker pro celé video
│   └── cycles_timeline.py      # Vizualizace cyklů
├── export/
│   ├── json_exporter.py
│   └── pdf_exporter.py
└── models/
    └── mediapipe_config.py

training/
├── swimxyz_parser.py           # CSV parser pro SwimXYZ formát
├── dataset_loader.py           # PyTorch Dataset (SwimXYZDataset)
├── angle_utils.py              # Výpočet úhlů kloubů (48 keypointů)
├── template_generator.py       # Generování referenčních šablon
├── train_classifier.py         # Training script (CUDA, AMP, early stopping)
└── models/
    └── style_classifier.py     # LSTM + Attention (4 třídy)
```

### Threading model prototypu

```
Main Thread: PySide6 event loop (UI only)
    ↓
Video Decoder Thread: OpenCV frame extraction
    ↓ FrameBuffer (queue.Queue, max 30)
Pose Estimator Thread: MediaPipe inference
    ↓ Results Queue
UI Renderer: Display updates
```

### Klíčové ML parametry

```python
StyleClassifierConfig(
    num_keypoints=48,          # SwimXYZ base formát
    keypoint_dims=3,           # x, y, z
    sequence_length=32,        # sliding window
    hidden_size=256,
    num_lstm_layers=2,
    num_classes=4,             # freestyle, backstroke, breaststroke, butterfly
    dropout=0.3,
    bidirectional=True,
    use_attention=True,
)
# Training: AdamW lr=1e-3, CosineAnnealing, early stopping patience=10
```

### Joint definitions (angle_utils.py)

| Joint          | Keypoint Indices (SwimXYZ base 48kp)      |
| -------------- | ----------------------------------------- |
| left_elbow     | L_UpperArm(20), L_Forearm(11), L_Hand(12) |
| right_elbow    | R_UpperArm(39), R_Forearm(30), R_Hand(31) |
| left_shoulder  | Neck(21), L_Clavicle(4), L_UpperArm(20)   |
| body_alignment | Head(1), Spine2(41), Pelvis(0)            |

---

## Plán diplomové práce

### Struktura textu

1. Úvod — motivace, cíl, přínos
2. Rešerše — biomechanika plavání, pose estimation architektury, datasety, ML ve sportu, podvodní výzvy
3. Návrh řešení — architektura, referenční model, výběr modelu, metriky, porovnávací metoda
4. Implementace — předzpracování videa, ML pipeline, webová aplikace, referenční databáze
5. Experimenty a vyhodnocení — přesnost PE, kvalita detekce chyb, testování na reálných videích
6. Závěr

### Pracovní balíky (TODO)

```
A. REŠERŠE A PŘÍPRAVA (4-6 týdnů)
   A1. Literární rešerše — biomechanika plavání
   A2. Literární rešerše — pose estimation a ML
   A3. Získání datasetů (SwimXYZ ✅, Augsburg — žádost odeslána, SwimmerNET — žádost odeslána)
   A4. Definice metrik a prahů pro 2 úrovně (Dítě + Pokročilý)

B. EXPERIMENTY S POSE ESTIMATION (4-6 týdnů)
   B1. Benchmark: MediaPipe, RTMPose, ViTPose na plaveckých datech
   B2. Fine-tuning na SwimXYZ (side-view freestyle jako první)
   B3. Testování na různých pohledech kamery

C. BIOMECHANICKÁ ANALÝZA (4-5 týdnů)
   C1. Pipeline: keypoints → biomechanické metriky
   C2. Vytvoření referenčních vzorů (min 1 styl × 1 pohled × 2 úrovně)
   C3. Implementace porovnávací metody (DTW + pravidlový systém + skóre 0-100)

D. WEBOVÁ APLIKACE (4-6 týdnů)
   D1. Backend FastAPI (upload, DB, async processing, WebSocket progress)
   D2. Integrace ML pipeline
   D3. Frontend Vue.js (upload, progress, výsledky, video overlay, historie)

E. VYHODNOCENÍ A DIPLOMKA (4-6 týdnů)
   E1. Testování na reálných videích (různé úrovně, porovnání s trenérem)
   E2. Sepsání textu
   E3. Příprava na obhajobu
```

**Kritická cesta**: A3 → B1 → B2 → C1 → C2 → C3 → D2 → E1

**Paralelně**: Rešerše (A1,A2) + stahování dat (A3); Backend (D1) + Frontend (D3) + ML experimenty (B); Text průběžně

### Minimální životaschopný rozsah

1. Kompletní rešerše
2. Benchmark PE modelů na plaveckých datech
3. Fine-tuning na SwimXYZ (freestyle side-view)
4. Pipeline keypoints → biomechanické metriky
5. Referenční systém pro 1 styl × 1 pohled × 2 úrovně
6. Fungující porovnání s detekcí chyb
7. Základní webové rozhraní (upload → výsledky)
8. Vyhodnocení na reálných videích

---

## Datasety

| Dataset                   | Typ             | Velikost                           | Přístup          | Status                                         |
| ------------------------- | --------------- | ---------------------------------- | ---------------- | ---------------------------------------------- |
| **SwimXYZ**               | Syntetický      | 11,520 videí, 3.4M snímků, 4 styly | Veřejný (Zenodo) | ✅ Annotations staženy, freestyle videa stažena |
| Augsburg Swimming Channel | Reálný          | Více sessions, 4 styly             | Na žádost        | ✉️ Žádost odeslána                             |
| SwimmerNET                | Reálný podvodní | 2,021 snímků, kraul                | Na žádost        | ✉️ Žádost odeslána                             |
| CADDY Underwater          | Reálný podvodní | ~10k stereo snímků potápěčů        | Veřejný (GitHub) | Ke stažení                                     |
| Cao & Yan                 | Reálný podvodní | 2,500 obrázků                      | Nejasné          | —                                              |

---

## Klíčová literatura (výběr)

### Biomechanika plavání

- Maglischo (2003) *Swimming Fastest* — zlatý standard · KNIHA (Human Kinetics, ISBN 9780736031806) · [Internet Archive](https://archive.org/details/swimmingfastest0000magl) · ⚠️ NESTAŽENO — sehnat z knihovny
- Craig & Pendergast (1979) — V = SR × SL vztah · PAYWALL (LWW) · [PubMed](https://pubmed.ncbi.nlm.nih.gov/530025/)
- Psycharakis & Sanders (2010) — body roll review · PAYWALL (Taylor & Francis) · [ResearchGate preprint](https://www.researchgate.net/publication/282148298_Body_roll_in_swiming_A_review)
- Chollet et al. (2000) — Index of Coordination (IdC) · PAYWALL (Thieme) · [ResearchGate preprint](https://www.researchgate.net/publication/12632597_A_New_Index_of_Coordination_for_the_Crawl_Description_and_Usefulness)
- Virag et al. (2014) — prevalence biomechanických chyb (dropped elbow 61.3%) · [PMC open access](https://pmc.ncbi.nlm.nih.gov/articles/PMC4000476/)
- Barden & Kell (2014) — vztah stroke parametrů a critical swimming speed
- Barbosa et al. (2011) — Biomechanics of Competitive Swimming Strokes · [IntechOpen open access](https://www.intechopen.com/chapters/19665)
- Toussaint et al. (2000) — Biomechanics of Swimming (drag faktor K, propelling efficiency e_p, power balance) · KNIHA (Garrett & Kirkendall, Exercise and Sport Science, pp. 639–660) · ✅ STAŽENO

### Pose estimation

- ViTPose (Xu et al., NeurIPS 2022) — Vision Transformer, škálovatelný 20M-1B params · [arXiv:2204.12484](https://arxiv.org/abs/2204.12484)
- RTMPose (Jiang et al., 2023) — 75.8% AP COCO, 90+ FPS CPU, 430+ FPS GPU · [arXiv:2303.07399](https://arxiv.org/abs/2303.07399)
- Einfalt, Zecha & Lienhart (WACV 2018, CVPR 2019) — plavecky-specifický PE · [WACV 2018 PDF](https://opus.bibliothek.uni-augsburg.de/opus4/frontdoor/deliver/index/docId/61054/file/WACV18_einfalt.pdf) · [CVPR 2019 CVF](https://openaccess.thecvf.com/content_CVPRW_2019/html/CVSports/Zecha_Refining_Joint_Locations_for_Human_Pose_Tracking_in_Sports_Videos_CVPRW_2019_paper.html)
- Giulietti et al. (2023) — SwimmerNET, podvodní PE · [MDPI Sensors open access](https://www.mdpi.com/1424-8220/23/4/2364)
- DeepLabCut (Mathis et al., 2018) — markerless PE z ~200 anotovaných snímků · PAYWALL (Nature) · [PubMed Central](https://pmc.ncbi.nlm.nih.gov/articles/PMC6400582/) · [GitHub](https://github.com/DeepLabCut/DeepLabCut)

### RAG a LLM ve sportu

- Comendant (2024) — RAG-enhanced LLM coaching for swimming (bakálářka, University of Twente) · [PDF](https://essay.utwente.nl/fileshare/file/101013/Comendant_BA_EEMCS.pdf)
- Talha et al. (2025) — Talking Tennis: biomechanics → LLM feedback · [arXiv:2510.03921](https://arxiv.org/abs/2510.03921)
- BoxingPro (2024) — IoT-LLM boxing coaching, GPT-4 hodnocení 4.0/5.0 · [MDPI Electronics open access](https://www.mdpi.com/2079-9292/14/21/4155)
- Lewis et al. (2020) — RAG for Knowledge-Intensive NLP Tasks · [arXiv:2005.11401](https://arxiv.org/abs/2005.11401) · [NeurIPS PDF](https://proceedings.neurips.cc/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf)
- **Žádný recenzovaný CV→RAG→LLM pipeline pro plavání neexistuje** — toto je hlavní přínos práce

### Datasety — papery

- Fiche et al. (2023) — SwimXYZ dataset, ACM SIGGRAPH MIG · [arXiv:2310.04360](https://arxiv.org/abs/2310.04360) · [Zenodo data](https://zenodo.org/records/8399376)

---

## Cílová architektura (v2 — webová)

```
Frontend (Vue.js 3 + Vite + Tailwind + Pinia)
    │ REST API + WebSocket
Backend (FastAPI + Celery + Redis)
    ├── Pose Estimation (ViTPose/RTMPose, ONNX)
    ├── Ragdoll Constraints (filtrování nerealistických póz, vyhlazení sekvencí)
    ├── Biomechanics Extractor
    ├── Comparator (DTW/ML)
    └── Feedback Generator (pravidlový systém + ML modely)
Storage (PostgreSQL + File Storage)
```

### Ragdoll constraints

Post-processing vrstva po pose estimation. Klouby mají definované limity rotace (loket 0-150°, rameno max abdukce, koleno 0-170° atd.). Detekce přes ragdoll odfiltruje:

- Fyzikálně nemožné pózy (artefakty z okluzí, reflexů pod vodou)
- Výkyvy mezi framy (temporální vyhlazení)
- Záměny levá/pravá strana (běžný problém u plavců v boční rotaci)

Zvlášť důležité pro podvodní záběry, kde pose estimation dělá víc chyb kvůli refrakci a bublinám.

### Upload flow

1. Video + výběr úrovně (Dítě / Pokročilý) + pohled (side/front/underwater) + styl
2. WebSocket progress bar
3. Výsledky: metriky, odchylky, doporučení, video s overlay pózy, score 0-100

### Referenční systém — prahy podle úrovně

| Metrika            | Dítě (8–14) | Pokročilý (15+) |
| ------------------ | ----------- | --------------- |
| Frekvence záběru   | 40-60/min   | 30-65/min       |
| Rotace těla        | 10-60°      | 30-55°          |
| Úhel loktu (catch) | 100-170°    | 130-170°        |
| Tolerance odchylek | ±25°        | ±15°            |

---

## Coding standards

- **Type hints povinné** na všech funkcích
- **Komentáře anglicky**, vysvětlují PROČ (ne CO)
- **Logging** místo print()
- **Dataclasses** pro datové struktury
- **snake_case** pro soubory, funkce; **PascalCase** pro třídy; **UPPER_SNAKE_CASE** pro konstanty
- **Testy**: pytest, cíl ≥80% coverage
- **Error handling**: graceful degradation, nikdy silent failures
- **Commit messages**: anglicky, krátký summary + detailní popis, BEZ co-author tagů

---

## Autorovy poznámky a nápady

- Cvičící appka pro děti a mírně pokročilé
- Individualizovaný video feedback — uložiště dokumentů
- Platební metoda (monetizace)
- Cílová skupina: děti, mírně pokročilí
- GDPR videí — řešit soukromí
- Nějaká záštita (spolupráce s organizací?)
- Následný feedback (follow-up po analýze)

---

## Příkazy pro práci s prototypem

```bash
# Aktivace
cd prototyp
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac
pip install -r requirements.txt

# Spuštění aplikace
python src/main.py

# Testy
pytest tests/ -v

# Generování template
python -m training.template_generator --style freestyle

# Trénink klasifikátoru
python -m training.train_classifier --multi-style --epochs 50 --no-amp

# Download datasetu
python scripts/download_dataset.py --dataset swimxyz --annotations-only
python scripts/download_dataset.py --dataset swimxyz --style freestyle --all-parts
```

---

## Rozhodnuté otázky

1. **Deadline odevzdání** — cca rok (únor 2027), dostatek času na plný rozsah
2. **GPU přístup** — osobní NVIDIA RTX 3060 + škola poskytne výkon na trénink (fine-tuning ViTPose/RTMPose zvládnutelný)
3. **Kontakt na trenéra** — možný, není potvrzený; autor sám aktivně plave a závodí v triatlonu
4. **Primární styl** — kraul (freestyle) jako první, nejvíc dat i praktického využití
5. **Reálná videa** — autor si je pořídí sám (plave aktivně)
6. **Počet kategorií plavců** — 2: Dítě (8–14) + Pokročilý (15+). Profesionál jako budoucí rozšíření. Důvody: jednodušší validace, méně dat potřeba, dostatečná granularita pro diplomku.

## Stále otevřené otázky

1. ~~**Desktop vs. Web**~~ → **ROZHODNUTO: Web aplikace** — server zpracovává video i veškerou ML inference. Prototyp (PySide6) slouží jen jako proof-of-concept.
2. ~~**RAG implementace**~~ → **ROZHODNUTO: Bez LLM/RAG** — feedback bude generovaný čistě ML pipeline (pravidlový systém + natrénované modely), ne LLM. Důvody proti LLM/RAG: závislost na externích API (OpenAI, Anthropic) = single point of failure; nedeterministické výstupy (stejný vstup → různý feedback); latence a náklady na inference; nemožnost plně fungovat offline; obtížná reprodukovatelnost experimentů. V diplomce diskutovat jako alternativní přístup s rozborem trade-offs, ne jako budoucí rozšíření.

---

## DTW rešerše (únor 2026)

### Rozhodnutí

**DTW zůstává hlavní metodou** pro porovnávání plavecké techniky s referenčními šablonami.

### Doporučená konfigurace

- **DTW-D** (dependent multivariate) — jeden warping path pro všechny klouby, zachovává inter-joint koordinaci
- **Sakoe-Chiba band** constraint — zamezí patologickým zarovnáním, `r` ≈ 15% délky cyklu
- **Segmentace** na jednotlivé záběry před DTW (ne celé kolo najednou)
- **DBA** (DTW Barycenter Averaging) pro konstrukci referenčních šablon z expertních záběrů

### Benchmark baseline (pro diplomku)

Porovnat DTW-D proti: Euclidean distance (baseline), LCSS (robustnost vůči šumu)

### Známé limitace DTW

- O(N²) komplexita — pro jednotlivé záběry (100–300 samples) není problém
- Citlivost na šum — řešit Butterworth filtrem před DTW
- Není metrika (nesplňuje trojúhelníkovou nerovnost)
- Bez constraintu produkuje nesmyslné warping paths

### Klíčové zdroje pro citaci

- Sakoe & Chiba (1978) — originální DTW paper
- Keogh et al. — "Everything you know about DTW is wrong" (UCR)
- Shokoohi-Yekta et al. (2017) — DTW-D vs DTW-I pro multivariate (Springer Data Mining)
- S-WFDTW (2025, Scientific Reports) — fitness scoring s BlazePose, analogický use case
- PMC 2025 — paddle stroke klasifikace s DTW v reálném čase
- PMC 2024 — optimal warping path selection pro gait analysis
- Cuturi & Blondel (ICML 2017) — Soft-DTW (diferencovatelná varianta, pro případnou integraci s DL)

### Alternativy (diskuze v diplomce, neimplementovat)

- LCSS, EDR, MSM — robustnější vůči šumu, ale méně literatury v biomechanice
- ROCKET/TCN/Transformer — black box, žádný interpretovatelný warping path
- Soft-DTW — zajímavé pro budoucí práci (DL loss funkce)
- FastDTW — studie z 2020 ukázala, že je často pomalejší než constrained DTW

---

## Klasifikace stylu — rešerše (únor 2026)

### Stav

Stávající LSTM v `prototyp/training/models/style_classifier.py` = proof-of-concept (99.67% na SwimXYZ). V diplomce nebude prezentován jako finální řešení — slouží jen jako výchozí bod. Finální model bude zvolen na základě rešerše metod.

### Zkoumané architektury a trade-offs

| Architektura               | Výhody                                                                                    | Nevýhody                                                                   | Použití v diplomce       |
| -------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------ |
| BiLSTM + Attention         | Temporální kontext obou směrů, interpretovatelné attention váhy, osvědčený na keypointech | Sekvenční inference (nelze paralelizovat)                                  | **Zvolená architektura** |
| GRU/BiGRU                  | Méně parametrů, rychlejší trénink                                                         | Kratší paměť než LSTM                                                      | Ablation experiment      |
| TCN (dilatované konvoluce) | Paralelizovatelný, exponenciální receptive field                                          | Méně přirozený pro temporální data                                         | Non-recurrent baseline   |
| InceptionTime              | Multi-scale, SOTA na benchmarcích                                                         | Složitější architektura, overkill pro 4 třídy                              | Diskuze v rešerši        |
| Transformer                | Globální kontext, attention                                                               | Vyžaduje velké datasety, zbytečná složitost pro krátké sekvence            | Diskuze v rešerši        |
| ROCKET/MiniROCKET          | Špičková přesnost, rychlý trénink                                                         | **Black box** — náhodná jádra, neinterpretovatelné, závislost na 3rd party | **Odmítnuto**            |

### Best practices pro klasifikaci z keypointů

- Z-normalizace per-joint (nezávislost na absolutní pozici/velikosti)
- BiLSTM preferován nad unidirectional — offline klasifikace, plný kontext
- Attention pooling místo last-hidden-state — identifikuje klíčové fáze záběru
- Dropout 0.3 + weight decay proti overfittingu na syntetická data

### Domain gap: syntetická vs. reálná data

- SwimXYZ je syntetický → model se učí "čisté" pohyby bez šumu PE
- Při nasazení na reálná data (s šumem z ViTPose/RTMPose) očekávat pokles accuracy
- Mitigace: augmentace šumem při tréninku, fine-tuning na reálných datech

### Experimentální plán (kapitola 5)

1. BiLSTM + Attention vs. TCN — rekurence vs. konvoluce (dva odlišné principy)
2. Ablace: GRU místo LSTM, bez attention, unidirectional
3. Vliv délky sekvence (16, 32, 64 framů)
4. Cross-domain: trénink na SwimXYZ, test na reálných datech

---

_Last Updated: 2026-03-02_
_Status: Prototyp Phase 0-2 kompletní. Diplomka ve fázi plánování. Kategorie plavců: 2 (Dítě + Pokročilý)._
