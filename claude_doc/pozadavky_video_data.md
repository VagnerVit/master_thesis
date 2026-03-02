# Požadavky na video data — SwimAth

**Účel**: Specifikace požadovaných video dat pro diplomovou práci SwimAth.
**Aktualizováno**: 2026-03-02

---

## 1. Čtyři účely videí v projektu

### A) Fine-tuning pose estimation (balík B2)

|                      |                                                                         |
| -------------------- | ----------------------------------------------------------------------- |
| **Účel**             | Naučit ViTPose/RTMPose rozpoznávat klíčové body na plavcích             |
| **Potřebuje**        | Videa s anotacemi keypointů (nebo semi-supervised přístup)              |
| **SwimXYZ pokryje?** | ✅ ANO — syntetická data s perfektními anotacemi, 48 keypointů           |
| **Reálná data**      | Malý validační set (~100–200 ručně anotovaných framů)                   |
| **Závěr**            | Primárně SwimXYZ, doplnit malým reálným setem pro cross-domain evaluaci |

### B) Referenční šablony DTW (balík C2)

|                      |                                                                          |
| -------------------- | ------------------------------------------------------------------------ |
| **Účel**             | Vytvořit "ideální" vzor záběru pro každou úroveň                         |
| **Požadavek**        | 1 styl (kraul) × 1–3 pohledy × 2 úrovně = **2–6 šablon**                 |
| **Na šablonu**       | Min. 3–5 plavců dané úrovně, 5–10 čistých záběrových cyklů od každého    |
| **SwimXYZ pokryje?** | ČÁSTEČNĚ — dospělí (Pokročilý). Děti NE.                                 |
| **Reálná data**      | **NUTNÉ** pro kategorii Dítě (8–14 let). Ideálně i validace Pokročilých. |

### C) Validace pipeline (balík E1)

|                      |                                                                            |
| -------------------- | -------------------------------------------------------------------------- |
| **Účel**             | Otestovat celý pipeline na reálných videích, porovnat s hodnocením trenéra |
| **Požadavek**        | Videa plavců RŮZNÝCH úrovní, NEZÁVISLÁ na trénovacích/šablonových datech   |
| **Ground truth**     | Hodnocení od kvalifikovaného trenéra                                       |
| **SwimXYZ pokryje?** | ❌ NE — validace musí být na reálných datech                                |
| **Reálná data**      | **NUTNÉ** — toto je hlavní blocker                                         |

### D) Benchmark pose estimation modelů (balík B1)

|                      |                                                               |
| -------------------- | ------------------------------------------------------------- |
| **Účel**             | Porovnat MediaPipe vs RTMPose vs ViTPose na plaveckých datech |
| **Požadavek**        | Společný dataset s ground truth anotacemi                     |
| **SwimXYZ pokryje?** | ✅ ANO pro syntetický benchmark                                |
| **Reálná data**      | Ideálně malý reálný set pro real-world benchmark              |

---

## 2. Technické požadavky — podloženo literaturou a pipeline analýzou

### 2.1 Rozlišení

**Požadavek: min. 720p (1280×720), ideálně FHD (1920×1080)**

Zdůvodnění:

- Pipeline interně resizuje na 224×224 px pro inference (`video_processor.py:target_size`), ale vstupní rozlišení ovlivňuje kvalitu detekce keypointů — vyšší rozlišení = přesnější lokalizace kloubů před resizem
- Confidence threshold 0.7 (`mediapipe_config.py`) — při nižším rozlišení více framů padne pod práh → ztráta dat
- **Plavec musí zabírat ≥25% šířky snímku** — při 720p to znamená min. ~180 px na postavu. Pod ~150 px jsou klouby pod rozlišovací schopností PE modelů (loket, zápěstí = jednotky pixelů, nerozlišitelné od šumu)
- Při FHD (1080p) a 25% šířky = ~270 px na postavu → výrazně spolehlivější detekce, zejména distálních kloubů (zápěstí, kotník)
- **720p je pragmatický kompromis** pro data od institucí, která nemusí mít nejnovější vybavení

### 2.2 FPS (snímková frekvence)

**Požadavek: min. 30 FPS, ideálně 60 FPS**

Zdůvodnění z pipeline:

- **Konkrétní výpočet pro děti:** SR dětí 46–56 cycles/min → 1 cyklus = 1.07–1.30 s → při 30 FPS = **32–39 framů na cyklus**
- **Konkrétní výpočet pro dospělé:** SR pokročilých 30–65 cycles/min → 1 cyklus = 0.92–2.0 s → při 30 FPS = 28–60 framů na cyklus
- **Fázová analýza:** záběrový cyklus kraulu má 4 fáze (entry/catch, pull, push, recovery). Žádná fáze nesmí mít méně než **5 framů** pro spolehlivou detekci. Nejkratší fáze (push) trvá ~10–15% cyklu → při 30 FPS a 32 framech = 3–5 framů → **hraniční**. Při 60 FPS = 6–10 framů → spolehlivé.
- `stroke_analyzer.py`: `min_cycle_frames=20` — při 25 FPS a SR=65: 25×(60/65) = 23 framů — **těsně nad limitem**, nespolehlivé
- Butterworth low-pass filter cutoff ~6 Hz (A4_metriky_prahy.md sekce 10.4) → Nyquist: potřeba min. 12 FPS, pro kvalitní filtrování 4× = **24+ FPS**
- DTW Sakoe-Chiba band r ≈ 15% délky cyklu → vyšší FPS = jemnější granularita warpingu
- **Závěr**: 30 FPS je absolutní minimum. 60 FPS výrazně zlepšuje fázovou analýzu (zejména u dětí s vyšším SR), DTW přesnost a filtrování šumu.

### 2.3 Délka záznamu

**Požadavek: min. 10 kompletních záběrových cyklů na plavce (~30s plavání)**

Zdůvodnění:

- DTW šablony: DBA (DTW Barycenter Averaging) potřebuje statisticky reprezentativní vzorek — min. 5 cyklů pro robustní průměr, 10+ pro spolehlivou šablonu
- Style classifier: `sequence_length=32`, `stride=16` → 10 cyklů × ~35 framů = 350 framů → ~20 sliding windows — dostatečné pro klasifikaci
- Validace: potřeba dostatečného počtu cyklů pro výpočet per-metric variance a confidence intervals
- **Ideálně 1–2 min** aktivního plavání = 20–40 cyklů → robustnější statistika

### 2.4 Pozice a vzdálenost kamery

**Side-view (MUST-HAVE):**

- Kamera kolmo na dráhu, výška ~1m nad hladinou, vzdálenost 3–5m
- Plavec zabírá ≥25% šířky snímku
- Zachytí: SR, SL, úhel loktu (všechny 4 fáze záběru), body alignment, timing

**Front-view (SHOULD-HAVE):**

- Na konci dráhy, frontální pohled na připlývajícího plavce
- Zachytí: rotaci trupu (shoulder roll, hip roll), symetrii záběru, hand entry crossover

**Underwater (NICE-TO-HAVE):**

- Pod hladinou, boční nebo šikmý pohled
- Zachytí: fáze záběru pod vodou (catch-pull-push), úhel tahu, pozici ruky
- Pozor: refrakce a bubliny zhoršují PE → nutné ragdoll constraints

#### Tabulka: Které metriky se měří z jakého pohledu

| Metrika                                                          | Side-view               | Front-view              | Underwater              |
| ---------------------------------------------------------------- | ----------------------- | ----------------------- | ----------------------- |
| **Úhel loktu** — 4 fáze (entry, catch, pull, push)               | ✅ Primární pohled       | ⚠️ Jen koronální rovina | ✅ Detailní pull-through |
| **Úhel kolene** (flutter kick)                                   | ✅ Sagitální rovina      | ❌                       | ⚠️ Refrakce             |
| **Body alignment** (úhel trup-nohy)                              | ✅                       | ❌                       | ⚠️                      |
| **Stroke Rate** (SR)                                             | ✅                       | ✅                       | ⚠️ Bubliny překrývají   |
| **Stroke Length** (SL)                                           | ✅ (s kalibrací)         | ❌                       | ❌                       |
| **Rotace ramen** (shoulder roll, typicky 60–110° celkový rozsah) | ⚠️ Jen vertikální posuv | ✅ Primární pohled       | ⚠️                      |
| **Rotace kyčlí** (hip roll)                                      | ⚠️                      | ✅                       | ⚠️                      |
| **L/R asymetrie záběru**                                         | ❌                       | ✅ Primární pohled       | ❌                       |
| **Hand entry pozice** (crossover, wide entry)                    | ⚠️                      | ✅                       | ✅                       |
| **Průběh tahu pod vodou** (catch → pull → push)                  | ⚠️ Jen viditelná část   | ❌                       | ✅ Primární pohled       |

**→ Side-view je nejuniverzálnější** — pokrývá kloubové úhly, SR, SL, body alignment.
**→ Front-view doplňuje** rotační metriky a symetrii, které z boku nelze měřit.
**→ Underwater** je klíčový pro analýzu tahu pod vodou, ale obtížně získatelný.

### 2.5 Formát a kodek

- **MP4 (H.264/H.265)** — standardní, plná kompatibilita s OpenCV `cv2.VideoCapture`
- Alternativy: AVI, MOV — taky OK, OpenCV je přečte
- **Důležité**: konstantní FPS (ne variable frame rate z mobilů!) — jinak frame skipping v `video_processor.py` nefunguje správně

### 2.6 Proč potřebujeme dětská data

Dětská biomechanická data jsou **hlavní blocker** pro kategorii Dítě (8–14 let). Důvody:

1. **Prakticky jediné měření kloubových úhlů u dětí při kraulu** v literatuře pochází z jedné studie (n=11, věk 8–13 let). Vzorek je příliš malý pro spolehlivé prahy — prahy v A4_metriky_prahy.md jsou z velké části extrapolace z dospělé literatury s rozšířenou tolerancí.

2. **SR dětí (46–56 c/min) je výrazně jiný rozsah než dospělí (30–50 c/min)**. Děti kompenzují kratší končetiny a nižší sílu záběru vyšším SR → nelze jednoduše extrapolovat dospělé prahy. Stejně tak SL dětí (1.0–2.0 m) je výrazně kratší než u dospělých (1.5–2.6 m).

3. **Variabilita pohybu u dětí je zásadně vyšší** než u dospělých — nezralá motorická koordinace, rostoucí organismus, nestabilní technika. Referenční šablony (DTW) vytvořené z dospělých dat nefungují — průměrný warping path bude příliš vzdálený od reálného dětského záběru.

4. **Body roll u dětí je v literatuře identifikován jako výzkumná mezera** — existuje jeden vzorek 11 dětí se shoulder roll 33–53°, ale bez hip roll dat. Prahy jsou odvozeny s bezpečnostní marží, ne z dat.

5. **Syntetický SwimXYZ dataset neobsahuje dětské modely** — pouze dospělé SMPL modely. Nelze z něj generovat dětské referenční šablony.

**Závěr:** Bez reálných dětských dat nelze kategorii Dítě validovat. Min. potřeba: 5 dětí (8–14 let), side-view kraul, 10+ cyklů na plavce.

---

## 3. Kategorie plavců a minimální počty

| Úroveň        | Věk  | Popis                                                                                 | Min. plavců | Ideálně | Účel               | SR range    |
| ------------- | ---- | ------------------------------------------------------------------------------------- | ----------- | ------- | ------------------ | ----------- |
| **Dítě**      | 8–14 | Plavecký kurz nebo dětský oddíl, rostoucí organismus                                  | 5           | 8–10    | Šablony + validace | 40–65 c/min |
| **Pokročilý** | 15+  | Aktivně plavající dospělý — od rekreačních po závodní (triatlonisté, oddíloví plavci) | 8–10        | 12+     | Šablony + validace | 30–65 c/min |

**Celkem: min. 13–15 plavců (ideálně 20+)**

> **Proč více plavců:** Každý plavec je nezávislý vzorek. Data slouží k vytvoření referenčních šablon a k validaci systému — čím více různých plavců, tím spolehlivější výsledky. Plavce použité pro šablony nesmím použít pro validaci (nezávislost testovacích dat).

> **Poznámka**: Kategorie „Profesionál" (národní/mezinárodní úroveň) je plánována jako budoucí rozšíření — v diplomce neimplementujeme vlastní šablony pro tuto úroveň, ale diskutujeme jako možnost.

### Co natočit od každého plavce

1. **Side-view kraul**: min. 10 kompletních záběrových cyklů (~30s plavání)
2. **Front-view kraul** (pokud dostupné): min. 10 cyklů
3. **Underwater kraul** (pokud dostupné): min. 5 cyklů
4. **Metadata formulář**: věk, pohlaví, kolik let plave, tréninková frekvence, závodní úroveň, výška, rozpětí paží
5. **GDPR souhlas**: podpis informovaného souhlasu (u dětí zákonný zástupce)

### Podmínky nahrávání

| Parametr            | Požadavek                                  | Poznámka                                |
| ------------------- | ------------------------------------------ | --------------------------------------- |
| **Bazén**           | 25m nebo 50m                               | Čistá voda (průhlednost pro underwater) |
| **Oblečení**        | Plavky (ne triko), kontrastní barva k vodě | Pro viditelnost keypoints               |
| **Plavecká čepice** | Ano                                        | Pomáhá PE rozlišit hlavu od vody        |
| **Osvětlení**       | Rovnoměrné, bez silných odlesků na hladině | Odrazy zhoršují detekci                 |
| **Stativ**          | Pevný, bez vibrací                         | Pohyb kamery znehodnotí data            |

---

## 4. SwimXYZ vs. reálná data

| Účel                     | SwimXYZ                                     | Reálná data                                           |
| ------------------------ | ------------------------------------------- | ----------------------------------------------------- |
| PE fine-tuning (B2)      | ✅ Primární zdroj (48 kp, perfektní GT)      | Malý validační set (~100–200 framů)                   |
| PE benchmark (B1)        | ✅ Syntetický benchmark                      | Malý reálný benchmark (~50 framů s ručními anotacemi) |
| Šablony Dítě (C2)        | ❌ Neobsahuje děti (jen dospělé SMPL modely) | **NUTNÉ — 5 dětí**                                    |
| Šablony Pokročilý (C2)   | ✅ Lze generovat                             | Validační porovnání na reálných datech                |
| Validace pipeline (E1)   | ❌ Nelze                                     | **NUTNÉ — 13–15 plavců**                              |
| Ground truth trenér (E1) | ❌                                           | **NUTNÉ — hodnocení trenérem**                        |

**SwimXYZ pohledy kamery** (5 typů): Aerial, Front, Side_above_water, Side_underwater, Side_water_level — pokrývají side + front + underwater, ale jsou syntetické (žádný šum z reálného PE).

**Domain gap**: Model trénovaný na SwimXYZ se učí "čisté" pohyby bez šumu PE → při nasazení na reálná data očekávat pokles accuracy. Proto je cross-domain validace na reálných datech klíčová.

---

## 5. Akční kroky pro kontakty (aktualizováno 2026-03-02)

### David Prycl / BALUO (UP Olomouc) — PRIORITA 1 ✅ odpověděl

- **Stav**: Kontaktoval kolegu s databází videí, ochoten poskytnout. Ukázka: youtube.com/watch?v=ijmb06JR74o
- **Akce**: ✉️ Odpovědět s konkrétní specifikací (viz sekce 8.1)
- **Ptát se na**: Kolik plavců? Jaké úrovně (děti?)? Formát/rozlišení? Úhly kamery? Anotace?

### Michaela Bátorová (VUT Brno CESA) — PRIORITA 1 ✅ odpověděla

- **Stav**: Nabízí telefonát v úterý dopoledne
- **Akce**: ☎️ Zavolat, body viz sekce 8.2
- **Klíčové**: Garant vodních sportů, plavecké kurzy — potenciál pro dětské plavce!

### Dan Jurák (FTVS UK Praha, flume) — PRIORITA 1 (přes Macase)

- **Stav**: Macas přesměroval, dal Juráka do CC. Jurák má videozáznamy z flumu.
- **Akce**: ✉️ Napsat přímo Jurákovi (viz sekce 8.3)
- **Klíčové**: Flume s underwater oknem — kontrolované podmínky, ideální pro side + underwater

### ČSPS — Český svaz plaveckých sportů — PRIORITA 2 (nová cesta přes EA)

- **Stav**: Juliana Daguano (European Aquatics) potvrdila — race analysis footage zdarma pro federace
- **Akce**: ✉️ Napsat ČSPS s odkazem na Daguano (viz sekce 8.4)
- **Klíčové**: Závodní záběry kompetitivních plavců

### Hannah Jowitt (Aquatics GB) — PRIORITA 3 (přes Kinga)

- **Stav**: Mark King (Loughborough) přesměroval
- **Akce**: ✉️ Napsat Hannah Jowitt (viz sekce 8.5)
- **Klíčové**: 10 kamer (4 underwater), profesionální setup

### Vlastní natáčení — ZÁLOŽNÍ PLÁN

- Vít + 2–3 známí triatlonisté/plavci, místní bazén
- Telefon na stativu (side + front), GoPro pro underwater
- Pokryje: Pokročilý. **Nepokryje: Dítě** — nutná spolupráce s institucí (GDPR dětí).

---

## 6. Prioritizace

### Must-have (bez toho diplomka není obhajitelná)

1. **20+ reálných videí plavců** (side-view kraul, 2 kategorie) pro šablony a validaci
2. **5–10 dětských plavců** (8–14 let) pro kategorii Dítě (referenční šablony + validace)
3. **8–12 pokročilých plavců** (15+) pro kategorii Pokročilý (validace + reálné šablony)
4. **Hodnocení trenérem** alespoň u 8 plavců (ground truth — systém říká X, shoduje se to s trenérem?)
5. **Side-view** jako primární pohled kamery

### Should-have (výrazně zvýší kvalitu)

5. Front-view záběry od stejných plavců
6. Underwater záběry (alespoň od části plavců)
7. Závodní záběry kompetitivních plavců (ČSPS / European Aquatics)
8. Flume záběry (Dan Jurák) — kontrolované podmínky
9. 60 FPS místo 30 FPS

### Nice-to-have

10. Data z Loughborough (multi-camera)
11. Více stylů než kraul
12. Longitudinální data (stejný plavec v čase)

---

## 7. GDPR a etické aspekty

- **Informovaný souhlas** od každého natáčeného plavce (u dětí zákonný zástupce)
- **Účel**: zpracování v rámci diplomové práce, akademický výzkum
- **Anonymizace**: v publikovaných výsledcích bez identifikace osob
- **Uložení**: lokální, ne veřejně dostupné
- **Šablonu souhlasu** připravit předem (česky)
- **Schválení etickou komisí** — ověřit, zda ČVUT vyžaduje pro tento typ výzkumu

---

## 8. Draft emaily a příprava na hovory

### 8.1 David Prycl / BALUO (odpověď na jeho nabídku)

**Komu**: david.prycl@upol.cz
**Předmět**: Re: Žádost o plavecká video data — diplomová práce FIT ČVUT

Zdravím, Davide,

moc děkuji za ochotu a za ukázkové video! Rád bych upřesnil, co přesně potřebuji:

**Co měřím a proč je to důležité z bočního pohledu:**
Systém z videa automaticky extrahuje pózu plavce a měří kloubové úhly — především úhel loktu ve 4 fázích záběru (entry, pull, push, recovery), úhel kolene při kopu, polohu těla ve vodě (body alignment) a frekvenci/délku záběru. Většina těchto metrik se nejspolehlivěji měří z **bočního pohledu** (side-view, kamera kolmo na dráhu).

**Co potřebuji:**

- **Styl**: Kraul (freestyle) — priorita číslo 1
- **Pohled kamery**: Side-view (boční, kolmo na dráhu) — MUST-HAVE. Front-view nebo underwater jako bonus.
- **Rozlišení**: Min. HD (1280×720), ideálně FHD. Plavec by měl zabírat aspoň čtvrtinu šířky záběru — jinak klouby nemají dostatek pixelů pro detekci.
- **FPS**: Min. 30 FPS. Při vyšším SR (u dětí 46–56 cyklů/min) je jeden cyklus jen 1–1.3 sekundy → při 30 FPS je to 32–39 snímků na cyklus, z čehož nejkratší fáze záběru má jen 3–5 snímků. 60 FPS by výrazně pomohlo.
- **Rozsah**: Min. 10 kompletních záběrových cyklů na plavce (~30s plavání)

**Proč hledám i dětské plavce (8–14 let):**
V celé biomechanické literatuře existuje prakticky jedno jediné měření kloubových úhlů u dětí při kraulu — vzorek 11 dětí. To je příliš málo na spolehlivé referenční hodnoty. Frekvence záběru dětí je výrazně vyšší než u dospělých (46–56 vs. 30–50 cyklů/min) a variabilita pohybu je zásadně větší — referenční šablony z dospělých dat na děti nefungují. Bez reálných dětských záběrů nemůžu kategorii Dítě v systému validovat.

**K čemu data použiju:**

Model trénuji na syntetickém datasetu (počítačem generovaní plavci). Data od vás použiji k **validaci** — ověření, že systém správně detekuje techniku i na reálných záběrech. Čím více různých plavců, tím spolehlivější validace — každý plavec je nezávislý vzorek.

**Konkrétní otázky:**

1. Kolik plavců přibližně máte v databázi?
2. Zahrnuje i **dětské plavce** (8–14 let)?
3. Z jakých úhlů kamery jsou záběry? (boční / čelní / podvodní?)
4. Jaké je rozlišení a FPS vašich kamer?
5. Existují k videím anotace nebo hodnocení trenérem? (= ground truth pro validaci — systém říká "dropped elbow" → shoduje se to s trenérem?)

Jsem flexibilní a rád se přizpůsobím tomu, co je k dispozici. Případně bych rád přijel osobně a probral detaily.

Děkuji!

S pozdravem
Bc. Vít Vágner
FIT ČVUT v Praze
vit.vagner@memos.cz

---

### 8.2 Michaela Bátorová (VUT Brno CESA) — body pro telefonát

**Kdy**: Úterý dopoledne (domluvený hovor)
**Tel**: 732120614

**Představení**:

- Vít Vágner, FIT ČVUT, diplomka na automatickou analýzu plavecké techniky z videa
- Sám aktivně závodím v triatlonu — osobní motivace

**K čemu data použiju** (vysvětlit srozumitelně):

- Model trénuju na **syntetickém datasetu** (počítačem generovaní plavci s perfektními anotacemi) — to už mám (SwimXYZ, 11 520 videí)
- Reálná data od ní potřebuji ke **dvěma věcem**:
  1. **Referenční vzory pro děti** — "jak má vypadat správná technika dítěte". Z počítačových dat dětské vzory nelze vytvořit (SwimXYZ obsahuje jen dospělé modely). Potřebuji nahrát skutečné děti, z videí systém extrahuje pózu a vytvoří referenční šablonu.
  2. **Validace systému** — ověření, že to funguje na reálných plavcích. Systém řekne "loket o 15° níž při záběru" → shoduje se to s tím, co vidí trenér?
- Nepotřebuji tisíce videí — **stačí desítky kvalitních záběrů od různých plavců**

**Co potřebuji:**

1. **Natočit videa plavců ze dvou cílových skupin**: děti (8–14) a pokročilí dospělí (15+)
2. **Hlavně kraul**, side-view (boční pohled kolmo na dráhu) + ideálně front-view
3. **Proč děti:** V celé biomechanické literatuře existuje prakticky jediné měření kloubových úhlů u dětí při kraulu (11 dětí). Děti mají výrazně vyšší frekvenci záběru (46–56 cyklů/min vs. 30–50 u dospělých) a mnohem větší variabilitu pohybu — referenční data z dospělých jednoduše nelze použít. Bez reálných dětských záběrů nemůžu dětskou kategorii validovat.
4. **Kolik dětí:** Ideálně **8–10 dětí** (min. 5). Každé dítě je nezávislý vzorek — potřebuji dostatečnou rozmanitost, abych vytvořil spolehlivé referenční vzory a měl nezávislá data pro validaci.
5. Technicky: min. HD rozlišení, 30+ FPS, min. 10 záběrových cyklů od plavce (~30s plavání)
6. Od každého plavce potřebuji metadata: věk, pohlaví, kolik let plave, tréninková frekvence

**Co konkrétně měřím:**

- Úhel loktu při záběru (ve 4 fázích — entry, pull, push, recovery)
- Frekvenci a délku záběru
- Koordinaci paží (časový vztah mezi propulzními fázemi levé a pravé paže)
- Polohu těla ve vodě (body alignment)
- Z frontálního pohledu navíc: rotaci ramen/kyčlí a symetrii záběru

**Otázky na ni**:

- Mají underwater kameru nebo GoPro?
- Kolik úrovní plavců prochází jejich kurzy? Mají děti 8–14 let?
- Jaké je rozlišení a FPS jejich kamer?
- Jaký je jejich GDPR proces pro natáčení studentů? Mají šablonu souhlasu?
- Mají už existující záběry z kurzů?
- Byl by možný přístup k bazénu na 1–2 natáčecí sessions?
- **Mohl by trenér k videím dát stručné hodnocení techniky?** (např. "dropped elbow", "nedostatečná rotace") — slouží jako ground truth pro validaci, zda systém detekuje správné chyby

**Co můžu nabídnout**:

- **Analýzu techniky pro jejich studenty** jako protislužbu — automatický report s biomechanickými metrikami pro každého plavce (kloubové úhly, frekvence záběru, rotace trupu, porovnání s referenčními hodnotami pro danou věkovou kategorii)
- Citaci a poděkování v diplomce
- Sdílení výsledků výzkumu

**GDPR**:

- Připravím informovaný souhlas (česky)
- U dětí podpis zákonného zástupce
- Data jen pro akademický výzkum, anonymizovaná v publikacích

---

### 8.3 Dan Jurák (FTVS UK Praha, flume)

**Komu**: daniel.jurak@ftvs.cuni.cz
**Předmět**: Plavecká video data z flumu — diplomová práce FIT ČVUT (doporučení od Mgr. Macase)

Dobrý den,

jmenuji se Vít Vágner a jsem student magisterského programu na FIT ČVUT. Kontakt na Vás jsem dostal od Mgr. Macase — píši diplomovou práci na automatickou analýzu plavecké techniky z videa pomocí pose estimation a strojového učení.

Data z plaveckého flumu by pro můj výzkum byla ideální — **konstantní rychlost plavce** znamená kontrolované podmínky, což výrazně zjednodušuje porovnávání mezi plavci a eliminuje variabilitu způsobenou zrychlováním/zpomalováním. Model trénuji na syntetickém datasetu (SwimXYZ) a data z flumu bych použil k **validaci** — ověření, že systém funguje správně na reálných záběrech z profesionálního setupu. Zároveň flume typicky umožňuje boční i podvodní pohled, což pokrývá klíčové metriky:

- Z **bočního pohledu** měřím úhel loktu ve 4 fázích záběru, úhel kolene, polohu těla ve vodě, frekvenci a délku záběru
- Z **podvodního pohledu** měřím průběh tahu pod vodou (catch → pull → push) a trajektorii ruky

Konkrétně bych potřeboval:

- **Styl**: Kraul (freestyle)
- **Pohledy**: Boční (side-view) + podvodní okno — ideální kombinace
- **Rozsah**: Min. 10 záběrových cyklů na plavce (~30s plavání)
- **Rozlišení**: Min. HD (1280×720), 30+ FPS (60 FPS ideální)
- **Metadata plavců**: Věk, úroveň, kolik let plave — pokud existují
- **Trenérské hodnocení**: Pokud k záznamům existuje hodnocení od trenéra, bylo by to nesmírně cenné jako ground truth pro validaci systému

Otázky:

1. Kolik plavců přibližně máte v archívu z flumu?
2. V jakém formátu a rozlišení jsou záznamy?
3. Je flume aktuálně funkční? (Mgr. Macas zmínil, že v době jeho odpovědi nefungoval.)

Jsem připraven podepsat dohodu o nakládání s daty a Vaši práci budu citovat.

Děkuji za zvážení.

S pozdravem
Bc. Vít Vágner
FIT ČVUT v Praze
vit.vagner@memos.cz

---

### 8.4 Český svaz plaveckých sportů (přes European Aquatics)

**Komu**: ales.zenahlik@czechswimming.cz (nebo jakub.tesarek@czechswimming.cz)
**Předmět**: Video data závodních plavců — diplomová práce FIT ČVUT + European Aquatics race analysis

Dobrý den,

jmenuji se Vít Vágner a studuji na FIT ČVUT, kde píši diplomovou práci na automatickou analýzu plavecké techniky z videa. Obracím se na Vás na doporučení paní Juliany Daguano, Media Relations and Media Operations Manager v European Aquatics.

Paní Daguano mi potvrdila, že **European Aquatics poskytuje národním federacím zdarma přístup k race analysis záběrům** ze svých soutěží — stahují se přes link sdílený na Team Leaders meetingu. Rád bych se zeptal:

1. **Využívá Český svaz tuto službu?** Pokud ano, bylo by možné získat přístup k části těchto záběrů pro akademický výzkum?
2. **Disponuje svaz vlastními záznamy** z tréninků SCM nebo z kvalifikačních závodů?

**Co konkrétně potřebuji a k čemu:** Závodní záběry kraulistů z bočního pohledu (side-view). Model trénuji na syntetickém datasetu — závodní záběry od vás poslouží k **validaci na kompetitivní úrovni plavců** (ověření, že systém správně detekuje techniku i u závodních plavců). Z těchto záběrů systém měří úhly kloubů, frekvenci záběru a koordinaci paží. Ideálně HD rozlišení, 30+ FPS.

Jsem připraven podepsat dohodu o nakládání s daty. Sám aktivně závodím v triatlonu, takže je to pro mě i osobní téma.

Děkuji za odpověď.

S pozdravem
Bc. Vít Vágner
FIT ČVUT v Praze
vit.vagner@memos.cz

---

### 8.5 Hannah Jowitt (Aquatics GB / Loughborough)

**Komu**: hannah.jowitt@aquaticsgb.com
**Subject**: Swimming video data for academic research — master's thesis (referred by Prof. Mark King)

Dear Ms. Jowitt,

My name is Vít Vágner and I am a master's student in Software Engineering at the Czech Technical University in Prague. Professor Mark King at Loughborough University kindly directed me to you.

I am writing my thesis on automated swimming technique analysis from video. The system uses pose estimation models to extract body keypoints from video and then computes biomechanical metrics — specifically trunk rotation (shoulder roll typically 60–110° total range), elbow angle across all four stroke phases, and inter-arm coordination timing. These metrics are compared against reference templates to detect technique errors automatically.

**Why real-world data is critical:** My model is trained on synthetic data (SwimXYZ dataset — computer-generated swimmers with perfect keypoint annotations). I need real-world data for **validation and testing** — to verify that the system works correctly on real swimmers in real pool conditions. Real pool environments introduce noise that synthetic data cannot replicate — water surface reflections, refraction effects underwater, partial occlusions by lane ropes and splash. Your multi-camera setup would also allow me to validate how the system generalises across different camera angles. Without real-world validation data, I cannot reliably quantify how well the system performs in practice.

**What I would need:**

- **Stroke**: Freestyle (front crawl) — primary interest
- **Camera angles**: Side-view (for joint angles, stroke rate, body alignment) and underwater (for pull-through analysis). Your 10-camera setup with 4 underwater cameras would be ideal.
- **Skill levels**: Various levels — from recreational to competitive swimmers
- **Technical specs**: Min. HD resolution (1280×720), 30+ FPS
- **Volume**: At least 10 complete stroke cycles per swimmer (~30 seconds)
- **Coach assessments** (if available): Any qualitative evaluation of technique would serve as ground truth for validation

Even a small subset of recordings would be extremely valuable.

I would be happy to:

- Sign a formal data sharing agreement
- Cite Loughborough/Aquatics GB in my thesis
- Share results of my analysis

Could you advise whether academic data access might be possible, and what the appropriate next steps would be?

Thank you for your time.

Best regards,
Bc. Vít Vágner
Faculty of Information Technology
Czech Technical University in Prague
vit.vagner@memos.cz
