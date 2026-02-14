# Start New Claude Session - Copy & Paste Instructions

Když začínáš novou Claude session na novém zařízení, zkopíruj a pošli tento prompt:

---

## 🚀 Prompt Pro Novou Session

```
Pokračuji na projektu SwimAth (Swimming Style Analysis using ML).

Repository: https://github.com/VagnerVit/SwimAth.git
Branch: main

Prosím:
1. Přečti si CLAUDE.md - project instructions
2. Přečti si SESSION_HANDOFF.md - technical handoff a co je hotovo
3. Přečti si TODO.md - task list a priority

Aktuální stav datasetu: [DOPLŇ: stažený/nestažený/částečně]
Chci pokračovat na: [DOPLŇ: Phase 1 testing / Phase 2 ML training / Phase 3 / konkrétní task]

Začni mi shrnutím:
- Co je hotovo (stručně)
- Co je priority next steps
- Jestli potřebuješ nějaké info ode mě
```

---

## 📝 Vyplň Před Odesláním

**Dataset status** - vyber jednu možnost:
- `nestažený` - ještě jsem nespustil download
- `stažený - annotations only (6.7 GB)` - mám jen anotace
- `stažený - Freestyle Part 1 (44 GB)` - mám annotations + Freestyle Part 1
- `stažený - full SwimXYZ (300 GB)` - mám všechno

**Co chceš dělat** - vyber nebo napiš vlastní:
- `Phase 1 testing - otestovat MVP aplikaci`
- `Phase 2 ML training - natrénovat YOLOv8 classifier`
- `Stáhnout dataset`
- `Opravit bug v [konkrétní modul]`
- `Přidat feature [co]`
- `Pokračovat kde jsme skončili` (Claude sám zjistí z TODO.md)

---

## ✅ Zkrácená Verze (Minimal)

Pokud chceš jen rychle pokračovat:

```
Pokračuji na SwimAth (https://github.com/VagnerVit/SwimAth.git).
Přečti CLAUDE.md, SESSION_HANDOFF.md a TODO.md.
Dataset: [stažený/nestažený]
Chci: [pokračovat kde jsme skončili / konkrétní task]
```

---

## 🎯 První Akce Claude by Měl Udělat

Po tomto promptu, Claude by měl:
1. ✅ Přečíst CLAUDE.md (project instructions)
2. ✅ Přečíst SESSION_HANDOFF.md (technical context)
3. ✅ Přečíst TODO.md (task list)
4. ✅ Shrnout ti co je hotovo
5. ✅ Říct co je next priority
6. ✅ Začít pracovat nebo se zeptat na missing info

---

## 💡 Tipy

### Pokud Claude Neví Kde Začít
```
Přečti si SESSION_HANDOFF.md sekci "Immediate Next Steps" a postupuj podle toho.
```

### Pokud Chceš Specifickou Akci
```
Pokračuji na SwimAth. Přečti CLAUDE.md a SESSION_HANDOFF.md.
Konkrétně chci: [implementovat stroke analyzer / stáhnout dataset / otestovat MVP / atd.]
```

### Pokud Jen Chceš Status Update
```
Pokračuji na SwimAth. Jaký je aktuální stav projektu podle TODO.md?
Co je nejvyšší priorita?
```

---

## 🔧 Troubleshooting

### "Claude neví o projektu"
→ Ujisti se že ses připojil k správnému Git repo
→ Zkontroluj že files CLAUDE.md, SESSION_HANDOFF.md existují
→ Řekni: "Clone repo z https://github.com/VagnerVit/SwimAth.git a přečti dokumentaci"

### "Claude dělá něco jiného než jsem chtěl"
→ Buď konkrétnější: "Chci konkrétně implementovat XYZ v souboru ABC.py"
→ Odkázat na TODO.md: "Podle TODO.md je priorita Phase 1 testing, začni tím"

### "Claude nečte dokumentaci"
→ Explicitně: "Před pokračováním MUSÍŠ přečíst CLAUDE.md a SESSION_HANDOFF.md"

---

## 📱 Pro Mobilní / Rychlý Start

Ultra-krátká verze (jedna věta):

```
SwimAth projekt: přečti CLAUDE.md + SESSION_HANDOFF.md, dataset [status], pokračuj na [task]
```

---

**Doporučení**: Použij první plnou verzi promptu, vyplň placeholders, a Claude bude mít veškerý kontext.
