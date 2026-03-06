# rag_llm_sport — RAG a LLM ve sportu

4 papery. Použití v diplomce: diskuze proč jsi zvolil pravidlový systém místo LLM/RAG feedbacku.

---

### Comendant_2024_RAG_swimming_coaching.pdf
- **Autoři**: Comendant A., 2024, bakalářská práce, University of Twente
- **Co to je**: RAG-enhanced LLM coaching pro plavání — chatbot s retrieval z plavecké literatury
- **Přínos pro SwimAth**: **Nejpřímější konkurent/alternativa.** Jediná práce kombinující RAG + LLM + plavání. Cituj jako hlavní zdroj pro diskuzi "proč ne LLM". Slabiny: závislost na OpenAI API, nedeterministické výstupy, halucinace, obtížná reprodukovatelnost.
- **Kapitola**: 2 (Rešerše — RAG/LLM), 6 (Závěr — diskuze alternativ)

### RAG_Lewis_2020_NeurIPS.pdf
- **Autoři**: Lewis P. et al., 2020, NeurIPS
- **Co to je**: RAG — Retrieval-Augmented Generation pro knowledge-intensive NLP úlohy
- **Přínos pro SwimAth**: Fundamentální RAG paper. Musíš citovat když vysvětluješ co RAG je a proč jsi ho nepoužil.
- **Kapitola**: 2 (Rešerše — RAG definice)

### Talking_Tennis_Talha_2025.pdf
- **Autoři**: Dashore T. et al., 2025, arXiv
- **Co to je**: Talking Tennis — biomechanická analýza tenisu → LLM generuje zpětnou vazbu
- **Přínos pro SwimAth**: Analogický pipeline k tomu, co bys dělal s LLM (CV → metriky → LLM feedback). Porovnání přístupů: oni používají LLM, ty pravidlový systém. Diskuze trade-offs.
- **Kapitola**: 2 (Rešerše — ML ve sportu), 6 (Diskuze)

### BoxingPro_2024_IoT_LLM_coaching.pdf
- **Autoři**: Zhu X. et al., 2024, MDPI Electronics
- **Co to je**: BoxingPro — IoT senzory + GPT-4 pro boxerský coaching, hodnocení 4.0/5.0
- **Přínos pro SwimAth**: Další analogie sport + AI. Ukazuje, že LLM coaching funguje (4.0/5.0), ale s IoT senzory (ne video PE). Doplňková reference.
- **Kapitola**: 2 (Rešerše — ML ve sportu)

---

## Klíčový argument pro diplomku

**Žádný recenzovaný end-to-end pipeline CV → biomechanické metriky → personalizovaný feedback pro plavání neexistuje.** Comendant (2024) je nejblíž, ale je to bakalářka s chatbotem, ne CV pipeline. Talking Tennis je pro tenis. BoxingPro je IoT, ne video. Toto je hlavní přínos tvé práce.
