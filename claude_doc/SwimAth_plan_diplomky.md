# SwimAth — Plán diplomové práce

## Struktura diplomové práce (kapitoly)

1. **Úvod** — motivace, cíl práce, přínos
2. **Rešerše / Teoretická část**
   - Biomechanika plavání (styly, metriky, co dělá dobrého plavce)
   - Odhad lidské pózy (architektury: OpenPose → HRNet → ViTPose → RTMPose)
   - Existující datasety (SwimXYZ, Augsburg, SwimmerNET, ...)
   - ML ve sportovní analýze (existující systémy, co chybí)
   - Podvodní výzvy (refrakce, bubliny, viditelnost)
3. **Návrh řešení**
   - Architektura systému (Vue.js + FastAPI + ML pipeline)
   - Referenční model (3 úrovně × pohledy × styly)
   - Výběr pose estimation modelu a důvody
   - Návrh biomechanických metrik pro každou úroveň
   - Porovnávací metoda (DTW / klasifikátor)
4. **Implementace**
   - Předzpracování videa
   - ML pipeline (pose estimation → metriky → porovnání)
   - Webová aplikace (frontend + backend)
   - Referenční databáze
5. **Experimenty a vyhodnocení**
   - Přesnost pose estimation na plaveckých datech
   - Kvalita detekce chyb vs. ruční hodnocení trenérem
   - Testování na reálných videích (různé úrovně, pohledy)
   - Limity systému
6. **Závěr** — shrnutí, přínos, budoucí práce

---

## TODO list — pracovní balíky

### A. REŠERŠE A PŘÍPRAVA

- [ ] **A1. Literární rešerše — biomechanika plavání**
  - Prostudovat klíčové zdroje (Maglischo, Riewald, Craig & Pendergast)
  - Definovat metriky techniky pro každou úroveň
  - Sepsat kapitolu rešerše — biomechanika
  - *Odhadovaný rozsah: 2 týdny*

- [ ] **A2. Literární rešerše — pose estimation a ML**
  - Prostudovat architektury (ViTPose, RTMPose, HRNet, MediaPipe)
  - Prostudovat plavecky-specifické práce (Augsburg, SwimmerNET, SwimXYZ)
  - Prostudovat existující sportovní analytické systémy
  - Sepsat kapitolu rešerše — technická část
  - *Odhadovaný rozsah: 2 týdny*

- [ ] **A3. Získání datasetů**
  - [x] Odeslat žádost — Augsburg Swimming Channel
  - [x] Odeslat žádost — SwimmerNET
  - [ ] Stáhnout SwimXYZ ze Zenodo (~300 GB)
  - [ ] Stáhnout CADDY Underwater dataset
  - [ ] Prozkoumat a ohodnotit získaná data
  - *Odhadovaný rozsah: 1–4 týdny (záleží na odpovědích)*

- [ ] **A4. Definice metrik a prahů pro 3 úrovně**
  - Na základě literatury + konzultace s trenérem
  - Začátečníci: co sledovat, jaké odchylky tolerovat
  - Mírně pokročilí: zpřísnění, přidání metrik
  - Experti: jemné detaily, úzké tolerance
  - Vytvořit tabulku: metrika × úroveň × optimální rozsah × práh chyby
  - *Odhadovaný rozsah: 1 týden*

---

### B. EXPERIMENTY S POSE ESTIMATION

- [ ] **B1. Benchmark existujících modelů na plaveckých datech**
  - Spustit MediaPipe, RTMPose, ViTPose na vzorcích plaveckého videa
  - Porovnat přesnost, rychlost, chybové módy
  - Rozhodnout se pro model (nebo kombinaci)
  - Zdokumentovat výsledky pro diplomku
  - *Odhadovaný rozsah: 1–2 týdny*

- [ ] **B2. Fine-tuning vybraného modelu na SwimXYZ**
  - Připravit trénovací data (side-view freestyle jako první)
  - Fine-tune ViTPose/RTMPose
  - Vyhodnotit zlepšení oproti base modelu
  - Otestovat přenos na reálná data (pokud dostupná z Augsburgu)
  - *Odhadovaný rozsah: 2–3 týdny*

- [ ] **B3. Testování na různých pohledech kamery**
  - Side-view (primární)
  - Front-view (pokud data)
  - Underwater (pokud data)
  - Zdokumentovat, kde model funguje a kde selhává
  - *Odhadovaný rozsah: 1 týden*

---

### C. BIOMECHANICKÁ ANALÝZA

- [ ] **C1. Pipeline: keypoints → biomechanické metriky**
  - Implementovat výpočet: frekvence záběru, délka záběru
  - Implementovat výpočet: rotace těla, poloha hlavy
  - Implementovat výpočet: úhly kloubů (loket, rameno)
  - Implementovat detekci fází záběru (catch, pull, push, recovery)
  - *Odhadovaný rozsah: 2 týdny*

- [ ] **C2. Vytvoření referenčních vzorů**
  - Vybrat segmenty správné techniky z dostupných dat
  - Vypočítat referenční sekvence pro alespoň 1 styl × 1 pohled × 3 úrovně
  - Uložit jako .npy + metrics.json + error_thresholds.json
  - *Odhadovaný rozsah: 1–2 týdny*

- [ ] **C3. Implementace porovnávací metody**
  - DTW pro temporální porovnání sekvencí záběrů
  - Pravidlový systém pro detekci konkrétních chyb
  - Skórovací systém (overall score 0–100)
  - Generování textové zpětné vazby
  - *Odhadovaný rozsah: 2 týdny*

---

### D. WEBOVÁ APLIKACE

- [ ] **D1. Backend — FastAPI základ**
  - Projekt + struktura + config
  - Upload endpoint + validace videa
  - PostgreSQL + SQLAlchemy model
  - Async zpracování (BackgroundTasks nebo Celery)
  - WebSocket pro progress
  - API pro výsledky
  - *Odhadovaný rozsah: 2 týdny*

- [ ] **D2. Backend — integrace ML pipeline**
  - Napojení pose estimation modelu
  - Napojení biomechanické analýzy
  - Napojení porovnávacího systému
  - End-to-end: video in → výsledky out
  - *Odhadovaný rozsah: 1–2 týdny*

- [ ] **D3. Frontend — Vue.js**
  - Upload stránka (video + výběr úrovně/pohledu/stylu)
  - Progress bar (WebSocket)
  - Výsledková stránka (metriky, odchylky, doporučení)
  - Video přehrávač s overlay pózy
  - Historie analýz
  - *Odhadovaný rozsah: 2–3 týdny*

---

### E. VYHODNOCENÍ A DIPLOMKA

- [ ] **E1. Testování na reálných videích**
  - Natočit/sehnat videa plavců různých úrovní
  - Spustit analýzu, porovnat s hodnocením trenéra
  - Zdokumentovat úspěšnost a limity
  - *Odhadovaný rozsah: 1–2 týdny*

- [ ] **E2. Sepsání diplomové práce**
  - Průběžně psát po dokončení každého bloku
  - Finální kompilace a revize
  - Obrázky, tabulky, grafy z experimentů
  - *Odhadovaný rozsah: průběžně + 2–3 týdny na finalizaci*

- [ ] **E3. Příprava na obhajobu**
  - Prezentace (10–15 slidů)
  - Demo aplikace
  - Připravit odpovědi na očekávané otázky
  - *Odhadovaný rozsah: 1 týden*

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
                        D3 (frontend) ──► E1 (testování) ──► E2 (text) ──► E3 (obhajoba)
```

**Kritická cesta:** A3 (datasety) → B1 → B2 → C1 → C2 → C3 → D2 → E1

**Co můžeš dělat paralelně:**
- Rešerši (A1, A2) psát současně se stahováním datasetů (A3)
- Backend základ (D1) a frontend (D3) stavět současně s ML experimenty (B1, B2)
- Text diplomky (E2) psát průběžně po každém dokončeném bloku

---

## Odhad celkového rozsahu

| Blok | Rozsah | Poznámka |
|---|---|---|
| A. Rešerše a příprava | 4–6 týdnů | Lze začít ihned |
| B. Pose estimation experimenty | 4–6 týdnů | Závisí na datech |
| C. Biomechanická analýza | 4–5 týdnů | Jádro diplomky |
| D. Webová aplikace | 4–6 týdnů | Lze paralelně s B/C |
| E. Vyhodnocení a psaní | 4–6 týdnů | Průběžně + finalizace |
| **Celkem** | **~14–20 týdnů** | S paralelním prací |

---

## Minimální životaschopný rozsah (pokud nestíháš)

Pokud by byl čas kritický, diplomka stojí i s tímto minimem:

1. ✅ Rešerše (kompletní)
2. ✅ Benchmark pose estimation modelů na plaveckých datech
3. ✅ Fine-tuning na SwimXYZ (alespoň freestyle side-view)
4. ✅ Pipeline keypoints → biomechanické metriky
5. ✅ Referenční systém pro 1 styl × 1 pohled × 3 úrovně
6. ✅ Fungující porovnání s detekcí chyb
7. ✅ Základní webové rozhraní (upload → výsledky)
8. ✅ Vyhodnocení na reálných videích

Co může jít do "budoucí práce":
- Více stylů a pohledů kamery
- Podvodní korekce refrakce
- Pokročilá vizualizace (side-by-side, 3D)
- Uživatelské účty, historie

---

## Otevřené otázky k rozhodnutí

1. **Jaký je deadline odevzdání?** → ovlivní rozsah
2. **Máš přístup ke GPU pro trénování?** → fine-tuning ViTPose potřebuje GPU
3. **Máš kontakt na trenéra pro konzultaci metrik?** → A4 bude kvalitnější
4. **Na jaký styl se zaměřit první?** → kraul je nejčastější a má nejvíc dat
5. **Budeš mít reálná videa pro testování?** → natočit u bazénu?
