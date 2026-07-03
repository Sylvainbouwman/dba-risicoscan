# DBA Risicoscan

Indicatieve beoordeling van arbeidsrelaties op basis van de **negen gezichtspunten** uit het *Deliveroo-arrest* (HR 24 maart 2023) en het *Uber-arrest* (HR 21 februari 2025).

**Live:** [dba-risicoscan.streamlit.app](https://dba-risicoscan.streamlit.app)

---

## Wat doet deze tool?

De DBA Risicoscan helpt MKB-accountants en fiscalisten bij het in kaart brengen van de risico's van ZZP-constructies voor hun klanten. De tool beoordeelt een **concrete opdracht** aan de hand van de negen gezichtspunten die de Hoge Raad heeft vastgesteld voor de kwalificatie van arbeidsrelaties.

De tool geeft **geen eindoordeel** ("wel of geen dienstbetrekking") — dat is voorbehouden aan de Belastingdienst en de rechter. In plaats daarvan geeft de tool per gezichtspunt een gemotiveerd signaal, zodat risico's zichtbaar worden en de gebruiker gericht verbeterpunten kan doorvoeren.

---

## Hoe werkt het?

**Stap 1 — Opdracht:** vul de basisgegevens in van de concrete opdracht (opdrachtgever, opdrachtnemer, sector, werkzaamheden).

**Stap 2 — Vragenlijst:** beantwoord 25 vragen verdeeld over de negen gezichtspunten, gebaseerd op de feitelijke situatie.

**Stap 3 — Analyse & Resultaat:** de tool analyseert elk gezichtspunt met onderbouwing en bronverwijzing, toont sterke risicosignalen en concrete verbeterpunten, en genereert een downloadbaar Word-risicomemo.

---

## Juridisch kader

De negen gezichtspunten uit het Deliveroo-arrest (ECLI:NL:HR:2023:443), bevestigd in het Uber-arrest (ECLI:NL:HR:2025:329):

1. Aard en duur van de werkzaamheden
2. Wijze waarop werkzaamheden en werktijden worden bepaald
3. Inbedding van het werk in de organisatie
4. Verplichting het werk persoonlijk uit te voeren
5. Wijze waarop de contractuele regeling tot stand is gekomen
6. Wijze waarop de beloning wordt bepaald en uitbetaald
7. Hoogte van de beloning
8. Al dan niet betalen van omzetbelasting
9. Gedrag als ondernemer in het economisch verkeer

Tussen deze gezichtspunten geldt geen rangorde; zij worden holistisch gewogen.

**Actuele stand van zaken (3 juli 2026):**
- Normale handhaving hervat per 1 januari 2025
- Modelovereenkomsten: geen nieuwe beoordelingen meer since 6 september 2024; bestaande geldig t/m 31 december 2029
- Wet VBAR (rechtsvermoeden): nog niet ingevoerd

---

## Technische opzet

| Bestand | Inhoud |
|---|---|
| `app.py` | Streamlit UI — 3 tabbladen: Opdracht / Vragenlijst / Analyse |
| `knowledge_base.py` | Juridische kennisbasis: negen gezichtspunten, SZW-tabel, bronnen, actuele feiten |
| `prompts.py` | Systeemprompt (kennisbasis embedded) en prompt-builder |
| `export.py` | Word-memo generator (.docx) |

**Model:** Claude Opus (Anthropic)  
**Framework:** Streamlit

### Lokaal draaien

```bash
pip install -r requirements.txt
streamlit run app.py
```

API-sleutel instellen via `.streamlit/secrets.toml`:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

---

## Disclaimer

Deze tool biedt een indicatieve risicoanalyse en geen fiscaal of juridisch advies. De beoordeling van de arbeidsrelatie is voorbehouden aan de Belastingdienst en de rechter, op basis van alle feiten en omstandigheden en de feitelijke uitvoering van de opdracht.
