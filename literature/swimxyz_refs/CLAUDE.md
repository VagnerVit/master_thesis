# swimxyz_refs — Reference vytěžené ze SwimXYZ paperu (Fiche et al., 2023)

22 paperů. Citované v SwimXYZ datasetu + doplňkové relevantní reference.
Získáno: 2026-03-05

---

## Pose Estimation — backbone modely

### Dosovitskiy_2020_ViT.pdf
- **Autoři**: Dosovitskiy A. et al., 2020, ICLR
- **Co to je**: Vision Transformer (ViT) — backbone architektura pro ViTPose
- **Přínos pro SwimAth**: Musíš citovat v PE rešerši. ViT je základ ViTPose, který fine-tunuješ na SwimXYZ. Vysvětluje proč transformery fungují na obrazových datech (patch embedding, self-attention).
- **Kapitola**: 2 (Rešerše — PE architektury)

### Cao_2017_OpenPose.pdf
- **Autoři**: Cao Z., Simon T., Wei S.-E., Sheikh Y., 2017, CVPR
- **Co to je**: OpenPose — real-time multi-person 2D PE přes Part Affinity Fields
- **Přínos pro SwimAth**: Baseline PE metoda. Bottom-up přístup (vs. top-down ViTPose). Cituj jako referenční bod v benchmarku B1. SwimXYZ používá OpenPose formát anotací.
- **Kapitola**: 2 (Rešerše — PE architektury), 5 (Benchmark)

### MediaPipe_Lugaresi_2019.pdf
- **Autoři**: Lugaresi C. et al., 2019, arXiv
- **Co to je**: MediaPipe framework — ML pipeline pro mobilní/edge inference
- **Přínos pro SwimAth**: Tvůj prototyp (Phase 0-2) používá MediaPipe Pose. Cituj jako výchozí PE řešení, které nahrazuješ ViTPose/RTMPose ve v2.
- **Kapitola**: 4 (Implementace — prototyp)

## 3D Body Models — SMPL

### Loper_2015_SMPL_body_model.pdf
- **Autoři**: Loper M., Mahmood N., Romero J., Pons-Moll G., Black M.J., 2015, ACM TOG
- **Co to je**: SMPL — parametrický 3D model lidského těla (shape β + pose θ → mesh)
- **Přínos pro SwimAth**: SwimXYZ dataset poskytuje anotace ve formátu SMPL. Musíš citovat při popisu datasetu. SMPL definuje 21 body joints, ze kterých odvozuješ biomechanické metriky.
- **Kapitola**: 2 (Rešerše — body modely), 3 (Návrh — dataset), 4 (Implementace)

### Bogo_2016_Keep_it_SMPL.pdf
- **Autoři**: Bogo F., Kanazawa A., Lassner C., Gehler P., Romero J., Black M.J., 2016, ECCV
- **Co to je**: SMPLify — první automatický fitting SMPL na 2D keypointy z jednoho snímku
- **Přínos pro SwimAth**: Kontext pro SMPL pipeline. Ukazuje jak se z 2D keypointů rekonstruuje 3D póza — relevantní pokud budeš zvažovat 3D rekonstrukci z monokulárního videa.
- **Kapitola**: 2 (Rešerše — 3D reconstruction)

## Analogické systémy — PE + feedback

### Fieraru_2021_AIFit.pdf
- **Autoři**: Fieraru M., Zanfir M., Pirlea S.C., Olaru V., Sminchisescu C., 2021, CVPR
- **Co to je**: AIFit — 3D PE → segmentace cviků → porovnání s trenérem → interpretovatelný feedback pro fitness
- **Přínos pro SwimAth**: **Nejbližší analogie k tvému systému.** Řeší stejný problém (PE → odchylky od reference → feedback), ale pro fitness cviky na suchu. Cituj jako hlavní related work. Klíčový rozdíl: ty řešíš vodní prostředí, které je výrazně náročnější pro PE.
- **Kapitola**: 2 (Rešerše — ML ve sportu), 3 (Návrh — porovnání přístupů)

### Wang_2019_AI_Coach.pdf
- **Autoři**: Wang J., Qiu K., Peng H., Fu J., Zhu J., 2019, ACM Multimedia
- **Co to je**: AI Coach — deep PE + analýza pro personalizovaný atletický trénink
- **Přínos pro SwimAth**: Další analogický systém. PE + personalizovaná zpětná vazba pro sportovce. Obecný sport, ne plavání specificky.
- **Kapitola**: 2 (Rešerše — ML ve sportu)

## Sportovní datasety

### Tang_2023_Flag3D.pdf
- **Autoři**: Tang Y. et al., 2023, CVPR
- **Co to je**: Flag3D — 3D fitness dataset s jazykovými instrukcemi (60 cvičení, 180k sekvencí)
- **Přínos pro SwimAth**: Ukazuje trend propojení 3D PE dat s jazykovým feedbackem. Inspirace pro strukturu tvého feedback systému. Diskuze v rešerši — porovnání datasetů.
- **Kapitola**: 2 (Rešerše — datasety)

## Syntetická data pro PE

### Black_2023_BEDLAM.pdf
- **Autoři**: Black M.J. et al., 2023, CVPR
- **Co to je**: BEDLAM — syntetický dataset realistických lidských těl v pohybu (validace, že syntetická data fungují pro PE trénink)
- **Přínos pro SwimAth**: Podpora pro tvůj přístup — trénink PE na syntetickém SwimXYZ datasetu. BEDLAM ukázal, že model trénovaný jen na syntetických datech překonává SOTA na reálných datech.
- **Kapitola**: 2 (Rešerše — syntetická data), 5 (Experimenty — domain gap diskuze)

### Varol_2017_Synthetic_Humans.pdf
- **Autoři**: Varol G. et al., 2017, CVPR
- **Co to je**: SURREAL — první large-scale syntetický dataset pro PE (6.5M snímků z SMPL + MoCap)
- **Přínos pro SwimAth**: Pionýrský paper o učení PE ze syntetických dat. Cituj jako základ přístupu, který SwimXYZ rozšiřuje na plaveckou doménu.
- **Kapitola**: 2 (Rešerše — syntetická data)

### Mahmood_2019_AMASS.pdf
- **Autoři**: Mahmood N. et al., 2019, ICCV
- **Co to je**: AMASS — unifikovaný archiv motion capture dat jako SMPL povrchy (>40 hodin, 300+ subjektů)
- **Přínos pro SwimAth**: Zdrojová data pro syntetické datasety. SwimXYZ používá SMPL formát kompatibilní s AMASS. Kontextová reference.
- **Kapitola**: 2 (Rešerše — datasety, syntetická data)

## Generativní modely (kontext SwimXYZ pipeline)

### Li_2022_GANimator.pdf
- **Autoři**: Li P. et al., 2022, ACM TOG
- **Co to je**: GANimator — generativní model pro syntézu nových pohybů z jedné sekvence
- **Přínos pro SwimAth**: SwimXYZ používá GANimator pro generování diverzních plaveckých pohybů. Cituj při popisu jak SwimXYZ dataset vznikl.
- **Kapitola**: 3 (Návrh — popis datasetu)

### Starke_2022_DeepPhase.pdf
- **Autoři**: Starke S., Mason I., Komura T., 2022, ACM TOG
- **Co to je**: DeepPhase — periodické autoenkodéry pro učení fázových manifoldů pohybu
- **Přínos pro SwimAth**: SwimXYZ paper používá PAE z DeepPhase pro klastrování plaveckých stylů (T-SNE vizualizace). Cituj pokud budeš replikovat ten experiment nebo jako alternativu k tvému LSTM klasifikátoru.
- **Kapitola**: 2 (Rešerše — klasifikace stylů), 5 (Experimenty)

### Goodfellow_2014_GAN.pdf
- **Autoři**: Goodfellow I. et al., 2014, NeurIPS
- **Co to je**: Generative Adversarial Networks — základní paper
- **Přínos pro SwimAth**: Teoretický základ pro GANimator (viz výše). Cituj jen pokud podrobněji popisuješ generativní pipeline SwimXYZ.
- **Kapitola**: 2 (Rešerše — deep learning základy)

## Plavecky-specifická PE a analýza

### Ceseracciu_2011_markerless_front_crawl.pdf
- **Autoři**: Ceseracciu E. et al., 2011, Journal of Biomechanics
- **Co to je**: Markerless analýza kraulu — jeden z prvních pokusů o PE bez markerů pro plavání
- **Přínos pro SwimAth**: Přímá reference pro tvůj pipeline. Ukazuje historický vývoj markerless analýzy plavání. Porovnání s marker-based systémy.
- **Kapitola**: 2 (Rešerše — PE v plavání)

### Zecha_2017_kinematic_params_PE_swimmers.pdf
- **Autoři**: Zecha D., Eggert C., Lienhart R., 2017, Electronic Imaging
- **Co to je**: Odvozování kinematických parametrů závodních plavců z PE — Augsburg skupina
- **Přínos pro SwimAth**: Doplněk k Einfalt WACV 2018. Ukazuje jak z PE extrahovat biomechanické metriky (stroke rate, frekvence). Přímý předchůdce tvého pipeline keypoints → metriky.
- **Kapitola**: 2 (Rešerše — PE v plavání), 3 (Návrh — extrakce metrik)

### Zecha_2012_swimmer_detection_stroke_rate.pdf
- **Autoři**: Zecha D., Greif T., Lienhart R., 2012, SPIE Multimedia on Mobile Devices
- **Co to je**: Detekce plavce a odhad pózy pro kontinuální měření stroke rate
- **Přínos pro SwimAth**: Rané práce Augsburg skupiny. Automatická detekce plavce + stroke rate — základ, na kterém staví pozdější Einfalt 2018 a Zecha 2017.
- **Kapitola**: 2 (Rešerše — PE v plavání)

### Ascenso_2021_PhD_markerless_mocap_swimming.pdf
- **Autoři**: Ascenso G., 2021, PhD thesis, Manchester Metropolitan University
- **Co to je**: Celá disertace o markerless motion capture pro plaveckou biomechaniku (FISHnet + POSEidon modely)
- **Přínos pro SwimAth**: Přímý konkurent/předchůdce. Řeší podobný problém (markerless PE pro plavání), ale jiným přístupem. Detailní diskuze výzev vodního prostředí. Klíčový related work.
- **Kapitola**: 2 (Rešerše — PE v plavání), 3 (Porovnání přístupů)

### Kirmizibayrak_2011_digital_analysis_swimming.pdf
- **Autoři**: Kirmizibayrak C. et al., 2011, Int. J. Virtual Reality
- **Co to je**: Digitální analýza a vizualizace plaveckého pohybu
- **Přínos pro SwimAth**: Ranější přístup k vizualizaci plavecké techniky. Kontextová reference pro historii oboru.
- **Kapitola**: 2 (Rešerše — analýza plavání)

### Greif_2009_annotated_swimmer_dataset.pdf
- **Autoři**: Greif T., Lienhart R., 2009, Technical Report, Uni Augsburg
- **Co to je**: Anotovaný dataset pro PE plavců — 15 cyklů znaku, >1200 anotovaných framů
- **Přínos pro SwimAth**: Jeden z prvních anotovaných datasetů pro PE plavců. Cituj v rešerši datasetů jako předchůdce SwimXYZ.
- **Kapitola**: 2 (Rešerše — datasety)

### Woinoski_2020_automated_swimming_analytics.pdf
- **Autoři**: Woinoski T., 2020, SFU Undergrad Research Symposium
- **Co to je**: Automatizovaná plavecká analytika s hlubokými neuronovými sítěmi
- **Přínos pro SwimAth**: Analogický projekt — DNN pro analýzu plavání. Kontextová reference.
- **Kapitola**: 2 (Rešerše — ML ve sportu)

## Alternativní sběr dat — dron (aerial view)

### DroneSwim_2025_aerial_swimming_analysis.pdf
- **Autoři**: Tran T. et al., 2024, DroNet '24 (ACM Workshop on Micro Aerial Vehicle Networks)
- **Co to je**: Analýza plaveckého výkonu z aerial videa pořízeného dronem (DJI Mavic 3 Pro, 4K@60fps, výška 8m). Pipeline: MediaPipe BlazePose → úhly paží, stroke duration (FFT), rychlost (kalibrace přes značky bazénu), Symmetry Index.
- **Přínos pro SwimAth**: Zajímavý alternativní pohled kamery — aerial view doplňuje tvé side/front/underwater. Používají MediaPipe (stejně jako tvůj prototyp). Ukazují konkrétní problémy: detection rate klesá při závodech (splashes) na 56%, L/R swap keypointů u kraulu. SI threshold 10% pro symetrii — můžeš převzít.
- **Klíčové výsledky**: Stroke duration error <0.3s, velocity error <0.35 m/s. 5 plavců (3F, 2M), kraul.
- **Kapitola**: 2 (Rešerše — alternativní přístupy k video analýze plavání)

## IMU-based přístupy (porovnání)

### Delhaye_2022_IMU_swimming.pdf
- **Autoři**: Delhaye E. et al., 2022, MDPI Sensors
- **Co to je**: Automatická klasifikace plaveckých stylů a měření lap time z jednoho IMU senzoru
- **Přínos pro SwimAth**: Porovnání video-based vs. IMU-based přístupu ke klasifikaci stylů. Video nabízí bohatší data (pózy, úhly), IMU je jednodušší na sběr.
- **Kapitola**: 2 (Rešerše — alternativní přístupy)
