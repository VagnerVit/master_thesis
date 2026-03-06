# A4 — Definice biomechanických metrik a prahů pro SwimAth

_Freestyle (kraul), 2 úrovně: Dítě (8–14) a Pokročilý (15+)_
_Zpracováno z literatury: 2026-03-05_

---

## 1. Kinematické metriky (měřitelné z videa)

### 1.1 Stroke Rate (SR) — frekvence záběrů

| Úroveň | Rozsah | Jednotka | Zdroj |
|---------|--------|----------|-------|
| Dítě (8–14) | 30–60 | záběrů/min | odvozeno z Chollet 2000, nižší frekvence u dětí |
| Pokročilý — distance (800m) | 32–40 | záběrů/min | Chollet 2000: G1 36.2±3.1, G2 33.8±3.1, G3 31.7±4.6 |
| Pokročilý — middle (100m) | 44–50 | záběrů/min | Chollet 2000: G1 49.5±4.3, G2 45.2±3.7, G3 44.8±4.6 |
| Pokročilý — sprint (50m) | 50–58 | záběrů/min | Chollet 2000: G1 54±4, G2 51.6±4.9, G3 49.7±5.8 |

**Detekce z videa**: počet cyklů / čas. Jeden cyklus = entry pravé ruky → entry pravé ruky.

### 1.2 Stroke Length (SL) — délka záběru

| Úroveň | Rozsah | Jednotka | Zdroj |
|---------|--------|----------|-------|
| Dítě (8–14) | 1.2–2.0 | m/záběr | odvozeno, menší tělo |
| Pokročilý — distance | 2.3–2.8 | m/záběr | Chollet 2000: G1 2.47±0.3 |
| Pokročilý — sprint | 1.9–2.2 | m/záběr | Chollet 2000: G1 2.01±0.1 |

**Poznámka**: V = SR × SL (Craig & Pendergast 1979). Nelze měřit přímo z bočního videa bez kalibrace bazénu. Buď odhadnout z délky bazénu / počtu záběrů, nebo ponechat jako odvozenou metriku.

### 1.3 Index of Coordination (IdC)

| Úroveň | Rozsah | Interpretace | Zdroj |
|---------|--------|-------------|-------|
| Dítě | -15 až -5% | catch-up (normální pro nízké rychlosti) | odvozeno |
| Pokročilý — distance | -10 až -4% | catch-up (efektivní pro šetření energie) | Chollet 2000: G1 -6.9±7.1 |
| Pokročilý — sprint | -2 až +3% | opposition/superposition (kontinuální propulze) | Chollet 2000: G1 +2.53±4.4 |

**Detekce z videa**: Vyžaduje přesnou identifikaci fází záběru (entry, catch, pull, push, recovery). Náročné na přesnost PE.

---

## 2. Úhlové metriky (přímo měřitelné z keypointů)

### 2.1 Rotace trupu — Body Roll

| Metrika | Dítě (8–14) | Pokročilý (15+) | Jednotka | Zdroj |
|---------|-------------|-----------------|----------|-------|
| Rotace ramen (celkový rozsah L+R) | 40–80° | 50–110° | stupně | Psycharakis 2010: elite 106.6±8.4° |
| Rotace boků (celkový rozsah L+R) | 20–40° | 35–60° | stupně | Psycharakis 2010: elite 50.4±12.3° |
| Asymetrie ramen (L vs R) | toleruj ≤15° | toleruj ≤10° | stupně | Psycharakis 2010: 8.2±4.8° u elite |
| Asymetrie boků | toleruj ≤15° | toleruj ≤8° | stupně | Psycharakis 2010: 5.9±3.9° |

**Klíčové poznatky z literatury**:
- Ramena se točí výrazně víc než boky (Psycharakis 2010)
- Rychlejší plavci točí rameny MÉNĚ, ne víc (korelace s rychlostí)
- Únava zvyšuje rotaci boků, ramena zůstávají stabilní
- Tradiční doporučení ~45° celkové rotace je zjednodušení — reálně 50–110° u elite
- Asymetrie je normální a nekoreluje s výkonem

**Detekce z videa**: Front view — přímo z úhlu ramen/boků vůči horizontále. Side view — obtížné, jen odhad z šířky ramen.

### 2.2 Úhel loktu

| Fáze | Správně | Chyba | Prevalence chyby | Zdroj |
|------|---------|-------|-------------------|-------|
| Pull-through (záběr) | Loket výš než ruka, směřuje laterálně | "Dropped elbow" — loket klesne pod ruku | **61.3%** i u elite | Virag 2014 |
| Recovery (přenos) | Loket výš než zápěstí | "Dropped elbow" — loket nízko | **53.2%** i u elite | Virag 2014 |
| Catch (záběr) | 130–170° (Dítě: 100–170°) | <100° příliš ohnutý, >170° rovná ruka | — | CLAUDE.md prahy |

**Prahové úhly pro detekci**:

| Metrika | Dítě | Pokročilý | Jednotka |
|---------|------|-----------|----------|
| Úhel loktu při catch | 100–170° | 130–170° | stupně |
| Loket vs ruka (pull) — vertikální rozdíl | loket ≥ ruka | loket > ruka | kvalitativní → Y-souřadnice |
| Loket vs zápěstí (recovery) — vertikální rozdíl | loket ≥ zápěstí | loket > zápěstí | kvalitativní → Y-souřadnice |
| Tolerance odchylek od reference | ±25° | ±15° | stupně |

### 2.3 Pozice ruky při vstupu do vody (entry)

| Metrika | Správně | Chyba | Prevalence | Zdroj |
|---------|---------|-------|------------|-------|
| Laterální pozice | Laterálně od hlavy, mediálně od ramene | Překřížení středové linie / příliš široký | **45.2%** | Virag 2014 |
| Úhel vstupu | Prsty napřed (fingers-first) | Palec napřed (thumb-first) | **38.7%** | Virag 2014 |
| Pattern záběru | Rovný tah dozadu | S-tvar (zastaralá technika) | **32.3%** | Virag 2014 |

**Detekce z videa**: Front view — X-souřadnice ruky vs hlava vs rameno. Úhel vstupu vyžaduje velmi přesný PE.

### 2.4 Pozice hlavy

| Správně | Chyba | Prevalence | Zdroj |
|---------|-------|------------|-------|
| Neutrální (linie hlava–páteř) | Oči dopředu (head-up) | **46.8%** | Virag 2014 |

**Detekce z videa**: Side view — úhel hlava–krční páteř–hrudní páteř. Body alignment: Head(1)–Spine2(41)–Pelvis(0) ze SwimXYZ keypointů.

---

## 3. Fázové metriky (temporal)

### 3.1 Délka propulzní fáze (% cyklu)

| Úroveň / rychlost | Pull + Push | Zdroj |
|--------------------|-------------|-------|
| Distance (800m) | 43.1% | Chollet 2000 |
| Middle (100m) | 46.5% | Chollet 2000 |
| Sprint (50m) | 49.0% | Chollet 2000 |

**Interpretace**: Vyšší procento = více času v propulzi = lepší využití záběru.

### 3.2 Synchronizace kopu

| Úroveň | Typ kopu | Zdroj |
|---------|----------|-------|
| Dítě | 2-beat nebo 4-beat (normální) | Chollet 2000 |
| Pokročilý — distance | 4-beat nebo 6-beat | Chollet 2000: 58% six-beat u G1 |
| Pokročilý — sprint | 6-beat (91% u elite) | Chollet 2000 |

**Detekce z videa**: Počet kopů na záběrový cyklus. Vyžaduje detekci pohybu nohou.

---

## 4. Souhrnná tabulka — prahy pro SwimAth implementaci

### Kvantitativní metriky (automaticky měřitelné)

| # | Metrika | Dítě (8–14) | Pokročilý (15+) | Tolerance | Pohled kamery | Priorita |
|---|---------|-------------|-----------------|-----------|--------------|----------|
| 1 | Stroke Rate | 30–60/min | 32–58/min (dle distance) | ±8/min | side / front | VYSOKÁ |
| 2 | Body roll — ramena (celkový) | 40–80° | 50–110° | ±25° / ±15° | front | VYSOKÁ |
| 3 | Body roll — boky (celkový) | 20–40° | 35–60° | ±15° / ±10° | front | STŘEDNÍ |
| 4 | Asymetrie ramen | ≤15° | ≤10° | — | front | STŘEDNÍ |
| 5 | Úhel loktu (catch) | 100–170° | 130–170° | ±25° / ±15° | side | VYSOKÁ |
| 6 | Dropped elbow (pull) | loket ≥ ruka (Y) | loket > ruka (Y) | — | front / side | VYSOKÁ |
| 7 | Dropped elbow (recovery) | loket ≥ zápěstí (Y) | loket > zápěstí (Y) | — | side | VYSOKÁ |
| 8 | Hand entry position | lat. od hlavy, med. od ramene | lat. od hlavy, med. od ramene | ±10cm / ±5cm | front | STŘEDNÍ |
| 9 | Body alignment (hlava) | úhel ≤25° od neutrální | úhel ≤15° od neutrální | — | side | VYSOKÁ |
| 10 | IdC | -15 až -5% | -10 až +3% | — | side | NÍZKÁ (těžká detekce) |

### Kvalitativní metriky (pravidlový systém)

| # | Chyba | Podmínka detekce | Feedback (CZ) |
|---|-------|-----------------|---------------|
| 1 | Dropped elbow (pull) | Y_loket < Y_ruka během pull fáze | "Loket klesá pod ruku při záběru — držte loket výš a směřujte ho do strany" |
| 2 | Dropped elbow (recovery) | Y_loket < Y_zápěstí během recovery | "Loket je nízko při přenosu paže — vedťe loket nad zápěstím" |
| 3 | Head-up pozice | úhel hlava-páteř > threshold | "Hlava je příliš zvednutá — dívejte se na dno bazénu, ne dopředu" |
| 4 | Překřížení středové linie | X_ruka překříží X_hlava (vstup) | "Ruka vstupuje přes středovou linii — vstupujte rukou v šířce ramene" |
| 5 | Nedostatečná rotace | body roll < minimum pro úroveň | "Nedostatečná rotace trupu — otáčejte se více z boků a ramen" |
| 6 | Nadměrná rotace | body roll > maximum pro úroveň | "Příliš velká rotace trupu — snižte rozsah otáčení" |
| 7 | Asymetrická rotace | |L_roll - R_roll| > threshold | "Rotace je nesymetrická — otáčíte se více na {stranu}" |

---

## 5. Implementační poznámky

### Co lze reálně měřit z videa (side view)
- Stroke rate (počet cyklů / čas) — SPOLEHLIVÉ
- Úhel loktu při catch — SPOLEHLIVÉ
- Dropped elbow (pull/recovery) — STŘEDNĚ SPOLEHLIVÉ (závisí na PE přesnosti)
- Body alignment / pozice hlavy — SPOLEHLIVÉ
- Body roll — NESPOLEHLIVÉ (potřeba front view)

### Co lze reálně měřit z videa (front view)
- Body roll (ramena + boky) — SPOLEHLIVÉ
- Hand entry position — STŘEDNĚ SPOLEHLIVÉ
- Asymetrie — SPOLEHLIVÉ
- Úhel loktu — NESPOLEHLIVÉ (perspektiva)

### Minimální sada pro diplomku (1 styl × 1 pohled × 2 úrovně)
**Freestyle, side view:**
1. Stroke rate
2. Úhel loktu (catch + pull + recovery)
3. Dropped elbow detekce
4. Body alignment (pozice hlavy)
5. Skóre 0-100 přes DTW porovnání s referencí

---

## 6. Zdroje

| Zkratka | Plná citace |
|---------|-------------|
| Virag 2014 | Virag B. et al. (2014). Prevalence of freestyle biomechanical errors. PMC 4000476 |
| Chollet 2000 | Chollet D. et al. (2000). A New Index of Coordination for the Crawl. Int J Sports Med |
| Psycharakis 2010 | Psycharakis S.G., Sanders R.H. (2010). Body roll in swimming: A review. J Sports Sci |
| Craig 1979 | Craig A.B., Pendergast D.R. (1979). Relationships of SR, SL, and velocity. Med Sci Sports |
| Barbosa 2011 | Barbosa T.M. et al. (2011). Biomechanics of Competitive Swimming Strokes. IntechOpen |
| Toussaint 2000 | Toussaint H.M. et al. (2000). Biomechanics of Swimming. Garrett & Kirkendall |
| Barden 2014 | Barden J.M., Kell R.T. (2014). Relationships Between Stroke Parameters and CSS |
