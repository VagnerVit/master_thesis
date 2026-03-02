# AI analýza plavání: datasety a literatura pro diplomovou práci

**Oblast AI analýzy plavání se nachází na produktivním průsečíku počítačového vidění, sportovní biomechaniky a nově vznikajících LLM technologií — ale naráží na kritický nedostatek anotovaných dat.** Existuje pouze jeden rozsáhlý veřejný dataset (SwimXYZ, syntetický) pro odhad plavecké pózy, zatímco datasety z reálného prostředí jsou dostupné pouze na akademickou žádost. Zároveň literatura ukazuje, že žádný existující systém nekombinuje CV analýzu plavání s RAG-rozšířenou LLM zpětnou vazbou pro trenéry — to představuje jasnou mezeru vhodnou pro diplomovou práci. Tento dokument katalogizuje všechny identifikovatelné datasety a sestavuje rozsáhlou knihovnu zdrojů napříč čtyřmi výzkumnými oblastmi.

---

## ČÁST 1: Dostupné plavecké datasety pro odhad pózy

### Datasety specifické pro plavání

Krajina plaveckých datasetů je řídká, ale roste. **SwimXYZ** (Fiche et al., 2023) je nejdůležitější zdroj: syntetický dataset obsahující **11 520 videí s cca 3,4 miliony snímků** s ground-truth 2D a 3D anotacemi kloubů ve formátu COCO, pokrývající všechny čtyři závodní styly. Byl vygenerován pomocí GANimator s SMPL modely těl ve virtuálních bazénech a je volně ke stažení ze Zenodo (anotace na zenodo.org/record/8399376, s oddělenými archivy videí pro každý styl). Článek vyšel na ACM SIGGRAPH MIG 2023. Omezením je nízká diverzita subjektů a prostředí.

Pro reálná anotovaná data má **Univerzita v Augsburgu** nejucelenější výzkumný program. Jejich **Greif & Lienhart Swimmer Pose Dataset** (2009) obsahuje přes 1 200 anotovaných snímků plavců ve znaku zaznamenaných přes skleněnou stěnu plaveckého kanálu se 14 kloubovými pozicemi na snímek. Širší **Augsburg Swimming Channel Dataset** (Einfalt, Zecha & Lienhart, 2012–2019) rozšiřuje záběr na všechny čtyři styly od závodních plavců. Oba jsou dostupné na akademickou žádost (MMC Lab, uni-augsburg.de). Klíčové články: Einfalt et al. (WACV 2018), Zecha et al. (CVPR Workshops 2019).

**SwimmerNET** (Giulietti et al., *Sensors* 2023) poskytuje 2 021 snímků podvodního freestyle videa se segmentačními maskami částí těla (hlava, ramena, lokty, zápěstí, boky) s ~1mm průměrnou chybou. Kontakt: Università Politecnica delle Marche. **Cao & Yan** (*Multimedia Tools and Applications*, 2024) sestavili 2 500 podvodních obrázků se 3 615 označenými plavci ve 14 COCO klíčových bodech. **Fani et al.** (IEEE ICIP 2018) mají podvodní front-view video kraulu klasifikované podle kvality záběru (vysoký loket vs. padající loket) — kontakt: University of New Brunswick.

| Dataset | Rok | Typ | Velikost | Styly | Přístup | Anotace |
|---|---|---|---|---|---|---|
| SwimXYZ | 2023 | Syntetické video | 11 520 videí, 3,4M snímků | Všechny 4 | Veřejný (Zenodo) | 2D+3D klouby, SMPL |
| Augsburg Swimming Channel | 2012–2019 | Reálné video | Více sessions | Všechny 4 | Na žádost | Klouby těla, události |
| Greif & Lienhart | 2009 | Reálné video | 1 200+ snímků | Znak | Na žádost | 14 kloubových pozic |
| SwimmerNET | 2023 | Reálné podvodní | 2 021 snímků | Kraul | Na žádost | Segmentační masky |
| Cao & Yan | 2024 | Reálné podvodní | 2 500 obrázků | Všechny 4 | Nejasné | 14 klíčových bodů (COCO) |
| SwimTrack-v1 | 2022 | Závodní video | 10 závodů | Všechny 4 + polohový | Registrace | Bounding boxy, záběry |
| Fani et al. | 2018 | Reálné podvodní | Malý | Kraul | Na žádost | Klasifikace záběrů |
| SwimMistakes | 2025 | Reálné obrázky | ~2 720 obrázků | 3 styly | Na žádost | YOLO bbox + chyby |
| DeepDASH | 2020 | Závodní video | Více závodů | Všechny 4 | Na žádost | Detekce + tracking |

### Závodní a benchmarkové datasety

**SwimTrack-v1** z MediaEval 2022 (organizátor: École Centrale de Lyon/LIRIS) nabízí závodní video elitních plavců natáčené z boku bazénu v HD až 4K při 25–50 fps, pokrývající všechny styly. Anotace zahrnují bounding boxy, počty záběrů, matice homografie a text z výsledkové tabule. Přístup vyžaduje registraci na multimediaeval.github.io. Navazující úloha **SportsVideo** pokračovala na MediaEval 2023.

Framework **Woinoski, Harell & Bajić** (arXiv:2001.04433, Simon Fraser University, 2020) definuje anotační pokyny pro závodní video s šesti třídami aktivit (na bloku, skok, pod vodou, plavání, obrátka, dohmátnutí), ale dataset nebyl veřejně vydán. **SwimMistakes** (Al-Majnoni et al., ETASR 2025) obsahuje ~2 720 augmentovaných obrázků s nesprávnými plaveckými pohyby v motýlku, znaku a prsou s YOLO anotacemi.

### Podvodní a mezidoménové datasety

**CADDY Underwater Stereo-Vision Dataset** (EU FP7, Univerzita v Záhřebu) je nejvýznamnější veřejný podvodní dataset lidské pózy — obsahuje ~10 000 stereo snímků gest potápěčů plus ~12 700 stereo snímků volně plavajících potápěčů se synchronizovanými IMU daty. Volně dostupný na GitHubu. Ačkoli není specifický pro plavání, jeho podvodní anotace a charakteristiky distorze jsou přímo použitelné pro experimenty s doménovou adaptací.

Wang et al. (*Scientific Reports*, 2024) vytvořili **3D point cloud dataset** pro rozpoznávání pózy na povrchu i pod vodou pomocí LiDAR. Pro širší podvodní počítačové vidění aggreguje repozitář **Awesome Underwater Datasets** (GitHub) desítky podvodních datasetů.

### Multisportovní datasety s plaveckou komponentou

Několik velkých datasetů zahrnuje plavecké třídy: **UCF101** (13 320 videí, 101 kategorií včetně prsou, volně dostupný), **Kinetics-400/600/700** (DeepMind, stovky tisíc klipů včetně plavání), **Sports Videos in the Wild** (SVW, 4 100 videí, 30 sportů). Pro sportovní odhad pózy: **ASPset-510** (La Trobe University, 510 klipů, 100K+ 3D póz, veřejný), **SportsPose** (176K+ dynamických 3D sportovních póz, veřejný na GitHubu), **FineGym** (708 hodin gymnastiky s hierarchickými anotacemi). Na Kaggle je **Swimming and Drowning Dataset** (~14 736 obrázků) pro klasifikaci plavců.

---

## ČÁST 2: Zdroje pro literární rešerši

### A) Biomechanika plavání: základní texty a klíčový výzkum

**Klíčové učebnice:**
- Maglischo, E. W. (2003). *Swimming Fastest*. Human Kinetics. 800 stran — encyklopedický zlatý standard pokrývající techniku záběrů, vztahy frekvence/délky záběru, odpor a propulzi.
- Riewald, S. & Rodeo, S. (2015). *Science of Swimming Faster*. Human Kinetics — nejkomplexnější moderní reference s kapitolami předních odborníků.
- Counsilman, J. E. (1968/1994). *The Science of Swimming*. Prentice Hall — průkopnická práce.
- Stager, J. M. & Tanner, D. A. (2005). *Handbook of Sports Medicine and Science: Swimming*. Wiley-Blackwell — oficiální svazek MOV.
- Colwin, C. (2002). *Breakthrough Swimming*. Human Kinetics.
- Seifert, L. & Chollet, D. (2011). *World Book of Swimming: From Science to Performance*. Nova Science.
- Barbosa, T. M. et al. (2011). Biomechanics of Competitive Swimming Strokes. In *Biomechanics in Applications*, IntechOpen (open-access).

**Frekvence a délka záběru:**
- Craig, A. B. & Pendergast, D. R. (1979). Relationships of stroke rate, distance per stroke, and velocity in competitive swimming. *Medicine and Science in Sports and Exercise*, 11(3), 278–283. — zavedli fundamentální vztah **V = SR × SL**.
- Craig, A. B. et al. (1985). Velocity, stroke rate, and distance per stroke during elite swimming competition. *Medicine and Science in Sports and Exercise*, 17(6), 625–634.
- Staunton, C. A. et al. (2025). Stroke rate–stroke length dynamics in elite freestyle swimming: application of kernel density estimation. *Frontiers in Sports and Active Living*.
- Morais, J. E. et al. (2023). Stroke rate–stroke length optimization in sprint freestyle. *Journal of Sports Science and Medicine*.
- Morais, J. E. et al. (2022). Propulsive force and SR-SL relationship. *Frontiers in Physiology*.

**Rotace a převalování těla:**
- Psycharakis, S. G. & Sanders, R. H. (2010). Body roll in swimming: A review. *Journal of Sports Sciences*, 28(3), 229–236. — klíčový přehled.
- Psycharakis, S. G. & Sanders, R. H. (2008). Shoulder and hip roll patterns in front crawl. *Journal of Applied Biomechanics*.
- Sanders, R. H. & Psycharakis, S. G. (2009). Rolling rhythms in front crawl swimming with six-beat kick. *Journal of Biomechanics*, 42(8), 1035–1041.
- Andersen, J. T. et al. (2020). Kinematic differences in shoulder roll and hip roll at different front crawl speeds in national level swimmers. *Journal of Strength and Conditioning Research*, 34(1), 20–25.
- Yanai, T. (2001). What causes the body to roll in front-crawl swimming? *Journal of Applied Biomechanics*, 17(1), 28–42.
- Gonjo, T. et al. (2021). Body roll amplitude and timing in backstroke and front crawl. *Scientific Reports*, 11, 2565.

**Koordinace a fáze záběru:**
- Chollet, D., Chalies, S. & Chatard, J. C. (2000). A new index of coordination for the crawl: description and usefulness. *International Journal of Sports Medicine*, 21(1), 54–59. — zavedli **Index of Coordination (IdC)**.
- Seifert, L. et al. (2004). Effect of velocity on arm coordination in front crawl. *Journal of Sports Sciences*, 22(7), 651–660.
- Seifert, L. et al. (2014). Coordination pattern variability in swimming. *Sports Medicine*, 44(6), 815–828.

**Propulze a odpor:**
- Toussaint, H. M. & Truijens, M. (2005). Biomechanical aspects of peak performance in human swimming. *Animal Biology*, 55(1), 17–40. — propulzní efektivita **46–77 %** u elitních kraulařů.
- Santos, K. B. et al. (2022). Numerical and experimental methods used to evaluate active drag in swimming: A systematic narrative review. *Frontiers in Physiology*, 13, 938658.
- Zamparo, P. et al. (2020). Energy cost of swimming. *European Journal of Applied Physiology*, 120, 1735–1750.
- Schleihauf, R. E. (1979). A hydrodynamic analysis of swimming propulsion. In *Swimming III*, 70–109.

**Závodní analýza a biomechanika závodů:**
- Cappaert, J. M., Pease, D. L. & Troup, J. P. (1995). Biomechanical highlights of world champion and Olympic swimmers. *Journal of Applied Biomechanics*.
- Arellano, R. et al. (1994). Analysis of 50m, 100m, and 200m freestyle swimmers at the 1992 Olympic Games. *Journal of Applied Biomechanics*, 10(2), 189–199.
- Gonjo, T. & Olstad, B. H. (2021). Race Analysis in Competitive Swimming: A Narrative Review. *Int. J. Environ. Res. Public Health*, 18(1), 69.
- Barbosa, T. M. et al. (2024). Race analysis in swimming: bibliometric review. *Frontiers in Sports and Active Living*.
- **International Symposium on Biomechanics and Medicine in Swimming** (BMS, ročníky I–XIV) — hlavní konference oboru.

**Metriky efektivity a srovnání elit/nováčků:**
- Costill, D. L. et al. (1985). Swimming economy concept (stroke index). *Medicine and Science in Sports and Exercise*.
- Barbosa, T. M. et al. (2010). Energetics and biomechanics as determining factors of swimming performance: Updating the state of the art. *Journal of Science and Medicine in Sport*, 13(3), 262–269.
- Barden, J. M. & Kell, R. T. (2014). Prevalence of freestyle biomechanical errors in elite competitive swimmers. *Sports Health*, 6(3), 218–226. — padající loket při záběru (61,3 %), padající loket při přenosu (53,2 %), nesprávná poloha hlavy (46,8 %), nedostatečná rotace.
- Vilas-Boas, J. P. (2023). Swimming biomechanics: from the pool to the lab … and back. *Sports Biomechanics*.

### A2) Pediatrická plavecká biomechanika

Specifická oblast biomechaniky plavání zaměřená na mladé plavce (8–16 let). Klíčová pro kategorii "Dítě" v projektu SwimAth. Výzkum je relativně řídký — většina biomechanických studií pracuje s dospělými závodními plavci.

**Kinematika a výkonnost mladých plavců:**
- Sanders, R. H. (2007). Kinematics, coordination, variability, and biological noise in the prone flutter kick at different levels of a "learn-to-swim" programme. *J Sports Sciences*, 25(2), 213–227. DOI: 10.1080/02640410600631025. — Kloubové úhly kolene, kyčle, kotníku při flutter kicku napříč úrovněmi; Fourierova analýza.
- Morais, J. E. et al. (2012). Linking selected kinematic, anthropometric and hydrodynamic variables to young swimmer performance. *Pediatric Exercise Science*, 24(4), 649–664. DOI: 10.1123/pes.24.4.649. — Kinematický a hydrodynamický profil mladých plavců.
- Barbosa, T. M. et al. (2014). Young swimmers' classification based on kinematics, hydrodynamics, and anthropometrics. *J Applied Biomechanics*, 30(2), 310–315. DOI: 10.1123/jab.2013-0038. — 67 mladých plavců, 25m front crawl max.
- Morais, J. E. et al. (2018). The transfer of strength and power into the stroke biomechanics of young swimmers over a 34-week period. *European J Sport Science*, 18(6), 787–795. DOI: 10.1080/17461391.2018.1453869. — 27 plavců (13.33 let), longitudinální studie.
- Morais, J. E. et al. (2024). Effects of anthropometrics, thrust, and drag on stroke kinematics and 100m performance of young swimmers using path-analysis modeling. *Scand J Med Sci Sports*, 34(2), e14578. DOI: 10.1111/sms.14578. — 25 adolescentů (15.75 let).

**Koordinace a asymetrie u mládeže:**
- Silva, A. F. et al. (2019). Task Constraints and Coordination Flexibility in Young Swimmers. *Motor Control*, 23(4), 535–552. DOI: 10.1123/mc.2018-0070. — 18 plavců 13–15 let, IdC při různých rychlostech.
- Silva, A. F. et al. (2022). The Effect of a Coordinative Training in Young Swimmers' Performance. *IJERPH*, 19(12), 7020. DOI: 10.3390/ijerph19127020. — 26 mladých plavců, Qualisys multi-camera, 50m sprint.
- Morais, J. E. et al. (2020). Upper-limb kinematics and kinetics imbalances in the determinants of front-crawl swimming at maximal speed in young international level swimmers. *Scientific Reports*, 10, 11683. DOI: 10.1038/s41598-020-68581-3. — 22 muži (15.92 let), L/R imbalance horních končetin.
- Morais, J. E. et al. (2023). Identifying Differences in Swimming Speed Fluctuation in Age-Group Swimmers by Statistical Parametric Mapping. *J Sports Science & Medicine*, 22(2), 358–366. DOI: 10.52082/jssm.2023.358. — Intracyklická rychlostní variace.

**Klasifikace a přehledy:**
- Morais, J. E. et al. (2022). Young Swimmers' Classification Based on Performance and Biomechanical Determinants: Determining Similarities Through Cluster Analysis. *Motor Control*, 26(3), 396–411. DOI: 10.1123/mc.2021-0126. — 38 plavců (15–16 let), cluster analýza.
- Silva, A. F. et al. (2025). Front crawl swimming coordination: a systematic review. *Sports Biomechanics*, 24(2), 127–146. DOI: 10.1080/14763141.2022.2125428. — Systematic review vč. mládežnických studií.
- Morais, J. E. et al. (2021). Young Swimmers' Anthropometrics, Biomechanics, Energetics, and Efficiency as Underlying Performance Factors: A Systematic Narrative Review. *Frontiers in Physiology*, 12, 691274. PMC8481572. — Klíčový review biomechaniky dětských plavců.
- Jerszyński, D. et al. (2013). Changes in selected parameters of swimming technique in young novice swimmers. *J Human Kinetics*, 37, 161–171. DOI: 10.2478/hukin-2013-0037. — Úhel loktu u začínajících dětí (n=11, 8–13 let).

**Klíčové zjištění pro projekt SwimAth:**
- Většina studií pochází od skupiny Morais/Barbosa/Marinho (IPB Bragança, Portugalsko) — dominantní tým v oblasti.
- Přímá 3D kinematická data kloubových úhlů (shoulder, knee, hip per-phase) u dětí prakticky neexistují.
- Sanders 2007 je jediný zdroj s detailními kloubovými úhly dolních končetin u dětí (flutter kick).
- L/R asymetrie u mládeže: Morais 2020 poskytuje první systematická data.
- IdC u mládeže: Silva 2019 doplňuje mezeru v Morais 2021 review.

### B) Odhad pózy ve sportu a plavání

**Odhad pózy specifický pro plavání:**
- Einfalt, M., Zecha, D. & Lienhart, R. (2018). Activity-conditioned continuous human pose estimation for performance analysis of athletes using the example of swimming. *IEEE WACV 2018*.
- Zecha, D., Einfalt, M. & Lienhart, R. (2018). Kinematic pose rectification for performance analysis and retrieval in sports. *CVPR Workshops 2018*.
- Zecha, D., Einfalt, M. & Lienhart, R. (2019). Refining joint locations for human pose tracking in sports videos. *CVPR Workshops 2019*. — zlepšení 0,8–4,8 % PCK.
- Giulietti, N. et al. (2023). SwimmerNET: Underwater 2D Swimmer Pose Estimation Exploiting Fully Convolutional Neural Networks. *Sensors*, 23(4), 2364.
- Cao, Z. & Yan, X. (2024). Pose estimation for swimmers in video surveillance. *Multimedia Tools and Applications*. — HRNet-W32/W48 z podvodního pohledu.
- Hassanein, A. et al. (2025). RTMPose and Ensemble Learning for Real-Time Swimmer Talent Detection. *AMLTA 2025*, Springer.
- Ouyang, Z. et al. (2024). Optimization of Swim Pose Estimation and Recognition with Data Augmentation. *IEEE Conference*.
- Win, K. et al. (2024). Analyzing Swimming Performance Using Drone Captured Aerial Videos. *DroNet/ACM 2024*.
- Fani, H. et al. (2018). Swim Stroke Analytic: Front Crawl Pulling Pose Classification. *IEEE ICIP 2018*.

**Klíčové architektury odhadu pózy:**
- Cao, Z. et al. (2019). OpenPose: Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields. *IEEE TPAMI*, 43(1), 172–186. — bottom-up multi-person, až 135 klíčových bodů.
- Sun, K. et al. (2019). Deep High-Resolution Representation Learning for Visual Recognition. *CVPR 2019*. — **77,0 mAP na COCO** (vs. OpenPose 61,8).
- Xu, Y. et al. (2022). ViTPose: Simple Vision Transformer Baselines for Human Pose Estimation. *NeurIPS 2022*. — škálovatelný od 20M do 1B parametrů.
- Xu, Y. et al. (2023). ViTPose++: Vision Transformer for Generic Body Pose Estimation. *arXiv:2212.04246*.
- Lugaresi, C. et al. (2019). MediaPipe: A Framework for Building Perception Pipelines. *arXiv:1906.08172*.
- Bazarevsky, V. et al. (2020). BlazePose: On-device Real-time Body Pose tracking. *arXiv:2006.10204*. — 33 klíčových bodů, vhodný pro mobil.
- Jiang, T. et al. (2023). RTMPose: Real-Time Multi-Person Pose Estimation based on MMPose. *arXiv:2303.07399*. — 75,8 % AP na COCO, 90+ FPS CPU, 430+ FPS GPU.
- Mathis, A. et al. (2018). DeepLabCut: markerless pose estimation of user-defined body parts with deep learning. *Nature Neuroscience*, 21, 1281–1289. — přesnost na lidské úrovni z ~200 anotovaných snímků.
- Cronin, N. J. et al. (2019). Markerless 2D kinematic analysis of underwater running: A deep learning approach. *Journal of Biomechanics*, 87, 75–82. — <3 pixely průměrný rozdíl pod vodou.

**Podvodní výzvy a doménová adaptace:**
- Kwon, Y. H. & Casebolt, J. B. (2006). Effects of light refraction on the accuracy of camera calibration and reconstruction in underwater motion analysis. *Sports Biomechanics*, 5(2), 315–340.
- Akkaynak, D. et al. (2023). A Survey on Underwater Computer Vision. *ACM Computing Surveys*, 55(13s), 1–44. — absorpce, rozptyl, refrakce.
- Li, J. et al. (2018). WaterGAN: Unsupervised Generative Network to Enable Real-time Color Correction of Monocular Underwater Images. *IEEE RA-L*, 3(1), 387–394.
- TUDA (2023). Domain Adaptation for Underwater Image Enhancement. *IEEE Transactions on Image Processing*.
- Seegräber, M. et al. (2024). Open-source underwater refractive camera calibration toolbox. *arXiv*.

**Přehledy a surveyy:**
- Zheng, C. et al. (2023). Deep Learning-Based Human Pose Estimation: A Survey. *ACM Computing Surveys*.
- Comprehensive survey on pose estimation and tracking in sports (2025). *Artificial Intelligence Review*, Springer.
- Colyer, S. L. et al. (2018). A Review of the Evolution of Vision-Based Motion Analysis and the Integration of Advanced Computer Vision Methods Towards Developing a Markerless System. *Sports Medicine – Open*, 4, 24.
- Munea, T. L. et al. (2023). Human Pose Estimation Using Deep Learning: A Systematic Literature Review. *Machine Learning and Knowledge Extraction*, 5(4), 81.
- Commercial vision sensors and AI-based pose estimation frameworks for markerless motion analysis in sports (2025). *Frontiers in Physiology*.

### C) AI a LLM ve sportovní analýze

**RAG ve sportovním koučování:**
- Comendant, A. (2024). RAG-enhanced LLM coaching for swimming. Bakalářská práce, University of Twente. — LLMUR (LLM + uživatelský model + RAG s GPT-4o) vs. samotný LLM, 3týdenní studie.
- Lewis, P. et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *NeurIPS 2020*. — základní RAG architektura.
- **Žádné jiné recenzované práce neaplikují RAG specificky na sportovní analytiku.**

**LLM koučování a porozumění sportu:**
- Lee, J. (2025). ChatGPT-guided half-marathon preparation: a 2-month case study. *arXiv*.
- Hegde, A. et al. (2024). Behavior science-infused LLM for physical activity coaching. *PLOS Digital Health*.
- JMIR scoping review (2025). Evaluation methods for LLM-based exercise coaches. *PMC*.
- Xia, H. et al. (2024). SportQA: A Benchmark for Sports Understanding in Large Language Models. *arXiv:2402.15862*. — 70 000+ otázek, testování GPT-4, LLaMA2, PaLM2.
- Li, H. et al. (2024). Sports-QA: A Large-Scale Video Question Answering Benchmark for Complex and Professional Sports. *arXiv:2401.01505*.

**Biomechanika → přirozený jazyk pipeline:**
- Talha, M. et al. (2025). Talking Tennis: Language Feedback from 3D Biomechanical Action Recognition. *arXiv:2510.03921*. — extrakce biomechanických rysů přes CNN-LSTM → LLM zpětná vazba.
- BoxingPro (2024). An IoT-LLM Framework for Automated Boxing Coaching via Wearable Sensor Data Fusion. *MDPI Electronics*, 14(21), 4155. — GPT-4 hodnocení 4,0/5,0 na biomechanickou správnost.
- Čamernik, J. et al. (2022). Review of Real-Time Biomechanical Feedback Systems in Sport and Rehabilitation. *Sensors*, 22(8), 3006.
- Wongsirichot, T. et al. (2024). Deep learning-based human body pose estimation in providing feedback for physical movement: A review. *Heliyon*.
- **Žádný ekvivalentní pipeline neexistuje pro plavání.**

**CV pipeline pro sportovní video:**
- Wang, J. et al. (2019). AI Coach: Deep Human Pose Estimation and Analysis for Personalized Athletic Training Assistance. *ACM MM 2019*.
- Thomas, G. et al. (2017). A Survey on Content-Aware Video Analysis for Sports. *IEEE TCSVT*, 27(6), 1265–1279.
- Woinoski, R., Harell, A. & Bajić, I. V. (2020). Towards Automated Swimming Analytics Using Deep Neural Networks. *AAAI Workshop / arXiv:2001.04433*.
- Hall, A. et al. (2020). The detection, tracking, and temporal action localisation of swimmers for automated analysis. *Neural Computing and Applications*. — DeepDASH, F1=97,5 %.

**AI ve výkonnosti plavání:**
- Systematic review (2025). AI for swimming recommendation systems. *Discover Applied Sciences*, Springer. — 42 studií (2018–2024), >80 % zaměřeno na klasifikaci záběrů.
- Molinari, D. et al. (2024). Swimming Performance Interpreted through Explainable AI (XAI). *Applied Sciences*, 14(12), 5218. — SHAP, r²=0,93.
- Xie, Y. et al. (2017). Machine learning of swimming data via wisdom of crowd and regression analysis. *Mathematical Biosciences and Engineering*.
- Delhaye, C. et al. (2022). Automatic Swimming Activity Recognition and Lap Time Assessment Based on a Single IMU. *Sensors*, 22(15), 5786. — Bi-LSTM, F1=0,96.
- Brunner, G. et al. (2019). Swimming style recognition and lap counting using a smartwatch and deep learning. *ISWC 2019*. — F1=97,4 %.

### D) Metody videoanalýzy v plavání

**Pohled z boku a z kraje bazénu:**
- Mooney, R. et al. (2016). Application of Video-Based Methods for Competitive Swimming Analysis: A Systematic Review. *Sports Medicine – Open*, 2(1), 37.
- Einfalt, M. et al. (2018), Zecha, D. et al. (2018, 2019) — viz sekce B výše.
- Silvatti, A. P. et al. (2024). Viability of 2D Swimming Kinematical Analysis Using a Single Moving Camera. *Applied Sciences*, 14(15), 6560.
- Cortesi, M. et al. (2016). Action sport cameras as an instrument to perform a 3D underwater motion analysis. *PLOS ONE*, 11(8), e0160490. — 1,28 mm střední chyba.
- Ruiz-Teba, A. et al. (2025). Validity and Reliability of 2D Video Analysis for Swimming Kick Start Kinematics. *PMC*.

**Detekce záběrů a temporální analýza:**
- Victor, B. et al. (2017). Continuous Video to Simple Signals for Swimming Stroke Detection with Convolutional Neural Networks. *CVPR Workshops 2017*. — F-score=0,92.
- Hall, A. et al. (2020). DeepDASH. *Neural Computing and Applications*. — **F1=97,5 %**, HISORT.
- Hakozaki, T. et al. (2018). CNN + multi-LSTM for stroke estimation. *Journal of Signal Processing*.
- Jacquelin, N. et al. (2022). SwimTrack: Swimmers and Stroke Rate Detection in Elite Race Videos. *MediaEval 2022*.
- Wang, Z. et al. (2020). Swimming Stroke Phase Segmentation Based on Wearable Motion Capture. *IEEE TIM*. — 98,22 % přesnost.
- Magalhães, F. et al. (2019). Inertial Sensors in Swimming: Detection of Stroke Phases through 3D Wrist Trajectory. *Journal of Biomechanical Engineering*.

**Sledování plavců a analýza přenosů:**
- Sha, L. et al. (2013, 2014). Swimmer Localization from a Moving Camera. *IEEE DICTA*.
- Slawson, S. E. et al. (2018). Stroke parameters from 2012 Olympic footage. *Proceedings of the Institution of Mechanical Engineers*.
- Chang, M. C. et al. (2025). A butterfly stroke swimming recording and performance analysis system. *Measurement*. — 25m, YOLOv4, 120 031 trénovacích obrázků.
- Toyoda, K. et al. (2019). Aerial and underwater drone combination for 3D swimming pose reconstruction.

**Komerční a výzkumné systémy:**
- Dartfish (dartfish.com/swimming/) — zlatý standard komerčních platforem.
- Pla, R. et al. (2021). TritonWear vs. video comparison. *Int. J. Sports Science & Coaching*. — 3,22 % MAPE pro čas kola.
- Qualisys (qualisys.com) — optické motion capture kamery pro podvodní použití (Miqus Underwater).
- CONTEMPLAS/TEMPLO (contemplas.com) — multikamerové systémy pro národní svazy.
- Kinovea — open-source pro 2D analýzu.
- Hamidi Rad, M. et al. (2020). A Novel Macro-Micro Approach for Swimming Analysis Using IMU Sensors. *Frontiers in Bioengineering and Biotechnology*, 8, 597738.

---

## Příležitost pro diplomovou práci: kde se datasety a literatura sbíhají

Tři konvergentní mezery definují nejsilnější přínos práce:

1. **Problém nedostatku dat**: Pouze SwimXYZ poskytuje rozsáhlé veřejné anotace, ale jeho syntetická povaha omezuje přímou použitelnost. Fine-tuning moderních architektur (ViTPose, RTMPose) na syntetických datech s doménovou adaptací na reálné plavecké záběry je nedostatečně prozkoumaný, ale slibný směr.

2. **Mezera v generování zpětné vazby**: Talking Tennis a BoxingPro demonstrují biomechanika→jazyk pipeline pro jiné sporty, ale **žádný ekvivalentní systém neexistuje pro plavání**.

3. **Mezera v RAG koučování**: Pouze jedna bakalářská práce zkoumala RAG pro plavecké koučování, bez žádných recenzovaných publikací. Systém řetězící odhad plavecké pózy → extrakci biomechanických parametrů → RAG-rozšířenou LLM zpětnou vazbu by byl skutečně nový.

Dataset SwimXYZ plus přístup na akademickou žádost k datasetům Augsburg a SwimmerNET poskytují realizovatelný datový základ. Architektury ViTPose/RTMPose nabízejí nejlepší kompromis přesnost-rychlost. A kompletní absence publikovaných CV→RAG→LLM plaveckých koučovacích pipeline znamená, že i prototypová implementace by představovala smysluplný přínos oboru.
