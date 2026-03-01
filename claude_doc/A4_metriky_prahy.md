# A4 — Biomechanické metriky a prahy pro 3 úrovně plavců

**Autor:** Vít Vágner | **Datum:** 2026-02-22 | **Status:** Research dokument pro kapitolu 3 diplomky

---

## 1. Přehled metrik

Systém SwimAth analyzuje plaveckou techniku kraulu (front crawl) z videa pomocí pose estimation a porovnání s referenčními šablonami. Níže jsou definovány biomechanické metriky extrahované z keypointů, jejich optimální rozsahy pro 3 úrovně plavců a zdůvodnění prahů.

### Úrovně plavců

| Úroveň | Popis | Věk / typická rychlost | Definice |
|--------|-------|------------------------|----------|
| **Dítě** | Rostoucí organismus, kratší končetiny, nezralá motorická koordinace | 8–14 let | Pediatrické biomechanické prahy (Jerszyński 2013; Barbosa 2019; Santos 2023) |
| **Plavec** | Dospělý pravidelný plavec, regionální závodní úroveň | 1:15–2:00 min (50–75 % WR) | Dříve „mírně pokročilý" — prahy beze změny |
| **Kompetitivní** | Závodní plavec, národní/mezinárodní úroveň, systematický trénink | < 1:15 min (> 75 % WR) | Dříve „expert" — prahy beze změny |

Klasifikace dospělých vychází z Schnitzler, Seifert & Button (2021): High = 82.5% WR, Medium = 69.3% WR. Kategorie „Dítě" je definována věkem (8–14 let) a vychází z pediatrické plavecké literatury — biomechanické prahy nelze jednoduše odvodit z % WR kvůli vývojovým rozdílům v antropometrii a motorické koordinaci.

**Zdůvodnění věkového rozmezí 8–14 let:**
- **Dolní hranice 8 let:** minimální věk pro systematický nácvik plavecké techniky. Jerszyński et al. (2013) zahrnovali děti od 8 let.
- **Horní hranice 14 let:** přibližně odpovídá PHV (peak height velocity) — přechodu na dospělou biomechaniku. Po dosažení PHV se mění antropometrické proporce, síla a koordinace.
- Pro plavce 15+ let s dětskou antropometrií systém doporučuje kategorii Plavec s rozšířenou tolerancí.

**Poznámka — dospělý začátečník:** Systém aktuálně nemá samostatnou kategorii pro dospělého začátečníka. Dospělý začátečník by měl použít kategorii Plavec, která má nejširší tolerance u dospělých. Kategorie Dítě je nevhodná — dospělý má jinou antropometrii, sílu a rozsah pohybu.

---

## 2. Stroke parametry

### 2.1 Stroke Rate (SR) — Frekvence záběru

**Definice:** Počet kompletních záběrových cyklů za minutu (cycles/min). Jeden cyklus = záběr levou i pravou paží.

**Jak se měří z keypointů:** Detekce periodicity vertikální pozice zápěstí nebo úhlu ramene. Počet detekovaných cyklů / čas segmentu × 60.

| Úroveň | Sub-max tempo | Maximální tempo | Zdroj |
|--------|---------------|-----------------|-------|
| Dítě | 40–60 cycles/min | 50–65 cycles/min | Barbosa 2019; Santos 2023; Vorontsov 2002 |
| Plavec | 30–45 cycles/min | 42–50 cycles/min | Schnitzler 2021; Chollet 2000 (G2) |
| Kompetitivní | 35–50 cycles/min | 48–65 cycles/min | Schnitzler 2021; Staunton 2025; Chollet 2000 (G1) |

**Zdůvodnění:** Chollet (2000) měřil SR u 43 plavců ve 3 skupinách: G1 (nejlepší) průměr 49.5±4.3 str/min při V100, G3 (nejslabší) 44.8±4.6. Schnitzler (2021) potvrdil u kompetitivních při maximu 54.09±3.99, u plavců 46.05±6.16 cycles/min. Staunton (2025) uvádí elitní sprinterský SR 56–67 cycles/min (50m), 48–55 (100m), 35–48 (1500m). Barbosa (2019) a Santos (2023) uvádějí u dětí 11–13 let SR 0.76–0.93 Hz ≈ 46–56 cycles/min. Děti kompenzují kratší SL vyšším SR — proto je rozsah pro kategorii Dítě posunutý výše.

**Poznámka — širší rozsah SR u Kompetitivních (35–65 cycles/min):** Rozsah 30 cyklů je záměrně širší než u Plavce (20 cyklů), protože elitní plavci adaptují SR dramaticky podle distance: sprint 50m 56–67 cycles/min, 100m 48–55, 1500m 35–48 (Staunton 2025). SR u Kompetitivních proto není diagnostický práh ale populační rozsah zahrnující celé spektrum závodních vzdáleností. Systém by měl SR violations u Kompetitivních vážit méně než u jiných kategorií — odchylka od rozsahu spíše indikuje netypickou vzdálenost než chybnou techniku.

**Poznámka:** SR samotný není indikátorem kvality — záleží na kombinaci SR × SL = V. Děti mohou mít vysoký SR s krátkým SL, ale to je u rostoucího organismu fyziologicky normální, ne nutně chyba techniky.

### 2.2 Stroke Length (SL) — Délka záběru

**Definice:** Vzdálenost, kterou tělo urazí během jednoho kompletního záběrového cyklu (m/stroke).

**Jak se měří z keypointů:** Horizontální posun pelvis keypointu mezi dvěma po sobě jdoucími cykly (pokud je k dispozici globální referenční rámec). Alternativně: V / SR.

**Závislost na rychlosti:** SL není plně automatická metrika — výpočet SL = V / SR vyžaduje absolutní rychlost plavce, která vyžaduje buď kalibraci kamery, nebo uživatelský vstup (délka bazénu + čas úseku). Bez tohoto vstupu se SL nehodnotí (stejně jako SI). Horizontální posun pelvis keypointu v pixelech poskytuje jen relativní odhad a závisí na vzdálenosti kamery.

| Úroveň | Typický SL | Zdroj |
|--------|-----------|-------|
| Dítě | 1.0–2.0 m | Barbosa 2019; Santos 2023 (11–13 let: 1.55–1.93 m) |
| Plavec | 1.5–2.2 m | Chollet 2000 (G2: 2.03–2.45 m); Correia 2023 |
| Kompetitivní | 2.0–2.6 m | Chollet 2000 (G1: 2.01–2.47 m); Staunton 2025 |

**Zdůvodnění:** Craig & Pendergast (1979) formulovali V = SR × SL a ukázali, že lepší plavci udržují vyšší SL. Chollet (2000) zjistil SL = 2.47±0.3 m u G1 při V800. Staunton (2025) uvádí pro elitní muže při 100m: 2.1–2.3 m, při 1500m: 2.2–2.6 m. Santos (2023) a Barbosa (2019) uvádějí SL 1.55–1.93 m u dětí 11–13 let — kratší SL odpovídá kratším končetinám a nižší síle záběru.

### 2.3 Stroke Index (SI) — Index efektivity

**Definice:** SI = V × SL (m²/s). Vyšší SI = efektivnější technika (Costill et al. 1985).

| Úroveň | Typický SI | Zdroj |
|--------|-----------|-------|
| Dítě | < 1.5 m²/s | Barbosa 2011; Sánchez & Arellano 2002 |
| Plavec | 1.5–3.0 m²/s | Chollet 2000; Correia 2023 |
| Kompetitivní | > 3.0 m²/s | Chollet 2000 (G1 V100: 1.76 × 2.15 ≈ 3.8) |

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

**Graceful degradation:** Pokud `phase_confidence < threshold`, systém potlačí fázově závislé metriky (elbow per-phase, IdC) a reportuje jen agregáty (celkový DTW, SR, body roll). Uživateli se zobrazí upozornění: „Detekce fáze záběru není spolehlivá — zobrazuji pouze celkové metriky."

#### Fáze catch (vstup ruky do vody a příprava záběru)

| Úroveň | Optimální rozsah | Tolerance | Zdroj |
|--------|-----------------|-----------|-------|
| Dítě | 100–170° | ±25° | Jerszyński 2013 (extrapolace z min. úhlu pod vodou); Maglischo 2003 |
| Plavec | 130–170° | ±15° | Maglischo 2003 |
| Kompetitivní | 140–170° (natažená paže při vstupu) | ±8° | Maglischo 2003 |

**Zdůvodnění:** Při vstupu ruky do vody by paže měla být téměř natažená (140–170°). Příliš ohnutý loket při catch indikuje předčasný záběr. Ruka vstupuje do vody vpředu před ramenem, prsty napřed. U dětí (8–14 let) je rozsah výrazně širší — Jerszyński et al. (2013) měřili minimální úhel loktu pod vodou u začínajících dětí 8–13 let (n=11) a pozorovali hodnoty 130–156° (front crawl), ale catch fáze nebyla izolovaně měřena. Tolerance ±25° reflektuje vyšší variabilitu dětského pohybu.

**Caveat (Dítě):** Prahy pro kategorii Dítě ve fázi catch jsou odvozeny extrapolací z dospělé literatury a omezeného vzorku Jerszyński et al. (2013, n=11). Jerszyński měřil minimální úhel loktu pod vodou (ne izolovanou catch fázi). Pediatrická 3D kinematická data pro catch fázi neexistují.

#### Fáze pull-through (propulzní záběr pod vodou)

| Úroveň | Optimální rozsah | Tolerance | Zdroj |
|--------|-----------------|-----------|-------|
| Dítě | 80–160° | ±25° | Jerszyński 2013 (min. úhel loktu pod vodou 130–156° u začínajících dětí 8–13 let) |
| Plavec | 80–120° | ±15° | Maglischo 2003; Virag 2014 |
| Kompetitivní | 80–100° (high elbow pull) | ±8° | Maglischo 2003; Virag 2014 |

**Zdůvodnění:** Maglischo (2003) popisuje ideální „high elbow catch" s maximální flexí loktu ~90° uprostřed pull fáze. Virag et al. (2014) zjistili, že „dropped elbow" (loket klesne pod úroveň zápěstí, úhel > 120°) je nejčastější biomechanická chyba u kraulu — vyskytuje se u **61.3% ramen** i u elitních závodních plavců. Při správné technice loket zůstává výše než zápěstí po celou dobu pull-through.

**Detekce chyb:**
- **Dropped elbow:** elbow_y > wrist_y AND elbow_angle > 120° → severity: moderate (120–140°), severe (> 140°)
- **Příliš natažená paže:** elbow_angle > 150° během pull → neefektivní záběr, „paddle" technika

#### Fáze push (dokončení záběru)

| Úroveň | Optimální rozsah | Tolerance | Zdroj |
|--------|-----------------|-----------|-------|
| Dítě | 80–170° | ±25° | Jerszyński 2013 (extrapolace z min. úhlu pod vodou); Cappaert 1996 |
| Plavec | 120–170° | ±15° | Cappaert 1996 |
| Kompetitivní | 140–175° (téměř plné natažení) | ±8° | Cappaert 1996; Maglischo 2003 |

**Zdůvodnění:** Ve fázi push se loket opět natahuje — ruka tlačí vodu směrem ke stehnu. Cappaert et al. (1996) zjistili, že elitní plavci mají vyšší rozšíření loktu ve fázi push než ne-elitní. Plné natažení (> 140°) před výstupem z vody maximalizuje délku propulzní dráhy.

**Poznámka — nízká diskriminační síla:** Fáze push je nejméně diagnosticky citlivá ze všech fází záběru. Rozsah pro Plavce (120–170° = 50°) propustí prakticky jakýkoli reálný úhel. Cappaert (1996) ukazuje směrový signál (elitní = vyšší natažení), ale 2D měření z bočního pohledu nemá dostatečnou přesnost pro užší rozsah — loket se při push pohybuje částečně v transverzální rovině, která je z boku neviditelná. Systém by měl push violations vážit méně než pull-through nebo catch violations.

#### Fáze recovery (přenos paže nad vodou)

| Úroveň | Optimální rozsah | Tolerance | Zdroj |
|--------|-----------------|-----------|-------|
| Dítě | 50–160° | ±25° | Jerszyński 2013 (extrapolace z min. úhlu pod vodou); tolerantní |
| Plavec | 70–130° | ±15° | Virag 2014 |
| Kompetitivní | 80–120° (high elbow recovery) | ±8° | Maglischo 2003; Virag 2014 |

**Zdůvodnění:** Během recovery by loket měl zůstat výše než zápěstí. Dropped elbow při recovery (prevalence 53.2%, Virag 2014) vede k tomu, že loket vstoupí do vody dříve než ruka → nesprávná pozice při hand entry → zvýšené riziko impingementu ramene.

**Detekce chyb (recovery):**
- **Dropped elbow:** elbow_y < wrist_y během nadvodní fáze → severity: moderate/severe
- **Příliš nízký oblouk:** elbow_y blízko k shoulder_y → krátký recovery, zvýšený odpor

### 3.2 Úhel ramene (Shoulder Angle)

**Definice:** Úhel mezi loktem, ramenem a kyčlí. Indikátor rozsahu pohybu a rotace ramene.

**Keypointy:** elbow → shoulder → hip (MediaPipe: 13/14 → 11/12 → 23/24)

| Úroveň | Optimální rozsah | Tolerance | Zdroj |
|--------|-----------------|-----------|-------|
| Dítě | 110–180° | ±30° | Extrapolace z dospělé literatury; rozšířená tolerance |
| Plavec | 130–180° | ±15° | Barbosa 2011; Cappaert 1996 |
| Kompetitivní | 140–180° | ±8° | Maglischo 2003; Cappaert 1996 |

**Zdůvodnění:** Cappaert et al. (1996) porovnávali olympijské a ne-elitní plavce: elitní mají vyšší rozšíření loktu ve fázi push a lepší streamline pozici ramene.

**Caveat (Dítě):** Prahy odvozeny extrapolací z dospělé literatury; pediatrická 3D kinematická data pro úhel ramene neexistují. Tolerance ±30° reflektuje vyšší variabilitu dětského pohybu.

### 3.3 Úhel kolene (Knee Angle)

**Definice:** Úhel mezi kyčlí, kolenem a kotníkem. Indikátor techniky kopání.

**Keypointy:** hip → knee → ankle (MediaPipe: 23/24 → 25/26 → 27/28)

| Úroveň | Optimální rozsah | Tolerance | Zdroj |
|--------|-----------------|-----------|-------|
| Dítě | 120–180° | ±30° | Extrapolace z dospělé literatury; rozšířená tolerance |
| Plavec | 140–180° | ±15° | Arellano 2003; Barbosa 2008 |
| Kompetitivní | 150–180° (téměř natažené) | ±8° | Maglischo 2003 |

**Zdůvodnění:** Efektivní flutter kick vychází z kyčlí, ne z kolen. Maglischo (2003) doporučuje téměř nataženou nohu (150–180°) s mírným ohybem kolene. Přílišné ohýbání (< 130°) indikuje „bicycle kick" — kopání z kolen, které zvyšuje odpor. Arellano et al. (2003) uvádí, že zvýšení frekvence kopu s nataženějším kolenem optimalizuje rychlost.

**Caveat (Dítě):** Prahy odvozeny extrapolací z dospělé literatury; pediatrická 3D kinematická data pro úhel kolene neexistují. U dětí je vyšší flexe kolene částečně fyziologická (kratší končetiny, nižší síla).

### 3.4 Úhel kyčle (Hip Angle)

**Definice:** Úhel mezi ramenem, kyčlí a kolenem. Indikátor pozice těla ve vodě (streamline).

**Keypointy:** shoulder → hip → knee (MediaPipe: 11/12 → 23/24 → 25/26)

| Úroveň | Optimální rozsah | Tolerance | Zdroj |
|--------|-----------------|-----------|-------|
| Dítě | 130–180° | ±30° | Extrapolace z dospělé literatury; rozšířená tolerance |
| Plavec | 150–180° | ±15° | Barbosa 2011 |
| Kompetitivní | 160–180° | ±8° | Maglischo 2003 |

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

| Úroveň | Přijatelná odchylka od shoulder_x | Zdroj |
|--------|-----------------------------------|-------|
| Dítě | ±20 cm (normalizováno na shoulder width) | Extrapolace z Virag 2014; rozšířená tolerance |
| Plavec | ±10 cm | Virag 2014 |
| Kompetitivní | ±5 cm (ruka vstupuje přesně v linii ramene) | Virag 2014; Maglischo 2003 |

**Severity:**
- Crossover (ruka za středovou osou): **severe** — zvyšuje impingement ramene
- Příliš široký vstup (ruka > 1.5× shoulder width laterálně): **moderate** — snižuje efektivitu záběru
- Mírná odchylka: **minor**

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

| Úroveň | Optimální entry_width | Zdroj |
|--------|----------------------|-------|
| Dítě | 0.1–1.2 | Extrapolace; tolerantní |
| Plavec | 0.3–0.9 | Virag 2014 |
| Kompetitivní | 0.3–0.8 (laterálně od hlavy, mediálně od ramene) | Virag 2014; Maglischo 2003 |

---

## 4. Rotace trupu (Body Roll)

### 4.1 Rotace ramen (Shoulder Roll)

**Definice:** Úhel rotace ramenní osy kolem podélné osy těla. Měří se jako úhel vektoru L_shoulder → R_shoulder vůči horizontále (z frontálního pohledu) nebo jako maximální náklon ramen při záběru (z bočního pohledu).

**Keypointy:** Projekce vektoru (L_shoulder − R_shoulder) do roviny kolmé na směr plavání.

| Úroveň | Optimální rozsah (na jednu stranu) | Celkový rozsah L↔R | Zdroj |
|--------|-----------------------------------|---------------------|-------|
| Dítě | 10–60° | 20–120° | Jerszyński 2013 (33–53° shoulder roll u dětí); rozšířená tolerance ±30° |
| Plavec | 30–50° | 60–100° | Psycharakis & Sanders 2010; Cappaert 1995 |
| Kompetitivní | 30–55° | 60–110° | Psycharakis 2008: mean 106.6±8.4° total; Yanai 2001: 58° per side |

**Zdůvodnění:**
- Psycharakis & Sanders (2008) měřili 10 národních/mezinárodních plavců: celkový rozsah rotace ramen (L→R) = **106.6 ± 8.4°**, rotace kyčlí = **50.4 ± 12.3°**.
- Cappaert et al. (1995) u olympijských finalistů: shoulder roll 34.4 ± 1.7° (sub-elite), hip roll −17.8 ± 1.5° (sub-elite) vs. 35.4 ± 2.5° / 8.3 ± 1.5° (elite).
- Virag et al. (2014): optimální body roll ~45° podél podélné osy. Roll > 45° nebo < 45° je považován za chybu (nadměrný/nedostatečný roll).
- Yanai (2001): shoulder roll 58° per side při 1.6 m/s; Yanai (2003): shoulder roll klesá z 75° na 66° při zvýšení rychlosti z 1.3 na 1.6 m/s.
- Psycharakis & Sanders (2008): **rychlejší plavci rotují rameny méně** (P < 0.05 korelace mezi shoulder roll a rychlostí).
- Payton et al. (1999): trunk roll 66° (dýchání) vs 57° (bez dýchání).

**Poznámka k rozsahu Kompetitivní (30–55°):** Rozsah je populační distribuce, ne kvalitativní standard — elitní plavci legitimně variují v závislosti na individuální technice a rychlosti (Psycharakis & Sanders 2008). Dolní hranice 30° (shodná s Plavcem) reflektuje zjištění, že rychlejší plavci rotují rameny méně (P < 0.05).

**Klíčový poznatek:** Rotace ramen je funkce individuální techniky, ne jen úrovně. Pro účely detekce chyb: nedostatečná rotace (< 30° per side) nebo nadměrná rotace (> 60° per side) jsou problematické u dospělých. U dětí je variabilita výrazně vyšší — Jerszyński (2013) pozoroval shoulder roll 33–53° u 11 dětí (8–13 let), ale vzorek je příliš malý na definitivní prahy.

**Caveat (Dítě):** Body roll u dětí je v literatuře identifikován jako výzkumná mezera (Psycharakis 2010). Prahy jsou odvozeny z omezeného vzorku Jerszyński (2013) a rozšířeny o bezpečnostní marži.

### 4.2 Rotace kyčlí (Hip Roll)

| Úroveň | Optimální rozsah (na jednu stranu) | Zdroj |
|--------|-----------------------------------|-------|
| Dítě | 5–40° | Extrapolace; rozšířená tolerance ±30° |
| Plavec | 15–30° | Cappaert 1995 |
| Kompetitivní | 20–35° | Psycharakis 2008: mean 50.4±12.3° total |

**Poznámka:** Kyčle se rotují výrazně méně než ramena. U sub-elitních plavců Cappaert (1995) zjistil opačný směr rotace kyčlí vůči ramenům — to zvyšuje čelní plochu a odpor.

### 4.3 Asymetrie rotace (L/R)

**Definice:** |roll_left − roll_right| — rozdíl v rotaci na dýchající a nedýchající stranu.

| Úroveň | Přijatelná asymetrie | Zdroj |
|--------|---------------------|-------|
| Dítě | < 25° | Extrapolace; rozšířená tolerance |
| Plavec | < 12° | Psycharakis 2008 |
| Kompetitivní | < 8° | Psycharakis 2008: mean 8.2±4.8° shoulder, 5.9±3.9° hip |

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

**Robustnost:** Detekce fází z 2D keypointů je méně přesná než z video analýzy (Chollet používal manuální anotaci). Klíčové body pro automatickou detekci:
- **Začátek propulze:** inflexní bod wrist_x velocity (z pozitivní na negativní)
- **Konec propulze:** wrist opouští oblast pod trupem (wrist_y > hip_y nebo wrist viditelně nad vodou)
- **Hladina vody:** aproximace `water_line_y ≈ mean(shoulder_y_L, shoulder_y_R)` — viz sekce 3.1

### 5.2 Hodnoty IdC podle úrovně a rychlosti

#### Chollet et al. (2000) — originální data (43 plavců, 3 skupiny)

| Skupina | Popis | IdC V800 | IdC V100 | IdC V50 |
|---------|-------|----------|----------|---------|
| G1 (14 plavců) | Nejlepší výkon | −6.9 ± 7.1% | −0.9 ± 5.4% | +2.53 ± 4.4% |
| G2 (15 plavců) | Střední výkon | −6.65 ± 3% | −3.55 ± 4% | −1.6 ± 5.7% |
| G3 (14 plavců) | Nejslabší výkon | −9.4 ± 5.4% | −5.1 ± 5.4% | −3.7 ± 5% |
| Celý vzorek | Průměr | −7.6 ± 6.4% | −3.2 ± 5.1% | −0.9 ± 5.6% |

#### Schnitzler, Seifert & Button (2021) — 3 jasné úrovně

| Úroveň | IdC @ 70% max | IdC @ 100% max | SR @ 100% max |
|--------|---------------|----------------|---------------|
| Kompetitivní (82.5% WR) | −3.4 ± 3.2% | +6.4 ± 5.6% | 54.09 ± 3.99 |
| Plavec (69.3% WR) | −8.1 ± 3.8% | −2.5 ± 4.5% | 46.05 ± 6.16 |
| Dítě (45.4% WR) | +1.2 ± 6.4% | +7.5 ± 7.0% | 45.90 ± 6.05 |

**Upozornění:** Schnitzler (2021) měřil dospělé plavce — skupina „Low" (45.4% WR) jsou dospělí začátečníci, ne děti. Mapování na kategorii Dítě je přibližné; hodnoty IdC a SR slouží jako orientační srovnání. Pozitivní IdC u začátečníků neindikuje kvalitní superpozici — reflektuje nekoordinované, chaotické pohyby paží s vysokou variabilitou (SD 6–9%).

#### Další studie

| Zdroj | Vzorek | IdC |
|-------|--------|-----|
| Matsuda et al. (2014) | Elite @ 75% max | −9.15% |
| Matsuda et al. (2014) | Elite @ max | +1.63% |
| Matsuda et al. (2014) | Beginners @ 75% max | −3.65% |
| Matsuda et al. (2014) | Beginners @ max | +0.27% |
| Correia et al. (2023) meta-analýza | Závodní plavci (400m) | −11.0% (CI: −14.3 to −7.8%) |
| Schnitzler et al. (2009) | Národní úroveň (400m race) | −15.4 to −15.9% |
| Seifert et al. (2010) | Národní vs. regionální | Národní signifikantně vyšší IdC |

### 5.3 Prahy IdC pro SwimAth

| Úroveň | IdC sub-max | IdC max | Interpretace |
|--------|-------------|---------|-------------|
| Dítě | Nehodnotí se | Nehodnotí se | Koordinace je nezralá a variabilní; hodnotí se pouze `std(IdC)` napříč cykly. Barbosa 2021 review: IdC u dětí vykazuje vysokou variabilitu (SD 6–9 %). |
| Plavec | −8% až −3% | −5% až 0% | Catch-up, progrese směrem k opposition |
| Kompetitivní | −4% až 0% | 0% až +5% (superposition) | Opposition/superposition dle rychlosti |

**Poznámka pro implementaci:** IdC je pokročilá metrika vyžadující přesnou detekci fází záběru. V první verzi SwimAth bude implementována jako sekundární metrika. Primární metriky (kloubové úhly, SR, body roll) jsou robustnější.

---

## 6. Body Alignment (Streamline)

### 6.1 Pozice hlavy (Head Position)

**Definice:** Úhel pohledu / pozice hlavy vůči páteři. Virag (2014): „eyes-forward head-carrying angle" je biomechanická chyba s prevalencí **46.8%**.

**Správně:** Hlava v neutrální pozici, imaginární linie od hlavy přes páteř. Plavec se dívá na dno bazénu.
**Chybně:** Hlava zvednutá dopředu (eyes-forward) — zvyšuje odpor, narušuje streamline, zvyšuje riziko impingementu ramene.

**Keypointy:** Úhel mezi nose/ear, neck/spine a pelvis.

| Úroveň | Tolerance | Zdroj |
|--------|-----------|-------|
| Dítě | Hlava zvednutá tolerována s upozorněním | Virag 2014 (extrapolace) |
| Plavec | Hlava by měla být neutrální mimo dýchání | Virag 2014; Maglischo 2003 |
| Kompetitivní | Neutrální pozice povinná | Virag 2014 |

### 6.2 Body Alignment Score

**Definice:** Úhel mezi head, spine2 a pelvis keypointy. Čím blíže 180°, tím lepší streamline.

| Úroveň | Optimální rozsah | Tolerance |
|--------|-----------------|-----------|
| Dítě | 140–180° | ±30° |
| Plavec | 160–180° | ±15° |
| Kompetitivní | 170–180° | ±8° |

---

## 7. Symetrie (L/R Asymmetry)

**Definice:** Pro každý párový kloub (loket L/R, rameno L/R, koleno L/R, kyčel L/R) se počítá: |angle_left − angle_right|. Vysoká asymetrie indikuje nerovnoměrnou techniku.

| Úroveň | Přijatelná asymetrie kloubů | Přijatelná asymetrie body roll |
|--------|----------------------------|-------------------------------|
| Dítě | < 30° | < 25° |
| Plavec | < 15° | < 12° |
| Kompetitivní | < 8° | < 8° |

**Zdroj:** Psycharakis & Sanders (2008): mean shoulder roll asymmetry 8.2 ± 4.8° u národních/mezinárodních plavců. Symetrie je silnější indikátor konzistence techniky než absolutní úhly.

---

## 7b. Integrace metrik s DTW pipeline

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

### 7b.1 Trade-off: Z-normalizace vs. absolutní detekce

Z-normalizace per-joint (sekce 10.4) je nutná pro shape comparison v DTW — umožňuje porovnávat temporální tvar pohybu nezávisle na absolutní flexibilitě plavce. Avšak z-normalizace **odstraňuje amplitudový signál**, který je klíčový pro error detection. Plavec s loktem na 85° (správná high-elbow technika) a plavec s loktem na 140° (dropped elbow) mají po z-normalizaci identické trajektorie, pokud je temporální tvar stejný. DTW komponenta proto **nemůže** detekovat absolutní odchylky od biomechanických norem.

**Kompenzace:** Pravidlový systém operuje na **raw (nenormalizovaných) úhlech** — právě proto je dvouvrstvý přístup nezbytný. DTW hodnotí shape similarity, pravidlový systém hodnotí absolutní hodnoty. Tento trade-off je vědomé designové rozhodnutí.

**Navrhovaná hybrid normalizace (budoucí práce):**
- **Min-max normalizace na temporální osu:** Eliminuje SR-induced stretch (záběry různé délky se zarovnají na stejný počet framů), ale amplituda úhlů se NEZZ-normalizuje.
- **Alternativa:** DTW distance = `shape_distance + α × amplitude_penalty`, kde `amplitude_penalty = |mean(query_j) − mean(ref_j)|` penalizuje systematické posuny absolutní úrovně kloubu j.
- Trade-off: hybrid normalizace zachovává amplitudový signál, ale ztrácí invarianci vůči individuální flexibilitě — vyžaduje per-level referenční šablony (aktuální přístup toto podporuje).

### 7b.2 Fázově podmíněné DTW

DTW zarovnává přes celý cyklus — catch v analyzovaném záběru může matchovat pull v referenci, pokud je warping path dostatečně široký. Per-joint cost pak neřekne, **ve které fázi** je odchylka. Pro lokalizovanou zpětnou vazbu typu „loket příliš natažený při pull" nestačí vědět, že „loket je celkově odlišný".

**Navrhované varianty (budoucí práce):**

1. **DTW separátně na 4 sub-sekvence:** Každá fáze (catch, pull, push, recovery) se porovnává zvlášť → 4 fázově lokalizované skóre per joint. Nevýhoda: vyžaduje spolehlivou detekci fázových hranic v obou sekvencích (viz Phase Confidence výše).
2. **Phase label jako dodatečný feature dimension:** K souřadnicím kloubů přidat one-hot phase label → warping path přirozeně matchuje stejné fáze, protože přechod pull→catch má vysokou cost. Elegantní, ale vyžaduje tuning váhy phase dimension.
3. **Post-hoc phase mapping (minimální implementace):** Po DTW zarovnání zpětně mapovat warping path na fáze reference a reportovat per-phase cost: `cost_catch = Σ dtw_cost[i] where ref_phase[i] == catch`. Nevyžaduje detekci fází v query, pouze v referenční šabloně.

### 7b.3 DBA variance envelope

Aktuální DBA šablona je single average — variabilita populace, ze které byla šablona konstruována, je zahozena. DTW cost 15° u kloubu, kde populace variuje s σ = 20°, je méně alarmující než DTW cost 15° u kloubu s σ = 5°.

**Navržené rozšíření:**
- Spolu s DBA šablonou ukládat **per-frame, per-joint SD** (variance envelope): `σ_template[t][j] = std(aligned_values[t][j])` z trénovacích záběrů po DTW zarovnání k šabloně.
- DTW cost přepočítat na z-skóre: `z_cost_j = dtw_cost_j / σ_template_j`
- Kloub s DTW cost 15° kde σ = 20° → z = 0.75 (v normě). Kloub s DTW cost 15° kde σ = 5° → z = 3.0 (výrazná odchylka).
- Threshold pro flagování: z_cost > 2.0 (mimo 2 SD populace).

---

## 7c. Korelace a kauzální vazby mezi metrikami

### Redundantní páry (double-counting)

Některé metriky sdílejí společný failure mode — jedno biomechanické selhání generuje dvě detekované chyby, což zkresluje celkový obraz a přetěžuje zpětnou vazbu.

| Pár | Typ korelace | Společný failure mode |
|-----|-------------|----------------------|
| Hip angle + Body alignment | Geometrická | Sinking hips — pokles kyčlí způsobí odchylku v obou metrikách současně, protože hip angle je subkomponentou body alignment |
| Body roll asymmetry + L/R joint asymmetry | Kauzální řetězec | Asymetrické dýchání → nedostatečná rotace na jednu stranu → asymetrické kloubové úhly |
| Shoulder angle + Elbow catch angle | Mechanická vazba | Dropped shoulder → dropped catch — rameno a loket tvoří kinematický řetězec |

**Doporučení pro implementaci:** U redundantních párů systém reportuje **primární metriku** (hip angle, body roll asymmetry, elbow catch) a sekundární uvádí jen jako doplňkovou informaci, ne jako samostatnou chybu. Konkrétně:
- Pokud hip_angle violation AND body_alignment violation → reportovat hip angle jako primární, body alignment jako „souvisí s pozicí kyčlí"
- Pokud body_roll_asymmetry AND joint_asymmetry → reportovat body roll jako root cause
- Pokud shoulder_angle violation AND elbow_catch violation → reportovat elbow catch jako primární (přímo měřitelná chyba), shoulder angle jako kontext

### Synergické kombinace (combined rules)

Některé kombinace metrik mají vyšší diagnostickou hodnotu než izolované metriky:

**1. SR × IdC interakce:**
- SR = 50 + IdC = −10% → catch-up degradace při vysokém tempu (warning: plavec nestíhá propulzní navázání)
- SR = 50 + IdC = +2% → agresivní superpozice (OK pro Kompetitivní, warning pro Plavce)
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
if level == "Kompetitivní" and SR > 50 and IdC < -8:
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

## 7d. Temporální stabilita (únavový profil)

Aktuální systém analyzuje jednotlivé záběry izolovaně. Analýza trendu přes série po sobě jdoucích záběrů umožňuje detekovat únavou podmíněnou degradaci techniky.

**Navrhované metriky (implementace v2):**

- **Rolling average DTW cost:** Klouzavý průměr DTW cost přes N consecutive strokes (doporučeno N = 5). Rostoucí trend indikuje degradaci techniky.
- **SR drift:** Nárůst SR v čase (plavec zrychluje tempo, ale zkracuje záběr) — typický únavový vzor.
- **SL drift:** Pokles SL v čase — complementární k SR drift.
- **Korelace SR↑ + IdC↓:** Současný nárůst SR a pokles IdC indikuje catch-up degradation při únavě — plavec nestíhá plynule navazovat propulzní fáze při vyšším tempu.
- **σ(DTW) across strokes:** Rolling variance DTW cost detekuje ztrátu konzistence — unavený plavec má vyšší variabilitu mezi záběry.

**Implementační poznámka:** Vyžaduje analýzu celé série záběrů (ne jednotlivý záběr) a stabilní segmentaci záběrů. V první verzi systému nebude implementováno.

---

## 8. Souhrnná tabulka metrik a prahů

### 8.1 Primární metriky (implementace v1)

| # | Metrika | Jednotka | Dítě (8–14 let) | Plavec | Kompetitivní | Zdroj |
|---|---------|----------|-----------------|-----------|-------------|-------|
| 1a | Elbow angle — catch | ° | 100–170 (±25) | 130–170 (±15) | 140–170 (±8) | Jerszyński 2013; Maglischo 2003 |
| 1b | Elbow angle — pull-through | ° | 80–160 (±25) | 80–120 (±15) | 80–100 (±8) | Jerszyński 2013; Virag 2014 |
| 1c | Elbow angle — push | ° | 80–170 (±25) | 120–170 (±15) | 140–175 (±8) | Jerszyński 2013; Cappaert 1996 |
| 1d | Elbow angle — recovery | ° | 50–160 (±25) | 70–130 (±15) | 80–120 (±8) | Jerszyński 2013; Virag 2014 |
| 2 | Shoulder angle | ° | 110–180 (±30) | 130–180 (±15) | 140–180 (±8) | Extrapolace†; Cappaert 1996 |
| 3 | Knee angle (kick) | ° | 120–180 (±30) | 140–180 (±15) | 150–180 (±8) | Extrapolace†; Maglischo 2003 |
| 4 | Hip angle (streamline) | ° | 130–180 (±30) | 150–180 (±15) | 160–180 (±8) | Extrapolace†; Maglischo 2003 |
| 5 | Shoulder roll (per side) | ° | 10–60 | 30–55 | 30–55 | Jerszyński 2013; Psycharakis 2010 |
| 6 | Body alignment | ° | 140–180 | 160–180 | 170–180 | Extrapolace†; Maglischo 2003 |
| 7 | Stroke Rate | cycles/min | 40–60 | 30–50 | 35–65‡ | Barbosa 2019; Santos 2023; Chollet 2000 |
| 8 | Hand entry position | norm. | 0.1–1.2 | 0.3–0.9 | 0.3–0.8 | Extrapolace†; Virag 2014 |

† **Extrapolace:** Prahy pro kategorii Dítě u metrik 2–4, 6, 8 jsou odvozeny extrapolací z dospělé literatury.

‡ **Širší rozsah SR u Kompetitivních (35–65):** Záměrně pokrývá celé spektrum závodních vzdáleností (sprint 56–67, 1500m 35–48, Staunton 2025). Viz sekce 2.1. Pediatrická 3D kinematická data pro tyto metriky neexistují. Tolerance ±30° (vs. ±25° pro úhel loktu) reflektuje vyšší pohybovou variabilitu dětí.

### 8.2 Sekundární metriky (implementace v2)

| # | Metrika | Jednotka | Dítě (8–14 let) | Plavec | Kompetitivní | Zdroj |
|---|---------|----------|-----------------|-----------|-------------|-------|
| 9 | Stroke Length | m/cycle | 1.0–2.0 | 1.5–2.2 | 2.0–2.6 | Barbosa 2019; Santos 2023; Craig 1979 |
| 10 | Index of Coordination | % | nehodnotí se* | −8 až 0 | −4 až +5 | Chollet 2000; Schnitzler 2021 |
| 11 | L/R joint asymmetry | ° | < 30 | < 15 | < 8 | Extrapolace†; Psycharakis 2008 |
| 12 | Body roll asymmetry | ° | < 25 | < 12 | < 8 | Extrapolace†; Psycharakis 2008 |
| 13 | Hip roll (per side) | ° | 5–40 | 15–35 | 20–35 | Extrapolace†; Psycharakis 2008 |

### 8.3 Tolerance odchylek a severity

Tolerance se liší podle typu metriky:
- **Elbow angle (všechny fáze):** Dítě ±25°, Plavec ±15°, Kompetitivní ±8°
- **Ostatní kloubové úhly (shoulder, knee, hip, body alignment):** Dítě ±30°, Plavec ±15°, Kompetitivní ±8°

| Severity | Dítě | Plavec | Kompetitivní |
|----------|------|-----------|-------------|
| OK | V rozsahu | V rozsahu | V rozsahu |
| Minor | Elbow < 12,5°; ostatní < 15° | Odchylka < 7,5° | Odchylka < 4° |
| Moderate | Elbow < 25°; ostatní < 30° | Odchylka < 15° | Odchylka < 8° |
| Severe | Elbow > 25°; ostatní > 30° | Odchylka > 15° | Odchylka > 8° |

---

## 9. Prevalence biomechanických chyb

Z Virag et al. (2014), studie 31 univerzitních závodních plavců (62 ramen):

| Chyba | Prevalence | Fáze | Detekce z keypointů |
|-------|-----------|------|---------------------|
| Dropped elbow (pull-through) | **61.3%** | Pull-through | elbow_y > wrist_y AND elbow_angle > 120° |
| Dropped elbow (recovery) | **53.2%** | Recovery | elbow_y < wrist_y during aerial phase |
| Eyes-forward head | **46.8%** | Celý cyklus | head_angle deviates from neutral |
| Incorrect hand position (entry) | **45.2%** | Hand entry | hand crosses midline OR too wide |
| Incorrect hand entry angle | **38.7%** | Hand entry | thumb-first entry (rotation of wrist) |
| Incorrect pull-through pattern | **32.3%** | Pull-through | S-shaped or excessive horizontal adduction |

**Klíčový poznatek:** I u závodních plavců jsou biomechanické chyby velmi časté. Dropped elbow je nejčastější chyba a je signifikantně asociován s incorrect hand entry position (P = 0.009) a thumb-first hand entry (P = 0.027).

---

## 10. Extrakce metrik z keypointů

### 10.1 Vstupní formát

- **MediaPipe Pose:** 33 keypointů (x, y, visibility) — používá prototyp
- **SwimXYZ Base:** 48 keypointů (x, y, z) — trénovací data
- **COCO-17/25:** standardní formáty pro ViTPose/RTMPose

### 10.2 Mapování na metriky

| Metrika | Keypointy (MediaPipe) | Výpočet |
|---------|----------------------|---------|
| Elbow angle | shoulder(11/12), elbow(13/14), wrist(15/16) | 3-point angle at vertex (elbow) |
| Shoulder angle | elbow(13/14), shoulder(11/12), hip(23/24) | 3-point angle at vertex (shoulder) |
| Knee angle | hip(23/24), knee(25/26), ankle(27/28) | 3-point angle at vertex (knee) |
| Hip angle | shoulder(11/12), hip(23/24), knee(25/26) | 3-point angle at vertex (hip) |
| Shoulder roll | L_shoulder(11), R_shoulder(12) | arctan((y_L - y_R) / (x_L - x_R)) z frontálního pohledu |
| Hip roll | L_hip(23), R_hip(24) | Analogicky k shoulder roll |
| Body alignment | nose(0)/ear(7,8), mid_shoulder, mid_hip | Angle of 3 midpoints along body axis |
| Stroke rate | wrist(15/16) y-trajectory | Peak detection, count peaks / time |
| Head position | nose(0), mid_shoulder(avg 11,12), mid_hip(avg 23,24) | Deviation from straight line |
| Hand entry position | wrist(15/16), shoulder(11/12), nose(0), mid_hip | \|wrist_x − shoulder_x\| / shoulder_width |
| IdC | wrist(15/16) x+y trajectory pro obě paže | Fázová detekce + lag time (viz sekce 5.1b) |

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

### 10.5 Odvozené features (navržené)

Kromě přímých kloubových úhlů lze z keypointů odvodit features s vyšší diagnostickou hodnotou:

| Feature | Vstup | Výpočet | Účel |
|---------|-------|---------|------|
| Wrist velocity (pull) | wrist_x[t] | d(wrist_x)/dt při pull midpoint | Rozliší paddle (lineární) vs. S-pull (sinusoidální) techniku záběru |
| Temporal L/R lag | wrist_y peaks L vs R | Δt mezi peaky | Časová asymetrie — silnější indikátor než statická L/R odchylka úhlů |
| Shoulder/hip roll ratio | shoulder_roll, hip_roll | ratio + sign agreement | Detekuje opačný hip roll (Cappaert 1995: sub-elitní plavci rotují kyčle opačně) |
| σ(DTW) across strokes | DTW_cost per stroke | rolling variance | Detekce únavy / degradace techniky (viz sekce 7d) |
| Phase duration ratios | phase timestamps | t_pull/t_cycle, t_recovery/t_cycle | Nerovnoměrné rozložení fází — příliš dlouhá recovery indikuje neefektivní přenos paže |

Tyto features jsou navrženy pro implementaci v2. V první verzi systému se extrahují pouze přímé kloubové úhly a stroke parametry.

---

## 11. Specifika podle pohledu kamery

| Pohled | Primární metriky (spolehlivé) | Sekundární (orientační) | Nedostupné |
|--------|------------------------------|------------------------|------------|
| **Boční (side)** | Elbow angle (všechny fáze), knee angle, hip angle, body alignment, stroke rate | Shoulder roll (jen vertikální posuv), shoulder angle | L/R asymetrie, hand entry crossover |
| **Přední (front)** | Shoulder roll, hip roll, L/R asymetrie, hand entry position (crossover, width) | Elbow angle (koronální rovina) | Knee angle (sagitální), body alignment (hloubka) |
| **Podvodní** | Elbow angle (pull-through), hand path | Knee angle | Body roll (refrakce), stroke rate (bubliny), hand entry |

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
15. **Cappaert, J. M. et al. (1995/1996).** Biomechanical highlights of world champion and Olympic swimmers. — Shoulder/hip roll u olympioniků.
16. **Yanai, T. (2001, 2003, 2004).** Sources and causes of body roll; shoulder roll decreases with speed. — Shoulder roll 58–75°.
17. **Fiche, G. et al. (2023).** SwimXYZ: A large-scale dataset. ACM SIGGRAPH MIG. — 11520 videí, 48 keypointů, 4 styly.

### Pediatrické zdroje (nově přidané)

18. **Jerszyński, D. et al. (2013).** Changes in selected parameters of swimming technique in the back crawl and the front crawl in young novice swimmers. *Journal of Human Kinetics*, 37, 161–171. DOI: 10.2478/hukin-2013-0037, PMC3796834. — Minimální úhel loktu pod vodou u začínajících dětí (n=11, 8–13 let): 130–156° (front crawl).
19. **Barbosa, T. M. et al. (2019).** Skillful swimming in age-groups is determined by anthropometrics, biomechanics and energetics. *Frontiers in Physiology*, 10, 73. DOI: 10.3389/fphys.2019.00073, PMC6384257. — SR/SL u chlapců 11–13 let ve třech výkonnostních skupinách.
20. **Santos, C. C. et al. (2023).** Performance tiers within a competitive age group of young swimmers are characterized by different kinetic and kinematic behaviors. *Sensors*, 23(11), 5113. PMC10255363. — SR, SL, rychlost u chlapců 12.4 let ve 3 výkonnostních skupinách.
21. **Vorontsov, A. R. (2002).** Multi-year training of young swimmers. In *World Book of Swimming*, pp. 399–424. — Longitudinální data stroke parametrů u mládeže.
22. **Barbosa, T. M. et al. (2021).** A narrative review of youth swimming biomechanics. *International Journal of Environmental Research and Public Health*, 18(19), 10286. PMC8481572. — Přehled biomechaniky dětských plavců vč. IdC.
23. ~~Chen 2023~~ — Odstraněno. IdC u dětí pokrývá Barbosa et al. (2021) review (#22).

### Stav stažení zdrojů

- [x] Schnitzler, Seifert & Button (2021) — `Schnitzler_Seifert_Button_2021_adaptability_swimming.pdf`
- [ ] Seifert, Chollet & Bardy (2004) — paywall
- [x] Matsuda et al. (2014) — `Matsuda_2014_intracyclic_velocity_coordination.pdf`
- [ ] Potdevin et al. (2006) — paywall
- [x] Correia et al. (2023) — `Correia_2023_400m_frontcrawl_meta_analysis.pdf`
- [ ] Staunton et al. (2025) — PMC12541611
- [ ] Cappaert et al. (1995) — conference proceedings
- [x] Jerszyński et al. (2013) — `Stanula_2013_youth_swimming_technique.pdf` (soubor zachovává původní název)
- [x] Barbosa et al. (2019) — `Barbosa_2019_hydrodynamic_young_swimmers.pdf`
- [x] Santos et al. (2023) — `Morais_2023_biomechanical_determinants_young_swimmers.pdf` (soubor zachovává původní název)
- [x] Barbosa et al. (2021) review — `Barbosa_2021_narrative_review_youth_swimming.pdf`
- [ ] Vorontsov (2002) — kniha, nestaženo

---

## 13. Verifikační kontrola

- [x] Každý práh má literární citaci nebo explicitní poznámku o extrapolaci (†)
- [x] Dítě má vždy **nejširší** rozsah a nejvyšší toleranci
- [x] Tolerance klesá: Dítě (±25°/±30°) → Plavec (±15°) → Kompetitivní (±8°)
- [x] Tabulky jsou konzistentní (monotónní zpřísnění od Dítě po Kompetitivní)
- [x] Metriky jsou extrahovatelné z keypointů (MediaPipe/COCO)
- [x] Dokument pokrývá všech 6 kategorií: kloubové úhly, stroke parametry, rotace trupu, koordinace (IdC), symetrie, streamline
- [x] Dokument je použitelný jako podklad pro sekci 3.4 kapitoly 3 diplomky
- [x] Prahy pro „Plavec" a „Kompetitivní" se nezměnily oproti původním „Mírně pokročilý" a „Expert" (pouze rename)
- [x] Metriky s nedostatkem pediatrických dat mají explicitní caveat
- [ ] **Limitace:** U metrik 2–4, 6, 8 (shoulder, knee, hip, body alignment, hand entry) neexistují pediatrická 3D kinematická data — prahy jsou extrapolací z dospělé literatury s rozšířenou tolerancí. Validace na dětské populaci je nezbytná.

### 13.1 Přehled zdrojů dat pro kategorii Dítě

| # | Metrika | Pediatrický zdroj | Typ dat |
|---|---------|-------------------|---------|
| 1a–1d | Elbow angle (všechny fáze) | Jerszyński 2013 (n=11, 8–13 let) | Přímé měření (min. úhel pod vodou), ale ne per-phase |
| 2 | Shoulder angle | **Žádný** | Extrapolace z dospělé literatury |
| 3 | Knee angle | **Žádný** | Extrapolace z dospělé literatury |
| 4 | Hip angle | **Žádný** | Extrapolace z dospělé literatury |
| 5 | Shoulder roll | Jerszyński 2013 (n=11) | Přímé měření (33–53°), ale malý vzorek |
| 6 | Body alignment | **Žádný** | Extrapolace z dospělé literatury |
| 7 | Stroke Rate | Barbosa 2019; Santos 2023 | Přímé měření (velké vzorky, 11–13 let) |
| 8 | Hand entry position | **Žádný** | Extrapolace z dospělé literatury |

**Shrnutí:** 6 z 11 primárních metrik (2, 3, 4, 6, 8, plus per-phase diferenciace metriky 1) nemá přímý pediatrický zdroj. Jerszyński 2013 (n=11) zahrnuje POUZE beginners — nereprezentuje celé spektrum 8–14 let (chybí talentovaní dětští plavci s vyspělou technikou).

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

_Last updated: 2026-02-22_
