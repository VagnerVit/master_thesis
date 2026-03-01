# TODO: Sekce Datasety do diplomky

**Status**: Připraveno k implementaci, zatím neimplementovat.

---

## `paper/chapters/02_reserse.tex` — sekce Datasety (řádek 112, prázdná)

Struktura sekce:
1. Úvodní odstavec — nedostatek anotovaných plaveckých dat, jen 1 velký veřejný dataset
2. **SwimXYZ** (Fiche 2023) — syntetický, 11 520 videí, 48 kp, Zenodo, GANimator+SMPL
3. **Augsburg Swimming Channel** (Einfalt 2018/2019) — reálný, skleněná stěna, 1200+ snímků, 14 kloubů
4. **SwimmerNET** (Giulietti 2023) — podvodní, 2021 snímků, segmentační masky, ~1mm chyba
5. **Cao & Yan** (2024) — podvodní, 2500 obrázků, 14 COCO kp, HRNet
6. **SwimTrack-v1** (MediaEval 2022) — závodní video, HD–4K, 25–50 FPS
7. **CADDY** (podvodní stereo) — mezidoménový, veřejný, ~10k+12.7k stereo snímků
8. Srovnávací tabulka (Dataset | Rok | Typ | Velikost | Styly | Přístup | Anotace)
9. Závěr — jen SwimXYZ volně dostupný a dostatečně velký, nutnost vlastního sběru dat

## `paper/references.bib` — chybějící záznamy k přidání

```bibtex
einfalt2019     — Zecha, Einfalt, Lienhart — CVPRW 2019
swimtrack2022   — Ravi et al. — MediaEval 2022
caddy2016       — Chavez et al. — JMSE 2019
cao2024underwater — Cao & Yan — Multimedia Tools 2024
cronin2019underwater — Cronin et al. — J Biomech 2019
```

Už existují v bib: `fiche2023swimxyz`, `giulietti2023`, `einfalt2018`
