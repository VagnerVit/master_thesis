# Analysis Modes — Koncept přepínačů analýzy

**Autor:** Vit Vagner | **Datum:** 2026-03-05 | **Status:** Implementační návrh (koncept)
**Scope:** Pouze kraul (freestyle). Ostatní styly jako budoucí vývoj.
**Navazuje na:** `A4_metriky_prahy.md` (prahy a metriky), `SwimAth_v2_architektura (1).md` (cílová architektura)

---

## 1. Motivace

Aktuální systém má jednu sadu referenčních rozsahů pro kraul, aplikovanou uniformně bez ohledu na kontext plavání. To je zásadní problém:

- **Sprint (50-100m)** má fundamentálně jinou biomechaniku než **vytrvalost (400m+)**: vyšší SR, agresivnější catch, méně body rollu, 6-beat kick
- **Start** (skok, streamline, breakout) je úplně jiná fáze než volné plavání — jiné klíčové keypointy, jiné metriky
- **Obrátky** (approach, flip/open turn, push-off, streamline, breakout) taktéž vyžadují samostatnou analýzu

V A4 dokumentu (sekce 2.1) je SR explicitně označen jako informativní metrika: _"Bez uživatelského vstupu ‚typ úseku' (sprint/middle/distance) systém SR nehodnotí jako chybu."_ Analysis modes tento problém řeší — uživatel specifikuje kontext a systém použije odpovídající prahy.

---

## 2. Přehled módů

| Mód            | Popis                                      | Typ analýzy                                                              |
| -------------- | ------------------------------------------ | ------------------------------------------------------------------------ |
| **Sprint**     | 50-100m závodní úseky, maximální intenzita | Modifikované prahy (vyšší SR, agresivnější catch, méně body rollu)       |
| **Vytrvalost** | 400m+ distance, sub-maximální intenzita    | Modifikované prahy (nižší SR, delší glide, více body rollu, 2-beat kick) |
| **Se startem** | Video obsahuje skok ze startovního bloku   | Segmentace videa: start (dive + streamline + breakout) + volné plavání   |
| **Obrátky**    | Video obsahuje obrátku/obrátky             | Segmentace videa: approach + turn + push-off + streamline + breakout     |

### Kombinovatelnost módů

Módy nejsou vzájemně exkluzivní. Uživatel vybírá:

1. **Intenzita** (povinné): Sprint NEBO Vytrvalost
2. **Fáze** (volitelné, multi-select): Se startem, S obrátkami

Příklady kombinací:

- Sprint + se startem = 50m závod ze startovního bloku
- Vytrvalost + s obrátkami = 400m+ trénink
- Sprint + se startem + s obrátkami = 100m závod (start + 1 obrátka + finish)

---

## 3. Architektura — jak módy modifikují pipeline

```
Upload: video + úroveň (Dítě/Pokročilý) + pohled + mód (intenzita + fáze)
    |
    v
[Phase Detector] -- pouze pokud mód obsahuje start/obrátky
    | Segmentuje video na fáze: start | plavání | obrátka | plavání | ...
    v
[Pose Estimation] -- na celé video
    |
    v
[Biomechanics Extractor]
    | Používá ModeConfig pro výběr:
    |   - referenčních prahů (sprint vs. vytrvalost)
    |   - aktivních metrik (které se hodnotí)
    |   - tolerancí odchylek
    v
[Comparator] -- DTW + pravidlový systém s mode-specific prahy
    |
    v
[Feedback Generator] -- mode-aware šablony a tipy
    |
    v
Výstup: per-fáze skóre + celkové skóre + feedback
```

### Co mód mění v pipeline

| Komponenta         | Sprint vs. Vytrvalost                                     | Start/Obrátky                                       |
| ------------------ | --------------------------------------------------------- | --------------------------------------------------- |
| Phase Detector     | Nepoužívá se                                              | Segmentuje video na fáze                            |
| Reference prahy    | Jiné optimální rozsahy (tabulka sekce 4)                  | Vlastní sada metrik per fáze                        |
| Aktivní metriky    | Stejné metriky, jiné váhy                                 | Jiné metriky (entry angle, streamline tightness...) |
| Tolerance odchylek | Sprint přísnější na SR; vytrvalost přísnější na body roll | Per-fáze tolerance                                  |
| DTW šablony        | Oddělené šablony sprint/vytrvalost                        | Bez DTW (pravidlový systém)                         |
| Feedback šablony   | Jiné tipy a doporučení                                    | Fáze-specifický feedback                            |

---

## 4. Referenční prahy per mód — Sprint vs. Vytrvalost

### 4.1 Stroke parametry

| Metrika         | Sprint (50-100m) | Vytrvalost (400m+) | Zdroj                                                        |
| --------------- | ---------------- | ------------------ | ------------------------------------------------------------ |
| SR (Pokročilý)  | 48-67 cycles/min | 30-48 cycles/min   | Staunton 2025 (elitní: 50m 56-67, 100m 48-55, 1500m 35-48)   |
| SR (Dítě)       | 50-70 cycles/min | 40-55 cycles/min   | Barbosa 2019; Santos 2023 (extrapolace dle poměru dospělých) |
| IdC (Pokročilý) | -2% až +8%       | -12% až -2%        | Chollet 2000 (V50: +2.5%; V800: -6.9%); Schnitzler 2021      |
| IdC (Dítě)      | Nehodnotí se     | Nehodnotí se       | Vysoká variabilita (Morais 2021)                             |

**Zdůvodnění:**

- Staunton (2025) poskytuje distančně specifická data pro elitní plavce. Sprint = vyšší SR, kratší SL. Distance = nižší SR, delší SL.
- Chollet (2000): IdC roste od catch-up (-6.9% při V800) k opposition/superposition (+2.5% při V50). Seifert (2007): práh přechodu ~1.8 m/s.
- Millet (2002): catch-up při sprintu u pokročilých = chyba koordinace. Catch-up při vytrvalosti = přijatelné.

### 4.2 Kloubové úhly

| Metrika            | Sprint          | Vytrvalost      | Zdůvodnění                                                                                          |
| ------------------ | --------------- | --------------- | --------------------------------------------------------------------------------------------------- |
| Elbow catch        | 120-160° (±12°) | 140-170° (±15°) | Sprint: agresivnější early vertical forearm; vytrvalost: delší glide s nataženou paží               |
| Elbow pull-through | 75-115° (±12°)  | 80-125° (±15°)  | Sprint: hlubší flexe pro maximální propulzi; vytrvalost: mírně menší flexe pro úsporu energie       |
| Elbow recovery     | 60-120° (±12°)  | 70-130° (±15°)  | Sprint: rychlejší recovery, více ohnutý; vytrvalost: relaxovanější                                  |
| Shoulder angle     | 130-180° (±12°) | 130-180° (±15°) | Bez výrazného rozdílu — závisí více na individuální technice                                        |
| Knee angle         | 135-175° (±12°) | 150-180° (±15°) | Sprint: větší flexe kolene (6-beat kick, vyšší amplituda); vytrvalost: téměř natažené (2-beat kick) |
| Hip angle          | 150-180° (±12°) | 155-180° (±15°) | Sprint: mírně nižší kvůli agresivnějšímu kopu; vytrvalost: lepší streamline                         |

**Poznámka k tolerancím:** Sprint má užší tolerance (±12°) než vytrvalost (±15°), protože při maximální intenzitě je menší prostor pro odchylky — každý stupeň stojí výkon. U vytrvalosti je důležitější udržitelnost a úspora energie.

### 4.3 Body roll

| Metrika                             | Sprint | Vytrvalost | Zdroj                                                                                                |
| ----------------------------------- | ------ | ---------- | ---------------------------------------------------------------------------------------------------- |
| Shoulder roll (per side, Pokročilý) | 25-45° | 35-55°     | Yanai 2003: roll klesá z 75° na 66° při zvýšení rychlosti; Psycharakis 2008: rychlejší = méně rotace |
| Shoulder roll (per side, Dítě)      | 10-50° | 15-60°     | Jerszyński 2013; rozšířená tolerance                                                                 |
| Hip roll (Pokročilý)                | 10-25° | 15-35°     | Cappaert 1995; nižší hip roll při sprintu                                                            |
| Roll asymmetrie (Pokročilý)         | < 10°  | < 12°      | Přísnější u sprintu — asymetrie stojí víc výkonu při maximální intenzitě                             |

**Zdůvodnění:**

- Yanai (2003): shoulder roll klesá z 75° na 66° při zvýšení rychlosti z 1.3 na 1.6 m/s
- Psycharakis & Sanders (2008): rychlejší plavci rotují rameny méně (P < 0.05)
- Při sprintu je menší body roll funkční — umožňuje vyšší SR a rychlejší recovery

### 4.4 Kick pattern

Kick pattern je klíčový diferenciátor mezi sprint a vytrvalost módem.

| Metrika                             | Sprint       | Vytrvalost   | Detekce                                        |
| ----------------------------------- | ------------ | ------------ | ---------------------------------------------- |
| Kick count per full cycle           | 5-7 (6-beat) | 1-3 (2-beat) | Oscilace ankle/knee keypointů per stroke cycle |
| Kick amplitude (knee flexion range) | 25-45°       | 10-25°       | max(knee_angle) - min(knee_angle) per kick     |
| Kick regularity (CV)                | < 0.15       | < 0.25       | Coefficient of variation kick-to-kick duration |

**Detekce kick patternu z keypointů:**

1. Extrakce vertikální oscilace ankle keypointů (27/28)
2. Peak detection na ankle_y signálu (podobně jako stroke cycle detection na wrist_y)
3. Počet detekovaných kick peaků per stroke cycle = kick count
4. Amplituda = range of knee angle (25/26) per kick cycle

**Poznámka:** Kick pattern detekce je spolehlivější z bočního pohledu. Z frontálního pohledu jsou nohy často překryté a ankle keypointy mají nízké confidence. U dětí je kick pattern variabilnější a nemusí odpovídat čistému 2-beat nebo 6-beat vzoru.

**Zdůvodnění 2-beat vs 6-beat:**

- Deschodt (1999): kopání zlepšuje trajektorii zápěstí → lepší mechanika paží (~+10% rychlosti)
- Brooks (2000): nohy primárně zvedají těžiště a udržují alignment, ne propulzi
- Sprint: 6-beat kick zajišťuje stabilitu při vysokém SR a maximální propulzi
- Vytrvalost: 2-beat kick šetří energii (nohy spotřebují ~30% celkové energie, ale generují jen ~10% propulze)

### 4.5 Severity per mód

| Severity | Sprint (Pokročilý) | Vytrvalost (Pokročilý) |
| -------- | ------------------ | ---------------------- |
| OK       | V rozsahu          | V rozsahu              |
| Minor    | < 6° od hranice    | < 8° od hranice        |
| Moderate | < 12° od hranice   | < 15° od hranice       |
| Severe   | > 12° od hranice   | > 15° od hranice       |

Pro Dítě zůstávají severity prahy z A4 dokumentu beze změny (±25° elbow, ±30° ostatní) — u dětí nerozlišujeme sprint/vytrvalost tak striktně.

---

## 5. Start analýza (Proof of Concept)

### 5.1 Fáze startu

```
[Startovní blok] → [Odraz] → [Let] → [Vstup] → [Streamline] → [UDK] → [Breakout] → [Volné plavání]
     (1)            (2)        (3)       (4)         (5)          (6)       (7)            (8)
```

Pro analýzu z videa (boční pohled, kamera u bazénu) jsou realisticky detekovatelné fáze 3-8. Fáze 1-2 (na bloku) vyžadují kameru zaměřenou na startovní blok.

**Poznámka k UDK (Underwater Dolphin Kick):** Po vstupu do vody a streamline fázi většina plavců přechází do podvodního dolphin kicku — vlnovitý pohyb celého těla pod hladinou. U elitních plavců je UDK často nejrychlejší fáze závodu. Pravidla FINA povolují podvodní fázi max. 15m od stěny. U amatérů a dětí je UDK často slabá stránka nebo zcela chybí.

### 5.2 Detekce fází z keypointů

| Fáze              | Detekce z keypointů                                         | Heuristika                                                                               |
| ----------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Let (3)           | Všechny keypointy nad vodní hladinou, velký Y-displacement  | `all_keypoints_y < water_line_y AND velocity_y > threshold`                              |
| Vstup (4)         | Postupný pokles keypointů pod water line (hlava → nohy)     | `head_y crosses water_line_y downward`                                                   |
| Streamline (5)    | Minimální joint movement, body alignment ~180°              | `std(joint_angles) < threshold AND body_alignment > 170°`                                |
| UDK (6)           | Periodická oscilace celého těla pod hladinou, paže u hlavy  | `ankle_y oscillation > threshold AND all_keypoints below water_line AND wrist near head` |
| Breakout (7)      | První detekovaný stroke cycle (wrist movement nad hladinou) | `wrist_y oscillation starts AND wrist crosses water_line upward`                         |
| Volné plavání (8) | Normální stroke cycles                                      | Přepnutí na standardní stroke analýzu                                                    |

**Water line detection:** Aproximace přes průměrnou y-pozici ramen v klidových framech (před startem nebo po ustálení plavání). Pro start analýzu je přesnější detekce nutná — okraj bazénu / vodní hladina jako referenční linie.

### 5.3 Metriky startu

| Metrika              | Popis                                     | Detekce z keypointů                                                             | Optimální rozsah (Pokročilý)                |
| -------------------- | ----------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------- |
| Entry angle          | Úhel těla vůči vodní hladině při vstupu   | Úhel vektoru head→feet vůči horizontále v momentě, kdy hlava protíná water line | 30-45° (Maglischo 2003)                     |
| Streamline tightness | Jak těsně jsou paže přitisknuté k hlavě   | `abs(wrist_y - ear_y)` + `abs(elbow_angle - 180°)`                              | Paže < 10° od osy těla                      |
| Streamline duration  | Jak dlouho plavec drží streamline         | Počet framů od vstupu do prvního stroke                                         | Závisí na rychlosti — 3-8m podvodní fáze    |
| Breakout timing      | Rychlost přechodu z UDK do prvního záběru | Framů od konce UDK do peak prvního wrist cycle                                  | Plynulý přechod, bez pauzy                  |
| Depth consistency    | Konzistence hloubky během streamline/UDK  | Variance pelvis_y během streamline + UDK fáze                                   | Nízká variance = lepší                      |
| UDK kick count       | Počet dolphin kopů pod vodou              | Peak detection na ankle_y oscillation během UDK fáze                            | 3-8 kopů (závisí na rychlosti a distanci)   |
| UDK kick frequency   | Frekvence dolphin kopů                    | Počet ankle_y peaků / trvání UDK fáze                                           | 2.5-4.0 Hz (Pokročilý)                      |
| UDK kick amplitude   | Amplituda vlnění těla                     | `max(ankle_y) - min(ankle_y)` per kick cycle, normalizováno na body length      | Konzistentní, bez útlumu                    |
| UDK body undulation  | Vlnovitý pohyb od hlavy přes trup k nohám | Fázový posun oscilace mezi head_y, hip_y, ankle_y                               | Plynulý wave pattern (head -> hip -> ankle) |

### 5.4 Feedback pro start

| Chyba                 | Detekce                             | Feedback (CZ)                                                                             |
| --------------------- | ----------------------------------- | ----------------------------------------------------------------------------------------- |
| Příliš strmý vstup    | entry_angle > 50°                   | "Vstup do vody je příliš strmý — ztrácíte rychlost a hloubku. Zkuste plošší trajektorii." |
| Příliš plochý vstup   | entry_angle < 25°                   | "Vstup je příliš plochý — belly flop efekt zvyšuje odpor. Zkuste mírně strmější úhel."    |
| Neudržený streamline  | streamline_duration < min_threshold | "Streamline fáze je příliš krátká — podvodní fáze je nejrychlejší část, využijte ji."     |
| Volný streamline      | streamline_tightness > threshold    | "Paže nejsou těsně u hlavy — utáhněte streamline pozici pro menší odpor."                 |
| Žádný/slabý UDK       | udk_kick_count < 2                  | "Chybí podvodní dolphin kick — přidejte 3-6 kopů po startu pro vyšší rychlost."           |
| Nízká UDK frekvence   | udk_kick_frequency < 2.0 Hz         | "Dolphin kick je pomalý — zkuste zrychlit frekvenci kopů pod vodou."                      |
| Nekonzistentní UDK    | udk_amplitude CV > 0.3              | "Dolphin kick ztrácí amplitudu — udržujte konzistentní sílu kopů."                        |
| Chybí body undulation | fázový posun head-hip-ankle < thr   | "Dolphin kick vychází jen z nohou — zapojte celé tělo do vlnovitého pohybu."              |
| Pomalý breakout       | breakout_gap > threshold            | "Přechod z podvodní fáze do prvního záběru je pomalý — plynule navažte."                  |

### 5.5 Limitace start analýzy

- **Boční pohled:** Entry angle a streamline jsou dobře viditelné. Hloubka (z-osa) není.
- **Podvodní část:** Pokud kamera je nad vodou, streamline a UDK fáze jsou zkreslené refrakcí. **UDK analýza je spolehlivá primárně z podvodního pohledu kamery.**
- **Bez kalibrace kamery:** Absolutní vzdálenost breakoutu (v metrech) nelze měřit.
- **PoC kvalita:** Detekce fází je heuristická (ne ML), chybovost na reálných datech bude vyšší.
- **UDK vs. flutter kick:** Detekce rozlišuje UDK (celotělová undulace) od flutter kicku (izolovaný pohyb nohou) pomocí fázového posunu head -> hip -> ankle. Pokud fázový posun chybí, jde o flutter kick, ne UDK.

---

## 6. Turn analýza (Proof of Concept)

### 6.1 Fáze obrátky

```
[Approach] → [Flip/Turn] → [Push-off] → [Streamline] → [UDK] → [Breakout] → [Volné plavání]
    (1)          (2)           (3)           (4)          (5)       (6)            (7)
```

### 6.2 Typy obrátek

| Typ                   | Použití                                | Klíčový rozdíl                                                          |
| --------------------- | -------------------------------------- | ----------------------------------------------------------------------- |
| **Flip turn (salto)** | Kraul, znak                            | Rotace přes hlavu, nohy na stěnu, push-off na zádech → rotace do kraulu |
| **Open turn**         | Prsa, motýlek (+ začátečníci u kraulu) | Dotek stěny rukou, obrat, push-off                                      |

Pro kraul je primární **flip turn**. Open turn u začátečníků lze zmínit jako variantu.

### 6.3 Detekce fází z keypointů

| Fáze           | Detekce                                       | Heuristika                                                                     |
| -------------- | --------------------------------------------- | ------------------------------------------------------------------------------ |
| Approach (1)   | Poslední 2-3 záběry před obrátkou             | Plavec se přibližuje ke kraji záběru — `pelvis_x` konverguje k hranici         |
| Flip (2)       | Rychlá rotace celého těla                     | `angular_velocity(body_alignment)` > threshold; keypointy se rychle přesouvají |
| Push-off (3)   | Rychlý horizontální pohyb od stěny            | `velocity_x(pelvis)` > threshold, směr opačný než approach                     |
| Streamline (4) | Stejné jako u startu                          | `std(joint_angles) < threshold AND body_alignment > 170°`                      |
| UDK (5)        | Dolphin kick pod vodou (stejné jako u startu) | `ankle_y oscillation > threshold AND all_keypoints below water_line`           |
| Breakout (6)   | První stroke cycle                            | `wrist_y oscillation starts AND wrist crosses water_line upward`               |

**Detekce stěny bazénu:** Bez explicitní detekce stěny z obrazu se pozice stěny aproximuje jako x-pozice, kde plavec zastaví horizontální pohyb a začne rotaci. Alternativně: uživatel může označit frame obrátky manuálně.

### 6.4 Metriky obrátky

| Metrika              | Popis                                              | Detekce                                                                                 | Optimální (Pokročilý)                                     |
| -------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| Approach consistency | Stabilita SR v posledních 3 záběrech před obrátkou | SR variance posledních 3 cycles vs. předchozích                                         | Nízká variance (plavec nebrzdí ani nezrychluje chaoticky) |
| Flip speed           | Rychlost rotace                                    | Počet framů od zahájení flipu do nohou na stěně                                         | Krátký flip = lepší (ale závisí na FPS)                   |
| Push-off angle       | Úhel těla při odrazení                             | body_alignment angle v prvním framu po push-off                                         | 170-180° (co nejrovnější streamline)                      |
| Push-off power       | Rychlost po odrazu                                 | `max(velocity_x(pelvis))` po push-off                                                   | Vyšší = lepší                                             |
| Streamline quality   | Kvalita streamline po push-off                     | Stejné metriky jako u startu (tightness, duration)                                      | Paže těsně, dlouhý streamline                             |
| UDK metriky          | Dolphin kick po obrátce                            | Stejné jako u startu: kick count, frequency, amplitude, body undulation (viz sekce 5.3) | Viz sekce 5.3                                             |
| Breakout timing      | Kdy plavec zahájí záběry                           | Vzdálenost (ve framech) od stěny do prvního stroke                                      | Optimálně po ztrátě rychlosti pod swimming speed          |

### 6.5 Feedback pro obrátky

| Chyba                   | Feedback (CZ)                                                                |
| ----------------------- | ---------------------------------------------------------------------------- |
| Nekonzistentní approach | "Zpomalení před obrátkou — udržujte stabilní tempo až do stěny."             |
| Pomalý flip             | "Rotace je pomalá — zkuste kompaktnější tuck pozici."                        |
| Špatný push-off angle   | "Odraz není rovný — nohy a trup by měly být v jedné linii."                  |
| Krátký streamline       | "Streamline po obrátce je příliš krátký — využijte podvodní fázi."           |
| Žádný/slabý UDK         | "Chybí podvodní dolphin kick po obrátce — přidejte 3-6 kopů."                |
| Nekonzistentní UDK      | "Dolphin kick po obrátce ztrácí amplitudu — udržujte konzistentní sílu."     |
| Příliš brzký breakout   | "Zahajujete záběry příliš brzy — streamline + UDK je rychlejší než plavání." |
| Příliš pozdní breakout  | "Breakout je příliš pozdě — ztrácíte rychlost v podvodní fázi."              |

### 6.6 Limitace turn analýzy

- **Flip turn je rychlý pohyb** — při 30 FPS trvá flip ~10-15 framů. Pose estimation bude mít výrazně vyšší chybovost (motion blur, okluzě).
- **Stěna bazénu** není keypointem — detekce pozice stěny je heuristická.
- **Podvodní fáze** po push-off: stejné problémy jako u startu (refrakce, viditelnost). UDK analýza vyžaduje podvodní kameru pro spolehlivé výsledky.
- **PoC kvalita:** Spolehlivě detekovatelné jsou approach consistency a streamline quality. Flip speed a push-off angle budou méně přesné.

---

## 7. Feedback per mód

### 7.1 Sprint-specifické tipy

| Situace                              | Feedback                                                                                                   |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| Nízký SR (< 48/min u Pokročilého)    | "Nízká frekvence záběru pro sprint — zkuste zkrátit glide fázi a zrychlit recovery."                       |
| Příliš velký body roll (> 45°)       | "Nadměrná rotace trupu zpomaluje — při sprintu je efektivnější menší rotace (25-40°)."                     |
| Catch-up koordinace (IdC < -5%)      | "Catch-up koordinace při sprintu zpomaluje — záběry by měly plynule navazovat (opposition/superposition)." |
| 2-beat kick detekován                | "Při sprintu je doporučen 6-beat kick pro stabilitu a propulzi."                                           |
| Elbow catch příliš natažený (> 160°) | "Loket při catch je příliš natažený — zkuste agresivnější early vertical forearm."                         |

### 7.2 Vytrvalost-specifické tipy

| Situace                            | Feedback                                                                                           |
| ---------------------------------- | -------------------------------------------------------------------------------------------------- |
| Vysoký SR (> 50/min u Pokročilého) | "Vysoká frekvence záběru pro vytrvalost — zkuste delší glide fázi pro úsporu energie."             |
| Nedostatečný body roll (< 35°)     | "Nedostatečná rotace trupu — při vytrvalosti pomáhá větší rotace efektivnějšímu záběru a dýchání." |
| 6-beat kick detekován              | "Při vytrvalosti zvažte 2-beat kick — šetří energii bez výrazné ztráty rychlosti."                 |
| Vysoká variabilita SR (CV > 0.15)  | "Nekonzistentní tempo — udržujte stabilní rytmus pro efektivní pacing."                            |

### 7.3 Rozdíl ve váhách metrik

| Metrika           | Váha (Sprint) | Váha (Vytrvalost) | Důvod                                                            |
| ----------------- | ------------- | ----------------- | ---------------------------------------------------------------- |
| SR                | Vysoká        | Střední           | Sprint: SR je klíčový parametr výkonu                            |
| Body roll         | Střední       | Vysoká            | Vytrvalost: roll je důležitější pro efektivitu a dýchání         |
| Elbow catch       | Vysoká        | Střední           | Sprint: agresivní catch = klíčová propulze                       |
| Knee angle (kick) | Vysoká        | Nízká             | Sprint: 6-beat kick je kritický; vytrvalost: 2-beat je OK        |
| IdC               | Vysoká        | Střední           | Sprint: superposition je cíl; vytrvalost: catch-up je přijatelný |
| Symetrie L/R      | Vysoká        | Střední           | Sprint: asymetrie stojí víc výkonu                               |

---

## 8. Upload flow — UI návrh

### 8.1 Parametry analýzy (rozšíření stávajícího upload formuláře)

```
Stávající parametry:
  - Úroveň plavce: Dítě (8-14) / Pokročilý (15+)
  - Pohled kamery: Z boku / Zepředu / Pod vodou
  - Plavecký styl: Kraul (jediný v scope diplomky)

Nové parametry (analysis mode):
  - Intenzita: Sprint (50-100m) / Vytrvalost (400m+)
  - Obsahuje start: Ano / Ne
  - Obsahuje obrátky: Ano / Ne
```

### 8.2 Wireframe

```
┌─────────────────────────────────────────────┐
│              NAHRÁT VIDEO                    │
│                                              │
│  [Drag & drop video / Vybrat soubor]         │
│                                              │
│  Úroveň plavce:                             │
│    (o) Dítě (8-14 let)                       │
│    (o) Pokročilý (15+)                       │
│                                              │
│  Pohled kamery:                              │
│    (o) Z boku  (o) Zepředu  (o) Pod vodou   │
│                                              │
│  Typ úseku:                                  │
│    (o) Sprint (50-100m)                      │
│    (o) Vytrvalost (400m+)                    │
│                                              │
│  Video obsahuje:                             │
│    [ ] Start ze startovního bloku            │
│    [ ] Obrátku/obrátky                       │
│                                              │
│         [Analyzovat]                         │
└─────────────────────────────────────────────┘
```

### 8.3 Výstup s módy

Výsledková stránka se rozšíří o per-fáze analýzu:

```
┌─────────────────────────────────────────────┐
│  VÝSLEDKY ANALÝZY — Sprint, se startem      │
│                                              │
│  Celkové skóre: 74/100                       │
│                                              │
│  ┌─── Start ──────────────────────────┐      │
│  │ Entry angle: 38° (OK)              │      │
│  │ Streamline: 2.1s (krátký!)         │      │
│  │ Breakout: plynulý                  │      │
│  │ Skóre startu: 68/100              │      │
│  └────────────────────────────────────┘      │
│                                              │
│  ┌─── Volné plavání (sprint) ─────────┐      │
│  │ SR: 54 cycles/min (OK pro sprint)  │      │
│  │ Body roll: 35° (OK)               │      │
│  │ Elbow catch: 145° (mírně vysoký)  │      │
│  │ Kick: 6-beat (OK pro sprint)       │      │
│  │ Skóre plavání: 76/100            │      │
│  └────────────────────────────────────┘      │
└─────────────────────────────────────────────┘
```

---

## 9. Modulová struktura

### 9.1 Nové moduly

| Modul               | Odpovědnost                                                                                | Závislosti                         |
| ------------------- | ------------------------------------------------------------------------------------------ | ---------------------------------- |
| `analysis_mode.py`  | `AnalysisMode` enum, `ModeConfig` dataclass, factory `get_mode_config(mode, style, level)` | Referenční prahy per mód           |
| `phase_detector.py` | Segmentace videa na fáze (start, plavání, obrátka) z keypoint trajektorií                  | Keypoint data, heuristiky          |
| `start_analyzer.py` | Analýza startovní fáze — metriky + feedback                                                | `phase_detector`, referenční prahy |
| `turn_analyzer.py`  | Analýza obrátky — metriky + feedback                                                       | `phase_detector`, referenční prahy |
| `kick_analyzer.py`  | Detekce kick patternu (2-beat vs 6-beat), amplituda, regularita                            | Ankle/knee keypoint data           |

### 9.2 Modifikované moduly

| Modul                                    | Změna                                                                                              |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `stroke_analyzer.py`                     | Přijímá `ModeConfig`, používá mode-specific referenční prahy místo hardcoded `FREESTYLE_REFERENCE` |
| `feedback_generator.py`                  | Mode-aware šablony, sprint vs. vytrvalost tipy, start/turn feedback                                |
| `mediapipe_angles.py` / ekvivalent ve v2 | Přidání kick-related výpočtů (ankle oscillation, kick count)                                       |

### 9.3 Datové struktury

```python
class AnalysisMode(str, Enum):
    SPRINT = "sprint"
    ENDURANCE = "endurance"

class AnalysisPhase(str, Enum):
    START = "start"
    SWIMMING = "swimming"
    TURN = "turn"

@dataclass
class ModeConfig:
    mode: AnalysisMode
    includes_start: bool
    includes_turns: bool
    level: str  # "child" | "advanced"
    camera_view: str  # "side" | "front" | "underwater"

    # Mode-specific reference ranges (loaded from config/JSON)
    joint_references: Dict[str, JointReference]
    sr_range: Tuple[float, float]
    idc_range: Optional[Tuple[float, float]]
    kick_pattern: str  # "6-beat" | "2-beat"
    body_roll_range: Tuple[float, float]
    tolerances: Dict[str, float]
    metric_weights: Dict[str, float]

@dataclass
class VideoPhase:
    phase_type: AnalysisPhase
    start_frame: int
    end_frame: int
    confidence: float  # How confident is the phase detection

@dataclass
class PhaseAnalysisResult:
    phase: VideoPhase
    metrics: Dict[str, float]
    deviations: List[JointDeviation]
    score: float
    feedback: List[str]

@dataclass
class FullAnalysisResult:
    mode_config: ModeConfig
    phases: List[PhaseAnalysisResult]  # Per-phase results
    overall_score: float
    overall_feedback: List[str]
```

---

## 10. Co tento dokument neřeší (budoucí vývoj)

- **Ostatní styly (znak, prsa, motýlek):** Každý styl má jiné fáze záběru, jiné klíčové metriky a jiné referenční prahy. Architektura módů je navržena tak, aby byla rozšiřitelná na další styly.
- **Automatická detekce módu z videa:** Systém by mohl automaticky rozpoznat sprint vs. vytrvalost z SR a detekovat start/obrátky z keypoint trajektorií bez uživatelského vstupu.
- **Phase detection přístup (OTEVŘENÁ OTÁZKA — k diskuzi s vedoucím):** Aktuální návrh používá heuristiky z keypoint trajektorií. Alternativy: (a) heuristiky + user fallback při nízkém confidence, (b) heuristiky + ML experiment pro srovnání v kapitole 5, (c) ML-first s natrénovaným klasifikátorem. Volba závisí na dostupnosti labeled dat a doporučení vedoucího.
- **Multi-view fúze:** Kombinace bočního + frontálního + podvodního pohledu pro 3D rekonstrukci.
- **Kategorie Profesionál:** Třetí úroveň s přísnějšími prahy (±8°).

---

_Last Updated: 2026-03-05_
