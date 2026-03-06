# SwimAth — Plán diplomové práce

## Zaměření: Softwarové inženýrství

Diplomka je zaměřená na **návrh a implementaci webového systému**. ML/PE je použitá technologie (jako databáze), ne předmět výzkumu. Hlavní přínos = end-to-end SW řešení.

---

## Struktura diplomové práce (kapitoly)

1. **Úvod** — motivace, cíl práce, přínos (SW systém pro analýzu plavecké techniky)
2. **Analýza problému**
   - 2.1 Doménová analýza — biomechanika plavání (stručně, max 10 stran)
   - 2.2 Existující řešení a konkurenční analýza
   - 2.3 Požadavky na systém (funkční, nefunkční, aktéři, use cases)
   - 2.4 Technologická rešerše (PE architektury, DTW, webové frameworky, async processing)
3. **Návrh řešení** ← JÁDRO PRÁCE pro SW inženýrství
   - 3.1 Požadavky na systém (FR, NFR, use case diagram)
   - 3.2 Architektura systému (C4 diagramy, komponentový diagram)
   - 3.3 Návrh API (REST endpointy, WebSocket protokol)
   - 3.4 Datový model (ER diagram, PostgreSQL schéma, Alembic migrace)
   - 3.5 Asynchronní zpracování (Celery + Redis, task lifecycle)
   - 3.6 Bezpečnost a ochrana dat (GDPR, validace, CORS)
   - 3.7 Návrh ML pipeline jako SW komponenty (Strategy pattern, pipeline orchestrace)
   - 3.8 Výběr modelu pro odhad pózy
   - 3.9 Ragdoll constraints
   - 3.10 Biomechanické metriky
   - 3.11 Referenční systém
   - 3.12 Porovnávací metoda (DTW)
   - 3.13 Klasifikace plaveckého stylu
   - 3.14 Diskuse alternativních přístupů
4. **Implementace**
   - 4.1 Předzpracování videa (OpenCV, FFmpeg normalizace)
   - 4.2 ML pipeline (ONNX Runtime, batching, error handling)
   - 4.3 Backend (FastAPI, routing, dependency injection, Pydantic)
   - 4.4 Frontend (Vue.js 3, Pinia, Canvas API video overlay)
   - 4.5 Asynchronní zpracování (Celery workers, WebSocket progress)
   - 4.6 Databáze (SQLAlchemy ORM, Alembic migrace, connection pooling)
   - 4.7 Referenční databáze (DBA generování, JSON schéma)
   - 4.8 Testovací strategie (unit, integrace, e2e, code coverage)
   - 4.9 CI/CD a deployment (Docker, docker-compose, GitHub Actions)
5. **Experimenty a vyhodnocení**
   - 5.1 Funkční testování (end-to-end scénáře)
   - 5.2 Výkonnostní testování (throughput, latence, škálovatelnost)
   - 5.3 Přesnost odhadu pózy (benchmark PE modelů — validace ML komponenty)
   - 5.4 Kvalita detekce chyb (precision/recall vs. trenér)
   - 5.5 Testování na reálných videích
   - 5.6 Uživatelské testování (alespoň návrh protokolu)
   - 5.7 Limity systému
6. **Závěr** — shrnutí, přínos, budoucí práce

---

## TODO list — pracovní balíky

### A. REŠERŠE A PŘÍPRAVA

- [ ] **A1. Literární rešerše — biomechanika plavání**
  - Prostudovat klíčové zdroje (Maglischo, Riewald, Craig & Pendergast)
  - Definovat metriky techniky pro každou úroveň
  - Sepsat kapitolu rešerše — biomechanika (stručně, max 10 stran)

- [ ] **A2. Literární rešerše — technologická**
  - PE architektury (ViTPose, RTMPose, HRNet, MediaPipe)
  - Plavecky-specifické práce (Augsburg, SwimmerNET, SwimXYZ)
  - Existující sportovní analytické systémy (konkurenční analýza)
  - Webové frameworky, async processing patterns
  - Sepsat kapitolu rešerše — technická část

- [ ] **A3. Získání datasetů**
  - [x] SwimXYZ ze Zenodo (~300 GB)
  - [x] Žádost — Augsburg Swimming Channel
  - [x] Žádost — SwimmerNET
  - [ ] Stáhnout CADDY Underwater dataset
  - [ ] Prozkoumat a ohodnotit získaná data

- [ ] **A4. Definice metrik a prahů pro 2 úrovně**
  - Na základě literatury + konzultace s trenérem
  - Dítě (8–14): základní metriky, širší tolerance
  - Pokročilý (15+): zpřísněné prahy
  - Vytvořit tabulku: metrika × úroveň × optimální rozsah × práh chyby

---

### B. EXPERIMENTY S POSE ESTIMATION

- [ ] **B1. Benchmark existujících modelů na plaveckých datech**
  - MediaPipe vs RTMPose vs ViTPose na SwimXYZ
  - Metriky: PCK, AP, MPJPE
  - Zdokumentovat výsledky

- [ ] **B2. Fine-tuning vybraného modelu na SwimXYZ**
  - Side-view freestyle jako první
  - Vyhodnotit zlepšení oproti base modelu
  - Otestovat přenos na reálná data

- [ ] **B3. Testování na různých pohledech kamery**
  - Side-view (primární), front-view, underwater
  - Zdokumentovat kde model funguje a kde selhává

---

### C. BIOMECHANICKÁ ANALÝZA

- [ ] **C1. Pipeline: keypoints → biomechanické metriky**
  - Implementovat výpočet: SR, SL, rotace, úhly kloubů
  - Implementovat detekci fází záběru

- [ ] **C2. Vytvoření referenčních vzorů**
  - Min 1 styl × 1 pohled × 2 úrovně
  - DBA generování, JSON schéma

- [ ] **C3. Implementace porovnávací metody**
  - DTW-D + Sakoe-Chiba constraint
  - Pravidlový systém detekce chyb
  - Skórovací systém 0–100
  - Generování textové zpětné vazby

---

### D. WEBOVÁ APLIKACE

- [ ] **D1. Backend — FastAPI základ**
  - Projekt + struktura + config
  - Upload endpoint + validace videa
  - PostgreSQL + SQLAlchemy + Alembic migrace
  - Celery + Redis async zpracování
  - WebSocket progress
  - REST API endpointy

- [ ] **D2. Backend — integrace ML pipeline**
  - ONNX Runtime inference
  - Strategy pattern pro PE modely
  - End-to-end: video in → výsledky out

- [ ] **D3. Frontend — Vue.js 3**
  - Upload (video + výběr úrovně/pohledu/stylu)
  - Progress bar (WebSocket)
  - Výsledky (metriky, odchylky, doporučení)
  - Video přehrávač s overlay pózy (Canvas API)
  - Historie analýz

- [ ] **D4. Testovací strategie**
  - Unit testy (pytest)
  - Integrace (TestClient)
  - E2E (Playwright)
  - Code coverage

- [ ] **D5. CI/CD a deployment**
  - Docker multi-stage build
  - docker-compose
  - GitHub Actions
  - Linting/formatting

---

### E. VYHODNOCENÍ A DIPLOMKA

- [ ] **E1. Funkční testování**
  - End-to-end scénáře
  - Test matrix (styl × pohled × úroveň)

- [ ] **E2. Výkonnostní testování**
  - Throughput (videí/hodinu)
  - Latence (upload → výsledek)
  - Paměťové nároky, GPU utilization

- [ ] **E3. Validace ML pipeline**
  - Přesnost PE modelů (jako ověření SW komponenty)
  - Kvalita detekce chyb vs. trenér

- [ ] **E4. Testování na reálných videích**
  - Autorova vlastní videa (triatlonista)
  - Různé podmínky nahrávání

- [ ] **E5. Sepsání diplomové práce**
  - Průběžně po dokončení každého bloku
  - Finální kompilace a revize

- [ ] **E6. Příprava na obhajobu**
  - Prezentace (max 12 minut, ~10–15 slidů)
  - Demo aplikace
  - Odpovědi na očekávané otázky

---

## Závislosti mezi úkoly

```
A1, A2 (rešerše) ──────────────────────────┐
    │                                       │
    ▼                                       ▼
A3 (datasety) ──► B1 (benchmark) ──► B2 (fine-tuning)
    │                                       │
    ▼                                       ▼
A4 (metriky/prahy) ──► C1 (pipeline) ──► C2 (reference) ──► C3 (porovnání)
                                                                  │
                        D1 (backend) ──► D2 (integrace ML) ◄──────┘
                            │                    │
                            ▼                    ▼
                        D3 (frontend) ──► E1-E4 (testování) ──► E5 (text) ──► E6 (obhajoba)
                            │
                        D4 (testy) + D5 (CI/CD)
```

**Kritická cesta:** A3 → B1 → B2 → C1 → C2 → C3 → D2 → E3

**Paralelně:**
- Rešerši (A1, A2) + stahování dat (A3)
- Backend (D1) + Frontend (D3) + ML experimenty (B)
- Testy (D4) + CI/CD (D5) průběžně
- Text diplomky (E5) průběžně

---

## Odhad celkového rozsahu

| Blok | Rozsah | Poznámka |
|------|--------|----------|
| A. Rešerše a příprava | 4–6 týdnů | Lze začít ihned |
| B. Pose estimation experimenty | 4–6 týdnů | Závisí na datech |
| C. Biomechanická analýza | 4–5 týdnů | Jádro ML |
| D. Webová aplikace + testy | 5–7 týdnů | Jádro SW inženýrství |
| E. Vyhodnocení a psaní | 4–6 týdnů | Průběžně + finalizace |
| **Celkem** | **~14–20 týdnů** | S paralelní prací |

---

## Minimální životaschopný rozsah

1. Kompletní rešerše
2. Benchmark PE modelů na plaveckých datech
3. Fine-tuning na SwimXYZ (freestyle side-view)
4. Pipeline keypoints → biomechanické metriky
5. Referenční systém pro 1 styl × 1 pohled × 2 úrovně
6. Fungující porovnání s detekcí chyb
7. Základní webové rozhraní (upload → výsledky)
8. Vyhodnocení na reálných videích
9. Výkonnostní testování systému

Co může jít do "budoucí práce":
- Více stylů a pohledů kamery
- Podvodní korekce refrakce
- Pokročilá vizualizace (side-by-side, 3D)
- Uživatelské účty, historie
- LLM prezentační vrstva

---

## Rozhodnuté otázky
1. **Deadline** — cca únor 2027, dostatek času
2. **GPU** — RTX 3060 + škola poskytne výkon
3. **Primární styl** — kraul (freestyle)
4. **Úrovně plavců** — 2: Dítě (8–14) + Pokročilý (15+)
5. **Architektura** — Web (Vue.js + FastAPI + Celery)
6. **Feedback** — Pravidlový systém + ML (bez LLM/RAG)
7. **LaTeX šablona** — FITthesis-LaTeX (oficiální FIT)
8. **Název práce** — "Návrh a implementace webového systému pro automatickou analýzu plavecké techniky z videa"
