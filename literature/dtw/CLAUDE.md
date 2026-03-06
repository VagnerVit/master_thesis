# dtw — Dynamic Time Warping literatura

5 paperů. Základ pro kapitolu o porovnávací metodě (DTW jako hlavní metoda SwimAth).

---

### Sakoe_Chiba_1978_DTW_original.pdf
- **Autoři**: Sakoe H., Chiba S., 1978, IEEE Trans. Acoustics, Speech and Signal Processing
- **Co to je**: Originální DTW paper — dynamické programování pro rozpoznávání řeči
- **Přínos pro SwimAth**: Fundamentální reference. Zavádí Sakoe-Chiba band constraint, který používáš (r ≈ 15% délky cyklu). Musíš citovat.
- **Kapitola**: 2 (Rešerše — DTW), 3 (Návrh — porovnávací metoda)

### Keogh_2004_exact_indexing_DTW.pdf
- **Autoři**: Keogh E. et al., 2004, Knowledge and Information Systems (Springer)
- **Co to je**: LB_Keogh — lower bounding pro přesné indexování DTW, O(n) místo O(n²) pro vyhledávání
- **Přínos pro SwimAth**: Cituj pro diskuzi škálovatelnosti. Pro jednotlivé záběry (100–300 samples) není O(n²) problém, ale pro budoucí rozšíření (databáze referencí) je LB_Keogh relevantní.
- **Kapitola**: 2 (Rešerše — DTW optimalizace)

### Keogh_DTW_myths.pdf
- **Autoři**: Keogh E. et al. (UCR)
- **Co to je**: "Everything you know about DTW is wrong" — vyvracení mýtů o DTW
- **Přínos pro SwimAth**: Klíčový paper pro zdůvodnění tvých návrhových rozhodnutí. Ukazuje, že constrained DTW je často rychlejší než FastDTW. Podpora pro tvoji volbu Sakoe-Chiba bandu místo FastDTW.
- **Kapitola**: 2 (Rešerše — DTW)

### Shokoohi-Yekta_2017_DTW_multivariate.pdf
- **Autoři**: Shokoohi-Yekta M. et al., 2017, Data Mining and Knowledge Discovery (Springer)
- **Co to je**: Porovnání dependent (DTW-D) vs independent (DTW-I) multivariate DTW
- **Přínos pro SwimAth**: Zdůvodňuje tvoji volbu DTW-D — jeden warping path pro všechny klouby zachovává inter-joint koordinaci. Klíčový paper pro kapitolu o návrhu porovnávací metody.
- **Kapitola**: 2 (Rešerše — DTW), 3 (Návrh — zdůvodnění DTW-D)

### S-WFDTW_2025_fitness_scoring.pdf
- **Autoři**: 2025, Nature Scientific Reports
- **Co to je**: Improved DTW pro fitness scoring — BlazePose + DTW varianta pro hodnocení cviků
- **Přínos pro SwimAth**: Nejbližší analogie k tvému DTW use case (PE → DTW → skóre 0-100). Analogický pipeline, jiná doména (fitness vs. plavání). Cituj jako related work.
- **Kapitola**: 2 (Rešerše — DTW ve sportu), 3 (Návrh — scoring)
