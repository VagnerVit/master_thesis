# A4 — Biomechanické metriky a prahy pro 2 úrovně plavců

**Autor:** Vít Vágner | **Datum:** 2026-03-02 | **Status:** Research dokument pro kapitolu 3 diplomky

---

## 1. Přehled metrik

Systém SwimAth analyzuje plaveckou techniku kraulu (front crawl) z videa pomocí pose estimation a porovnání s referenčními šablonami. Níže jsou definovány biomechanické metriky extrahované z keypointů, jejich optimální rozsahy pro 2 úrovně plavců a zdůvodnění prahů.

> **Proč analyzovat techniku:** Havriluk (2010) na vzorku 80 plavců prokázal, že technika (měřená jako drag coefficient) diskriminuje výkon ~2× lépe než síla — v 7 z 8 kombinací pohlaví × styl byl drag coefficient nadřazený prediktor. Chatard et al. (1990) potvrdili: „swimming mechanics were the primary factors differentiating the two groups." Analýza techniky z videa má proto větší potenciál pro zlepšení výkonu než měření síly.

> **Značení v1 / v2:** Metriky označené **v1** (primární, tabulka 8.1) budou implementovány v rámci diplomové práce. Metriky označené **v2** (sekundární, tabulka 8.2) jsou v diplomce pouze diskutovány jako budoucí rozšíření — vyžadují pokročilejší detekci (absolutní rychlost, přesná fázová segmentace) nebo mají nižší spolehlivost z 2D keypointů.

### Úrovně plavců

| Úroveň        | Popis                                                               | Věk / typická rychlost  | Definice                                                                     |
| ------------- | ------------------------------------------------------------------- | ----------------------- | ---------------------------------------------------------------------------- |
| **Dítě**      | Rostoucí organismus, kratší končetiny, nezralá motorická koordinace | 8–14 let                | Pediatrické biomechanické prahy (Jerszyński 2013; Barbosa 2019; Santos 2023) |
| **Pokročilý** | Aktivně plavající dospělý — od rekreačních po závodní plavce        | 15+, libovolná rychlost | Prahy pokrývají celé spektrum dospělých plavců (tolerance ±15°).             |

> **Budoucí rozšíření — Profesionál:** Kategorie pro národní/mezinárodní úroveň (< 1:15 min, > 75% WR) s přísnějšími prahy (±8°). V diplomce neimplementujeme, ale diskutujeme jako možné rozšíření.

Klasifikace dospělých vychází z Schnitzler, Seifert & Button (2021): High = 82.5% WR, Medium = 69.3% WR. Kategorie „Dítě" je definována věkem (8–14 let) a vychází z pediatrické plavecké literatury — biomechanické prahy nelze jednoduše odvodit z % WR kvůli vývojovým rozdílům v antropometrii a motorické koordinaci.

**Zdůvodnění věkového rozmezí 8–14 let:**

- **Dolní hranice 8 let:** minimální věk pro systematický nácvik plavecké techniky. Jerszyński et al. (2013) zahrnovali děti od 8 let.
- **Horní hranice 14 let:** přibližně odpovídá PHV (peak height velocity) — přechodu na dospělou biomechaniku. Po dosažení PHV se mění antropometrické proporce, síla a koordinace.
- Pro plavce 15+ let s dětskou antropometrií systém doporučuje kategorii Pokročilý s rozšířenou tolerancí.

**Poznámka — dospělý začátečník:** Kategorie Pokročilý pokrývá celé spektrum dospělých plavců včetně začátečníků. Tolerance ±15° je dostatečně široká. Kategorie Dítě je pro dospělé nevhodná — dospělý má jinou antropometrii, sílu a rozsah pohybu.

---

## 2. Stroke parametry

### Terminologie: záběrový cyklus

V dokumentu rozlišujeme dva pojmy:

- **Full cycle (kompletní cyklus):** Záběr levou i pravou paží. Odpovídá jednomu cyklu ve smyslu SR (cycles/min) a IdC.
- **Half-cycle (polo-cyklus):** Záběr jednou paží (single arm stroke). Detekce cyklů v prototypu (`find_peaks` na wrist_y) detekuje half-cycles — pro výpočet SR je nutné dělit 2.

Metriky, které používají full cycle: SR, SL, SI, IdC. Metriky, které se hodnotí per half-cycle (per paže): kloubové úhly, hand entry, fázově závislé prahy loktu.

> **Vliv antropometrie na stroke parametry:** Grimston & Hay (1986) ukázali, že tělesné proporce vysvětlují 89% variance SL, ale jen 17% variance rychlosti plavání. SR a SL normy proto musí zohledňovat tělesné proporce plavce — kratší plavci (typicky děti) mají fyziologicky kratší SL a vyšší SR, aniž by to bylo chybou techniky.

### 2.1 Stroke Rate (SR) — Frekvence záběru

**Definice:** Počet kompletních záběrových cyklů za minutu (cycles/min). Jeden cyklus = záběr levou i pravou paží.

**Jak se měří z keypointů:** Detekce periodicity vertikální pozice zápěstí nebo úhlu ramene. Počet detekovaných cyklů / čas segmentu × 60.

| Úroveň    | Sub-max tempo    | Maximální tempo  | Zdroj                                        |
| --------- | ---------------- | ---------------- | -------------------------------------------- |
| Dítě      | 40–60 cycles/min | 50–65 cycles/min | Barbosa 2019; Santos 2023; Vorontsov 2002    |
| Pokročilý | 30–50 cycles/min | 42–65 cycles/min | Schnitzler 2021; Chollet 2000; Staunton 2025 |

**Zdůvodnění:** Chollet (2000) měřil SR u 43 plavců ve 3 skupinách: G1 (nejlepší) průměr 49.5±4.3 str/min při V100, G3 (nejslabší) 44.8±4.6. Schnitzler (2021) potvrdil u kompetitivních při maximu 54.09±3.99, u plavců 46.05±6.16 cycles/min. Staunton (2025) uvádí elitní sprinterský SR 56–67 cycles/min (50m), 48–55 (100m), 35–48 (1500m). Barbosa (2019) a Santos (2023) uvádějí u dětí 11–13 let SR 0.76–0.93 Hz ≈ 46–56 cycles/min. Děti kompenzují kratší SL vyšším SR — proto je rozsah pro kategorii Dítě posunutý výše.

**Poznámka — SR jako informativní metrika:** Rozsah Pokročilých (30–65 cycles/min) pokrývá celé spektrum od rekreačních plavců (30–45, Chollet 2000 G2/G3) po závodní na různých distancích (sprint 56–67, 1500m 35–48, Staunton 2025). SR proto není diagnostický práh ale populační rozsah — odchylka spíše indikuje netypickou vzdálenost než chybnou techniku. Bez uživatelského vstupu „typ úseku" (sprint/middle/distance) systém SR nehodnotí jako chybu — pouze informativně zobrazuje hodnotu a trend.

**Poznámka:** SR samotný není indikátorem kvality — záleží na kombinaci SR × SL = V. Děti mohou mít vysoký SR s krátkým SL, ale to je u rostoucího organismu fyziologicky normální, ne nutně chyba techniky. Na elitní úrovni Huot-Marchand et al. (2005) zjistili, že 65% z 17 elitních plavců zlepšilo 200m výkon přes zvýšení SR (ne SL) — korelace SR/SL: r = 0.98. Kennedy et al. (1990) u olympioniků: muži měli 9.7% delší SL ale jen 1% vyšší SR — SL koreluje s tělesnou výškou, SR ne.

### 2.2 Stroke Length (SL) — Délka záběru

**Definice:** Vzdálenost, kterou tělo urazí během jednoho kompletního záběrového cyklu (m/stroke).

**Jak se měří z keypointů:** Horizontální posun pelvis keypointu mezi dvěma po sobě jdoucími cykly (pokud je k dispozici globální referenční rámec). Alternativně: V / SR.

**Závislost na rychlosti:** SL není plně automatická metrika — výpočet SL = V / SR vyžaduje absolutní rychlost plavce, která vyžaduje buď kalibraci kamery, nebo uživatelský vstup (délka bazénu + čas úseku). Bez tohoto vstupu se SL nehodnotí (stejně jako SI). Horizontální posun pelvis keypointu v pixelech poskytuje jen relativní odhad a závisí na vzdálenosti kamery.

| Úroveň    | Typický SL | Zdroj                                              |
| --------- | ---------- | -------------------------------------------------- |
| Dítě      | 1.0–2.0 m  | Barbosa 2019; Santos 2023 (11–13 let: 1.55–1.93 m) |
| Pokročilý | 1.5–2.6 m  | Chollet 2000; Correia 2023; Staunton 2025          |

**Zdůvodnění:** Craig & Pendergast (1979) formulovali V = SR × SL a ukázali, že lepší plavci udržují vyšší SL. Chollet (2000) zjistil SL = 2.47±0.3 m u G1 při V800. Staunton (2025) uvádí pro elitní muže při 100m: 2.1–2.3 m, při 1500m: 2.2–2.6 m. Santos (2023) a Barbosa (2019) uvádějí SL 1.55–1.93 m u dětí 11–13 let — kratší SL odpovídá kratším končetinám a nižší síle záběru.

### 2.3 Stroke Index (SI) — Index efektivity

**Definice:** SI = V × SL (m²/s). Vyšší SI = efektivnější technika (Costill et al. 1985).

| Úroveň    | Typický SI   | Zdroj                                 |
| --------- | ------------ | ------------------------------------- |
| Dítě      | < 1.5 m²/s   | Barbosa 2011; Sánchez & Arellano 2002 |
| Pokročilý | 1.5–4.0 m²/s | Chollet 2000; Correia 2023            |

**Poznámka — vyloučení z implementace:** SI vyžaduje absolutní rychlost plavce (m/s), kterou nelze z videa bez kalibrace kamery a známé vzdálenosti spolehlivě určit. Proto **SI není zařazen** do primárních ani sekundárních tabulek metrik (sekce 8). V budoucnu by mohl být dostupný, pokud uživatel zadá vzdálenost a čas úseku ručně.

---

## 3. Kloubové úhly (Joint Angles)

### 3.1 Úhel loktu (Elbow Angle)

**Definice:** Úhel mezi ramenem, loktem a zápěstím (3-point angle at elbow vertex). Měří se v 2D projekci z bočního pohledu.

**Keypointy:** shoulder → elbow → wrist (MediaPipe: 11/12 → 13/14 → 15/16)

Záběrový cyklus kraulu se skládá ze 4 fází (Chollet 2000): A (entry + catch), B (pull), C (push), D (recovery). Úhel loktu má pro každou fázi odlišný optimální rozsah, proto je nutné ho hodnotit odděleně.

**Detekce vodní hladiny (water line):** Bez explicitní segmentace vodní hladiny z obrazu se water line aproximuje jako:

1. **Primární metoda:** průměrná y-pozice ramen (`water_line_y ≈ mean(shoulder_y_L, shoulder_y_R)`). U kraulu jsou ramena přibližně na úrovni hladiny.
2. **Sekundární metoda:** minimální y-pozice zápěstí v rámci záběrového cyklu — odpovídá momentu, kdy ruka vstupuje do vody.
3. **Budoucí rozšíření:** detekce vodní hladiny pomocí edge detection nebo segmentačního modelu.

**Limitace:** Aproximace přes ramena funguje dobře u bočního pohledu při kraulu, ale selhává u znaku (ramena pod vodou) a při šikmém záběru.

**Detekce fáze:** Fáze se určuje z relativní pozice zápěstí vůči rameni a odhadnuté water line:

- **Catch:** wrist_y < water_line_y AND wrist vstupuje do vody (wrist_x se pohybuje dopředu)
- **Pull-through:** wrist_y > water_line_y, wrist se pohybuje pod tělem dozadu (wrist_x klesá)
- **Push:** wrist_y > hip_y, wrist se pohybuje k boku (wrist_x pokračuje dozadu)
- **Recovery:** wrist_y < water_line_y AND wrist je nad vodní hladinou (nadvodní fáze)

#### Spolehlivost detekce fáze (Phase Confidence)

Detekce fáze je single point of failure celého pravidlového systému — špatně přiřazená fáze způsobí, že kloubový úhel se porovnává s nesprávným prahem, což může generovat až 5 falešných chyb z jednoho záběru. Proto systém pro každý záběr vypočítává `phase_confidence` skóre založené na:

- **(a) Jasnost inflexního bodu wrist_x:** Ostrý inflexní bod (vysoký |d²(wrist_x)/dt²|) indikuje spolehlivou detekci přechodu catch → pull. Plochý profil = nejistá detekce.
- **(b) Konzistence s water_line:** Fáze pull/push by měly probíhat pod vodní hladinou, recovery nad ní. Porušení tohoto pravidla snižuje confidence.
- **(c) Plausibilita trvání fáze:** Žádná fáze by neměla trvat < 5 % nebo > 60 % cyklu. Extrémní hodnoty indikují chybnou segmentaci.

**Graceful degradation:** Pokud `phase_confidence < 0.7`, systém potlačí fázově závislé metriky (elbow per-phase, IdC) a reportuje jen agregáty (celkový DTW, SR, body roll). Uživateli se zobrazí upozornění: „Detekce fáze záběru není spolehlivá — zobrazuji pouze celkové metriky."

**Výchozí threshold 0.7:** Hodnota bude stanovena empiricky na testovacích datech. Výchozí 0.7 vychází z heuristiky: systém vyžaduje, aby alespoň 2 ze 3 indikátorů (inflexní bod, water_line konzistence, plausibilita trvání) byly v přijatelném rozsahu. Při validaci na reálných videích bude threshold upraven na základě ROC analýzy (false positive rate fázově závislých chyb vs. recall).

#### Fáze catch (vstup ruky do vody a příprava záběru)

| Úroveň    | Optimální rozsah | Tolerance | Zdroj                                                               |
| --------- | ---------------- | --------- | ------------------------------------------------------------------- |
| Dítě      | 100–170°         | ±25°      | Jerszyński 2013 (extrapolace z min. úhlu pod vodou); Maglischo 2003 |
| Pokročilý | 130–170°         | ±15°      | Maglischo 2003                                                      |

**Zdůvodnění:** Při vstupu ruky do vody by paže měla být téměř natažená (140–170°). Příliš ohnutý loket při catch indikuje předčasný záběr. Ruka vstupuje do vody vpředu před ramenem, prsty napřed. U dětí (8–14 let) je rozsah výrazně širší — Jerszyński et al. (2013) měřili minimální úhel loktu pod vodou u začínajících dětí 8–13 let (n=11) a pozorovali hodnoty 130–156° (front crawl), ale catch fáze nebyla izolovaně měřena. Tolerance ±25° reflektuje vyšší variabilitu dětského pohybu.

**Caveat (Dítě):** Prahy pro kategorii Dítě ve fázi catch jsou odvozeny extrapolací z dospělé literatury a omezeného vzorku Jerszyński et al. (2013, n=11). Jerszyński měřil minimální úhel loktu pod vodou (ne izolovanou catch fázi). Pediatrická 3D kinematická data pro catch fázi neexistují.

#### Fáze pull-through (propulzní záběr pod vodou)

| Úroveň    | Optimální rozsah | Tolerance | Zdroj                                                                             |
| --------- | ---------------- | --------- | --------------------------------------------------------------------------------- |
| Dítě      | 80–160°          | ±25°      | Jerszyński 2013 (min. úhel loktu pod vodou 130–156° u začínajících dětí 8–13 let) |
| Pokročilý | 80–120°          | ±15°      | Maglischo 2003; Virag 2014                                                        |

**Zdůvodnění:** Maglischo (2003) popisuje ideální „high elbow catch" s maximální flexí loktu ~90° uprostřed pull fáze. Virag et al. (2014) zjistili, že „dropped elbow" (loket klesne pod úroveň zápěstí, úhel > 120°) je nejčastější biomechanická chyba u kraulu — vyskytuje se u **61.3% ramen** i u elitních závodních plavců. Při správné technice loket zůstává výše než zápěstí po celou dobu pull-through.

Rouard & Billat (1990) kvantifikovali trvání fází záběru: pull fáze (45°→135°) trvá pouze ~19% celkového záběru (9.5% + 9.9%), ale je kritická pro propulzi. Keys et al. (2010) potvrdili hydrodynamický základ high-elbow catch: forearm perpendicular to flow = peak propulsive force (transient pressure wave at 0.3m depth). Bent-arm pull navíc snižuje svalovou aktivaci oproti straight-arm (Rouard 1990).

**Detekce chyb:**

- **Dropped elbow:** elbow_y > wrist_y AND elbow_angle > 120° → severity: moderate (120–140°), severe (> 140°)
- **Příliš natažená paže:** elbow_angle > 150° během pull → neefektivní záběr, „paddle" technika

#### Fáze push (dokončení záběru)

| Úroveň    | Optimální rozsah | Tolerance | Zdroj                                                              |
| --------- | ---------------- | --------- | ------------------------------------------------------------------ |
| Dítě      | 80–170°          | ±25°      | Jerszyński 2013 (extrapolace z min. úhlu pod vodou); Cappaert 1996 |
| Pokročilý | 120–175°         | ±15°      | Cappaert 1996; Maglischo 2003                                      |

**Zdůvodnění:** Ve fázi push se loket opět natahuje — ruka tlačí vodu směrem ke stehnu. Cappaert et al. (1996) zjistili, že elitní plavci mají vyšší rozšíření loktu ve fázi push než ne-elitní. Plné natažení (> 140°) před výstupem z vody maximalizuje délku propulzní dráhy.

**Poznámka — nízká diskriminační síla:** Fáze push je nejméně diagnosticky citlivá ze všech fází záběru. Rozsah pro Plavce (120–170° = 50°) propustí prakticky jakýkoli reálný úhel. Cappaert (1996) ukazuje směrový signál (elitní = vyšší natažení), ale 2D měření z bočního pohledu nemá dostatečnou přesnost pro užší rozsah — loket se při push pohybuje částečně v transverzální rovině, která je z boku neviditelná. Systém by měl push violations vážit méně než pull-through nebo catch violations.

#### Fáze recovery (přenos paže nad vodou)

| Úroveň    | Optimální rozsah | Tolerance | Zdroj                                                           |
| --------- | ---------------- | --------- | --------------------------------------------------------------- |
| Dítě      | 50–160°          | ±25°      | Jerszyński 2013 (extrapolace z min. úhlu pod vodou); tolerantní |
| Pokročilý | 70–130°          | ±15°      | Virag 2014; Maglischo 2003                                      |

**Zdůvodnění:** Během recovery by loket měl zůstat výše než zápěstí. Dropped elbow při recovery (prevalence 53.2%, Virag 2014) vede k tomu, že loket vstoupí do vody dříve než ruka → nesprávná pozice při hand entry → zvýšené riziko impingementu ramene.

**Detekce chyb (recovery):**

- **Dropped elbow:** elbow_y < wrist_y během nadvodní fáze → severity: moderate/severe
- **Příliš nízký oblouk:** elbow_y blízko k shoulder_y → krátký recovery, zvýšený odpor

### 3.2 Úhel ramene (Shoulder Angle)

**Definice:** Úhel mezi loktem, ramenem a kyčlí. Indikátor rozsahu pohybu a rotace ramene.

**Keypointy:** elbow → shoulder → hip (MediaPipe: 13/14 → 11/12 → 23/24)

| Úroveň    | Optimální rozsah | Tolerance | Zdroj                                                 |
| --------- | ---------------- | --------- | ----------------------------------------------------- |
| Dítě      | 110–180°         | ±30°      | Extrapolace z dospělé literatury; rozšířená tolerance |
| Pokročilý | 130–180°         | ±15°      | Barbosa 2011; Cappaert 1996; Maglischo 2003           |

**Zdůvodnění:** Cappaert et al. (1996) porovnávali olympijské a ne-elitní plavce: elitní mají vyšší rozšíření loktu ve fázi push a lepší streamline pozici ramene.

**Caveat (Dítě):** Prahy odvozeny extrapolací z dospělé literatury; pediatrická 3D kinematická data pro úhel ramene neexistují. Tolerance ±30° reflektuje vyšší variabilitu dětského pohybu.

### 3.3 Úhel kolene (Knee Angle)

**Definice:** Úhel mezi kyčlí, kolenem a kotníkem. Indikátor techniky kopání.

**Keypointy:** hip → knee → ankle (MediaPipe: 23/24 → 25/26 → 27/28)

| Úroveň    | Optimální rozsah | Tolerance | Zdroj                                                 |
| --------- | ---------------- | --------- | ----------------------------------------------------- |
| Dítě      | 120–180°         | ±30°      | Extrapolace z dospělé literatury; rozšířená tolerance |
| Pokročilý | 140–180°         | ±15°      | Arellano 2003; Barbosa 2008; Maglischo 2003           |

**Zdůvodnění:** Efektivní flutter kick vychází z kyčlí, ne z kolen. Maglischo (2003) doporučuje téměř nataženou nohu (150–180°) s mírným ohybem kolene. Přílišné ohýbání (< 130°) indikuje „bicycle kick" — kopání z kolen, které zvyšuje odpor. Arellano et al. (2003) uvádí, že zvýšení frekvence kopu s nataženějším kolenem optimalizuje rychlost.

**Caveat (Dítě):** Prahy odvozeny extrapolací z dospělé literatury; pediatrická 3D kinematická data pro úhel kolene neexistují. U dětí je vyšší flexe kolene částečně fyziologická (kratší končetiny, nižší síla).

**Poznámka k funkci kopu:** Brooks et al. (2000) prokázali, že nohy primárně zvedají těžiště a udržují alignment, nikoli generují horizontální propulzi (lift pažemi: r = .94; horizontální propulze pažemi: r = .84). Deschodt (1999) zjistil, že kopání zlepšuje trajektorii zápěstí pod vodou → lepší mechanika paží (~+10 % rychlosti). Metrika knee angle tedy hodnotí především alignment/drag, ne propulzi samotnou.

### 3.4 Úhel kyčle (Hip Angle)

**Definice:** Úhel mezi ramenem, kyčlí a kolenem. Indikátor pozice těla ve vodě (streamline).

**Keypointy:** shoulder → hip → knee (MediaPipe: 11/12 → 23/24 → 25/26)

| Úroveň    | Optimální rozsah | Tolerance | Zdroj                                                 |
| --------- | ---------------- | --------- | ----------------------------------------------------- |
| Dítě      | 130–180°         | ±30°      | Extrapolace z dospělé literatury; rozšířená tolerance |
| Pokročilý | 150–180°         | ±15°      | Barbosa 2011; Maglischo 2003                          |

**Zdůvodnění:** Vysoký úhel kyčle (blízko 180°) znamená lepší horizontální polohu těla — nižší odpor. Pokles kyčlí (úhel < 150°) zvyšuje čelní plochu a odpor. Maglischo (2003) zdůrazňuje streamline pozici jako základ efektivní techniky.

**Caveat (Dítě):** Prahy odvozeny extrapolací z dospělé literatury; pediatrická 3D kinematická data pro úhel kyčle neexistují. Děti mají vyšší variabilitu pozice těla ve vodě.

### 3.5 Hand Entry Position (Pozice vstupu ruky)

**Definice:** Pozice zápěstí při vstupu do vody relativně k rameni a středové ose těla. Správný vstup: ruka vstupuje do vody vpředu před ramenem, laterálně od hlavy, mediálně od ramene, prsty/malíček napřed (Virag 2014).

**Keypointy:** wrist(15/16), shoulder(11/12), nose(0), mid_hip(avg 23,24)

**Detekované chyby (Virag 2014, prevalence u závodních plavců):**

#### a) Crossover entry (ruka kříží středovou osu) — prevalence 45.2%

**Výpočet:** Středová osa těla = linie nose → mid_hip (v 2D projekci z frontálního pohledu). Při hand entry: pokud wrist_x překročí středovou osu na opačnou stranu → crossover.

```
midline_x = (nose_x + mid_hip_x) / 2
# Pro levou ruku (wrist_15):
crossover = wrist_15_x > midline_x  # levá ruka přešla doprava
# Pro pravou ruku (wrist_16):
crossover = wrist_16_x < midline_x  # pravá ruka přešla doleva
```

| Úroveň    | Přijatelná odchylka od shoulder_x        | Zdroj                                         |
| --------- | ---------------------------------------- | --------------------------------------------- |
| Dítě      | ±20 cm (normalizováno na shoulder width) | Extrapolace z Virag 2014; rozšířená tolerance |
| Pokročilý | ±10 cm                                   | Virag 2014; Maglischo 2003                    |

**Severity:**

- Crossover (ruka za středovou osou): **severe** — zvyšuje impingement ramene
- Příliš široký vstup (ruka > 1.5× shoulder width laterálně): **moderate** — snižuje efektivitu záběru
- Mírná odchylka: **minor**

**Injury prevention poznámka:** Yanai & Hay (1996) prokázali, že >70 % případů impingementu ramene nastává právě při hand entry, zbylých 30 % při zahájení pull fáze. Body roll nekoreloval s impingementem. Prevence: flexe lokte při vstupu paže do vody (ne natažená paže). Toto potvrzuje crossover jako **severe** chybu — kombinace crossover + natažený loket při vstupu = nejvyšší injury risk.

#### b) Thumb-first entry (palec vstupuje první) — prevalence 38.7%

**Výpočet:** Detekce rotace zápěstí při vstupu. Z 2D keypointů obtížně měřitelné — vyžaduje sledování orientace ruky (wrist → index_finger vs. wrist → pinky). V MediaPipe (33 keypointů) nejsou prsty dostupné; v modelech s hand keypointy (21 hand landmarks) by bylo možné.

**Poznámka pro implementaci:** Tato metrika je spolehlivě detekovatelná pouze z frontálního nebo podvodního pohledu. Z bočního pohledu je hand entry angle obtížně odlišitelný.

#### c) Wide entry (ruka vstupuje příliš daleko od hlavy)

**Výpočet:**

```
entry_width = |wrist_x - shoulder_x| / shoulder_width
# Správně: 0.3–0.8 (ruka mezi hlavou a ramenem)
# Chybně: > 1.0 (ruka za linií ramene) nebo < 0.2 (ruka téměř na střed)
```

| Úroveň    | Optimální entry_width | Zdroj                      |
| --------- | --------------------- | -------------------------- |
| Dítě      | 0.1–1.2               | Extrapolace; tolerantní    |
| Pokročilý | 0.3–0.9               | Virag 2014; Maglischo 2003 |

**Limitace normalizace `shoulder_width`:** Z bočního pohledu je `shoulder_width = |L_shoulder_x − R_shoulder_x|` silně závislá na rotaci trupu — při 45° body roll je projekce ramene ~70% skutečné šířky. Proto je hand entry position spolehlivá **pouze z frontálního pohledu**. Z bočního pohledu je tato metrika orientační a systém by ji měl reportovat s nižším confidence.

---

## 4. Rotace trupu (Body Roll)

### 4.1 Rotace ramen (Shoulder Roll)

**Definice:** Úhel rotace ramenní osy kolem podélné osy těla. Měří se jako úhel vektoru L_shoulder → R_shoulder vůči horizontále (z frontálního pohledu) nebo jako maximální náklon ramen při záběru (z bočního pohledu).

**Keypointy:** Projekce vektoru (L_shoulder − R_shoulder) do roviny kolmé na směr plavání.

| Úroveň    | Optimální rozsah (na jednu stranu) | Celkový rozsah L↔R | Zdroj                                                                   |
| --------- | ---------------------------------- | ------------------ | ----------------------------------------------------------------------- |
| Dítě      | 10–60°                             | 20–120°            | Jerszyński 2013 (33–53° shoulder roll u dětí); rozšířená tolerance ±30° |
| Pokročilý | 30–55°                             | 60–110°            | Psycharakis & Sanders 2010; Cappaert 1995; Psycharakis 2008; Yanai 2001 |

**Zdůvodnění:**

- Psycharakis & Sanders (2008) měřili 10 národních/mezinárodních plavců: celkový rozsah rotace ramen (L→R) = **106.6 ± 8.4°**, rotace kyčlí = **50.4 ± 12.3°**.
- Cappaert et al. (1995) u olympijských finalistů: shoulder roll 34.4 ± 1.7° (sub-elite), hip roll −17.8 ± 1.5° (sub-elite) vs. 35.4 ± 2.5° / 8.3 ± 1.5° (elite).
- Virag et al. (2014): optimální body roll ~45° podél podélné osy. Roll > 45° nebo < 45° je považován za chybu (nadměrný/nedostatečný roll).
- Yanai (2001): shoulder roll 58° per side při 1.6 m/s; Yanai (2003): shoulder roll klesá z 75° na 66° při zvýšení rychlosti z 1.3 na 1.6 m/s.
- Psycharakis & Sanders (2008): **rychlejší plavci rotují rameny méně** (P < 0.05 korelace mezi shoulder roll a rychlostí).
- Payton et al. (1999): trunk roll 66° (dýchání) vs 57° (bez dýchání).

**Data od olympijských šampionů** (Rushall, Swimming Science Bulletin #26, analýza z videa):

| Plavec          | Shoulder roll | Hip roll | Poznámka                                              |
| --------------- | ------------- | -------- | ----------------------------------------------------- |
| Perkins (40m)   | 49°           | 19°      | Shoulder-dominant roll, klasický distanční styl       |
| Perkins (1440m) | 41°           | 42°      | Únavová degradace — hip roll se zdvojnásobil!         |
| Sadovyi         | —             | —        | Body angle 3–15°, oscilace vázaná na entry            |
| Popov           | —             | —        | Body angle 17–20°, konzistentně vysoký (odlišný styl) |

Shoulder roll > 40° u všech champion plavců. Upper arm angles > 45° during pulls and recoveries. Perkins data potvrzují únavový efekt na body roll (viz sekce 7.3).

**Skilled vs. unskilled plavci** (Keppenham & Yanai 1995, MSSE abstract 1299):

- Skilled: shoulders 80° total, hips 50°; unskilled: shoulders 70° total, hips 40°
- Klíčový kvalitativní rozdíl: skilled rotují ramena a kyčle **současně** (synchronized); unskilled rotují **sekvenčně** (hips first, then shoulders) — toto je diagnosticky cennější než absolutní úhel
- Vstup paže u skilled: při body roll > 40°; u unskilled: při body roll < 0° (ruka vstupuje do vody na „špatné" straně rotace)

**Poznámka k rozsahu Pokročilý (30–55°):** Rozsah je populační distribuce, ne kvalitativní standard — plavci legitimně variují v závislosti na individuální technice a rychlosti (Psycharakis & Sanders 2008). Dolní hranice 30° reflektuje zjištění, že rychlejší plavci rotují rameny méně (P < 0.05).

#### Vliv dýchání na body roll

Payton et al. (1999) zjistili asymetrický trunk roll: 66° na dýchající straně vs. 57° na nedýchající straně (rozdíl ~9°). Psycharakis & McCabe (2010) potvrdili: „Swimmers increased shoulder roll when breathing by increasing mainly the roll of the shoulders towards the breathing side. Hip roll and swimming velocity are not significantly affected." Lee et al. (2008) zjistili, že breathing stroke mění sekvenci pohybů: head → hip → chest (destabilizující), zatímco non-breathing = hip → chest (koordinovaný). Předčasná rotace hlavy zvyšuje odpor a nestabilitu trupu.

Shoulder roll prahy (30–55°) proto platí odlišně pro breathing a non-breathing stroke:

- **Breathing stroke:** Přijatelný shoulder roll až 60° per side (dýchající strana)
- **Non-breathing stroke:** Shoulder roll > 55° per side indikuje nadměrnou rotaci

**Detekce breathing side z keypointů:** Rotace hlavy pro nádech je detekovatelná z nose a ear keypointů:

- Z frontálního pohledu: `head_rotation = |nose_x − midline_x|` — při dýchání se nos výrazně posouvá laterálně
- Z bočního pohledu: viditelnost ear keypointů — při dýchání na stranu kamery je vidět obě uši; při dýchání na opačnou stranu zmizí vzdálenější ucho

**Poznámka pro implementaci:** V první verzi (v1) systém nerozlišuje breathing/non-breathing stroke — prahy shoulder roll platí jako celkový rozsah. Rozlišení breathing side je navrženo pro v2 a vyžaduje validaci detekce head rotation na reálných datech.

**Klíčový poznatek:** Rotace ramen je funkce individuální techniky, ne jen úrovně. Pro účely detekce chyb: nedostatečná rotace (< 30° per side) nebo nadměrná rotace (> 60° per side) jsou problematické u dospělých. U dětí je variabilita výrazně vyšší — Jerszyński (2013) pozoroval shoulder roll 33–53° u 11 dětí (8–13 let), ale vzorek je příliš malý na definitivní prahy.

**Caveat (Dítě):** Body roll u dětí je v literatuře identifikován jako výzkumná mezera (Psycharakis 2010). Prahy jsou odvozeny z omezeného vzorku Jerszyński (2013) a rozšířeny o bezpečnostní marži.

### 4.2 Rotace kyčlí (Hip Roll)

| Úroveň    | Optimální rozsah (na jednu stranu) | Zdroj                                 |
| --------- | ---------------------------------- | ------------------------------------- |
| Dítě      | 5–40°                              | Extrapolace; rozšířená tolerance ±30° |
| Pokročilý | 15–35°                             | Cappaert 1995; Psycharakis 2008       |

**Poznámka:** Kyčle se rotují výrazně méně než ramena. U sub-elitních plavců Cappaert (1995) zjistil opačný směr rotace kyčlí vůči ramenům — to zvyšuje čelní plochu a odpor.

### 4.3 Asymetrie rotace (L/R)

**Definice:** |roll_left − roll_right| — rozdíl v rotaci na dýchající a nedýchající stranu.

| Úroveň    | Přijatelná asymetrie | Zdroj                            |
| --------- | -------------------- | -------------------------------- |
| Dítě      | < 25°                | Extrapolace; rozšířená tolerance |
| Pokročilý | < 12°                | Psycharakis 2008                 |

---

## 5. Index of Coordination (IdC)

### 5.1 Definice

IdC (Chollet et al. 2000) měří časový vztah mezi propulzními fázemi levé a pravé paže. Vyjádřen jako procento trvání záběrového cyklu.

- **IdC < 0%** → catch-up: mezera mezi propulzními fázemi (pauza v propulzi)
- **IdC = 0%** → opposition: propulzní fáze navazují bez mezery
- **IdC > 0%** → superposition: propulzní fáze se překrývají (kontinuální propulze)

### 5.1b Výpočet IdC z keypointů

IdC vyžaduje identifikaci 4 fází záběru (Chollet 2000) pro každou paži zvlášť:

**Fáze jedné paže (např. pravé):**

- **A (entry + catch):** od vstupu ruky do vody do začátku zpětného pohybu ruky. Detekce: wrist_16 se pohybuje dopředu (wrist_x roste) a poté zastaví / změní směr.
- **B (pull):** od začátku zpětného pohybu do bodu, kdy ruka dosáhne úrovně ramene. Detekce: wrist_x klesá AND wrist_y dosáhne úrovně shoulder_y. Toto je začátek propulze.
- **C (push):** od úrovně ramene do opuštění vody. Detekce: wrist_x pokračuje v klesání AND wrist_y roste nad hip_y → ruka opouští vodu.
- **D (recovery):** od opuštění vody do dalšího vstupu. Detekce: wrist je nad vodní hladinou (nadvodní fáze).

**Propulzní fáze = B + C** (pull + push). Nepropulzní fáze = A + D (entry/catch + recovery).

**Výpočet IdC:**

```python
# Pro jeden záběrový cyklus:
# Pravá paže: propulze začíná v čase t_R_start, končí v t_R_end
# Levá paže: propulze začíná v t_L_start, končí v t_L_end

# Lag time 1: začátek propulze pravé - konec propulze levé
LT1 = t_R_start - t_L_end

# Lag time 2: začátek propulze levé - konec propulze pravé
LT2 = t_L_start - t_R_end

# Průměrný lag time jako procento cyklu
cycle_duration = t_cycle_end - t_cycle_start
IdC = ((LT1 + LT2) / 2) / cycle_duration * 100  # v procentech

# Interpretace:
# IdC < 0: catch-up (mezera mezi propulzemi)
# IdC = 0: opposition (plynulý přechod)
# IdC > 0: superposition (překryv propulzí)
```

**Praktická detekce fází z wrist trajektorie:**

```python
# Vstupní data: wrist_x[t], wrist_y[t] pro jednu paži (filtrované)
# 1. Detekce cyklů: peak detection na wrist_y (maxima = nejvyšší bod recovery)
# 2. V rámci cyklu najdi:
#    - t_entry: wrist_y klesá pod water_line (pokud dostupná) nebo pod shoulder_y
#    - t_catch_end: lokální minimum wrist_x_velocity (ruka zastaví pohyb vpřed)
#    - t_pull_start = t_catch_end (= začátek propulze)
#    - t_push_end: wrist_y stoupá nad water_line / hip_y (ruka opouští vodu)
# 3. Propulzní interval: [t_pull_start, t_push_end]
```

**Robustnost a expected error:** Automatický IdC z 2D keypointů bude mít **výrazně nižší přesnost** než manuální anotace (Chollet 2000). Hlavní zdroje chyb: (1) nepřesná detekce wrist pod vodou (vysoká chybovost PE), (2) aproximace vodní hladiny, (3) rozlišení pull vs. push fáze. V diplomce je nutné tuto limitaci explicitně přiznat a zahrnout do expected error analysis — IdC hodnoty z automatické detekce je třeba interpretovat jako orientační, ne přesné. Klíčové body pro automatickou detekci:

- **Začátek propulze:** inflexní bod wrist_x velocity (z pozitivní na negativní)
- **Konec propulze:** wrist opouští oblast pod trupem (wrist_y > hip_y nebo wrist viditelně nad vodou)
- **Hladina vody:** aproximace `water_line_y ≈ mean(shoulder_y_L, shoulder_y_R)` — viz sekce 3.1

### 5.2 Hodnoty IdC podle úrovně a rychlosti

#### Chollet et al. (2000) — originální data (43 plavců, 3 skupiny)

| Skupina        | Popis           | IdC V800    | IdC V100    | IdC V50      |
| -------------- | --------------- | ----------- | ----------- | ------------ |
| G1 (14 plavců) | Nejlepší výkon  | −6.9 ± 7.1% | −0.9 ± 5.4% | +2.53 ± 4.4% |
| G2 (15 plavců) | Střední výkon   | −6.65 ± 3%  | −3.55 ± 4%  | −1.6 ± 5.7%  |
| G3 (14 plavců) | Nejslabší výkon | −9.4 ± 5.4% | −5.1 ± 5.4% | −3.7 ± 5%    |
| Celý vzorek    | Průměr          | −7.6 ± 6.4% | −3.2 ± 5.1% | −0.9 ± 5.6%  |

**Propulsive phase duration (Chollet 2000):** Podíl propulsivní fáze roste s rychlostí — 43.1 % (V800), 46.5 % (V100), 49.0 % (V50). Přechod z catch-up na opposition/superposition umožňuje vyšší propulsivní pokrytí cyklu. Seifert et al. (2007) identifikovali rychlostní práh ~1.8 m/s (tempo ~200m), při kterém koordinace typicky přechází z catch-up do opposition módu.

#### Schnitzler, Seifert & Button (2021) — 3 jasné úrovně

| Úroveň            | IdC @ 70% max | IdC @ 100% max | SR @ 100% max |
| ----------------- | ------------- | -------------- | ------------- |
| High (82.5% WR)   | −3.4 ± 3.2%   | +6.4 ± 5.6%    | 54.09 ± 3.99  |
| Medium (69.3% WR) | −8.1 ± 3.8%   | −2.5 ± 4.5%    | 46.05 ± 6.16  |
| Low (45.4% WR)    | +1.2 ± 6.4%   | +7.5 ± 7.0%    | 45.90 ± 6.05  |

**Upozornění:** Schnitzler (2021) měřil dospělé plavce — skupina „Low" (45.4% WR) jsou dospělí začátečníci, ne děti. Mapování na kategorii Dítě je přibližné; hodnoty IdC a SR slouží jako orientační srovnání. Pozitivní IdC u začátečníků neindikuje kvalitní superpozici — reflektuje nekoordinované, chaotické pohyby paží s vysokou variabilitou (SD 6–9%).

#### Další studie

| Zdroj                              | Vzorek                     | IdC                             |
| ---------------------------------- | -------------------------- | ------------------------------- |
| Matsuda et al. (2014)              | Elite @ 75% max            | −9.15%                          |
| Matsuda et al. (2014)              | Elite @ max                | +1.63%                          |
| Matsuda et al. (2014)              | Beginners @ 75% max        | −3.65%                          |
| Matsuda et al. (2014)              | Beginners @ max            | +0.27%                          |
| Correia et al. (2023) meta-analýza | Závodní plavci (400m)      | −11.0% (CI: −14.3 to −7.8%)     |
| Schnitzler et al. (2009)           | Národní úroveň (400m race) | −15.4 to −15.9%                 |
| Seifert et al. (2010)              | Národní vs. regionální     | Národní signifikantně vyšší IdC |

### 5.3 Prahy IdC pro SwimAth

| Úroveň    | IdC sub-max  | IdC max      | Interpretace                                                                                                                                          |
| --------- | ------------ | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dítě      | Nehodnotí se | Nehodnotí se | Koordinace je nezralá a variabilní; hodnotí se pouze `std(IdC)` napříč cykly. Morais 2021 review: IdC u dětí vykazuje vysokou variabilitu (SD 6–9 %). |
| Pokročilý | −8% až 0%    | −5% až +5%   | Catch-up → opposition/superposition dle rychlosti a úrovně                                                                                            |

**Catch-up = chyba u pokročilých:** Millet et al. (2002) zjistili, že catch-up koordinace „rychle mizí" u elitních plavců při zvýšení rychlosti, ale přetrvává u triatlonistů. Fernandes et al. (2010) explicitně konstatují: „catch-up stroking is not a technique that should be encouraged" — IdC a energetická náročnost korelují s rychlostí, ale ne přímo mezi sebou. Toto potvrzuje, že persistentní catch-up u kategorie Pokročilý je chybou hodnou feedbacku.

**Poznámka pro implementaci:** IdC je pokročilá metrika vyžadující přesnou detekci fází záběru. V první verzi SwimAth bude implementována jako sekundární metrika. Primární metriky (kloubové úhly, SR, body roll) jsou robustnější.

---

## 6. Body Alignment (Streamline)

### 6.1 Pozice hlavy (Head Position)

**Definice:** Úhel pohledu / pozice hlavy vůči páteři. Virag (2014): „eyes-forward head-carrying angle" je biomechanická chyba s prevalencí **46.8%**.

**Správně:** Hlava v neutrální pozici, imaginární linie od hlavy přes páteř. Plavec se dívá na dno bazénu.
**Chybně:** Hlava zvednutá dopředu (eyes-forward) — zvyšuje odpor, narušuje streamline, zvyšuje riziko impingementu ramene.

**Keypointy:** Úhel mezi nose/ear, neck/spine a pelvis.

| Úroveň    | Tolerance                                | Zdroj                      |
| --------- | ---------------------------------------- | -------------------------- |
| Dítě      | Hlava zvednutá tolerována s upozorněním  | Virag 2014 (extrapolace)   |
| Pokročilý | Hlava by měla být neutrální mimo dýchání | Virag 2014; Maglischo 2003 |

### 6.2 Body Alignment Score

**Definice:** Úhel mezi head, spine2 a pelvis keypointy. Čím blíže 180°, tím lepší streamline.

| Úroveň    | Optimální rozsah | Tolerance |
| --------- | ---------------- | --------- |
| Dítě      | 140–180°         | ±30°      |
| Pokročilý | 160–180°         | ±15°      |

---

## 7. Symetrie (L/R Asymmetry)

**Definice:** Pro každý párový kloub (loket L/R, rameno L/R, koleno L/R, kyčel L/R) se počítá: |angle_left − angle_right|. Vysoká asymetrie indikuje nerovnoměrnou techniku.

| Úroveň    | Přijatelná asymetrie kloubů | Přijatelná asymetrie body roll |
| --------- | --------------------------- | ------------------------------ |
| Dítě      | < 30°                       | < 25°                          |
| Pokročilý | < 15°                       | < 12°                          |

**Zdroj:** Psycharakis & Sanders (2008): mean shoulder roll asymmetry 8.2 ± 4.8° u národních/mezinárodních plavců. Symetrie je silnější indikátor konzistence techniky než absolutní úhly.

---

## 7.1 Integrace metrik s DTW pipeline

Biomechanické metriky a DTW porovnání s referenční šablonou tvoří dvě komplementární vrstvy analýzy:

1. **Pravidlový systém (metriky):** Pro každý frame/cyklus se vypočítají metriky z keypointů (úhly, SR, body roll, hand entry position) a porovnají s prahy pro danou úroveň plavce. Výstupem je seznam detekovaných chyb s severity (minor/moderate/severe) a konkrétními hodnotami odchylek. Tento systém poskytuje **interpretovatelnou, okamžitou zpětnou vazbu** typu „loket o 15° nízko při pull-through".

2. **DTW skóre (globální porovnání):** Celý segmentovaný záběr se porovnává s referenční šablonou pomocí DTW-D. Výstupem je:
   
   - **Celkové skóre 0–100** (normalizovaná DTW vzdálenost)
   - **Per-joint cost** — příspěvek každého kloubu k celkové vzdálenosti
   - **Temporální lokalizace** — warping path identifikuje, ve které fázi záběru je největší odchylka

3. **Kombinace:** Per-joint cost z DTW se mapuje na konkrétní metriky z pravidlového systému. Kloub s vysokým DTW cost + detected error z pravidlového systému = vysoká priorita pro zpětnou vazbu. Kloub s vysokým DTW cost bez detekované chyby = potenciálně neobvyklá (ale ne nutně chybná) technika.

Tento dvouvrstvý přístup umožňuje:

- Detekovat **známé chyby** pravidlovým systémem (vysoká přesnost, nízký recall)
- Detekovat **neobvyklé vzory** přes DTW (vysoký recall, nižší přesnost)
- Kombinovat oba signály pro robustní zpětnou vazbu

### 7.1.1 Trade-off: Z-normalizace vs. absolutní detekce

Z-normalizace per-joint (sekce 10.4) je nutná pro shape comparison v DTW — umožňuje porovnávat temporální tvar pohybu nezávisle na absolutní flexibilitě plavce. Avšak z-normalizace **odstraňuje amplitudový signál**, který je klíčový pro error detection. Plavec s loktem na 85° (správná high-elbow technika) a plavec s loktem na 140° (dropped elbow) mají po z-normalizaci identické trajektorie, pokud je temporální tvar stejný. DTW komponenta proto **nemůže** detekovat absolutní odchylky od biomechanických norem.

**Kompenzace:** Pravidlový systém operuje na **raw (nenormalizovaných) úhlech** — právě proto je dvouvrstvý přístup nezbytný. DTW hodnotí shape similarity, pravidlový systém hodnotí absolutní hodnoty. Tento trade-off je vědomé designové rozhodnutí.

**Navrhovaná hybrid normalizace (budoucí práce):**

- **Min-max normalizace na temporální osu:** Eliminuje SR-induced stretch (záběry různé délky se zarovnají na stejný počet framů), ale amplituda úhlů se NEZZ-normalizuje.
- **Alternativa:** DTW distance = `shape_distance + α × amplitude_penalty`, kde `amplitude_penalty = |mean(query_j) − mean(ref_j)|` penalizuje systematické posuny absolutní úrovně kloubu j.
- Trade-off: hybrid normalizace zachovává amplitudový signál, ale ztrácí invarianci vůči individuální flexibilitě — vyžaduje per-level referenční šablony (aktuální přístup toto podporuje).

### 7.1.2 Fázově podmíněné DTW

DTW zarovnává přes celý cyklus — catch v analyzovaném záběru může matchovat pull v referenci, pokud je warping path dostatečně široký. Per-joint cost pak neřekne, **ve které fázi** je odchylka. Pro lokalizovanou zpětnou vazbu typu „loket příliš natažený při pull" nestačí vědět, že „loket je celkově odlišný".

**Navrhované varianty (budoucí práce):**

1. **DTW separátně na 4 sub-sekvence:** Každá fáze (catch, pull, push, recovery) se porovnává zvlášť → 4 fázově lokalizované skóre per joint. Nevýhoda: vyžaduje spolehlivou detekci fázových hranic v obou sekvencích (viz Phase Confidence výše).
2. **Phase label jako dodatečný feature dimension:** K souřadnicím kloubů přidat one-hot phase label → warping path přirozeně matchuje stejné fáze, protože přechod pull→catch má vysokou cost. Elegantní, ale vyžaduje tuning váhy phase dimension.
3. **Post-hoc phase mapping (minimální implementace):** Po DTW zarovnání zpětně mapovat warping path na fáze reference a reportovat per-phase cost: `cost_catch = Σ dtw_cost[i] where ref_phase[i] == catch`. Nevyžaduje detekci fází v query, pouze v referenční šabloně.

### 7.1.3 DBA variance envelope

Aktuální DBA šablona je single average — variabilita populace, ze které byla šablona konstruována, je zahozena. DTW cost 15° u kloubu, kde populace variuje s σ = 20°, je méně alarmující než DTW cost 15° u kloubu s σ = 5°.

**Navržené rozšíření:**

- Spolu s DBA šablonou ukládat **per-frame, per-joint SD** (variance envelope): `σ_template[t][j] = std(aligned_values[t][j])` z trénovacích záběrů po DTW zarovnání k šabloně.
- DTW cost přepočítat na z-skóre: `z_cost_j = dtw_cost_j / σ_template_j`
- Kloub s DTW cost 15° kde σ = 20° → z = 0.75 (v normě). Kloub s DTW cost 15° kde σ = 5° → z = 3.0 (výrazná odchylka).
- Threshold pro flagování: z_cost > 2.0 (mimo 2 SD populace).

---

## 7.2 Korelace a kauzální vazby mezi metrikami

### Redundantní páry (double-counting)

Některé metriky sdílejí společný failure mode — jedno biomechanické selhání generuje dvě detekované chyby, což zkresluje celkový obraz a přetěžuje zpětnou vazbu.

| Pár                                       | Typ korelace     | Společný failure mode                                                                                                      |
| ----------------------------------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Hip angle + Body alignment                | Geometrická      | Sinking hips — pokles kyčlí způsobí odchylku v obou metrikách současně, protože hip angle je subkomponentou body alignment |
| Body roll asymmetry + L/R joint asymmetry | Kauzální řetězec | Asymetrické dýchání → nedostatečná rotace na jednu stranu → asymetrické kloubové úhly                                      |
| Shoulder angle + Elbow catch angle        | Mechanická vazba | Dropped shoulder → dropped catch — rameno a loket tvoří kinematický řetězec                                                |

**Doporučení pro implementaci:** U redundantních párů systém reportuje **primární metriku** (hip angle, body roll asymmetry, elbow catch) a sekundární uvádí jen jako doplňkovou informaci, ne jako samostatnou chybu. Konkrétně:

- Pokud hip_angle violation AND body_alignment violation → reportovat hip angle jako primární, body alignment jako „souvisí s pozicí kyčlí"
- Pokud body_roll_asymmetry AND joint_asymmetry → reportovat body roll jako root cause
- Pokud shoulder_angle violation AND elbow_catch violation → reportovat elbow catch jako primární (přímo měřitelná chyba), shoulder angle jako kontext

### Synergické kombinace (combined rules)

Některé kombinace metrik mají vyšší diagnostickou hodnotu než izolované metriky:

**1. SR × IdC interakce:**

- SR = 50 + IdC = −10% → catch-up degradace při vysokém tempu (warning: plavec nestíhá propulzní navázání)
- SR = 50 + IdC = +2% → agresivní superpozice (OK pro závodní plavce, warning pro rekreační)
- Aktuálně nerozlišeno — SR a IdC se hodnotí nezávisle

**2. Crossover entry + Dropped elbow pull:**

- Virag (2014) zjistil signifikantní asociaci (P = 0.009): crossover entry predikuje dropped elbow
- IF crossover AND dropped_elbow THEN severity += 1 a feedback identifikuje společnou root cause: „vstup ruky přes středovou osu způsobuje ztrátu high-elbow pozice"

**3. Body roll + Elbow catch:**

- Nedostatečný body roll (< 25° per side) → biomechanicky nemožné dosáhnout high elbow catch
- Feedback: „nedostatečná rotace trupu brání správnému záběru" místo dvou separátních chyb
- Detekce: shoulder_roll_per_side < 25 AND elbow_catch_angle < 120 → root cause = body roll

### Formalizace combined rules (pseudokód)

```python
# Combined rule 1: SR × IdC interaction
if level == "Pokročilý" and SR > 50 and IdC < -8:
    emit("catch-up degradation at high SR", severity="moderate")

# Combined rule 2: Crossover + Dropped elbow (Virag P=0.009)
if crossover_entry and dropped_elbow_pull:
    primary_error.severity += 1
    primary_error.feedback = "crossover entry causes dropped elbow"

# Combined rule 3: Body roll → Elbow catch chain
if shoulder_roll_per_side < 25 and elbow_catch_angle < 120:
    emit("insufficient body roll preventing high elbow catch",
         root_cause="body_roll", secondary="elbow_catch")
```

---

## 7.3 Temporální stabilita (únavový profil)

Aktuální systém analyzuje jednotlivé záběry izolovaně. Analýza trendu přes série po sobě jdoucích záběrů umožňuje detekovat únavou podmíněnou degradaci techniky.

**Navrhované metriky (implementace v2):**

- **Rolling average DTW cost:** Klouzavý průměr DTW cost přes N consecutive strokes (doporučeno N = 5). Rostoucí trend indikuje degradaci techniky.
- **SR drift:** Nárůst SR v čase (plavec zrychluje tempo, ale zkracuje záběr) — typický únavový vzor.
- **SL drift:** Pokles SL v čase — complementární k SR drift.
- **Korelace SR↑ + IdC↓:** Současný nárůst SR a pokles IdC indikuje catch-up degradation při únavě — plavec nestíhá plynule navazovat propulzní fáze při vyšším tempu.
- **σ(DTW) across strokes:** Rolling variance DTW cost detekuje ztrátu konzistence — unavený plavec má vyšší variabilitu mezi záběry.

**Empirický příklad — Keiren Perkins 1500m** (Rushall, Swimming Science Bulletin #26):

- Na 40m: hips 19°, shoulders 49° (shoulder-dominant roll, optimální)
- Na 1440m: hips 42°, shoulders 41° (hip roll se zdvojnásobil, shoulder roll klesl o 8°)
- Toto potvrzuje Psycharakis & Sanders (2010) review: „when tired, swimmers maintain shoulder rotation while increasing hip rotation" — hip roll kompenzuje ztrátu kontroly trupu

Tento pattern (shoulder/hip roll ratio convergence) je potenciálně detekovatelný z keypointů a mohl by sloužit jako early warning indikátor únavy.

**Seifert et al. (2007) — 100m závod:** Pomalejší plavci mění koordinaci od 3. délky a přecházejí na superposition v závěrečné délce (únava), ale SL klesá — tj. vyšší IdC nekompenzuje ztrátu SL. Rychlí plavci udržují stabilní koordinační mód celých 100m. Toto potvrzuje, že degradace = nestabilita koordinace + pokles SL.

**Psycharakis et al. (2010) — IVV caveat:** Intracyklické výkyvy rychlosti (IVV) zůstávají relativně konstantní celých 200m a nekorelují přímo s výkonem. IVV sám o sobě není chybou — je to přirozená vlastnost cyklického pohybu. Jako diagnostický indikátor funguje pouze v kombinaci s dalšími metrikami (IdC, SL drift).

**Implementační poznámka:** Vyžaduje analýzu celé série záběrů (ne jednotlivý záběr) a stabilní segmentaci záběrů. V první verzi systému nebude implementováno.

---

## 8. Souhrnná tabulka metrik a prahů

### 8.1 Primární metriky (implementace v1)

| #   | Metrika                    | Jednotka   | Dítě (8–14 let) | Pokročilý (15+) | Zdroj                                                  |
| --- | -------------------------- | ---------- | --------------- | --------------- | ------------------------------------------------------ |
| 1a  | Elbow angle — catch        | °          | 100–170 (±25)   | 130–170 (±15)   | Jerszyński 2013; Maglischo 2003                        |
| 1b  | Elbow angle — pull-through | °          | 80–160 (±25)    | 80–120 (±15)    | Jerszyński 2013; Virag 2014                            |
| 1c  | Elbow angle — push*        | °          | 80–170 (±25)    | 120–175 (±15)   | Jerszyński 2013; Cappaert 1996                         |
| 1d  | Elbow angle — recovery     | °          | 50–160 (±25)    | 70–130 (±15)    | Jerszyński 2013; Virag 2014                            |
| 2   | Shoulder angle             | °          | 110–180 (±30)   | 130–180 (±15)   | Extrapolace†; Cappaert 1996                            |
| 3   | Knee angle (kick)          | °          | 120–180 (±30)   | 140–180 (±15)   | Extrapolace†; Maglischo 2003                           |
| 4   | Hip angle (streamline)     | °          | 130–180 (±30)   | 150–180 (±15)   | Extrapolace†; Maglischo 2003                           |
| 5   | Shoulder roll (per side)   | °          | 10–60           | 30–55           | Jerszyński 2013; Psycharakis 2010                      |
| 6   | Body alignment             | °          | 140–180         | 160–180         | Extrapolace†; Maglischo 2003                           |
| 7   | Stroke Rate                | cycles/min | 40–60           | 30–65‡          | Barbosa 2019; Santos 2023; Chollet 2000; Staunton 2025 |
| 8   | Hand entry position        | norm.      | 0.1–1.2         | 0.3–0.9         | Extrapolace†; Virag 2014                               |

\* **Nízká váha push:** Metrika 1c (elbow push) má nízkou diskriminační sílu (viz sekce 3.1, fáze push) — 2D měření z bočního pohledu nemá dostatečnou přesnost. Push violations by systém měl vážit méně než pull-through (1b) nebo catch (1a).

† **Extrapolace:** Prahy pro kategorii Dítě u metrik 2–4, 6, 8 jsou odvozeny extrapolací z dospělé literatury. Pediatrická 3D kinematická data pro tyto metriky neexistují. Tolerance ±30° (vs. ±25° pro úhel loktu) reflektuje vyšší pohybovou variabilitu dětí.

‡ **Široký rozsah SR u Pokročilých (30–65):** Pokrývá celé spektrum od rekreačních (30–50, Chollet 2000 G2/G3) po závodní plavce na různých distancích (sprint 56–67, 1500m 35–48, Staunton 2025).

> **Poznámka:** Pokročilý pokrývá celé spektrum dospělých plavců — od rekreačních po závodní. Rozsahy jsou záměrně širší s tolerancí ±15°.

### 8.2 Sekundární metriky (implementace v2)

| #   | Metrika               | Jednotka | Dítě (8–14 let) | Pokročilý (15+) | Zdroj                                 |
| --- | --------------------- | -------- | --------------- | --------------- | ------------------------------------- |
| 9   | Stroke Length         | m/cycle  | 1.0–2.0         | 1.5–2.6         | Barbosa 2019; Santos 2023; Craig 1979 |
| 10  | Index of Coordination | %        | nehodnotí se*   | −8 až +5        | Chollet 2000; Schnitzler 2021         |
| 11  | L/R joint asymmetry   | °        | < 30            | < 15            | Extrapolace†; Psycharakis 2008        |
| 12  | Body roll asymmetry   | °        | < 25            | < 12            | Extrapolace†; Psycharakis 2008        |
| 13  | Hip roll (per side)   | °        | 5–40            | 15–35           | Extrapolace†; Psycharakis 2008        |

### 8.2b Start / Turn / UDK metriky (PoC, implementace v2)

| #   | Metrika                      | Jednotka   | Dítě (8–14 let)†  | Pokročilý (15+)  | Zdroj                                     |
| --- | ---------------------------- | ---------- | ------------------ | ----------------- | ----------------------------------------- |
| 14  | Entry angle (start)          | °          | 25–55 (±20)        | 20–40 (±10)       | Tor 2020; Benjanuvatra 2007               |
| 15  | Streamline tightness         | °          | < 25° od osy       | < 10° od osy      | Vantorre 2014                             |
| 16  | UDK kick frequency           | Hz         | 1.5–2.5 (±0.5)     | 2.0–2.5 (±0.3)    | Rejman 2017; Alves 2006                   |
| 17  | UDK kick amplitude           | m          | 0.30–0.65          | 0.40–0.60         | Rejman 2017; Alves 2006                   |
| 18  | UDK kick count (start)       | count      | 0–6                | 3–8               | Vantorre 2014                             |
| 19  | UDK kick count (turn)        | count      | 0–5                | 3–7               | —                                         |
| 20  | UDK amplitude consistency    | CV         | < 0.40             | < 0.25            | de Jesus et al.                           |
| 21  | Push-off angle (turn)        | °          | 150–180 (±25)      | 170–180 (±10)     | Lyttle et al. 1999                        |
| 22  | Approach SR consistency      | CV         | < 0.30             | < 0.15            | —                                         |

† **Caveat:** Pediatrická data pro start/turn/UDK biomechaniku prakticky neexistují. Prahy pro Dítě jsou extrapolovány z dospělých dat s rozšířenou tolerancí. U dětí 8–14 let je UDK často nerozvinutý a flip turn může být nahrazen open turnem — absence těchto dovedností **není hodnocena jako chyba**.

### 8.3 Tolerance odchylek a severity

Tolerance se liší podle typu metriky:

- **Elbow angle (všechny fáze):** Dítě ±25°, Pokročilý ±15°
- **Ostatní kloubové úhly (shoulder, knee, hip, body alignment):** Dítě ±30°, Pokročilý ±15°

| Severity | Dítě                       | Pokročilý      |
| -------- | -------------------------- | -------------- |
| OK       | V rozsahu                  | V rozsahu      |
| Minor    | Elbow < 13°; ostatní < 15° | Odchylka < 8°  |
| Moderate | Elbow < 25°; ostatní < 30° | Odchylka < 15° |
| Severe   | Elbow > 25°; ostatní > 30° | Odchylka > 15° |

**Poznámka:** Rozlišení minor/moderate u kategorie Dítě je orientační — při typické chybě pose estimation ±5–8° je rozdíl mezi 13° a 15° v šumu. Severity prahů budou validovány empiricky.

---

## 9. Prevalence biomechanických chyb

Z Virag et al. (2014), studie 31 univerzitních závodních plavců (62 ramen):

| Chyba                           | Prevalence | Fáze         | Detekce z keypointů                        |
| ------------------------------- | ---------- | ------------ | ------------------------------------------ |
| Dropped elbow (pull-through)    | **61.3%**  | Pull-through | elbow_y > wrist_y AND elbow_angle > 120°   |
| Dropped elbow (recovery)        | **53.2%**  | Recovery     | elbow_y < wrist_y during aerial phase      |
| Eyes-forward head               | **46.8%**  | Celý cyklus  | head_angle deviates from neutral           |
| Incorrect hand position (entry) | **45.2%**  | Hand entry   | hand crosses midline OR too wide           |
| Incorrect hand entry angle      | **38.7%**  | Hand entry   | thumb-first entry (rotation of wrist)      |
| Incorrect pull-through pattern  | **32.3%**  | Pull-through | S-shaped or excessive horizontal adduction |

**Poznámka o populaci:** Virag studoval 31 **univerzitních závodních plavců** (sub-elite) — to je specifická podmnožina kategorie „Pokročilý". U rekreačních dospělých plavců očekáváme vyšší prevalenci biomechanických chyb než uvedené hodnoty.

**Klíčový poznatek:** I u závodních plavců jsou biomechanické chyby velmi časté. Dropped elbow je nejčastější chyba a je signifikantně asociován s incorrect hand entry position (P = 0.009) a thumb-first hand entry (P = 0.027).

---

## 10. Extrakce metrik z keypointů

### 10.1 Vstupní formát

- **MediaPipe Pose:** 33 keypointů (x, y, visibility) — používá prototyp
- **SwimXYZ Base:** 48 keypointů (x, y, z) — trénovací data
- **COCO-17/25:** standardní formáty pro ViTPose/RTMPose

### 10.2 Mapování na metriky

| Metrika             | Keypointy (MediaPipe)                                | Výpočet                                                 |
| ------------------- | ---------------------------------------------------- | ------------------------------------------------------- |
| Elbow angle         | shoulder(11/12), elbow(13/14), wrist(15/16)          | 3-point angle at vertex (elbow)                         |
| Shoulder angle      | elbow(13/14), shoulder(11/12), hip(23/24)            | 3-point angle at vertex (shoulder)                      |
| Knee angle          | hip(23/24), knee(25/26), ankle(27/28)                | 3-point angle at vertex (knee)                          |
| Hip angle           | shoulder(11/12), hip(23/24), knee(25/26)             | 3-point angle at vertex (hip)                           |
| Shoulder roll       | L_shoulder(11), R_shoulder(12)                       | arctan((y_L - y_R) / (x_L - x_R)) z frontálního pohledu |
| Hip roll            | L_hip(23), R_hip(24)                                 | Analogicky k shoulder roll                              |
| Body alignment      | nose(0)/ear(7,8), mid_shoulder, mid_hip              | Angle of 3 midpoints along body axis                    |
| Stroke rate         | wrist(15/16) y-trajectory                            | Peak detection, count peaks / time                      |
| Head position       | nose(0), mid_shoulder(avg 11,12), mid_hip(avg 23,24) | Deviation from straight line                            |
| Hand entry position | wrist(15/16), shoulder(11/12), nose(0), mid_hip      | \|wrist_x − shoulder_x\| / shoulder_width               |
| IdC                 | wrist(15/16) x+y trajectory pro obě paže             | Fázová detekce + lag time (viz sekce 5.1b)              |

### 10.3 Limitace 2D projekce

Všechny metriky jsou počítány z 2D keypointů — projekce 3D pohybu do roviny kamery. To přináší systematické zkreslení závislé na pohledu kamery:

**Boční pohled (side view):**

- **Dobře měřitelné:** Elbow angle (sagitální rovina), knee angle, hip angle, body alignment, stroke rate.
- **Zkreslené:** Shoulder roll je viditelný pouze jako vertikální posuv ramen (ne skutečný úhel rotace). Rotace trupu způsobuje, že vzdálenější paže (od kamery) je opticky kratší → úhly vzdálenější strany jsou systematicky podhodnocené.
- **Nedostupné:** L/R asymetrie (vidíme jen jednu stranu), hand entry crossover (vyžaduje frontální pohled).

**Frontální pohled (front view):**

- **Dobře měřitelné:** Shoulder roll, hip roll, L/R asymetrie, hand entry position (crossover, width).
- **Zkreslené:** Elbow angle je viditelný v koronální rovině, ne v sagitální — pull-through probíhá převážně v sagitální rovině, takže frontální pohled měří jiný úhel než z boku.
- **Nedostupné:** Knee angle v sagitální rovině, body alignment (hloubka).

**Podvodní pohled:**

- **Dobře měřitelné:** Elbow angle při pull-through (nejlepší pohled na podvodní fázi), hand path.
- **Zkreslené:** Refrakce na rozhraní voda/vzduch deformuje pozice keypointů. Body roll je nespolehlivý.
- **Zvýšený šum:** Bubliny, odrazy a nízký kontrast způsobují vyšší chybovost pose estimation.

**Mitigace:**

- Pro každou kombinaci pohled × metrika definovat, zda je metrika **primární** (spolehlivá), **sekundární** (orientační) nebo **nedostupná**.
- V implementaci: metriky s nízkým confidence skóre z pose estimation nehodnotit (graceful degradation).
- V budoucnu: multi-view fúze (kombinace bočního + frontálního pohledu) pro 3D rekonstrukci.

### 10.4 Předzpracování

1. **Butterworth low-pass filter** (cutoff ~6 Hz) — odstranění šumu z pose estimation
2. **Z-normalizace per-joint** — nezávislost na pozici/velikosti plavce
3. **Temporální vyhlazení** — klouzavý průměr nebo Savitzky-Golay filtr
4. **Ragdoll constraints** — fyzikální limity kloubů (loket 0–150°, koleno 0–170°)
5. **Filtrování videí se šnorchlem:** Strumbelj et al. (2007) prokázali, že plavání se šnorchlem mění techniku (eliminace dýchání → odlišný body roll a timing). Videa z tréninku se šnorchlem nereprezentují skutečnou závodní techniku a neměla by být používána pro analýzu.

### 10.5 Odvozené features (navržené)

Kromě přímých kloubových úhlů lze z keypointů odvodit features s vyšší diagnostickou hodnotou:

| Feature                              | Vstup                   | Výpočet                            | Účel                                                                                                                                                                                                       |
| ------------------------------------ | ----------------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Wrist velocity (pull)                | wrist_x[t]              | d(wrist_x)/dt při pull midpoint    | Rozliší paddle (lineární) vs. S-pull (sinusoidální) techniku záběru                                                                                                                                        |
| Temporal L/R lag                     | wrist_y peaks L vs R    | Δt mezi peaky                      | Časová asymetrie — silnější indikátor než statická L/R odchylka úhlů                                                                                                                                       |
| Shoulder/hip roll ratio              | shoulder_roll, hip_roll | ratio + sign agreement             | Detekuje opačný hip roll (Cappaert 1995: sub-elitní plavci rotují kyčle opačně)                                                                                                                            |
| σ(DTW) across strokes                | DTW_cost per stroke     | rolling variance                   | Detekce únavy / degradace techniky (viz sekce 7.3)                                                                                                                                                         |
| Phase duration ratios                | phase timestamps        | t_pull/t_cycle, t_recovery/t_cycle | Nerovnoměrné rozložení fází — příliš dlouhá recovery indikuje neefektivní přenos paže                                                                                                                      |
| IVV (intracyclic velocity variation) | hip_x[t] within cycle   | (v_max − v_min) / v_mean per cycle | Diagnostický index techniky záběru (Schnitzler 2008). Muži mají větší catch-up než ženy při stejné rychlosti. Interpretovat pouze v kombinaci s IdC — IVV samotné nekoreluje s výkonem (Psycharakis 2010). |

Tyto features jsou navrženy pro implementaci v2. V první verzi systému se extrahují pouze přímé kloubové úhly a stroke parametry.

---

## 11. Specifika podle pohledu kamery

**Doporučení pro kraul:** Pro analýzu kraulu doporučujeme primárně **boční pohled (side view)** — pokrývá nejvíce primárních metrik (elbow angle ve všech fázích, knee, hip, body alignment, SR). Frontální pohled je vhodný jako doplněk pro body roll, L/R asymetrii a hand entry position. Podvodní pohled je nejužitečnější pro detailní analýzu pull-through fáze, ale má nejvyšší šum z pose estimation.

| Pohled             | Primární metriky (spolehlivé)                                                  | Sekundární (orientační)                              | Nedostupné                                              |
| ------------------ | ------------------------------------------------------------------------------ | ---------------------------------------------------- | ------------------------------------------------------- |
| **Boční (side)**   | Elbow angle (všechny fáze), knee angle, hip angle, body alignment, stroke rate | Shoulder roll (jen vertikální posuv), shoulder angle | L/R asymetrie, hand entry crossover                     |
| **Přední (front)** | Shoulder roll, hip roll, L/R asymetrie, hand entry position (crossover, width) | Elbow angle (koronální rovina)                       | Knee angle (sagitální), body alignment (hloubka)        |
| **Podvodní**       | Elbow angle (pull-through), hand path                                          | Knee angle                                           | Body roll (refrakce), stroke rate (bubliny), hand entry |

---

## 12. Literatura

### Primární zdroje (v `literature/`)

1. **Maglischo, E. W. (2003).** *Swimming Fastest.* Human Kinetics. — Zlatý standard plavecké biomechaniky. High elbow catch, streamline, kloubové úhly.
2. **Chollet, D., Chalies, S., & Chatard, J. C. (2000).** A new index of coordination for the crawl. *Int J Sports Med*, 21, 54–59. — Definice IdC, 3 skupiny plavců, SR/SL/IdC data.
3. **Virag, B. et al. (2014).** Prevalence of freestyle biomechanical errors in elite competitive swimmers. *Sports Health*, 6(3), 218–224. — 7 biomechanických parametrů, prevalence chyb, body roll ~45°.
4. **Psycharakis, S. G. & Sanders, R. H. (2010).** Body roll in swimming: A review. *J Sports Sciences*, 28(3), 229–236. — Shoulder roll 106.6°, hip roll 50.4°, asymetrie, rychlejší = méně rotace.
5. **Barbosa, T. M. et al. (2011).** Biomechanics of competitive swimming strokes. In *Biomechanics in Applications*. IntechOpen. — V = SR × SL, paže 85–90% propulze, dV profily.
6. **Craig, A. & Pendergast, D. (1979).** Relationships of stroke rate, distance per stroke and velocity. *MSSE*, 11, 278–283. — Fundamentální V = SR × SL vztah.
7. **Barden, J. M. & Kell, R. T. (2014).** Relationships between stroke parameters and critical swimming speed. *J Sports Sciences*. — Vztah stroke parametrů a CSS.

### Sekundární zdroje (z web research)

8. **Schnitzler, C., Seifert, L. & Button, C. (2021).** Adaptability in swimming pattern. *Frontiers in Sports and Active Living*, 3, 618990. — 3 jasné úrovně (High/Medium/Low), IdC a SR data.
9. **Seifert, L., Chollet, D. & Bardy, B. G. (2004).** Effect of swimming velocity on arm coordination. *J Sports Sciences*, 22(7), 651–660. — Velocity-dependent IdC transition.
10. **Seifert, L. et al. (2010).** Arm coordination, power, and swim efficiency. *Human Movement Science*, 29(3), 426–439. — Národní vs. regionální plavci.
11. **Matsuda, Y. et al. (2014).** Intracyclic velocity variation and arm coordination. *J Human Kinetics*, 44, 67–74. — Elite vs. beginner IdC adaptation range.
12. **Potdevin, F. et al. (2006).** Stroke frequency and arm coordination. *Int J Sports Med*, 27(3), 193–198. — Transition thresholds: 45–50 (non-expert) vs 50–55 (expert) cycles/min.
13. **Correia, R. A. et al. (2023).** Kinematic parameters of 400m front-crawl: A meta-analysis. *Frontiers in Sports and Active Living*, 5, 977739. — Pooled IdC −11.0%.
14. **Staunton, C. A. et al. (2025).** Stroke rate–stroke length dynamics in elite freestyle. *Frontiers in Sports and Active Living*, 7. — Elite SR/SL data.
15. **Cappaert, J. M., Pease, D. L. & Troup, J. P. (1996).** Biomechanical highlights of world champion and Olympic swimmers. In *Biomechanics and Medicine in Swimming VII* (pp. 76–80). London: E & FN Spon. — Shoulder/hip roll u olympioniků. Crawl: "symmetrical shoulder-hip roll" + "elevated elbows throughout the stroke" u champions; non-qualifiers opposing hip-shoulder rotations. [Abstrakt online](https://coachsci.sdsu.edu/swim/biomechs/cappaer2.htm)
16. **Yanai, T. (2001, 2003, 2004).** Sources and causes of body roll; shoulder roll decreases with speed. — Shoulder roll 58–75°.
17. **Fiche, G. et al. (2023).** SwimXYZ: A large-scale dataset. ACM SIGGRAPH MIG. — 11520 videí, 48 keypointů, 4 styly.

### Pediatrické zdroje (nově přidané)

18. **Jerszyński, D. et al. (2013).** Changes in selected parameters of swimming technique in the back crawl and the front crawl in young novice swimmers. *Journal of Human Kinetics*, 37, 161–171. DOI: 10.2478/hukin-2013-0037, PMC3796834. — Minimální úhel loktu pod vodou u začínajících dětí (n=11, 8–13 let): 130–156° (front crawl).
19. **Barbosa, T. M. et al. (2019).** Skillful swimming in age-groups is determined by anthropometrics, biomechanics and energetics. *Frontiers in Physiology*, 10, 73. DOI: 10.3389/fphys.2019.00073, PMC6384257. — SR/SL u chlapců 11–13 let ve třech výkonnostních skupinách.
20. **Santos, C. C. et al. (2023).** Performance tiers within a competitive age group of young swimmers are characterized by different kinetic and kinematic behaviors. *Sensors*, 23(11), 5113. PMC10255363. — SR, SL, rychlost u chlapců 12.4 let ve 3 výkonnostních skupinách.
21. **Vorontsov, A. R. (2002).** Multi-year training of young swimmers. In *World Book of Swimming*, pp. 399–424. — Longitudinální data stroke parametrů u mládeže; HR zóny pro věkové skupiny; 4 fáze víceletého tréninku. [Plný text online](https://coachsci.sdsu.edu/swim/bullets/voront16.htm)
22. **Morais, J. E. et al. (2021).** Young Swimmers' Anthropometrics, Biomechanics, Energetics, and Efficiency as Underlying Performance Factors: A Systematic Narrative Review. *Frontiers in Physiology*, 12, 691274. DOI: 10.3389/fphys.2021.691274, PMC8481572. — Přehled biomechaniky dětských plavců vč. IdC. (**Poznámka:** Dříve citováno jako "Barbosa 2021 review" — 1. autor je Morais.)
23. ~~Chen 2023~~ — Odstraněno. IdC u dětí pokrývá Morais et al. (2021) review (#22).
24. **Sanders, R. H. (2007).** Kinematics, coordination, variability, and biological noise in the prone flutter kick at different levels of a "learn-to-swim" programme. *J Sports Sciences*, 25(2), 213–227. DOI: 10.1080/02640410600631025, PMID 17127596. — Kloubové úhly kolene, kyčle, kotníku při flutter kicku napříč úrovněmi; Fourierova analýza frekvence, inter-joint koordinace.
25. **Morais, J. E. et al. (2012).** Linking selected kinematic, anthropometric and hydrodynamic variables to young swimmer performance. *Pediatric Exercise Science*, 24(4), 649–664. DOI: 10.1123/pes.24.4.649, PMID 23196769. — Kinematický a hydrodynamický profil mladých plavců.
26. **Barbosa, T. M. et al. (2014).** Young swimmers' classification based on kinematics, hydrodynamics, and anthropometrics. *J Applied Biomechanics*, 30(2), 310–315. DOI: 10.1123/jab.2013-0038, PMID 24043707. — 67 mladých plavců, 25m front crawl max, kinematika + hydrodynamika.
27. **Morais, J. E. et al. (2018).** The transfer of strength and power into the stroke biomechanics of young swimmers over a 34-week period. *European J Sport Science*, 18(6), 787–795. DOI: 10.1080/17461391.2018.1453869, PMID 29577827. — 27 plavců (13.33 ± 0.85 let), longitudinální, stroke biomechanika.
28. **Silva, A. F. et al. (2019).** Task Constraints and Coordination Flexibility in Young Swimmers. *Motor Control*, 23(4), 535–552. DOI: 10.1123/mc.2018-0070, PMID 31010390. — 18 plavců 13–15 let, IdC, koordinace při různých rychlostech.
29. **Silva, A. F. et al. (2022).** The Effect of a Coordinative Training in Young Swimmers' Performance. *IJERPH*, 19(12), 7020. DOI: 10.3390/ijerph19127020, PMC9222770. — 26 mladých plavců, Qualisys multi-camera, 50m sprint.
30. **Morais, J. E. et al. (2020).** Upper-limb kinematics and kinetics imbalances in the determinants of front-crawl swimming at maximal speed in young international level swimmers. *Scientific Reports*, 10, 11683. DOI: 10.1038/s41598-020-68581-3, PMC7363921. — 22 muži (15.92 let), L/R imbalance horních končetin.
31. **Silva, A. F. et al. (2025).** Front crawl swimming coordination: a systematic review. *Sports Biomechanics*, 24(2), 127–146. DOI: 10.1080/14763141.2022.2125428, PMID 36223481. — Systematic review koordinace front crawlu vč. mládežnických studií.
32. **Morais, J. E. et al. (2024).** Effects of anthropometrics, thrust, and drag on stroke kinematics and 100m performance of young swimmers using path-analysis modeling. *Scand J Med Sci Sports*, 34(2), e14578. DOI: 10.1111/sms.14578, PMID 38389142. — 25 adolescentů (15.75 let), path analysis.
33. **Morais, J. E. et al. (2023).** Identifying Differences in Swimming Speed Fluctuation in Age-Group Swimmers by Statistical Parametric Mapping. *J Sports Science & Medicine*, 22(2), 358–366. DOI: 10.52082/jssm.2023.358, PMC10244994. — Intracyklická rychlostní variace u mládežníků.
34. **Morais, J. E. et al. (2022).** Young Swimmers' Classification Based on Performance and Biomechanical Determinants: Determining Similarities Through Cluster Analysis. *Motor Control*, 26(3), 396–411. DOI: 10.1123/mc.2021-0126, PMID 35483698. — 38 plavců (15–16 let), cluster analýza kinematiky.

### Zdroje z coachsci.sdsu.edu (Swimming Science Journal)

35. **Rushall, B. S.** Crawl Stroke Body Dynamics in Male Champions. *Swimming Science Bulletin* #26. — 3D analýza body roll u olympijských šampionů (Perkins, Sadovyi, Popov, Hoffman). Shoulder roll > 40° u všech; Perkins fatigue data: hips 19°→42°, shoulders 49°→41° (40m vs 1440m). [Online](https://coachsci.sdsu.edu/swim/bullets/bodydyns.htm)
36. **Keppenham, B. C. & Yanai, T. (1995).** Limb motions and body roll in skilled and unskilled front crawl swimmers. *MSSE*, 27(5), Supplement abstract 1299. — Skilled: shoulders 80° total, hips 50°; unskilled: 70°/40°. Skilled roll simultaneously, unskilled sequentially. [Online](https://coachsci.sdsu.edu/swim/biomechs/keppenha.htm)
37. **Lee, J., Mellifont, R., Winstanley, J. & Burkett, B. (2008).** Body roll in simulated freestyle swimming. *Int J Sports Med*, 29, 569–573. — Breathing stroke mění roll sequence (head → hip → chest); early head turn increases drag. [Online](https://coachsci.sdsu.edu/swim/biomechs/lee.htm)
38. **Psycharakis, S. & McCabe, C. (2010).** Shoulder and hip roll differences between breathing and non-breathing conditions in front crawl swimming. BMS Oslo. — Shoulder roll increases mainly towards breathing side; hip roll and velocity unaffected. [Online](https://coachsci.sdsu.edu/swim/biomechs/psychara.htm)
39. **Rouard, A. & Billat, R. (1990).** Influences of sex and level of performance on freestyle stroke: an electromyographic and kinematic study. *Int J Sports Med*, 11(2), 150–155. — Časové rozložení fáze záběru: pull (45–135°) = ~19 % cyklu. Bent-arm pull = nižší svalová aktivace, lepší efektivita. [Online](https://coachsci.sdsu.edu/swim/biomechs/rouard.htm)
40. **Kennedy, P., Brown, P., Chengalur, S. & Nelson, R. (1990).** Analysis of male and female Olympic swimmers in the 100m events. *Int J Sport Biomech*, 6, 187–197. — Males 9.7 % longer SL, only 1 % higher SR. SL = primary performance predictor, koreluje s výškou. [Online](https://coachsci.sdsu.edu/swim/biomechs/kennedy.htm)
41. **Grimston, S. & Hay, J. (1986).** Relationships among anthropometric and stroking characteristics of college swimmers. *MSSE*, 18(1), 60–68. — Antropometrie vysvětluje 89 % variance SL, ale jen 17 % variance rychlosti. [Online](https://coachsci.sdsu.edu/swim/biomechs/grimston.htm)
42. **Huot-Marchand, F., Nesi, X., Sidney, M., Alberty, M. & Pelayo, P. (2005).** Variations of stroking parameters associated with 200m competitive performance improvement in top-standard front crawl swimmers. *Sports Biomech*, 4(1), 89–100. — 65 % elitních plavců zlepšilo výkon přes zvýšení SR (ne SL). r = 0.98 korelace SR/SL. [Online](https://coachsci.sdsu.edu/swim/biomechs/huot.htm)
43. **Millet, G. P., Chollet, D., Chalies, S. & Chatard, J. (2002).** Coordination in front crawl in elite triathletes and elite swimmers. *Int J Sports Med*, 23(2), 99–104. — Catch-up „rapidly disappeared" u elite swimmers při zvýšení rychlosti, ale přetrvává u triatlonistů. [Online](https://coachsci.sdsu.edu/swim/biomechs/millet.htm)
44. **Schnitzler, C., Seifert, L., Ernwein, V. & Chollet, D. (2008).** Arm coordination adaptations assessment in swimming. *Int J Sports Med*, 29(6), 480–486. — IVV jako „diagnostic index of stroking technique error". Muži mají větší catch-up než ženy při stejné rychlosti. [Online](https://coachsci.sdsu.edu/swim/biomechs/schnitzl.htm)
45. **Fernandes, R., Keskinen, K., Querido, A., Machado, L. & Vilas-Boas, J. P. (2010).** Relationship between IdC and energy cost of swimming in expert swimmers. *BMS Oslo*. — IdC a energy cost korelují s rychlostí, ale ne přímo mezi sebou. „Catch-up stroking is not a technique that should be encouraged." [Online](https://coachsci.sdsu.edu/swim/biomechs/fernande.htm)
46. **Havriluk, R. (2010).** Performance level differences in swimming drag coefficient. *BMS Oslo*. — Drag coefficient effect size ~2× strength effect size u 80 swimmers. 7 z 8 gender × stroke kombinací: drag = lepší diskriminátor výkonu než síla. [Online](https://coachsci.sdsu.edu/swim/biomechs/havriluk.htm)
47. **Keys, M., Lyttle, A., Blanksby, B. & Cheng, L. (2010).** A full body computational fluid dynamic analysis of the freestyle stroke of a previous Olympic swimmer. *BMS Oslo*. — Hand-forearm perpendicular to flow = peak propulsive force. Transient pressure wave at 0.3m depth. [Online](https://coachsci.sdsu.edu/swim/biomechs/keys.htm)
48. **Yanai, T. & Hay, J. (1996).** Combinations of cycle rate and length for minimizing the muscular effort in front crawl swimming. *23rd ISBS Proceedings*. — >70 % impingementů ramene při hand entry, 30 % při zahájení pull. Body roll nekoreluje s impingementem. Prevence: flexe lokte při vstupu. [Online](https://coachsci.sdsu.edu/swim/biomechs/yanai.htm)
49. **Seifert, L., Chollet, D. & Bardy, B. (2007a).** Effect of swimming velocity on arm coordination in the front crawl. *J Sports Sci*, 22(6), 651–660. — Práh přechodu koordinace: ~1.8 m/s (~200m tempo). 3 koordinační módy: opposition, catch-up, superposition. SR 40–50 záběrů/min jako norma. [Online](https://coachsci.sdsu.edu/swim/biomechs/seifert.htm)
50. **Seifert, L., Chollet, D. & Chatard, J. (2007b).** Changes during a 100-m front crawl: effects of performance level and gender. *MSSE*, 39(10), 1784–1793. — Pomalejší plavci mění koordinaci od 3. délky; rychlí udržují stabilitu celých 100m.
51. **Deschodt, V. J., Arsac, L. M. & Rouard, A. H. (1999).** Relative contribution of arms and legs in humans to propulsion in 25-m sprint front-crawl swimming. *Eur J Appl Physiol*, 80, 192–199. — Kopání zlepšuje trajektorii zápěstí pod vodou → ~+10 % rychlosti. Velká inter-individuální variabilita. [Online](https://coachsci.sdsu.edu/swim/biomechs/deschodt.htm)
52. **Brooks, R. W., Lance, C. C. & Sawhill, J. A. (2000).** Kicking: primarily for balance, not propulsion. *BMS Melbourne*. — Nohy primárně zvedají těžiště a udržují alignment. Lift pažemi: r = .94; horizontální propulze pažemi: r = .84. [Online](https://coachsci.sdsu.edu/swim/biomechs/brooks.htm)
53. **Psycharakis, S. G., Naemi, R., Connaboy, C., McCabe, C. & Sanders, R. (2010).** Intra-cyclic variation of the velocity of the centre of mass of the body in front crawl swimming. *J Sports Sci*, 28(6), 651–660. — IVV zůstává relativně konstantní celých 200m; nekoreluje přímo s výkonem. [Online](https://coachsci.sdsu.edu/swim/biomechs/psychar3.htm)
54. **Strumbelj, B., Usaj, A. & Kapus, V. (2007).** The influence of using a snorkel on physiological and biomechanical responses in front crawl swimming. *Kinesiologia Slovenica*, 13(1), 14–22. — Šnorchl mění techniku (eliminace dýchání → odlišný body roll a timing); videa se šnorchlem nereprezentují závodní techniku.

### UDK, Start a Turn zdroje (nově přidané — březen 2026)

55. **Alves, F., Lopes, P., Veloso, A. & Martins-Silva, A. (2006).** Influence of body position on dolphin kick kinematics. *Portuguese J Sport Sciences*, 6(Suppl. 2), 12–14. — UDK kinematics prone/dorsal/lateral: frequency 2.08–2.35 Hz, amplitude 0.50–0.59 m, velocity 1.42–1.46 m/s.
56. **Arellano, R., Pardillo, S. & Gavilán, A. (1999).** Underwater undulatory swimming: kinematic characteristics, vortex generation and application during the start, turn and swimming strokes. *XX ISBS Proceedings*. — Elite UDK velocity 1.69 m/s, frequency 2.22 Hz.
57. **Connaboy, C., Coleman, S. & Sanders, R. (2009).** Hydrodynamics of undulatory underwater swimming: a review. *Sports Biomechanics*, 8(4), 360–380. — Body wave characteristics, Strouhal number 0.59–0.88, propulsive efficiency 11–29 %.
58. **Connaboy, C., Naemi, R., Brown, S., Psycharakis, S., McCabe, C., Coleman, S. & Sanders, R. (2015).** The key kinematic determinants of undulatory underwater swimming at maximal velocity. *J Sports Sciences*. — Ankle + knee motion = 93.3 % variance; body wave velocity r = 0.78. [PDF](https://www.pure.ed.ac.uk/ws/files/21759173/Connaboy_et_al_2015_version_approved_for_publication.pdf)
59. **Rejman, M., Kwaśna, A. & Chrobot, M. (2017).** Kinematic analysis of undulatory underwater swimming performed by young swimmers. *ISBS Proceedings*, 35(1). — Young swimmers: frequency 2.00 Hz, amplitude 0.46 m, velocity 1.08 m/s, St = 0.83.
60. **Higgs, A. J., Pease, D. L. & Sanders, R. H.** Angular velocities and body wave velocity in underwater dolphin kick. — Knee angular velocity: downkick 260°/s, upkick 190°/s; peak vertical toe velocity correlated with UDK velocity (r = 0.85).
61. **Vennell, R., Pease, D. & Wilson, B. (2006).** Wave drag on human swimmers. *J Biomechanics*, 39(4), 664–671. — Wave drag < 5 % at depth > 0.5 m (1 m/s), > 0.7 m (2 m/s).
62. **Lyttle, A. & Blanksby, B. (1999).** Optimising gliding and kicking in underwater swimming. *ISBS Proceedings*. — Drag reduction 15–18 % at 0.4 m depth; optimal glide depth 0.4–0.75 m. [ISBS](https://ojs.ub.uni-konstanz.de/cpa/article/view/2531)
63. **Elipot, M., Dietrich, G., Heilard, P. & Houel, N. (2009).** High-level swimmers' kinetic efficiency during the underwater phase of a grab start. *J Applied Biomechanics*, 25(1), 49–65. — Optimal kick initiation ~6 m from wall.
64. **Houel, N. & Elipot, M.** Velocity decay analysis after push-off. — Velocity at 5.5 m: 2.18 m/s, at 7.5 m: 1.76 m/s; premature kick initiation 1.69 m too early on average.
65. **Vantorre, J., Chollet, D. & Seifert, L. (2014).** Biomechanical analysis of the swim-start: a review. *J Sports Science & Medicine*, 13(2), 223–231. [PMC3990873](https://pmc.ncbi.nlm.nih.gov/articles/PMC3990873/) — 6 start phases; start contributes 0.8–26.1 % of race time; glide velocity minimum 2 m/s. ✅ `Vantorre_2014_Swim_Start_Review.pdf`
66. **Tor, E., Pease, D. L. & Ball, K. A. (2020).** Key parameters of the swimming start and their relationship to start performance. *J Sports Sciences*, 38(10), 1178–1186. [PMC7598512](https://pmc.ncbi.nlm.nih.gov/articles/PMC7598512/) — Entry angle ~20–22°; per 1 rad flatter = −0.5 s; flight distance males 3.2 m.
67. **Benjanuvatra, N., Lyttle, A., Blanksby, B. & Larkin, D. (2007).** Analysis of elite and non-elite grab and track start swimmers. *Int J Sport Biomech*. — Elite take-off angle 27.45 ± 5.99°, non-elite 39.62 ± 13.19°.
68. **Guimaraes, A. & Hay, J. (1985).** A mechanical analysis of the grab starting technique in swimming. *Int J Sport Biomech*, 1, 25–35. — Glide time explains 95 % variance of start time (r = 0.97).
69. **Cossor, J. & Mason, B. (2001).** Swim start performances at the Sydney 2000 Olympic Games. *XIX ISBS Proceedings*. — Negative correlation UW velocity ↔ 15m time (r = −0.734).
70. **Puel, F., Morlier, J., Mesnard, M. & Hellard, P. (2022).** Influence of wall contact time and tuck index on tumble turn performance in competitive swimming. *Frontiers in Sports and Active Living*, 4, 925273. [PMC9354539](https://pmc.ncbi.nlm.nih.gov/articles/PMC9354539/) — WCT males 0.37 s; tuck index optimal 0.64–0.77; push-off velocity 2.19 m/s.
71. **PMC6409673 (2019).** Kinetic analysis of tumble turns — countermovement force 875–973 N; push-off in body weights 1.1–1.5 BW.
72. **PMC12134280 (2025).** Phase-specific determinants of 100m freestyle performance — turn time ~20 % of total; breakout distance 7.11 m (males); UW speed 2.60 m/s.
73. **PMC8442910 (2021).** Underwater parameters by performance level — elite 100m SC total UW distance 37.50 m; UW speed 2.54 m/s.
74. **PMC8625813 (2021).** Kick start key parameters — max depth 0.90 m; take-off angle 40.6°; flight distance 2.73 m.
75. **Lyttle, A. & Benjanuvatra, N. (2005).** Start contribution to race time: 0.8 % (1500m) to 26.1 % (50m sprint).
76. **Hochstein, S. & Blickhan, R. (2011).** Vortex re-capturing and kinematics in human underwater undulatory swimming. *Human Movement Science*, 30(5), 998–1007. — National swimmers: UDK frequency 1.98–2.13 Hz, velocity 1.23 m/s.
77. **Marinho, D. A., Barbosa, T. M., Reis, V. M., Kjendlie, P. L., Alves, F. B., Vilas-Boas, J. P., Machado, L., Silva, A. J. & Rouboa, A. I. (2009).** Swimming propulsion forces are enhanced by a small finger spread. *J Applied Biomechanics*, 25(1). — Diminishing returns for depth > 0.75 m. [PMC3588683](https://pmc.ncbi.nlm.nih.gov/articles/PMC3588683/)
78. **de Jesus, K. et al.** UDK amplitude decay analysis: first 4 cycles 0.61 m → last 4 cycles 0.55 m.
79. **Bulgakova, N. & Makarenko, L. (1966).** Streamlined hands = 7 % less drag than shoulder-width arms.

> **Poznámka:** [Swimming Science Journal](https://coachsci.sdsu.edu/swim/index.htm) (coachsci.sdsu.edu, B. S. Rushall, SDSU) je archiv 115+ abstraktů biomechaniky plavání a originálních článků. Obsahuje abstrakty konferenčních příspěvků jinak nedostupných online (Cappaert 1996, Keppenham 1995 aj.) a detailní analýzy techniky olympijských šampionů.

### Stav stažení zdrojů

- [x] Schnitzler, Seifert & Button (2021) — `Schnitzler_Seifert_Button_2021_adaptability_swimming.pdf`
- [x] Seifert, Chollet & Bardy (2004) — `Seifert_2004_velocity_arm_coordination.pdf`
- [x] Matsuda et al. (2014) — `Matsuda_2014_intracyclic_velocity_coordination.pdf`
- [x] Potdevin et al. (2006) — `Potdevin_2006_stroke_frequency_coordination.pdf`
- [x] Correia et al. (2023) — `Correia_2023_400m_frontcrawl_meta_analysis.pdf`
- [x] Staunton et al. (2025) — `Staunton_2025_SR_SL_dynamics_elite.pdf`
- [x] Cappaert et al. (1996) — abstrakt online na coachsci.sdsu.edu/swim/biomechs/cappaer2.htm
- [x] Jerszyński et al. (2013) — `Stanula_2013_youth_swimming_technique.pdf` (soubor zachovává původní název)
- [x] Barbosa et al. (2019) — `Barbosa_2019_hydrodynamic_young_swimmers.pdf`
- [x] Santos et al. (2023) — `Morais_2023_biomechanical_determinants_young_swimmers.pdf` (soubor zachovává původní název)
- [x] Morais et al. (2021) review — `Barbosa_2021_narrative_review_youth_swimming.pdf` (soubor zachovává původní název; 1. autor je Morais)
- [x] Vorontsov (2002) — plný text online na coachsci.sdsu.edu/swim/bullets/voront16.htm
- [x] Sanders (2007) — `Sanders_2007_flutter_kick_kinematics.pdf`
- [x] Morais et al. (2012) — `Morais_2012_kinematic_profile_young_swimmers.pdf`
- [x] Barbosa et al. (2014 classification) — `Barbosa_2014_classification_kinematics.pdf`
- [x] Morais et al. (2018 transfer) — (staženo, Wiley)
- [x] Silva et al. (2019 coordination) — `Silva_2019_coordination_flexibility.pdf`
- [x] Silva et al. (2022 coordinative training) — (staženo, PMC)
- [x] Morais et al. (2020 imbalances) — (staženo, Nature Scientific Reports)
- [ ] Silva et al. (2025 coordination review) — Sci-Hub nemá (2022+), zkusit ResearchGate/EDD
- [x] Morais et al. (2024 path analysis) — (staženo, Wiley)
- [x] Morais et al. (2023 SPM) — (staženo, PMC)
- [ ] Morais et al. (2022 cluster) — Sci-Hub nemá (2022+), zkusit ResearchGate/EDD

**UDK / Start / Turn zdroje (nově přidané — březen 2026):**

- [x] Vantorre et al. (2014) — `Vantorre_2014_Swim_Start_Review.pdf`
- [ ] Alves et al. (2006) — UDK kinematics, Portuguese J Sport Sciences
- [x] Connaboy et al. (2009) — `Connaboy_2009_UDK_hydrodynamics_review.pdf`
- [x] Connaboy et al. (2015) — `Connaboy_2015_UDK_key_determinants.pdf`
- [ ] Rejman et al. (2017) — young swimmers UDK, ISBS Proceedings (nedostupné na Sci-Hub)
- [x] Tor et al. (2020) — `Tor_2020_start_performance.pdf`
- [x] Puel et al. (2022) — `Puel_2022_tumble_turn_WCT.pdf`
- [x] Vennell et al. (2006) — `Vennell_2006_wave_drag.pdf`
- [x] Lyttle & Blanksby (1999) — `Lyttle_1999_optimal_glide_depth.pdf`
- [ ] Elipot et al. (2009) — kick initiation distance (nedostupné na Sci-Hub)
- [x] PMC12134280 (2025) — `Phase_Determinants_100m_2025_PMC12134280.pdf`
- [x] PMC8442910 (2021) — `Underwater_Parameters_2021_PMC8442910.pdf`
- [x] Nicol et al. (2019, PMC6409673) — `Nicol_2019_tumble_turn_kinetics.pdf`
- [x] Hochstein & Blickhan (2011) — `Hochstein_2011_UDK_vortex.pdf`
- [x] Guimarães & Hay (1985) — `Guimaraes_1985_grab_start_mechanics.pdf`
- [x] Cossor & Mason (2001) — `Cossor_2001_sydney_starts.pdf`
- [x] Kick Start (2021, PMC8625813) — `Kick_Start_2021_PMC8625813.pdf`

---

## 13. Verifikační kontrola

- [x] Každý práh má literární citaci nebo explicitní poznámku o extrapolaci (†)
- [x] Dítě má vždy **nejširší** rozsah a nejvyšší toleranci
- [x] Tolerance klesá: Dítě (±25°/±30°) → Pokročilý (±15°)
- [x] Všechny tabulky (sekce 2–8) reflektují 2 kategorie (Dítě + Pokročilý)
- [x] Metriky jsou extrahovatelné z keypointů (MediaPipe/COCO)
- [x] Dokument pokrývá všech 6 kategorií: kloubové úhly, stroke parametry, rotace trupu, koordinace (IdC), symetrie, streamline
- [x] Dokument pokrývá UDK (sekce 15), starty (sekce 16) a obrátky (sekce 17) s kvantitativními daty a citacemi
- [x] UDK/start/turn prahy pro Dítě mají explicitní caveat o chybějících pediatrických datech
- [x] Souhrnná tabulka (sekce 8.2b) obsahuje nové start/turn/UDK metriky
- [ ] **Nová limitace:** UDK, start a turn literatura je převážně z PMC review článků — některé zdroje (Houel & Elipot, de Jesus, Higgs, Atkison) nemají kompletní citace (konferenční příspěvky). Doplnit plné citace při stahování.
- [x] Dokument je použitelný jako podklad pro sekci 3.4 kapitoly 3 diplomky
- [x] Metriky s nedostatkem pediatrických dat mají explicitní caveat
- [x] Kategorie „Pokročilý" pokrývá celé spektrum dospělých plavců s tolerancí ±15°
- [ ] **Limitace:** U metrik 2, 6, 8 (shoulder angle, body alignment, hand entry) neexistují pediatrická 3D kinematická data — prahy jsou extrapolací z dospělé literatury s rozšířenou tolerancí. Metriky 3, 4 (knee, hip) jsou částečně pokryté Sanders 2007 (flutter kick specificky). Validace na dětské populaci je nezbytná.

### 13.1 Přehled zdrojů dat pro kategorii Dítě

| #     | Metrika                    | Pediatrický zdroj                                                                 | Typ dat                                                   | Stav                  |
| ----- | -------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------- | --------------------- |
| 1a–1d | Elbow angle (všechny fáze) | Jerszyński 2013 (n=11, 8–13 let)                                                  | Přímé měření (min. úhel pod vodou), ale ne per-phase      | Částečný              |
| 2     | Shoulder angle             | Barbosa 2014 (67 plavců, celkový kinem. profil); Morais 2012 (kinem. + hydrodyn.) | Nepřímé — celková kinematika, ne izolovaný shoulder angle | † Stále extrapolace   |
| 3     | Knee angle                 | **Sanders 2007** (flutter kick kinematics, různé úrovně)                          | Přímé měření kloubových úhlů kolene při flutter kicku     | **Částečně vyplněno** |
| 4     | Hip angle                  | **Sanders 2007** (flutter kick kinematics, různé úrovně)                          | Přímé měření kloubových úhlů kyčle při flutter kicku      | **Částečně vyplněno** |
| 5     | Shoulder roll              | Jerszyński 2013 (n=11); Silva 2022 (Qualisys multi-camera)                        | Přímé měření, ale malé vzorky                             | Částečný              |
| 6     | Body alignment             | **Morais 2012** (angle of attack / body position u mladých plavců)                | Nepřímé — angle of attack, ne head-spine-pelvis úhel      | † Stále extrapolace   |
| 7     | Stroke Rate                | Barbosa 2019; Santos 2023; Morais 2018; Morais 2024                               | Přímé měření (velké vzorky, 11–16 let)                    | ✅ OK                  |
| 8     | Hand entry position        | **Žádný**                                                                         | Extrapolace z dospělé literatury                          | † Extrapolace         |
| 10    | IdC                        | **Silva 2019** (18 plavců 13–15 let, IdC); Silva 2025 review                      | Přímé měření IdC u mládeže                                | **Nově pokryto**      |
| 11–12 | L/R asymetrie              | **Morais 2020** (22 plavců 15.92 let, L/R imbalances)                             | Přímé měření L/R kinetiky a kinematiky horních končetin   | **Nově pokryto**      |

**Shrnutí po doplnění literatury (březen 2026):** Z 11 primárních metrik nyní:

- **3 metriky bez pediatrického zdroje:** Shoulder angle (2), body alignment (6), hand entry (8) — prahy zůstávají extrapolací z dospělé literatury.
- **2 metriky částečně pokryté:** Knee (3) a hip (4) — Sanders 2007 pokrývá flutter kick specificky, ne celý stroke cycle.
- **6 metrik s adekvátním pokrytím:** Elbow (1a–1d), shoulder roll (5), stroke rate (7), IdC (10), L/R asymetrie (11–12).
- Per-phase diferenciace metriky 1 (elbow angle per fázi záběru) stále nemá pediatrický zdroj.

**Zůstávající mezery (formulace pro diplomku):** "Pediatrická 3D kinematická data pro úhel ramene, body alignment a hand entry position v plavání neexistují — to je identifikovaná výzkumná mezera. Prahy pro kategorii Dítě u těchto metrik jsou odvozeny extrapolací z dospělé literatury s konzervativně rozšířenou tolerancí (±30°), což minimalizuje false positives."

### 13.2 Sensitivity analysis extrapolovaných prahů

Pro extrapolované metriky (2–4, 6, 8) je klíčová otázka: jak robustní jsou zvolené prahy?

**Navrhovaný postup:** Pro každý práh posunout hodnotu o ±10° a ±20° a zjistit, kolik záběrů v testovacím datasetu změní klasifikaci (z OK na chybu nebo naopak):

- Pokud ±10° změní < 5 % záběrů → práh je **robustní** (leží na plochém místě distribuce)
- Pokud ±10° změní > 20 % záběrů → práh je **křehký** (leží na strmém gradientu distribuce)

**Poznámka:** Tato analýza vyžaduje testovací dataset dětských plavců, který aktuálně není k dispozici. Bude provedena v rámci experimentální kapitoly, pokud se podaří získat data.

### 13.3 Formulace pro obhajobu

Kategorie Dítě funguje jako **conservative estimation mode** — systém identifikuje pouze severe deviations (odchylka > ±30° od extrapolovaného rozsahu), ne nuancované technické chyby. Široké tolerance záměrně minimalizují false positives za cenu nižšího recall. Zdůvodnění:

- Lepší je nevydat upozornění (a zmeškat drobnou chybu) než vydávat falešná upozornění na základě nepodložených prahů
- Trenér používající systém pro děti dostává DTW skóre jako primární metriku (shape similarity nezávisí na absolutních prazích) a pravidlový systém jako sekundární indikátor
- Prioritou je identifikace výrazně odlišné techniky, ne jemné tuning

---

## 14. Validační strategie

Tato sekce popisuje **navrhovaný** validační protokol, ne realizovaný experiment. Podrobná implementace bude v kapitole Experimenty.

### 14.1 Expert annotation protocol

**Návrh:**

1. 2 nezávislí trenéři anotují N videí (minimálně 50 záběrů, ideálně 100+) pomocí standardizované sady 7 typů chyb dle Virag 2014: (1) dropped elbow pull, (2) dropped elbow recovery, (3) eyes-forward head, (4) crossover entry, (5) thumb-first entry, (6) incorrect pull pattern, (7) excessive/insufficient body roll.
2. Každý záběr je anotován per-arm (L/R), celkem 7 × 2 = 14 binárních labels per záběr.
3. **Inter-rater reliability:** Cohen's κ pro každý typ chyby. Přijatelné: κ > 0.6 (substantial agreement).
4. Diskrepance (κ < 0.4) řešeny třetím hodnotitelem nebo konsensem.

**Poznámka:** Tento protokol je navržený, ne realizovaný. Pro diplomovou práci bude realizován v omezeném rozsahu (min. 50 záběrů, 2 hodnotitelé).

### 14.2 Threshold sensitivity analysis

Pro každou metriku s extrapolovanými prahy (Dítě metriky 2–4, 6, 8):

1. Systematicky posunout práh o ±5°, ±10°, ±15°, ±20°
2. Spočítat, kolik záběrů změní klasifikaci (z OK na chybu nebo naopak)
3. Výsledek: sensitivity curve — podíl záběrů s změněnou klasifikací jako funkce posunu prahu

**Interpretace:**

- Práh ±10° změní < 5 % záběrů → **robustní** (systém je stabilní i s nepřesnými prahy)
- Práh ±10° změní > 40 % záběrů → **křehký** (výsledky jsou silně závislé na přesnosti prahu)

### 14.3 Baseline comparison

Porovnání tří přístupů na stejném testovacím datasetu:

1. **Pravidlový systém only:** Metriky + prahy → detekce chyb. Metrika: precision, recall, F1 per error type (ground truth z expert annotation).
2. **DTW-only:** Per-joint DTW cost > threshold → flagování kloubu. Metrika: AUC per joint (per-joint cost vs. expert label).
3. **Combined:** Pravidlový systém + DTW → boosted detekce. Metrika: precision, recall, F1 per error type.

Očekávaný výsledek: Combined > Pravidlový > DTW-only pro known errors; DTW-only > Pravidlový pro novel/unusual technique patterns.

---

## 15. Underwater Dolphin Kick (UDK)

### 15.1 Definice a kontext

**Underwater Dolphin Kick (UDK)** je vlnovitý pohyb celého těla pod hladinou s pažemi ve streamline pozici (nad hlavou). Používá se po startu a po obrátkách jako přechodová fáze mezi odrazem/vstupem do vody a volným plaváním. Pravidla World Aquatics (dříve FINA) povolují podvodní fázi maximálně 15 m od stěny.

> **Proč analyzovat UDK:** U elitních plavců je UDK často nejrychlejší fáze závodu — podvodní rychlost po odrazu (2.18–2.60 m/s) výrazně převyšuje rychlost volného plavání (1.7–2.0 m/s). Elitní 100m freestylisté stráví pod vodou celkem 31–37 m ze 100 m (PMC8442910, 2021). Zlepšení UDK je proto jedním z nejefektivnějších způsobů, jak zrychlit celkový čas.

### 15.2 Frekvence kopů (Kick Frequency)

| Úroveň / studie | Frekvence | Zdroj |
| --- | --- | --- |
| Elite, prone | 2.35 ± 0.27 Hz | Alves et al. 2006 |
| Elite, dorsal | 2.30 ± 0.33 Hz | Alves et al. 2006 |
| Elite, lateral | 2.08 ± 0.36 Hz | Alves et al. 2006 |
| Elite, prone | 2.22 Hz | Arellano et al. 1999 |
| National | 2.13 ± 0.23 Hz | Connaboy et al. 2009 |
| National | 2.26 ± 0.16 Hz | Shimojo et al. |
| National | 1.98–2.13 Hz | Hochstein & Blickhan 2011 |
| Female swimmers | 1.99 ± 0.15 Hz | Yamakawa et al. |
| Young swimmers | 2.00 ± 0.39 Hz | Rejman et al. 2017 |

**Shrnutí:** Elite ~2.1–2.35 Hz, National ~2.0–2.13 Hz, Young ~2.0 Hz. Frekvence samotná negarantuje rychlost — vyšší frekvence zvyšuje energetickou náročnost bez nutného zvýšení rychlosti (Strouhal number trade-off, viz 15.9).

### 15.3 Amplituda kopů (Kick Amplitude)

| Úroveň / studie | Amplituda (peak-to-peak ankle) | Zdroj |
| --- | --- | --- |
| Elite, prone | 0.50 ± 0.06 m | Alves et al. 2006 |
| Elite, dorsal | 0.55 ± 0.08 m | Alves et al. 2006 |
| Elite, lateral | 0.59 ± 0.09 m | Alves et al. 2006 |
| Female swimmers | 0.48 ± 0.05 m | Yamakawa et al. |
| First 4 cycles post-wall | 0.61 ± 0.07 m | de Jesus et al. |
| Last 4 cycles post-wall | 0.55 ± 0.05 m | de Jesus et al. |
| Young swimmers | 0.46 ± 0.08 m | Rejman et al. 2017 |

**Shrnutí:** Elite ~0.48–0.59 m, Young ~0.46 m. Amplituda klesá s vzdáleností od stěny (de Jesus: 0.61 → 0.55 m) — indikátor ztráty síly/konzistence. Příliš velká amplituda zvyšuje čelní odpor.

### 15.4 Rychlost UDK (UDK Velocity)

| Úroveň / studie | Rychlost | Zdroj |
| --- | --- | --- |
| Elite, prone | 1.46 ± 0.15 m/s | Alves et al. 2006 |
| Elite, prone | 1.69 m/s | Arellano et al. 1999 |
| Male elite | 1.75 ± 0.16 m/s | Ikeda et al. |
| National | 1.60 ± 0.12 m/s | Shimojo et al. |
| National | 1.64 ± 0.20 m/s | Willems et al. |
| National | 1.20 ± 0.13 m/s | Connaboy et al. |
| National | 1.23 ± 0.04 m/s | Hochstein & Blickhan 2011 |
| Regional | 1.09 ± 0.13 m/s | Hochstein & Blickhan 2011 |
| Female swimmers | 1.35 ± 0.08 m/s | Yamakawa et al. |
| Young swimmers | 1.08 ± 0.13 m/s | Rejman et al. 2017 |
| At 5.5 m from wall | 2.18 ± 0.21 m/s | Houel et al. |
| At 7.5 m from wall | 1.76 ± 0.15 m/s | Houel et al. |

**Shrnutí:** Elite 1.46–1.85 m/s, National 1.20–1.64 m/s, Young ~1.08 m/s. Rychlost po odrazu od stěny prudce klesá — z 2.18 m/s (5.5 m) na 1.76 m/s (7.5 m). Breakout by měl nastat, když UDK rychlost klesne pod rychlost volného plavání.

### 15.5 Optimální hloubka

| Zjištění | Zdroj |
| --- | --- |
| Wave drag < 5 % total drag při hloubce > 0.5 m (1 m/s) a > 0.7 m (2 m/s) | Vennell et al. 2006 |
| Drag reduction 15–18 % při 0.4 m vs. hladina | Lyttle & Blanksby 1999 |
| Diminishing returns po 0.75 m hloubce | Marinho et al. 2009 |
| Zahájení kopů optimálně ~6 m od stěny | Elipot et al. 2009 |

**Praktické doporučení:** Glide při ~0.4–0.75 m hloubce. Příliš mělko = wave drag; příliš hluboko = delší cesta nahoru při breakoutu. Zahájení kopů by mělo být ~6 m od stěny (Elipot et al. 2009) — průměrný plavec zahajuje kopu o 1.69 m příliš brzy (Houel & Elipot).

### 15.6 Charakteristiky tělesné vlny (Body Wave)

UDK je vlnovitý pohyb, kde vlna progreduje od kyčlí směrem ke kotníkům se zvyšující se amplitudou.

| Parametr | Hodnota | Zdroj |
| --- | --- | --- |
| Body wave speed | 2–2.8× rychlost plavce ve vodě | Connaboy et al. |
| Ankle + knee motion | Vysvětluje 93.3 % variance rychlosti kopů | Connaboy et al. 2015 |
| Peak vertical toe velocity (downkick) | 2.38 m/s | Atkison et al. |
| Peak vertical toe velocity (upkick) | 1.99 m/s | Atkison et al. |
| Knee angular velocity (downkick) | 260 ± 28.9 °/s | Higgs et al. |
| Knee angular velocity (upkick) | 190 ± 43.6 °/s | Higgs et al. |

**Klíčový poznatek:** Efektivní UDK vyžaduje koordinovanou vlnu celého těla (hip → knee → ankle), ne izolovaný pohyb nohou. Fázový posun mezi segmenty je diagnostický — pokud head, hip a ankle oscilují synchronně (bez fázového posunu), jde o flutter kick z kolen, ne o UDK.

### 15.7 Rozsah pohybu kolene při UDK (Knee ROM)

| Úroveň / studie | Knee ROM | Zdroj |
| --- | --- | --- |
| Elite, prone | 119.34 ± 3.70° | Alves et al. |
| Male elite | 109.0 ± 10.8° (min angle) | Ikeda et al. |
| National | 89.6 ± 6.9° | Connaboy et al. |
| Male swimmers | 73.3 ± 6.6° | Yamakawa et al. |

**Srovnání s flutter kickem:** Knee ROM při UDK (73–119°) je výrazně větší než při flutter kicku při volném plavání (sekce 3.3: optimální 140–180°, tj. ROM ~0–40°). UDK vyžaduje hlubší flexi kolene pro generování vlnového pohybu.

### 15.8 Korelace s rychlostí UDK

| Proměnná | Korelace (r) | Zdroj |
| --- | --- | --- |
| Foot resultant acceleration | 0.94 | Alves et al. |
| Kick frequency | 0.90 | Alves et al. |
| Peak vertical toe velocity | 0.85 | Higgs et al. |
| Shoulder angle (streamline) | 0.80 | Ikeda et al. |
| Body wave velocity | 0.78 | Higgs et al. |
| Peak hip angular velocity | 0.73 | Higgs et al. |
| Max knee flexion/extension | 0.84–0.88 | Atkison et al. |

**Poznámka:** Streamline pozice ramen (r = 0.80, Ikeda) potvrzuje, že kvalita streamline je klíčová i během kopání, nejen při glide fázi.

### 15.9 Strouhal number a propulzní efektivita

| Organismus | Strouhal number (St) | Zdroj |
| --- | --- | --- |
| Ryby / delfíni (optimální) | 0.25–0.35 | — |
| Lidští plavci (průměr) | 0.59–0.88 (mean 0.80) | Connaboy et al. 2009 |
| Mladí plavci | 0.83 | Rejman et al. 2017 |

**Propulzní efektivita:** Lidé dosahují pouze 11–29 % propulzní efektivity UDK vs. ~56 % u kytovců (Connaboy et al. 2009). Vyšší frekvence kopů nemusí zvyšovat rychlost — optimalizace spočívá v koordinaci body wave a amplitudy, ne v pouhém zrychlení.

### 15.10 Biomechanické chyby UDK

| Chyba | Popis | Prevalence / zdroj |
| --- | --- | --- |
| Knee-dominant kicking | Iniciace z kolen (quadriceps) místo core/kyčlí — chybí body wave | Velmi časté u age-group plavců |
| Nadměrný pohyb hlavy | Brada příliš zasunutá nebo vystouplá → narušení streamline | Snižuje r = 0.80 korelaci shoulder angle/speed |
| Asymetrický timing | Nerovnoměrný čas downbeat vs. upbeat — slabší plavci tráví příliš dlouho na upbeatu | Connaboy et al. |
| Nadměrná amplituda | Velký kop za cenu zvýšení čelního odporu | Trade-off: amplituda vs. drag |
| Předčasné zahájení kopů | Průměrný plavec zahajuje kopu o 1.69 m příliš brzy po odrazu | Houel & Elipot |
| Příliš malá hloubka | Surfacing příliš brzy → wave drag | Vennell et al. 2006 |

### 15.11 Prahy per úroveň

| Metrika | Dítě (8–14 let)† | Pokročilý (15+) | Zdroj |
| --- | --- | --- | --- |
| Kick frequency | 1.5–2.5 Hz (±0.5 Hz) | 2.0–2.5 Hz (±0.3 Hz) | Rejman 2017; Alves 2006 |
| Kick amplitude | 0.30–0.65 m | 0.40–0.60 m | Rejman 2017; Alves 2006 |
| Kick count (po startu) | 0–6 kopů | 3–8 kopů | Vantorre 2014 |
| Kick count (po obrátce) | 0–5 kopů | 3–7 kopů | — |
| Amplitude consistency (CV) | < 0.40 | < 0.25 | de Jesus et al. |

† **Caveat (Dítě):** Pediatrická data pro UDK prakticky neexistují. Prahy jsou extrapolovány z Rejman et al. 2017 (young swimmers, bez specifikace věku) a rozšířeny o bezpečnostní marži. U dětí 8–14 let je UDK často nerozvinutý nebo zcela chybí — absence UDK u dítěte **není chyba**, ale informace pro trenéra. Systém reportuje „UDK nedetekován" bez negativního hodnocení.

### 15.12 Detekce UDK z keypointů

**Rozlišení UDK vs. flutter kick:**

```
UDK detekce:
1. Paže ve streamline: |wrist_y - ear_y| < threshold AND |elbow_angle - 180°| < 15°
2. Periodická oscilace ankle_y: peak detection → kick frequency
3. Fázový posun: phase_lag(head_y, hip_y, ankle_y) > 0
   - UDK: head vede, hip následuje, ankle jako poslední (body wave)
   - Flutter kick: hip a ankle oscilují přibližně synchronně
4. Amplituda: peak_to_peak(ankle_y) per cycle
5. Všechny keypointy pod water_line
```

**Keypointy (MediaPipe):** ear(7/8), shoulder(11/12), elbow(13/14), wrist(15/16), hip(23/24), knee(25/26), ankle(27/28)

### 15.13 Limitace

- **UDK analýza je spolehlivá primárně z podvodního pohledu kamery.** Z nadvodního bočního pohledu je podvodní fáze zkreslená refrakcí na rozhraní voda/vzduch — pozice keypointů pod hladinou jsou systematicky posunuté.
- Z nadvodního pohledu je možné detekovat **přítomnost/absenci UDK** a **přibližný kick count**, ale ne přesnou amplitudu nebo knee ROM.
- Strouhal number u lidských plavců (0.59–0.88) je daleko od hydrodynamicky optimálního rozsahu (0.25–0.35) — lidské tělo není optimalizované pro undulační lokomoci.

---

## 16. Biomechanika startu

### 16.1 Fáze startu

Vantorre et al. (2014) definují 6 fází plaveckého startu:

```
[Block] → [Flight] → [Entry] → [Glide] → [UDK] → [Breakout] → [Volné plavání]
  (1)        (2)        (3)       (4)       (5)       (6)            (7)
```

1. **Block phase:** Reakční čas + odraz ze startovního bloku
2. **Flight phase:** Tělo ve vzduchu po opuštění bloku
3. **Entry phase:** Vstup těla do vody
4. **Glide phase:** Streamline pozice pod vodou (bez pohybu končetin)
5. **UDK phase:** Podvodní dolphin kick (viz sekce 15)
6. **Breakout:** Přechod na první záběr volného plavání

> **Příspěvek startu k závodu:** Start tvoří 0.8 % (1500m) až 26.1 % (50m sprint) celkového závodního času (Lyttle & Benjanuvatra 2005). Podvodní fáze (0–15 m) je nejdůležitější proměnnou — negativní korelace mezi podvodní rychlostí a časem na 15 m: r = −0.734 (Cossor & Mason 2001).

### 16.2 Entry Angle (úhel vstupu do vody)

**Definice:** Úhel vektoru head → feet vůči horizontále v momentě, kdy hlava protíná vodní hladinu.

| Úroveň / studie | Entry angle | Zdroj |
| --- | --- | --- |
| Elite | 21.25 ± 5.59° | Wilson & Marino 1983 |
| Elite | 27.45 ± 5.99° | Benjanuvatra et al. 2007 |
| Non-elite | 39.62 ± 13.19° | Benjanuvatra et al. 2007 |
| Males, water entry | ~22° | Tor et al. 2020 |
| Females, water entry | ~20° | Tor et al. 2020 |
| Males, COM crossing waterline | ~38° | Tor et al. 2020 |
| Females, COM crossing waterline | ~42° | Tor et al. 2020 |
| Competitive (take-off angle) | 40.6 ± 1.5° | PMC8625813 2021 |

**Zdůvodnění:** Plošší vstup = menší odpor při vstupu do vody = zachování horizontální rychlosti. Tor et al. (2020) kvantifikovali: start time se zkrátí o 0.5 s na každý 1 radian (~57°) plošší entry angle. Elite plavci mají výrazně plošší vstup (21–28°) než non-elite (40°).

**Poznámka:** Rozdíl mezi „entry angle" (úhel těla při vstupu) a „take-off angle" (úhel vzletu z bloku). Take-off angle je vyšší (27–41°), entry angle nižší (20–28°) — tělo se naklání dolů během letu.

### 16.3 Flight Distance a Horizontal Velocity

| Metrika | Males | Females | Zdroj |
| --- | --- | --- | --- |
| Flight distance | 3.2 ± 0.3 m | 2.8 ± 0.2 m | Tor et al. 2020 |
| Horizontal velocity at entry | 4.4 ± 0.3 m/s | 4.0 ± 0.3 m/s | Tor et al. 2020 |
| Horizontal impulse (elite) | 3.60 ± 0.23 N·s | — | Vantorre et al. 2014 |
| Horizontal impulse (non-elite) | 3.17 ± 0.30 N·s | — | Vantorre et al. 2014 |

**Klíčové korelace (Tor et al. 2020):**

- Per 1 m further entry distance → −0.6 s start time
- Per 1 m/s higher horizontal velocity → −0.3 s start time

### 16.4 Streamline Quality

| Zjištění | Zdroj |
| --- | --- |
| Streamlined hands (jedna na druhé) = 7 % méně odporu než paže na šířku ramen | Bulgakova & Makarenko 1966 |
| Glide time vysvětluje 95 % variance start time (r = 0.97) | Guimaraes & Hay 1985 |
| Minimální glide velocity pro udržení výhody: 2 m/s | Vantorre et al. 2014 |
| Maximální hloubka během startu: ~0.90 ± 0.02 m | PMC8625813 2021 |

**Poznámka:** Guimaraes & Hay (1985) zjistili, že glide time je nejsilnější prediktor celkového start time — kvalita streamline pozice je důležitější než síla odrazu.

### 16.5 Breakout Distance a Time to 15m

| Metrika | Elite males | Elite females | Zdroj |
| --- | --- | --- | --- |
| Underwater distance (start) | 8.29 ± 0.95 m | 7.86 ± 0.93 m | PMC12134280 2025 |
| Water breakout distance | 11.88 ± 0.97 m | 11.09 ± 0.88 m | PMC12134280 2025 |
| Underwater speed | 2.49 ± 0.15 m/s | 2.27 ± 0.11 m/s | PMC12134280 2025 |
| Time to 15m | 5.64 ± 0.18 s | 6.41 ± 0.17 s | PMC12134280 2025 |

**Start phase breakdown (PMC12134280 2025, elite 100m FS finalists):**

| Fáze | Podíl na 15m čase |
| --- | --- |
| Block phase | ~11 % |
| Flight | ~5 % |
| Underwater (entry → breakout) | ~56 % |
| Free swim (breakout → 15m) | ~28 % |

### 16.6 Prahy per úroveň

| Metrika | Dítě (8–14 let)† | Pokročilý (15+) | Zdroj |
| --- | --- | --- | --- |
| Entry angle | 25–55° (±20°) | 20–40° (±10°) | Tor 2020; Benjanuvatra 2007 |
| Streamline tightness | Paže < 25° od osy těla | Paže < 10° od osy těla | Vantorre 2014 |
| Streamline duration | Informativní (bez prahu) | > 0.5 s glide před prvním kopem | Guimaraes & Hay 1985 |
| UDK po startu | 0–6 kopů (viz 15.11) | 3–8 kopů (viz 15.11) | Vantorre 2014 |
| Max depth | Informativní | 0.4–0.90 m | PMC8625813; Lyttle 1999 |

† **Caveat (Dítě):** Pediatrická data pro startovní biomechaniku neexistují. Entry angle u dětí bude pravděpodobně vyšší (strmější vstup) kvůli nižší síle odrazu a menší zkušenosti. Rozsah 25–55° je extrapolace z non-elite dospělých (Benjanuvatra 2007: 39.6 ± 13.2°) s rozšířenou tolerancí. U dětí mladších 10 let je start z bloku často nahrazen skokem z okraje bazénu — jiná biomechanika.

### 16.7 Detekce fází startu z keypointů

| Fáze | Detekce | Heuristika |
| --- | --- | --- |
| Flight | Všechny keypointy nad water line, velký Y-displacement | `all_keypoints_y < water_line_y AND velocity_y > threshold` |
| Entry | Postupný pokles keypointů pod water line (hlava → nohy) | `head_y crosses water_line_y downward` |
| Glide (streamline) | Minimální joint movement, body alignment ~180° | `std(joint_angles) < thr AND body_alignment > 170°` |
| UDK | Periodická oscilace, paže u hlavy (viz 15.12) | `ankle_y oscillation AND wrist near head` |
| Breakout | První detekovaný stroke cycle | `wrist crosses water_line upward` |

**Entry angle výpočet:**

```
# V momentě kdy head_y protíná water_line_y:
entry_angle = arctan(|head_y - ankle_y| / |head_x - ankle_x|)
# Alternativně: úhel vektoru head→pelvis vůči horizontále
```

### 16.8 Limitace

- **Boční pohled:** Entry angle a streamline jsou dobře viditelné. Hloubka (z-osa) není.
- **Podvodní fáze:** Pokud kamera je nad vodou, glide a UDK fáze jsou zkreslené refrakcí.
- **Bez kalibrace kamery:** Absolutní vzdálenosti (flight distance, breakout distance v metrech) nelze měřit — pouze relativní odhady z pixelů.
- **Block phase (1-2):** Vyžaduje kameru zaměřenou na startovní blok. Z bočního pohledu u bazénu jsou realisticky detekovatelné fáze 2–7.
- **Temporální rozlišení:** Flight phase trvá ~0.3 s (~9 framů @ 30 FPS) — nízký počet framů pro přesnou detekci entry angle.

---

## 17. Biomechanika obrátek (Flip Turn)

### 17.1 Fáze obrátky

```
[Approach] → [Flip] → [Wall Contact] → [Push-off] → [Streamline] → [UDK] → [Breakout]
    (1)         (2)         (3)             (4)           (5)          (6)       (7)
```

1. **Approach:** Poslední 2–3 záběry před obrátkou
2. **Flip (salto):** Rotace přes hlavu, nohy na stěnu
3. **Wall contact:** Nohy na stěně, příprava odrazu
4. **Push-off:** Odraz od stěny
5. **Streamline:** Klouzání v streamline pozici
6. **UDK:** Podvodní dolphin kick (viz sekce 15)
7. **Breakout:** Přechod na volné plavání

> **Příspěvek obrátky k závodu:** Obrátka tvoří ~20 % celkového času na 100 m freestyle (PMC12134280 2025). V 1500 m je podíl obrátek na celkovém čase ještě vyšší. Elite 100 m SC (short course) plavci stráví celkem 31–37 m pod vodou (všechny obrátky + start, PMC8442910 2021).

### 17.2 Typy obrátek

| Typ | Použití | Klíčový rozdíl |
| --- | --- | --- |
| **Flip turn (salto)** | Kraul, znak | Rotace přes hlavu, nohy na stěnu, push-off na zádech → rotace do kraulu |
| **Open turn** | Prsa, motýlek (+ začátečníci u kraulu) | Dotek stěny rukou, obrat, push-off |

Pro kraul je primární **flip turn**. Open turn u začátečníků lze zmínit jako variantu, ale metriky níže se vztahují k flip turn.

### 17.3 Wall Contact Time (WCT)

**Definice:** Doba, po kterou jsou nohy plavce v kontaktu se stěnou bazénu.

| Podmínka / studie | Males | Females | Zdroj |
| --- | --- | --- | --- |
| Short WCT | 0.30 ± 0.06 s | 0.25 ± 0.06 s | Puel et al. 2022 |
| Reference (optimal) | 0.37 ± 0.04 s | 0.30 ± 0.05 s | Puel et al. 2022 |
| Long WCT | 0.47 ± 0.05 s | 0.40 ± 0.09 s | Puel et al. 2022 |

**Zdůvodnění:** Reference WCT (~0.30–0.37 s) produkuje nejrychlejší 5m round-trip time (5mRTT). Příliš krátký WCT = nedostatečná síla odrazu (nohy nestihnou vyvinout plný impuls). Příliš dlouhý WCT = ztráta času na stěně bez odpovídajícího zvýšení push-off velocity.

### 17.4 Tuck Index

**Definice:** Poměr vzdálenosti chodidel od stěny k délce nohou při prvním kontaktu. Indikátor kompaktnosti tuck pozice.

| Podmínka | Tuck Index | Zdroj |
| --- | --- | --- |
| Reference | 0.65 ± 0.06 | Puel et al. 2022 |
| Optimal (predicted) | 0.70 ± 0.04 (range 0.64–0.77) | Puel et al. 2022 |
| Close tuck | 0.44 ± 0.10 | Puel et al. 2022 |
| Far tuck | 0.78–0.85 | Puel et al. 2022 |

**Zdůvodnění:** Optimal tuck index ~0.64–0.77 maximalizuje push-off velocity. Příliš blízko (close, < 0.50) = kolena příliš ohnutá → mechanicky nevýhodná pozice pro odraz. Příliš daleko (far, > 0.80) = nohy téměř natažené → krátký range of motion pro odraz.

### 17.5 Push-off Velocity

| Podmínka / studie | Males | Females | Zdroj |
| --- | --- | --- | --- |
| Short WCT | 2.05 ± 0.34 m/s | 1.76 ± 0.15 m/s | Puel et al. 2022 |
| Reference | 2.19 ± 0.29 m/s | 1.83 ± 0.14 m/s | Puel et al. 2022 |
| Long WCT | 2.13 ± 0.31 m/s | 1.77 ± 0.11 m/s | Puel et al. 2022 |
| Club to elite range | 1.5–2.5 m/s | — | Lyttle & Blanksby |
| Countermovement (land) | 1.90 ± 0.48 m/s | — | PMC6409673 2019 |

### 17.6 Push-off Force

| Podmínka / studie | Force (N) | Zdroj |
| --- | --- | --- |
| Short WCT | 1,195 ± 416 N | Puel et al. 2022 |
| Reference | 1,061 ± 359 N | Puel et al. 2022 |
| Long WCT (far tuck) | 1,293 ± 521 N | Puel et al. 2022 |
| Countermovement (water) | 875 ± 343 N | PMC6409673 2019 |
| No countermovement (water) | 973 ± 261 N | PMC6409673 2019 |
| Historical range | 536–1,190 N | Various |

**Typický rozsah:** 1.1–1.5 BW (body weight), extrémně až 2.0 BW.

**Poznámka pro SwimAth:** Push-off force nelze přímo měřit z keypointů. Proxy metrika: push-off velocity (odhadnutelná z horizontálního posunu pelvis keypointu po odrazu).

### 17.7 Turn Time Benchmarks

**Elite 100m freestyle finalists (PMC12134280 2025, n=59):**

| Metrika | Males | Females |
| --- | --- | --- |
| Total turn time (20m: 45–65m) | 9.72 ± 0.23 s | 10.90 ± 0.30 s |
| 5m-in time | 2.84 ± 0.11 s | 3.20 ± 0.16 s |
| Water breakout time | 2.75 ± 0.45 s | 2.40 ± 0.67 s |
| 15m-out time | 6.87 ± 0.15 s | 7.71 ± 0.18 s |
| Breakout distance (after turn) | 7.11 ± 0.88 m | 5.82 ± 1.21 m |
| Underwater speed (turn) | 2.60 ± 0.16 m/s | 2.49 ± 0.28 m/s |
| Turn velocity (VT20) | 2.059 ± 0.05 m/s | 1.690 ± 0.03 m/s |

**5m Round-Trip Time (5mRTT) — national level (Puel et al. 2022):**

| Podmínka | Males | Females |
| --- | --- | --- |
| Short WCT | 5.57 ± 0.63 s | 5.93 ± 0.23 s |
| Reference | 5.38 ± 0.49 s | 5.87 ± 0.33 s |
| Long WCT | 5.69 ± 0.51 s | 6.13 ± 0.36 s |

### 17.8 Approach Velocity

| Studie | Males | Females | Zdroj |
| --- | --- | --- | --- |
| National (reference) | 1.70 ± 0.10 m/s | 1.54 ± 0.08 m/s | Puel et al. 2022 |
| Elite 100m FS (implied) | ~1.76 m/s | ~1.56 m/s | PMC12134280 2025 |

**Klíčový poznatek:** Konzistentní approach velocity (stabilní SR v posledních 3 záběrech) je důležitější než absolutní rychlost — zpomalení nebo zrychlení před stěnou narušuje timing flipu.

### 17.9 Optimal Push-off Angle a Streamline

| Parametr | Hodnota | Zdroj |
| --- | --- | --- |
| Optimální knee angle při wall contact | ~90° | Lyttle et al. 1999 |
| Body alignment při push-off | 170–180° (co nejrovnější) | Lyttle et al. 1999 |
| Optimal glide depth po push-off | 0.4–0.75 m | Lyttle & Blanksby 1999 |
| Kick initiation velocity | 1.9–2.2 m/s (zahájit kopu při poklesu na tuto rychlost) | Elipot et al. 2009 |

### 17.10 Prahy per úroveň

| Metrika | Dítě (8–14 let)† | Pokročilý (15+) | Zdroj |
| --- | --- | --- | --- |
| Push-off angle (body alignment) | 150–180° (±25°) | 170–180° (±10°) | Lyttle et al. 1999 |
| Approach SR consistency (CV) | < 0.30 | < 0.15 | — |
| Streamline quality po push-off | Volnější tolerance (viz 16.6) | Tight streamline (viz 16.6) | Puel 2022 |
| UDK po obrátce | Viz 15.11 | Viz 15.11 | — |
| Breakout timing | Informativní | Breakout při UDK speed < swim speed | — |

† **Caveat (Dítě):** Pediatrická data pro flip turn biomechaniku neexistují. Mnoho dětí 8–14 let používá open turn místo flip turn — systém by měl rozlišovat typ obrátky. Prahy jsou extrapolovány z dospělé national-level literatury (Puel 2022) s rozšířenou tolerancí. Push-off force a velocity u dětí budou výrazně nižší kvůli nižší síle dolních končetin.

### 17.11 Biomechanické chyby obrátek

| Chyba | Detekce z keypointů | Severity |
| --- | --- | --- |
| Nekonzistentní approach (SR drop/spike) | SR variance posledních 3 cycles vs. předchozích | Moderate |
| Pomalý flip (otevřený tuck) | Počet framů od zahájení flipu do nohou na stěně | Minor–Moderate |
| Špatný push-off angle (ne-streamline) | body_alignment < 165° po push-off | Moderate–Severe |
| Příliš brzký breakout | Breakout při vysoké UDK velocity (> swim speed) | Moderate |
| Příliš pozdní breakout | Breakout při nízké UDK velocity nebo blízko 15 m | Minor |
| Žádný/slabý UDK | udk_kick_count < 2 po obrátce | Moderate |
| Nekonzistentní UDK amplitude | amplitude CV > 0.30 | Minor |

### 17.12 Detekce fází obrátky z keypointů

| Fáze | Detekce | Heuristika |
| --- | --- | --- |
| Approach | Poslední 2–3 záběry | `pelvis_x` konverguje k hranici záběru |
| Flip | Rychlá rotace celého těla | `angular_velocity(body_alignment)` > threshold |
| Push-off | Rychlý horizontální pohyb od stěny | `velocity_x(pelvis)` > threshold, směr opačný než approach |
| Streamline | Stejné jako u startu | `std(joint_angles) < thr AND body_alignment > 170°` |
| UDK | Viz 15.12 | Viz 15.12 |
| Breakout | První stroke cycle | `wrist crosses water_line upward` |

**Detekce stěny bazénu:** Bez explicitní detekce stěny z obrazu se pozice stěny aproximuje jako x-pozice, kde plavec zastaví horizontální pohyb a začne rotaci. Alternativně: uživatel označí frame obrátky manuálně.

### 17.13 Limitace

- **Flip turn je rychlý pohyb** — při 30 FPS trvá flip ~10–15 framů (~0.3–0.5 s). Pose estimation bude mít výrazně vyšší chybovost (motion blur, okluzně).
- **Stěna bazénu** není keypointem — detekce pozice stěny je heuristická.
- **Wall contact time** nelze přímo měřit z keypointů — proxy: počet framů s nohama na přibližné pozici stěny.
- **Push-off force** nelze měřit z videa — proxy: push-off velocity (horizontální posun pelvis).
- **Podvodní fáze** po push-off: stejné problémy jako u startu (refrakce, viditelnost). UDK analýza vyžaduje podvodní kameru pro spolehlivé výsledky.
- **PoC kvalita:** Spolehlivě detekovatelné jsou approach consistency a streamline quality. Flip speed a push-off angle budou méně přesné.

---

_Last updated: 2026-03-05_
