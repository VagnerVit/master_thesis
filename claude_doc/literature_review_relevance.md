# Přehled literatury — relevance pro SwimAth

_Generováno: 2026-03-05_
_Celkem: 52 PDF ve složce `literature/`_

---

## Tier 1 — KRITICKÉ (přímo citovat, tvoří páteř diplomky)

### Pose Estimation (jádro pipeline)

| Soubor | Autoři & rok | Proč je kritický |
|--------|-------------|------------------|
| `ViTPose_Xu_2022_NeurIPS.pdf` | Xu et al., 2022 | **Kandidát #1 na fine-tuning.** Vision Transformer, škálovatelný 20M–1B params, SOTA 80.9 AP COCO. Základ pro tvůj PE benchmark (balík B1–B2). |
| `RTMPose_Jiang_2023.pdf` | Jiang et al., 2023 | **Kandidát #2 na fine-tuning.** 75.8% AP, 90+ FPS CPU. Real-time alternativa k ViTPose — potřebuješ porovnat oba v benchmarku. |
| `Einfalt_WACV_2018_swimming_pose.pdf` | Einfalt, Zecha & Lienhart, 2018 | **Jediný swimming-specific PE paper.** Řeší refrakci, vodní prostředí, temporální vyhlazení (+16% zlepšení). Augsburg skupina = autoři datasetu, o který jsi žádal. |
| `SwimmerNET_Giulietti_2023.pdf` | Giulietti et al., 2023 | **Podvodní PE.** CNN pro underwater detekci s wide-angle kamerou, chyba ~1–10 mm. Relevantní pro underwater view analýzu. |
| `DeepLabCut_Mathis_2018_PMC.pdf` | Mathis et al., 2018 | **Referenční markerless PE.** ~200 anotovaných snímků stačí. Cituj jako alternativu, kterou jsi zvažoval. |

### Dataset

| Soubor | Autoři & rok | Proč je kritický |
|--------|-------------|------------------|
| `SwimXYZ_Fiche_2023_SIGGRAPH_MIG.pdf` | Fiche et al., 2023 | **Tvůj primární dataset.** 11,520 videí, 3.4M snímků, 4 styly, SMPL anotace. Musíš detailně popsat v kapitole 4. |

### Biomechanika — základní reference

| Soubor | Autoři & rok | Proč je kritický |
|--------|-------------|------------------|
| `Toussaint_2000_Biomechanics_of_Swimming.pdf` | Toussaint et al., 2000 | **Klasický přehled** — drag, propelling efficiency, energetika. Základ pro kapitolu 2. |
| `Barbosa_2011_biomechanics_competitive_swimming.pdf` | Barbosa et al., 2011 | **Biomechanika všech 4 stylů** — kinematika, kinetika, neuromuskulární analýza. Základní referenční rámec. |
| `Chollet_2000_Index_of_Coordination.pdf` | Chollet et al., 2000 | **Index of Coordination (IdC).** Klíčová metrika arm koordinace — implementuješ ji v biomechanickém extraktoru. |
| `Craig_Pendergast_1979_stroke_rate_velocity.pdf` | Craig & Pendergast, 1979 | **V = SR × SL vztah.** Fundamentální rovnice, na které stojí tvůj referenční systém prahů. |
| `Barden_Kell_2014_freestyle_biomechanical_errors.pdf` | Virag et al., 2014 | **Prevalence biomechanických chyb** — dropped elbow 61.3%. Přímo definuje, které chyby tvůj systém detekuje. |
| `Psycharakis_Sanders_2010_body_roll_review.pdf` | Psycharakis & Sanders, 2010 | **Body roll review.** Rotace trupu = jedna z tvých hlavních metrik (30–55° pro pokročilé). |

---

## Tier 2 — VELMI DŮLEŽITÉ (citovat v rešerši, podporují návrh)

### Biomechanika záběru — freestyle specifické

| Soubor | Autoři & rok | Relevance |
|--------|-------------|-----------|
| `Seifert_2004_velocity_arm_coordination.pdf` | Seifert et al., 2004 | Vztah rychlost–koordinace u různých úrovní plavců. Podpora pro tvoje 2 kategorie (Dítě/Pokročilý). |
| `Matsuda_2014_intracyclic_velocity_coordination.pdf` | Matsuda et al., 2014 | Intracyklické oscilace rychlosti (IVV) — možná další metrika pro tvůj systém. |
| `Staunton_2025_SR_SL_dynamics_elite.pdf` | Staunton et al., 2025 | Nejnovější paper o SR-SL dynamice u elit. 2D kernel density — zajímavá vizualizace pro výsledky. |
| `Potdevin_2006_stroke_frequency_coordination.pdf` | Potdevin et al., 2006 | Frekvence záběru vs. koordinace a efektivita — podpora pro tvoje prahy SR. |
| `Correia_2023_400m_frontcrawl_meta_analysis.pdf` | Correia et al., 2023 | Meta-analýza 400m kraul parametrů — agregovaná data pro validaci tvých referenčních hodnot. |

### Biomechanika — mladí plavci (tvoje kategorie "Dítě 8–14")

| Soubor | Autoři & rok | Relevance |
|--------|-------------|-----------|
| `Morais_2023_biomechanical_determinants_young_swimmers.pdf` | Morais et al., 2023 | SEM model: antropometrie + tah + drag → 100m výkon u mládeže. Strukturální model pro tvé prahy. |
| `Barbosa_2021_narrative_review_youth_swimming.pdf` | Morais et al., 2021 | Systematická rešerše faktorů ovlivňujících výkon mladých plavců — přímo relevantní pro kategorii Dítě. |
| `Morais_2012_kinematic_profile_young_swimmers.pdf` | Morais et al., 2012 | Kinematický profil mladých plavců podle výkonu — data pro nastavení prahů. |
| `Barbosa_2019_hydrodynamic_young_swimmers.pdf` | Barbosa et al., 2019 | Porovnání úrovní u mládeže — biomechanika, antropometrie, energetika. |
| `Barbosa_2014_classification_kinematics.pdf` | Barbosa et al., 2014 | Klasifikace plavců podle kinematiky — shluková analýza, inspirace pro tvůj kategorizační systém. |
| `Stanula_2013_youth_swimming_technique.pdf` | Jerszinski et al., 2013 | Změny parametrů techniky u mladých začátečníků — baseline pro kategorii Dítě. |

### RAG/LLM (diskuze v diplomce — proč jsi to odmítl)

| Soubor | Autoři & rok | Relevance |
|--------|-------------|-----------|
| `Comendant_2024_RAG_swimming_coaching.pdf` | Comendant, 2024 | **Přímo plavecký RAG coaching.** Bakalářka, University of Twente. Hlavní zdroj pro diskuzi "proč ne LLM". |
| `RAG_Lewis_2020_NeurIPS.pdf` | Lewis et al., 2020 | **Fundamentální RAG paper.** Musíš citovat, když diskutuješ RAG alternativu. |
| `Talking_Tennis_Talha_2025.pdf` | Dashore et al., 2025 | **Analogický pipeline** (biomechanika → LLM feedback) pro tenis. Porovnání přístupů v diskuzi. |
| `BoxingPro_2024_IoT_LLM_coaching.pdf` | Zhu et al., 2024 | IoT senzory + GPT-4 pro box. Další analogie sport+AI, hodnocení 4.0/5.0. |

---

## Tier 3 — UŽITEČNÉ (citovat selektivně, doplňkový kontext)

### Biomechanika — koordinace a adaptabilita

| Soubor | Autoři & rok | Relevance |
|--------|-------------|-----------|
| `Schnitzler_Seifert_Button_2021_adaptability_swimming.pdf` | Schnitzler et al., 2021 | Adaptabilita techniky s expertízou — teoretický rámec pro odlišné prahy. |
| `Silva_2019_coordination_flexibility.pdf` | Silva et al., 2019 | Koordinační flexibilita mládeže — doplněk k youth papírům. |
| `Task Constraints and Coordination.pdf` | Silva et al., 2019 | Omezení úlohy vs. koordinační schémata — podobné jako Silva 2019. |
| `The Effect of a Coordinative Training in Young.pdf` | Jerszinski et al., 2013 | Vliv koordinačního tréninku na techniku — doplněk pro cvičební doporučení. |
| `Sanders_2007_flutter_kick_kinematics.pdf` | Sanders, 2007 | Flutter kick kinematika — relevantní, pokud budeš analyzovat i nohy (ne jen horní tělo). |

### Biomechanika — pokročilá analýza

| Soubor | Autoři & rok | Relevance |
|--------|-------------|-----------|
| `Scandinavian Med Sci Sports - 2024 - Morais...` | Morais et al., 2024 | Efekty antropometrie na 100m kraul — novější verze Morais 2023 studie. |
| `European Journal of Sport Science - 2018 - Morais...` | Morais et al., 2018 | Transfer síly do biomechaniky záběru — 34týdenní longitudinální studie. |
| `Linking Selected Kinematic,.pdf` | Morais et al., 2012 | Strukturální model kinematika–antropometrie–výkon. |
| `Identifying Differences in Swimming Speed Fluctuation...` | Morais et al., 2023 | Oscilace rychlosti u mládeže — SPM analýza. |
| `Young Swimmers' Classification Based on Kinematics,.pdf` | Santos et al., 2023 | Klasifikace výkonnostních úrovní — top/mid/low tier. |
| `Upper-limb kinematics and kinetics.pdf` | (Autoři nezjištěni) | Kinematika horních končetin — relevantní pro analýzu záběru. |

### Starty a obrátky

| Soubor | Autoři & rok | Relevance |
|--------|-------------|-----------|
| `Vantorre_2014_Swim_Start_Review.pdf` | Vantorre et al., 2014 | Kompletní review biomechaniky startů — užitečné, pokud rozšíříš na analýzu startů. |
| `Phase_Determinants_100m_2025_PMC12134280.pdf` | Gao et al., 2025 | Fázové determinanty 100m — start/swim/turn/finish příspěvky. |
| `Connaboy_2009_UDK_hydrodynamics_review.pdf` | Connaboy et al., 2009 | UDK hydrodynamika review — pokud budeš analyzovat podvodní fázi. |
| `Connaboy_2015_UDK_key_determinants.pdf` | Connaboy et al., 2016 | Klíčové kinematické determinanty UDK. |

---

## Tier 4 — OKRAJOVÉ (citovat jen pokud rozšíříš scope)

### Starty a obrátky — specifické studie

| Soubor | Autoři & rok | Poznámka |
|--------|-------------|----------|
| `Kick_Start_2021_PMC8625813.pdf` | Matúš et al., 2021 | Kick start parametry — mimo scope (neanalyzuješ starty). |
| `Tor_2020_start_performance.pdf` | Tor et al., 2020 | Start performance determinanty. |
| `Cossor_2001_sydney_starts.pdf` | Cossor et al., 2001 | Sydney Olympics starty — historické. |
| `Guimaraes_1985_grab_start_mechanics.pdf` | Guimaraes & Hay, 1985 | Grab start mechanika — zastaralé. |
| `Hochstein_2011_UDK_vortex.pdf` | Hochstein, 2011 | UDK vortex formace — příliš specifické. |
| `Lyttle_1999_optimal_glide_depth.pdf` | Lyttle, 1999 | Optimální hloubka skluzu — mimo scope. |
| `Vennell_2006_wave_drag.pdf` | Vennell et al., 2006 | Wave drag na povrchu — fyzikální, ne PE/ML. |
| `Nicol_2019_tumble_turn_kinetics.pdf` | Nicol et al., 2019 | ⚠️ **Pozor — špatně zařazený soubor!** Obsahuje studii o svalové síle u starších žen, NE o obrátkách. |
| `Puel_2022_tumble_turn_WCT.pdf` | David et al., 2022 | Tumble turn wall contact time — mimo scope. |
| `Underwater_Parameters_2021_PMC8442910.pdf` | Pla et al., 2021 | Podvodní parametry elit — užitečné pouze pro underwater view. |

---

## Shrnutí

| Tier | Počet | Pokrytí |
|------|-------|---------|
| **1 — Kritické** | 12 | PE modely, dataset, základní biomechanika, chyby |
| **2 — Velmi důležité** | 15 | Freestyle metriky, youth biomechanika, RAG diskuze |
| **3 — Užitečné** | 15 | Koordinace, pokročilá analýza, starty/obrátky |
| **4 — Okrajové** | 10 | Specifické starty/obrátky, mimo scope |

### Co chybí v knihovně (doporučuji doplnit):

1. **Maglischo (2003) — Swimming Fastest** — zlatý standard biomechaniky, máš v CLAUDE.md jako "NESTAŽENO"
2. **Sakoe & Chiba (1978)** — originální DTW paper (potřebuješ pro DTW rešerši)
3. **Shokoohi-Yekta et al. (2017)** — DTW-D vs DTW-I paper (v CLAUDE.md citovaný)
4. **Keogh et al.** — UCR DTW benchmarky
5. **S-WFDTW (2025)** — fitness scoring s BlazePose (analogický use case)
6. **MediaPipe paper** — Lugaresi et al. (2019) — aktuálně používáš v prototypu
7. **COCO dataset paper** — Lin et al. (2014) — baseline pro PE benchmarky

### Poznámka k souboru `Nicol_2019_tumble_turn_kinetics.pdf`:

Tento soubor je **špatně zařazený** — neobsahuje studii o obrátkách v plavání, ale o svalové síle u starších žen. Buď se jedná o chybný download, nebo o záměnu souborů.
