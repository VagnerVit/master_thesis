# Datasety a kontakty pro SwimAth

**Stav**: 2026-03-02 (aktualizováno — nové 2 kategorie plavců)
**Cíl**: Získat reálná plavecká video data pro diplomku (syntetický SwimXYZ nestačí)

### Cílové kategorie plavců (aktualizováno 2026-03-02)

| Kategorie     | Věk  | Popis                                              | Min. plavců | Status dat                       |
| ------------- | ---- | -------------------------------------------------- | ----------- | -------------------------------- |
| **Dítě**      | 8–14 | Plavecký kurz, dětský oddíl                        | 5           | ❌ Nemáme — hlavní blocker        |
| **Pokročilý** | 15+  | Od rekreačních po závodní (triatlonisté, oddíloví) | 8–10        | ⚠️ Částečně (SwimXYZ syntetický) |

> Kategorie „Profesionál" = budoucí rozšíření, neimplementujeme v diplomce.

---

## Stávající datasety

| Dataset                       | Typ                              | Status            |
| ----------------------------- | -------------------------------- | ----------------- |
| **SwimXYZ**                   | Syntetický, 11520 videí, 4 styly | ✅ Staženo         |
| **Augsburg Swimming Channel** | Reálný, 4 styly                  | ❌ Zamítnuto (NDA) |
| **SwimmerNET**                | Reálný podvodní, kraul           | ⏳ Bez odpovědi    |

---

## ČR — Prioritní kontakty

### 1. Jan Šťastný — VUT Brno CESA

- **Pozice**: Biomechanics team lead, swimming research
- **Email**: Jan.Stastny@vut.cz
- **Tel**: +420 541 149 587
- **Web**: [cesa.vut.cz](https://www.cesa.vut.cz/)
- **ResearchGate**: [researchgate.net/profile/Jan-Stastny](https://www.researchgate.net/profile/Jan-Stastny)
- **ORCID**: 0000-0001-8058-4568
- **Proč**: 3 synchronizované podvodní kamery, data české reprezentace od 2009, IMU senzory, vlastní tachograf. Aktivní výzkum kinematiky záběrů.
- **Publikace**: "Kinematic and dynamic analysis of swimming technique of Czech national team 2009-2015", case study s IMU (2017)
- **📧 Status**: Odesláno 2026-02-21, ⏳ bez odpovědi
- **Co od něj potřebujeme**:
  - Side-view + underwater video kraul, závodní plavci (Pokročilý)
  - Podvodní záběry z 3 synchronizovaných kamer — pull-through analýza
  - Metadata plavců a ideálně trenérské hodnocení (ground truth)
  - Min. HD/30 FPS, 10+ cyklů na plavce

### 2. Michaela Bátorová — VUT Brno CESA — ✅ ODPOVĚDĚLA

- **Pozice**: Mgr. et. Mgr., Ph.D. — vyučující sportovních technologií, garant vodních sportů, veslování a netradičních her
- **Email**: Michaela.Batorova@vut.cz
- **Tel**: 732120614, +420 54114 9585
- **Centrum sportovních aktivit**, VUT v Brně, Kolejní 2, 612 00 Brno
- **Pokrývá kategorie**: 🧒 **Dítě** (plavecké kurzy!) + možná Pokročilý
- **📧 Odpověď (2026-02)**: Nabízí zavolat v úterý dopoledne — diskuze o možnostech spolupráce
- **Akce**: ☎️ Zavolat, připravit body (viz pozadavky_video_data.md sekce 8.2)
- **Co od ní konkrétně potřebujeme**:
  - **Hlavně dětské plavce (8–14 let)** — side-view kraul, min. 5 dětí, 10+ cyklů na plavce
  - Přístup k bazénu na 1–2 natáčecí sessions
  - Metadata: věk, pohlaví, kolik let plave
  - Existující záběry z kurzů (pokud mají)
  - GDPR proces pro natáčení dětí

### 3. FTVS UK Praha — Katedra plaveckých sportů — ✅ ODPOVĚDĚL (Macas → Jurák)

- **Email katedry**: ~~kps@ftvs.cuni.cz~~ (nefunguje, katedra přejmenována 2022)
- **Tel**: 22017 2020
- **Vedoucí**: Mgr. Tomáš Macas, Ph.D. (tomas.macas@ftvs.cuni.cz)
- **Plavecká sekce**: Mgr. Daniel Jurák, Ph.D. (daniel.jurak@ftvs.cuni.cz)
- **Web**: [ftvs.cuni.cz/FTVS-592.html](https://ftvs.cuni.cz/FTVS-592.html)
- **Proč**: Plavecký flume (6m, proud 0.5-2.5 m/s), podvodní pozorovací okno 3m, Dartfish software, underwater cameras. Diagnostika pro závodní plavce.
- **Pokrývá kategorie**: 🏊 **Pokročilý** (závodní plavci z flumu)
- **📧 Odpověď Macase (2026-02)**: Plavání neučí, flume bohužel nefunguje. Přesměroval na Dana Juráka — ten má videozáznamy z flumu. V kopii dal Juráka.
- **Akce**: ✉️ Napsat přímo Jurákovi (daniel.jurak@ftvs.cuni.cz) — zmínit přesměrování od Macase (viz pozadavky_video_data.md sekce 8.3)
- **Co od něj konkrétně potřebujeme**:
  - Side-view + podvodní záběry kraul z flumu (kontrolované podmínky = konstantní rychlost)
  - Pokročilí/závodní plavci
  - Metadata plavců + trenérské hodnocení (ground truth)
  - Min. HD/30 FPS, 10+ cyklů na plavce

### 4. BALUO — FTK UPOL Olomouc — ✅ ODPOVĚDĚL (Prycl)

- **Kontakt**: David Prycl, business development manager
- **Email**: david.prycl@upol.cz
- **Tel**: +420 775 111 781
- **Web**: [acbaluo.cz](https://www.acbaluo.cz/), [testbal.cz](https://www.testbal.cz/)
- **Proč**: Testovací bazén s kamerovým systémem, high-sequence kamery, centrum kinantropologického výzkumu.
- **Pokrývá kategorie**: 🏊 **Pokročilý** (+ otázka: mají i děti?)
- **📧 Odpověď (2026-02)**: Kontaktoval kolegu, který má databázi videí a je ochoten je poskytnout. Posílá ukázkové video: https://www.youtube.com/watch?v=ijmb06JR74o
- **Akce**: ✉️ Odpovědět s konkrétní specifikací požadovaných záběrů (viz pozadavky_video_data.md sekce 8.1)
- **Co od něj konkrétně potřebujeme**:
  - Side-view kraul, min. HD/30 FPS (60 FPS ideální), 10+ cyklů na plavce
  - Pokročilí dospělí plavci — hlavní přínos
  - **Otázka: mají i dětské plavce?** — klíčová informace
  - Metadata plavců (věk, úroveň)
  - Anotace/hodnocení trenérem (pokud existují)

### 5. ČSPS — Český svaz plaveckých sportů

- **Metodik**: Aleš Zenáhlík (ales.zenahlik@czechswimming.cz, +420 732 131 488)
- **Generální sekretář**: Jakub Tesárek (jakub.tesarek@czechswimming.cz, +420 725 560 436)
- **Web**: [czechswimming.cz](https://www.czechswimming.cz/)
- **Metodika**: [metodika.czechswimming.cz](https://metodika.czechswimming.cz/)
- **Proč**: Brána ke SCM datům, metodická videa, spolupráce s kluby.
- **📧 Status Zenáhlík**: Odesláno 2026-02-21, ⏳ bez odpovědi
- **Nová cesta**: European Aquatics (Juliana Daguano) doporučuje kontaktovat ČSPS — race analysis footage je zdarma pro národní federace
- **Akce**: ✉️ Napsat znovu ČSPS, zmínit doporučení od Daguano (viz pozadavky_video_data.md sekce 8.4)
- **Co od nich konkrétně potřebujeme**:
  - Závodní záběry kraulistů z bočního pohledu (race analysis footage od European Aquatics)
  - HD rozlišení, 30+ FPS
  - Závodní plavci = validace na kompetitivní úrovni

### 5. FSpS MUNI Brno

- **Vedoucí katedry atletiky/plavání**: doc. PaedDr. Jan Ondráček, Ph.D. (jan.ondracek@muni.cz)
- **Web**: [fsps.muni.cz/sportlab](https://www.fsps.muni.cz/sportlab)
- **Proč**: Simi Motion (8 high-speed kamer, 100 Hz). Spíše obecná sportovní diagnostika, ale potenciál pro spolupráci.

### 6. Element Swimming (komerční)

- **Email**: elementswimming@gmail.com
- **Tel**: +420 725 956 042
- **Web**: [elementswimming.cz](https://www.elementswimming.cz/)
- **Zakladatel**: Dominik Vavrečka
- **Proč**: Profesionální podvodní video analýza (Praha, Brno, Ostrava, Olomouc). Cena 2499-2999 Kč/session. Mohli by poskytnout anonymizovaná data za spolupráci.

### 7. Plavecké kluby

- **USK Praha**: info@uskplavani.cz, +420 775 949 690 — video trénink, bazén Podolí
- **Kometa Brno**: plavani@kometaplavani.cz, +420 541 247 731 — největší klub v ČR

---

## EU — Datasety k získání

### 1. SWIM-360 — University of Malta (NEJVYŠŠÍ priorita)

- **Lead**: Dr. Vanessa Camilleri
- **Web**: [swim-360.eu](https://swim-360.eu/)
- **Paper**: [Sensors 2025](https://www.mdpi.com/1424-8220/25/22/7047)
- **Proč**: Aktivně staví multimodální dataset (video + MediaPipe + IMU), 2024-2026, budget 200k EUR. Explicitně hledají spolupráci a chtějí data sdílet.
- **Akce**: Kontaktovat přes swim-360.eu, nabídnout spolupráci.

### 2. SwimTrack / SportsVideo — MediaEval

- **SwimTrack**: [HAL](https://hal.science/hal-03936053v1) (MediaEval 2022) — reálné závodní video, stroke rate detection
- **SportsVideo**: [HAL](https://hal.science/hal-04490839) (MediaEval 2023) — rozšíření SwimTrack, position detection
- **Lab**: LIRIS, Université Claude Bernard Lyon 1 / INSA Lyon
- **Akce**: Kontaktovat autory přes HAL, požádat o přístup jako challenge participant.

### 3. PLOS One HSD dataset

- **Paper**: [PLOS One 2024](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0337577)
- **Data**: Podvodní video, 480 plavců, 4 styly, věk 14-38
- **Proč**: PLOS policy mandátně vyžaduje sdílení dat. Čínská instituce.
- **Akce**: Email corresponding author s odkazem na PLOS data availability policy.

### 4. Loughborough University — National Centre for Swimming (UK) — ✅ ODPOVĚDĚL (King → Jowitt)

- **Web**: [lboro.ac.uk/microsites/ssehs/biomechanics/](https://www.lboro.ac.uk/microsites/ssehs/biomechanics/)
- **Data**: 10 synchronizovaných kamer (4 podvodní, 4 overhead), Vicon MoCap
- **Spolupráce**: British Swimming (Aquatics GB), Intel
- **Proč**: Technicky nejschopnější swimming lab v Evropě.
- **📧 Odpověď Mark King (2026-02)**: Přesměroval na Hannah Jowitt (hannah.jowitt@aquaticsgb.com). CC Fred Yeadon (M.R.Yeadon@lboro.ac.uk).
- **Akce**: ✉️ Napsat Hannah Jowitt (viz pozadavky_video_data.md sekce 8.5)
- **Co od nich konkrétně potřebujeme**:
  - Side-view + underwater video kraul z multi-camera setupu (10 kamer, 4 podvodní)
  - Různé úrovně plavců (recreational → competitive)
  - HD/30+ FPS, 10+ cyklů na plavce
  - Trenérské hodnocení (ground truth)
  - Klíčové pro validaci domain gap: syntetická → reálná data

### 5. IAT Leipzig (Německo)

- **Web**: [sport-iat.de](https://sport-iat.de/allgemeines)
- **BMS databáze**: [iat.uni-leipzig.de](https://www.iat.uni-leipzig.de/service/datenbanken/biomechanics-medicine-in-swimming) — 1266 článků, open access
- **Kontakt**: loew@iat.uni-leipzig.de
- **Proč**: Zdroj Augsburg dat (swimming channel). Německý ekvivalent INSEP.
- **Akce**: Formální akademický dopis.

### 6. DSHS Cologne (Deutsche Sporthochschule Köln)

- **Web**: [dshs-koeln.de](https://www.dshs-koeln.de/en/)
- **Výzkumný portál**: [fis.dshs-koeln.de](https://fis.dshs-koeln.de/en)
- **Proč**: 50m bazén, 19 vědeckých institutů, host BMS symposia.
- **Akce**: Hledat konkrétní výzkumníky přes portál.

### 7. INSEP — Francie

- **Email**: via [insep.fr/en/contacter](https://www.insep.fr/en/contacter)
- **Proč**: Francouzský národní sportovní institut, spolupráce s FFN.

### 8. INRIA NePTUNE — IMU data

- **Paper**: [Sensors 2022](https://www.mdpi.com/1424-8220/22/15/5786)
- **Data**: IMU, 35 plavců (resp. 91 v pozdějším paperu), 4 styly
- **Proč**: Ne video, ale čistá annotovaná IMU data. Doplněk k video analýze.

### 9. Cao & Yan — Massey University (NZ)

- **Paper**: [Springer 2024](https://link.springer.com/article/10.1007/s11042-023-16618-w)
- **Data**: Podvodní video, 14-point keypoints, HRNet

---

## Mezinárodní organizace

### 1. World Aquatics (ex-FINA)

- **Communications**: torin.koos@worldaquatics.com
- **Sports dept (legacy)**: sportsdep@fina.org
- **Media pool**: [mediapool.worldaquatics.com/contact_us](https://mediapool.worldaquatics.com/contact_us)
- **Biomechanika**: Russell Mark (consultant) — seminární materiály volně na resources.fina.org
- **Hawk-Eye/Sony partnerství** (2024-2028): 4K ultra slow-motion, tracking každého plavce, eliminace slepých míst pod vodou
- **Centre of Excellence** v Bahrainu (od 10/2025): sportovní věda + elite trénink
- **WADC konference**: [wadc.sweaquatics.com](https://www.wadc.sweaquatics.com/) — networking s vědci a trenéry
- **Russell Mark Video Library**: přes ASCA membership ($109/rok) — 70+ annotovaných videí techniky

### 2. OTAB — Olympic Television Archive Bureau

- **Email**: info@otab.com
- **Tel**: +44 (0)20 8233 5353
- **Web**: [otab.com](https://www.otab.com/)
- **Data**: 30 000+ hodin olympijského footage
- **Akce**: Email s akademickým research brief, vyjednat non-commercial rate.

### 3. European Aquatics (LEN) — ✅ ODPOVĚDĚLA (Daguano)

- **Email**: eaoffice@europeanaquatics.org, media@europeanaquatics.org
- **Web**: [europeanaquatics.org](https://europeanaquatics.org/)
- **Streaming**: [euroaquaticstv.com](https://www.euroaquaticstv.com)
- **MOU s INEFC** (Barcelona) — sports science spolupráce
- **📧 Odpověď Juliana Daguano (2026-02)**: Race analysis footage je zdarma pro národní federace — stahují přes link sdílený na Team Leaders meetingu. Doporučuje kontaktovat Český svaz plaveckých sportů (Czechia Swimming Federation).
- **Kontakt**: Juliana Daguano, Media Relations and Media Operations Manager, julianadaguano@europeanaquatics.org, +34 620 693 778
- **Akce**: → Kontaktovat ČSPS s odkazem na tuto odpověď

### 4. IOC — Olympic Studies Centre — ❌ SLEPÁ ULIČKA

- **Email**: studies.centre@olympic.org
- **Web**: [olympics.com/ioc/olympic-studies-centre](https://www.olympics.com/ioc/olympic-studies-centre)
- **Research granty**: PhD Students and Early Career Academics programme (roční výzva)
- **Footage**: images@olympic.org (primárně pro federace a broadcasters)
- **📧 Odpověď Content Licensing (2026-02)**: Mohou sdílet email se Studies Centre, ale bude jen **screen-only přístup k archívům**. Žádné footage pro výzkum nedodají.
- **Závěr**: ❌ Nepoužitelné pro projekt — nelze stáhnout videa

### 5. Swiss Timing / Omega

- **Email**: info@swisstiming.com
- **Data**: 2000 data pointů/sec/sportovec, tracking pozic, rychlostí
- **Realita**: Vyžaduje autorizaci od World Aquatics — nelze přímo.

---

## Veřejné zdroje (stáhnout hned)

- **Roboflow Universe**: [swimmer detection datasets](https://universe.roboflow.com/search?q=class:swimmer) — malé, detection-only, ale použitelné pro preprocessing
- **awesome-biomechanics**: [github.com/modenaxe/awesome-biomechanics](https://github.com/modenaxe/awesome-biomechanics) — kurátorský seznam open biomechanics datasetů
- **IAT BMS Bibliography**: [iat.uni-leipzig.de](https://www.iat.uni-leipzig.de/service/datenbanken/biomechanics-medicine-in-swimming) — 1266 swimming science papers

---

## Aktuální stav a další kroky (2026-03-02)

### Odpověděli — aktivní jednání (seřazeno podle pravděpodobnosti získání dat)

| #   | Kontakt                          | Odpověď                                  | Pokrývá                 | Další krok               | Priorita                              |
| --- | -------------------------------- | ---------------------------------------- | ----------------------- | ------------------------ | ------------------------------------- |
| 1   | **David Prycl** (BALUO)          | Kolega ochoten poskytnout databázi videí | Pokročilý (+ děti?)     | ✉️ Odpovědět s požadavky | 🔴 NEJVYŠŠÍ — nejkonkrétnější nabídka |
| 2   | **Bátorová** (VUT CESA)          | Zavolat v úterý                          | 🧒 **Dítě** + Pokročilý | ☎️ Zavolat s body        | 🔴 NEJVYŠŠÍ — jediný zdroj dětí       |
| 3   | **Macas → Jurák** (FTVS)         | Přesměrováno, má videa z flumu           | Pokročilý (flume)       | ✉️ Napsat Jurákovi       | 🟡 VYSOKÁ — flume = ideální podmínky  |
| 4   | **Daguano** (EA) → ČSPS          | Race analysis zdarma pro federace        | Závodní                 | ✉️ Napsat ČSPS           | 🟡 VYSOKÁ — nepřímá cesta             |
| 5   | **King** → Jowitt (Loughborough) | Přesměrováno na Aquatics GB              | Pokročilý + závodní     | ✉️ Napsat Jowitt         | 🟠 STŘEDNÍ — UK, formálnější proces   |

### Slepé uličky

| Kontakt                       | Důvod                                  |
| ----------------------------- | -------------------------------------- |
| **IOC Content Licensing**     | Jen screen-only přístup, žádné footage |
| **Augsburg Swimming Channel** | Zamítnuto (NDA)                        |

### Bez odpovědi (follow-up?)

Jan Šťastný (VUT), ČSPS Zenáhlík, SWIM-360 Malta, SwimTrack/MediaEval, PLOS One HSD, SwimmerNET, OTAB, World Aquatics

### Průběžně

- Natočit vlastní reálná data (triatlonové tréninky) — pokryje Pokročilý
- Stáhnout Roboflow swimmer detection datasets
