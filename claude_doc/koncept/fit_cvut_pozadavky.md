# Formální požadavky ČVUT FIT na diplomovou práci

## Rozsah
- **50–150 normostran** obsahového textu (bez obsahu, příloh, poznámek)
- 1 normostrana = 1 800 znaků včetně mezer → **90 000 – 270 000 znaků**

## Povinné části
1. **Zadání závěrečné práce** (podepsané děkanem a vedoucím katedry) — z ProjectsFIT
2. **Abstrakt** v češtině i angličtině
3. **Klíčová slova** — min. 20 znaků CZ, 30 znaků EN
4. **Prohlášení** o samostatném zpracování a úplnosti citací (podepsané)
5. **Řešení zadaného úkolu** (jádro práce)
6. **Závěrečné hodnocení výsledků**
7. **Seznam literatury** (bibliograficky korektní)
8. **Obsah** se seznamem příloh
9. **Final Thesis Agreement (FTA)** — z ProjectsFIT, musí být shodný

## Formátování
- Symboly a definice před prvním použitím
- Seznam obrázků, tabulek, použitých symbolů
- Vysoká typografická kvalita
- Index (volitelné)

## LaTeX šablona

| Šablona | Engine | Zdroj | Poznámka |
|---------|--------|-------|----------|
| **FITthesis-LaTeX** (doporučená) | XeLaTeX / LuaLaTeX | [GitLab FIT](https://gitlab.fit.cvut.cz/theses-templates/FITthesis-LaTeX) | Oficiální FIT šablona, řeší titulní stranu/prohlášení/abstrakty automaticky |
| CTUstyle 1/2 | pdfTeX + csplain | [petr.olsak.net](http://petr.olsak.net/ctustyle.html) | Celouniverzitní, plaintex (NE LaTeX) |
| CTUstyle 3 | OpTeX | dtto | Novější, funguje na Overleaf |
| ctuthesis | LaTeX | CIIRC | Od T. Hejdy, LaTeX wrapper |

**Doporučení: FITthesis-LaTeX** — XeLaTeX (kompatibilní se stávajícím main.tex), automaticky generuje titulní stranu, prohlášení, abstrakty.

**Tipy z [fit-thesis-tips](https://github.com/hroncok/fit-thesis-tips):**
- `pdfpages` pro vložení zadání (z ProjectsFIT PDF)
- Vektorové diagramy (TikZ/PGF), ne screenshoty
- `vlna` pro nedělitelné mezery v češtině
- Git pro text diplomky

## Odevzdání
- Elektronicky v KOS (PDF + přílohy jako .zip nebo odkaz na GitLab repo)
- 1 fyzický pracovní výtisk (libovolná vazba) k obhajobě
- FTA musí být shodný v systému i v práci

## Vedoucí práce
- Diplomová práce vyžaduje vedoucího s **Ph.D.** nebo vyšším titulem
- Může být i externí, ale musí mít doktorát

## Obhajoba
- **20 minut celkem**
- Prezentace: **max. 12 minut**
- Seznámení s posudky vedoucího a oponenta
- Odpovědi na otázky, diskuze s komisí
- Posudky k dispozici **min. 5 dní před obhajobou**

## Hodnotící kritéria (vedoucí + oponent)
- Splnění zadání
- Kvalita analýzy problému a rešerše
- Kvalita návrhu řešení
- Kvalita implementace
- Kvalita experimentů a vyhodnocení
- Formální úroveň textu
- Práce se zdroji a citace
- Samostatnost studenta (hodnotí vedoucí)

---

## Magisterské specializace na FIT ČVUT

Program: **Informatika** (jeden program, specializaci si student volí po přijetí)

### Dostupné specializace
1. Počítačová bezpečnost
2. Počítačové systémy a sítě
3. Programovací jazyky
4. Teoretická informatika
5. Umělá inteligence (dříve Znalostní inženýrství)
6. **Softwarové inženýrství**
7. Webové inženýrství

### Softwarové inženýrství — zaměření
- Matematické základy, optimalizace
- Paralelní a distribuované systémy
- Statistické metody
- Návrh a architektura SW systémů
- Není primárně zaměřené na ML/CV, ale práce s ML se tam dělají

### Umělá inteligence — zaměření
- Deep learning, ML, Computer vision
- Predikce, doporučovací systémy, NLP
- Lépe odpovídá ML/CV zaměření SwimAth

---

## Hodnocení: Pasuje SwimAth pod SW inženýrství?

**ANO, ALE s důrazem na SW aspekty.**

### Co je OK pro SW inženýrství
- Návrh a architektura webové aplikace (Vue.js + FastAPI + Celery pipeline)
- Asynchronní zpracování videa (WebSocket, task queue)
- Datový model a persistence (PostgreSQL)
- Testování a kvalita SW (unit testy, integrace)
- CI/CD pipeline
- Softwarový návrh ML pipeline jako systému (ne samotný ML výzkum)

### Co je problematické
- Pokud je jádro práce výzkum pose estimation a fine-tuning modelů → to je spíš AI/ML
- Pokud je hlavní přínos biomechanická analýza → to je spíš aplikovaná AI

### Doporučení podle specializace

| Aspekt | SW inženýrství | Umělá inteligence |
|--------|---------------|-------------------|
| Hlavní focus | Architektura systému, pipeline design | Fine-tuning PE, DTW experimenty |
| Rešerše | SW architektura, async processing, testing | Pose estimation, biomechanika, ML |
| Experimenty | Výkonnost systému, škálovatelnost | Přesnost PE, kvalita detekce chyb |
| Přínos | End-to-end SW řešení | ML pipeline pro plaveckou analýzu |

---

## Checklisty pro SwimAth

### Formální (jakákoli specializace)
- [ ] Ověřit, že vedoucí má Ph.D.
- [ ] Zaregistrovat téma v ProjectsFIT
- [ ] Použít FIT LaTeX šablonu (FITthesis-LaTeX)
- [ ] Abstrakt CZ + EN, klíčová slova
- [ ] FTA z ProjectsFIT
- [ ] Rozsah 50–150 normostran
- [ ] Repo na FIT GitLab (ne jen GitHub)

### Pro Softwarové inženýrství — posílit SW aspekty
- [ ] Kapitola o SW architektuře — detailní návrh systému, diagramy (C4, sekvenční, komponentové)
- [ ] Kapitola o návrhu API — REST endpoints, WebSocket protokol, datový model
- [ ] Testovací strategie — unit, integrace, e2e testy, pokrytí kódem
- [ ] Non-functional requirements — výkon, škálovatelnost, bezpečnost (GDPR videí!)
- [ ] Deployment architektura — Docker, CI/CD
- [ ] ML pipeline prezentovat jako SW komponentu, ne jako výzkumný experiment
- [ ] Zdůraznit softwarové vzory — Strategy pattern pro analyzéry, Factory pro PE modely, Observer pro progress

### Přeformulování názvu práce
- **Špatně**: "Analýza plavecké techniky pomocí pose estimation a ML"
- **Správně**: "Návrh a implementace webového systému pro automatickou analýzu plavecké techniky z videa"

---

## Navrhovaná struktura kapitol (SW inženýrství)

1. **Úvod** — motivace, cíle, přínos (SW systém, ne ML výzkum)
2. **Analýza problému**
   - 2.1 Doménová analýza (biomechanika plavání — max 10 stran)
   - 2.2 Existující řešení a konkurenční analýza
   - 2.3 Požadavky (funkční + nefunkční, use cases, aktéři)
   - 2.4 Technologická rešerše (PE modely, DTW, webové frameworky)
3. **Návrh řešení** ← JÁDRO PRÁCE
   - 3.1 Architektura systému (C4 diagramy)
   - 3.2 Návrh API (REST endpointy, WebSocket protokol)
   - 3.3 Datový model (ER diagram, PostgreSQL schema)
   - 3.4 Návrh ML pipeline jako SW komponenty
   - 3.5 Asynchronní zpracování (Celery + Redis)
   - 3.6 Bezpečnost a GDPR
4. **Implementace**
   - 4.1 Backend (FastAPI, Celery workers, DB migrace)
   - 4.2 Frontend (Vue.js 3, video overlay Canvas API)
   - 4.3 ML pipeline integrace (ONNX runtime, batching)
   - 4.4 Testovací strategie
   - 4.5 CI/CD a deployment
5. **Experimenty a vyhodnocení**
   - 5.1 Funkční testování
   - 5.2 Výkonnostní testování
   - 5.3 Validace ML pipeline (jako ověření SW komponenty)
   - 5.4 Uživatelské testování
6. **Závěr**

### Co zdůraznit vs. co zkrátit

| Aspekt | Rozsah | Důvod |
|--------|--------|-------|
| Biomechanika plavání | Krátce (5-10 stran) | Doménový kontext |
| PE modely | Stručná rešerše (5 stran) | Technologický výběr |
| **SW architektura** | **Detailně (15-20 stran)** | **Jádro práce** |
| **API + datový model** | **Detailně (10-15 stran)** | **Jádro práce** |
| **Implementace** | **Detailně (15-20 stran)** | **Jádro práce** |
| Fine-tuning PE | Stručně | Není SW inženýrství |
| **Testování + CI/CD** | **Detailně (10 stran)** | **Klíčové pro obor** |

---

## Rizika a mitigace

1. **"To je AI práce, ne SW"** — jasně strukturovat kapitoly tak, že ML je použitá technologie (jako databáze), ne předmět výzkumu
2. **"Málo SW inženýrství"** — přidat kapitolu o architektonických rozhodnutích (ADR), design patterns, testovací pyramidu
3. **"Moc široké téma"** — scope: freestyle only, side-view only, 2 úrovně plavců

### Klíčový fakt
Téma diplomky nemusí striktně odpovídat specializaci — záleží na vedoucím a katedře. Ale oponent a komise budou hodnotit práci optikou oboru, takže SW aspekty musí dominovat.

---

## Zdroje
- [Závěrečná práce — SZZ FIT ČVUT](https://courses.fit.cvut.cz/SZZ/prace/index.html)
- [Final Thesis — SFE FIT ČVUT](https://courses.fit.cvut.cz/SFE/thesis-topic.html)
- [Směrnice č. 58/2023](https://fit.cvut.cz/studenti/bakalar-magistr/predpisy/smernice-58-2023-zp-szz.pdf)
- [FITthesis-LaTeX](https://gitlab.fit.cvut.cz/theses-templates/FITthesis-LaTeX)
- [fit-thesis-tips](https://github.com/hroncok/fit-thesis-tips)
