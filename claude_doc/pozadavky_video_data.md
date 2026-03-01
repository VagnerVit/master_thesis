# Požadavky na video data — SwimAth

**Účel**: Specifikace požadovaných video dat pro diplomovou práci SwimAth.
**Aktualizováno**: 2026-03-01

---

## 1. Čtyři účely videí v projektu

### A) Fine-tuning pose estimation (balík B2)

| | |
|---|---|
| **Účel** | Naučit ViTPose/RTMPose rozpoznávat klíčové body na plavcích |
| **Potřebuje** | Videa s anotacemi keypointů (nebo semi-supervised přístup) |
| **SwimXYZ pokryje?** | ✅ ANO — syntetická data s perfektními anotacemi, 48 keypointů |
| **Reálná data** | Malý validační set (~100–200 ručně anotovaných framů) |
| **Závěr** | Primárně SwimXYZ, doplnit malým reálným setem pro cross-domain evaluaci |

### B) Referenční šablony DTW (balík C2)

| | |
|---|---|
| **Účel** | Vytvořit "ideální" vzor záběru pro každou úroveň |
| **Požadavek** | 1 styl (kraul) × 3 pohledy × 3 úrovně = **9 šablon** |
| **Na šablonu** | Min. 3–5 plavců dané úrovně, 5–10 čistých záběrových cyklů od každého |
| **SwimXYZ pokryje?** | ČÁSTEČNĚ — dospělí (Plavec, Kompetitivní). Děti NE. |
| **Reálná data** | **NUTNÉ** pro kategorii Dítě (8–14 let). Ideálně i validace ostatních úrovní. |

### C) Validace pipeline (balík E1)

| | |
|---|---|
| **Účel** | Otestovat celý pipeline na reálných videích, porovnat s hodnocením trenéra |
| **Požadavek** | Videa plavců RŮZNÝCH úrovní, NEZÁVISLÁ na trénovacích/šablonových datech |
| **Ground truth** | Hodnocení od kvalifikovaného trenéra |
| **SwimXYZ pokryje?** | ❌ NE — validace musí být na reálných datech |
| **Reálná data** | **NUTNÉ** — toto je hlavní blocker |

### D) Benchmark pose estimation modelů (balík B1)

| | |
|---|---|
| **Účel** | Porovnat MediaPipe vs RTMPose vs ViTPose na plaveckých datech |
| **Požadavek** | Společný dataset s ground truth anotacemi |
| **SwimXYZ pokryje?** | ✅ ANO pro syntetický benchmark |
| **Reálná data** | Ideálně malý reálný set pro real-world benchmark |

---

## 2. Technické požadavky — podloženo literaturou a pipeline analýzou

### 2.1 Rozlišení

**Požadavek: min. 720p (1280×720), ideálně FHD (1920×1080)**

Zdůvodnění:
- Pipeline interně resizuje na 224×224 px pro inference (`video_processor.py:target_size`), ale vstupní rozlišení ovlivňuje kvalitu detekce keypointů — vyšší rozlišení = přesnější lokalizace kloubů před resizem
- MediaPipe `model_complexity=2` (nejvyšší přesnost) profituje z vyššího vstupního rozlišení
- Confidence threshold 0.7 (`mediapipe_config.py`) — při nižším rozlišení více framů padne pod práh → ztráta dat
- **Plavec musí zabírat ≥25% šířky snímku** — jinak klouby < 10 px při 720p → pod rozlišovací schopností PE modelů
- Srovnání s literaturou: SwimTrack-v1 (MediaEval 2022) používá HD–4K, 25–50 FPS; Augsburg Swimming Channel pořizuje záběry přes profesionální high-sequence kamery
- **720p je pragmatický kompromis** pro data od institucí, která nemusí mít nejnovější vybavení

### 2.2 FPS (snímková frekvence)

**Požadavek: min. 30 FPS, ideálně 60 FPS**

Zdůvodnění z pipeline:
- Stroke rate kraul: 40–65 cycles/min (A4_metriky_prahy.md) → 1 cyklus = **0.9–1.5 s**
- Při 30 FPS = 27–45 framů na cyklus; při 60 FPS = 54–90 framů
- `stroke_analyzer.py`: `min_cycle_frames=20` — při 25 FPS a SR=65: 25×(60/65) = 23 framů — **těsně nad limitem**, nespolehlivé
- Butterworth low-pass filter cutoff ~6 Hz (A4_metriky_prahy.md sekce 10.4) → Nyquist: potřeba min. 12 FPS, pro kvalitní filtrování 4× = **24+ FPS**
- **Fázová analýza**: žádná fáze nemá trvat < 5% cyklu → při 30 FPS a cyklu 30 framů = 1.5 framu minimum → hraniční pro spolehlivou detekci fází
- DTW Sakoe-Chiba band r ≈ 15% délky cyklu → vyšší FPS = jemnější granularita warpingu
- **Závěr**: 30 FPS je absolutní minimum. 60 FPS výrazně zlepšuje fázovou analýzu, DTW přesnost a filtrování šumu.

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

### 2.5 Formát a kodek

- **MP4 (H.264/H.265)** — standardní, plná kompatibilita s OpenCV `cv2.VideoCapture`
- Alternativy: AVI, MOV — taky OK, OpenCV je přečte
- **Důležité**: konstantní FPS (ne variable frame rate z mobilů!) — jinak frame skipping v `video_processor.py` nefunguje správně

---

## 3. Metriky podle pohledu kamery

Které biomechanické metriky lze spolehlivě měřit z jakého pohledu (zdroj: A4_metriky_prahy.md):

| Pohled | Spolehlivé metriky | Problematické | Nedostupné |
|--------|-------------------|---------------|------------|
| **Side** | Elbow angle (entry/catch/pull/push), knee angle, hip angle, body alignment, SR, SL | Shoulder roll (jen vertikální posuv, ne skutečný úhel) | L/R asymetrie, hand entry crossover |
| **Front** | Shoulder roll, hip roll, L/R asymetrie, hand entry crossover/width | Elbow angle (v koronální rovině, ne sagitální) | Knee angle sagitální, body alignment (hloubka) |
| **Underwater** | Elbow angle (pull-through), hand path trajectory | Knee angle | Body roll (refrakce zkresluje), SR (bubliny překrývají) |

**→ Side-view je nejuniverzálnější** — pokrývá nejvíc klíčových metrik. Proto MUST-HAVE.
**→ Front-view doplňuje** rotační metriky a symetrii. SHOULD-HAVE.
**→ Underwater** je cenný pro pull-through analýzu, ale obtížně získatelný. NICE-TO-HAVE.

---

## 4. Kategorie plavců a minimální počty

| Úroveň | Věk | Popis | Min. plavců | Účel | SR range |
|---------|-----|-------|-------------|------|----------|
| **Dítě** | 8–14 | Plavecký kurz nebo dětský oddíl | 5–8 | Šablony + validace | 40–65 c/min |
| **Plavec** | 15+ | Rekreační/fitness plavec, zvládá kraul | 5–8 | Validace | 30–50 c/min |
| **Kompetitivní** | 15+ | Závodní plavec, trenér, triatlonista | 5–8 | Validace | 35–65 c/min |

**Celkem: min. 15–24 plavců**

### Co natočit od každého plavce

1. **Side-view kraul**: min. 10 kompletních záběrových cyklů (~30s plavání)
2. **Front-view kraul** (pokud dostupné): min. 10 cyklů
3. **Underwater kraul** (pokud dostupné): min. 5 cyklů
4. **Metadata formulář**: věk, pohlaví, kolik let plave, tréninková frekvence, závodní úroveň, výška, rozpětí paží
5. **GDPR souhlas**: podpis informovaného souhlasu (u dětí zákonný zástupce)

### Podmínky nahrávání

| Parametr | Požadavek | Poznámka |
|----------|-----------|----------|
| **Bazén** | 25m nebo 50m | Čistá voda (průhlednost pro underwater) |
| **Oblečení** | Plavky (ne triko), kontrastní barva k vodě | Pro viditelnost keypoints |
| **Plavecká čepice** | Ano | Pomáhá PE rozlišit hlavu od vody |
| **Osvětlení** | Rovnoměrné, bez silných odlesků na hladině | Odrazy zhoršují detekci |
| **Stativ** | Pevný, bez vibrací | Pohyb kamery znehodnotí data |

---

## 5. SwimXYZ vs. reálná data

| Účel | SwimXYZ | Reálná data |
|------|---------|-------------|
| PE fine-tuning (B2) | ✅ Primární zdroj (48 kp, perfektní GT) | Malý validační set (~100–200 framů) |
| PE benchmark (B1) | ✅ Syntetický benchmark | Malý reálný benchmark (~50 framů s ručními anotacemi) |
| Šablony Dítě (C2) | ❌ Neobsahuje děti (jen dospělé SMPL modely) | **NUTNÉ — 5–8 dětí** |
| Šablony Plavec (C2) | ✅ Lze generovat | Validační porovnání |
| Šablony Kompetitivní (C2) | ✅ Lze generovat | Validační porovnání |
| Validace pipeline (E1) | ❌ Nelze | **NUTNÉ — 15–24 plavců** |
| Ground truth trenér (E1) | ❌ | **NUTNÉ — hodnocení trenérem** |

**SwimXYZ pohledy kamery** (5 typů): Aerial, Front, Side_above_water, Side_underwater, Side_water_level — pokrývají side + front + underwater, ale jsou syntetické (žádný šum z reálného PE).

**Domain gap**: Model trénovaný na SwimXYZ se učí "čisté" pohyby bez šumu PE → při nasazení na reálná data očekávat pokles accuracy. Proto je cross-domain validace na reálných datech klíčová.

---

## 6. Akční kroky pro kontakty (aktualizováno dle odpovědí 2026-03-01)

### David Prycl / BALUO (UP Olomouc) — PRIORITA 1 ✅ odpověděl

- **Stav**: Kontaktoval kolegu s databází videí, ochoten poskytnout. Ukázka: youtube.com/watch?v=ijmb06JR74o
- **Akce**: ✉️ Odpovědět s konkrétní specifikací (viz sekce 7.1)
- **Ptát se na**: Kolik plavců? Jaké úrovně (děti?)? Formát/rozlišení? Úhly kamery? Anotace?

### Michaela Bátorová (VUT Brno CESA) — PRIORITA 1 ✅ odpověděla

- **Stav**: Nabízí telefonát v úterý dopoledne
- **Akce**: ☎️ Zavolat, body viz sekce 7.2
- **Klíčové**: Garant vodních sportů, plavecké kurzy — potenciál pro dětské plavce!

### Dan Jurák (FTVS UK Praha, flume) — PRIORITA 1 (přes Macase)

- **Stav**: Macas přesměroval, dal Juráka do CC. Jurák má videozáznamy z flumu.
- **Akce**: ✉️ Napsat přímo Jurákovi (viz sekce 7.3)
- **Klíčové**: Flume s underwater oknem — kontrolované podmínky, ideální pro side + underwater

### ČSPS — Český svaz plaveckých sportů — PRIORITA 2 (nová cesta přes EA)

- **Stav**: Juliana Daguano (European Aquatics) potvrdila — race analysis footage zdarma pro federace
- **Akce**: ✉️ Napsat ČSPS s odkazem na Daguano (viz sekce 7.4)
- **Klíčové**: Závodní záběry kompetitivních plavců

### Hannah Jowitt (Aquatics GB) — PRIORITA 3 (přes Kinga)

- **Stav**: Mark King (Loughborough) přesměroval
- **Akce**: ✉️ Napsat Hannah Jowitt (viz sekce 7.5)
- **Klíčové**: 10 kamer (4 underwater), profesionální setup

### Vlastní natáčení — ZÁLOŽNÍ PLÁN

- Vít + 2–3 známí triatlonisté/plavci, místní bazén
- Telefon na stativu (side + front), GoPro pro underwater
- Pokryje: Plavec + Kompetitivní. **Nepokryje: Dítě.**

---

## 7. Prioritizace

### Must-have (bez toho diplomka není obhajitelná)

1. **15+ reálných videí plavců** (side-view kraul, různé úrovně) pro validaci
2. **5+ dětských plavců** pro kategorii Dítě (šablony + validace)
3. **Hodnocení trenérem** alespoň u 10 plavců (ground truth)
4. **Side-view** jako primární pohled kamery

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

## 8. GDPR a etické aspekty

- **Informovaný souhlas** od každého natáčeného plavce (u dětí zákonný zástupce)
- **Účel**: zpracování v rámci diplomové práce, akademický výzkum
- **Anonymizace**: v publikovaných výsledcích bez identifikace osob
- **Uložení**: lokální, ne veřejně dostupné
- **Šablonu souhlasu** připravit předem (česky)
- **Schválení etickou komisí** — ověřit, zda ČVUT vyžaduje pro tento typ výzkumu

---

## 9. Draft emaily a příprava na hovory

### 9.1 David Prycl / BALUO (odpověď na jeho nabídku)

**Komu**: david.prycl@upol.cz
**Předmět**: Re: Žádost o plavecká video data — diplomová práce FIT ČVUT

Zdravím, Davide,

moc děkuji za ochotu a za ukázkové video! Rád bych upřesnil, co přesně potřebuji:

**Styl**: Primárně kraul (freestyle) — případně i další styly, ale kraul je priorita.

**Úhly kamery**: Ideálně side-view (boční pohled kolmo na dráhu), případně i front-view nebo underwater.

**Úrovně plavců**: Potřebuji pokrýt různé výkonnostní úrovně:
- Děti (8–14 let) — začátečníci nebo mírně pokročilí
- Rekreační/fitness plavci (dospělí)
- Závodní plavci / pokročilí

Čím větší škála úrovní, tím lépe — porovnávám techniku s referenčními vzory.

**Technické parametry**: Nejlepší by bylo rozlišení min. HD (1280×720), ideálně FHD, a 30+ FPS (60 FPS ideální). Ale rád bych viděl, co máte — i nižší rozlišení může být užitečné.

**Rozsah**: Od každého plavce ideálně alespoň 10 kompletních záběrových cyklů (cca 30 sekund plavání).

**Metadata**: Pokud k videím existují informace o plavci (věk, úroveň, kolik let plave), bylo by to velmi cenné.

Mám několik konkrétních otázek:
1. Kolik plavců přibližně máte v databázi?
2. Zahrnuje i dětské plavce?
3. Z jakých úhlů kamery jsou záběry pořízené?
4. Existují k videím nějaké anotace (keypointy, hodnocení trenérem)?

Jsem flexibilní a rád se přizpůsobím tomu, co je k dispozici. Případně bych rád přijel osobně a probral detaily.

Děkuji!

S pozdravem
Bc. Vít Vágner
FIT ČVUT v Praze
vit.vagner@memos.cz

---

### 9.2 Michaela Bátorová (VUT Brno CESA) — body pro telefonát

**Kdy**: Úterý dopoledne (domluvený hovor)
**Tel**: 732120614

**Představení**:
- Vít Vágner, FIT ČVUT, diplomka na automatickou analýzu plavecké techniky z videa
- Sám aktivně závodím v triatlonu — osobní motivace

**Co potřebuji**:
1. **Natočit videa plavců různých úrovní** — hlavně kraul, side-view + ideálně front-view
2. **Zejména děti (8–14 let)** — to je kategorie, kterou nemám jak pokrýt syntetickými daty
3. Technicky: min. HD rozlišení, 30+ FPS, min. 10 záběrových cyklů od plavce (~30s plavání)
4. Od každého plavce potřebuji i základní metadata (věk, úroveň, kolik let plave)

**Otázky na ni**:
- Mají underwater kameru nebo GoPro?
- Kolik úrovní plavců prochází jejich kurzy? (děti, dospělí začátečníci, pokročilí?)
- Jaký je jejich GDPR proces pro natáčení studentů? Mají šablonu souhlasu?
- Mají už existující záběry z kurzů?
- Byl by možný přístup k bazénu na 1–2 natáčecí sessions?

**Co můžu nabídnout**:
- Analýzu techniky pro jejich studenty jako protislužbu (výstup z mé aplikace)
- Citaci a poděkování v diplomce
- Sdílení výsledků výzkumu

**GDPR**:
- Připravím informovaný souhlas (česky)
- U dětí podpis zákonného zástupce
- Data jen pro akademický výzkum, anonymizovaná v publikacích

---

### 9.3 Dan Jurák (FTVS UK Praha, flume)

**Komu**: daniel.jurak@ftvs.cuni.cz
**Předmět**: Plavecká video data z flumu — diplomová práce FIT ČVUT (doporučení od Mgr. Macase)

Dobrý den,

jmenuji se Vít Vágner a jsem student magisterského programu na FIT ČVUT. Kontakt na Vás jsem dostal od Mgr. Macase — píši diplomovou práci na automatickou analýzu plavecké techniky z videa pomocí pose estimation a strojového učení.

Rád bych se zeptal, zda by bylo možné získat přístup k existujícím videozáznamům plavců pro výzkumné účely. Konkrétně bych potřeboval:

- **Styl**: Kraul (freestyle) — primární zájem
- **Pohledy**: Boční pohled (side-view), ideálně i z podvodního okna
- **Úrovně**: Různé výkonnostní úrovně — od rekreačních po závodní plavce
- **Rozsah**: Min. 10 záběrových cyklů od plavce (cca 30s plavání)
- **Rozlišení**: Min. HD (1280×720), 30+ FPS

Pár otázek:
1. Kolik plavců přibližně máte v archívu?
2. V jakém formátu a rozlišení jsou záznamy?
3. Existují k nim anotace nebo hodnocení od trenéra?

Jsem připraven podepsat dohodu o nakládání s daty a Vaši práci budu citovat.

Děkuji za zvážení.

S pozdravem
Bc. Vít Vágner
FIT ČVUT v Praze
vit.vagner@memos.cz

---

### 9.4 Český svaz plaveckých sportů (přes European Aquatics)

**Komu**: ales.zenahlik@czechswimming.cz (nebo jakub.tesarek@czechswimming.cz)
**Předmět**: Video data závodních plavců — diplomová práce FIT ČVUT + European Aquatics race analysis

Dobrý den,

jmenuji se Vít Vágner a studuji na FIT ČVUT, kde píši diplomovou práci na automatickou analýzu plavecké techniky z videa. Obracím se na Vás na doporučení paní Juliany Daguano, Media Relations Manager v European Aquatics.

Paní Daguano mi potvrdila, že European Aquatics poskytuje národním federacím zdarma přístup k race analysis záběrům ze svých soutěží (stahují přes link sdílený na Team Leaders meetingu). Rád bych se zeptal:

1. **Využívá Český svaz tuto službu?** Pokud ano, bylo by možné získat přístup k části těchto záběrů pro akademický výzkum?
2. **Disponuje svaz vlastními záznamy** z tréninků SCM nebo z kvalifikačních závodů, které by bylo možné poskytnout?

Pro mou diplomku potřebuji HD záběry závodních plavců (kraul, side-view nebo underwater), abych mohl validovat systém automatické analýzy techniky.

Jsem připraven podepsat dohodu o nakládání s daty. Sám aktivně závodím v triatlonu, takže je to pro mě i osobní téma.

Děkuji za odpověď.

S pozdravem
Bc. Vít Vágner
FIT ČVUT v Praze
vit.vagner@memos.cz

---

### 9.5 Hannah Jowitt (Aquatics GB / Loughborough)

**Komu**: hannah.jowitt@aquaticsgb.com
**Subject**: Swimming video data for academic research — master's thesis (referred by Prof. Mark King)

Dear Ms. Jowitt,

My name is Vít Vágner and I am a master's student in Software Engineering at the Czech Technical University in Prague. Professor Mark King at Loughborough University kindly directed me to you.

I am writing my thesis on automated swimming technique analysis from video using pose estimation and machine learning. I am looking for real-world swimming video data to validate my pipeline.

Specifically, I would need:
- **Stroke**: Freestyle (front crawl) — primary interest
- **Camera angles**: Side-view, and ideally underwater footage
- **Skill levels**: Various levels from recreational to competitive swimmers
- **Technical specs**: Min. HD resolution (1280×720), 30+ FPS
- **Volume**: At least 10 complete stroke cycles per swimmer (~30 seconds of swimming)

I understand Loughborough's National Centre for Swimming operates a multi-camera setup (including 4 underwater cameras). Even a small subset of recordings would be extremely valuable for my research.

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
