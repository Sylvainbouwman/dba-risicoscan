# DBA Risicoscan (map DBA-helper, remote `dba-risicoscan`)

Streamlit-tool die een arbeidsrelatie langs de negen gezichtspunten van het Deliveroo-arrest en het Uber-arrest legt, met Claude als analysemodel en een Word-memo als uitvoer. Geeft bewust geen eindoordeel.

## Publicatie

Er is geen workflow in deze repository (gemeten op origin/main): niets wordt naar `bouwman-tools` gekopieerd. De live tool staat op dba-risicoscan.streamlit.app. Of een push naar `main` die app direct bijwerkt hangt af van de Streamlit-koppeling, die niet in de repository staat en niet is gemeten. Behandel een push naar `main` daarom als mogelijke publicatie en werk op een eigen branch.

## Testen

```
& "C:\Python314\python.exe" -m unittest discover -s tests -v
```

Synthetisch, zonder API-aanroepen of sleutels (37 tests geslaagd op 02-10-2026). Er is geen pytest-configuratie. `streamlit` draai je via `python -m streamlit run app.py`. De sleutel `ANTHROPIC_API_KEY` staat in `.streamlit/secrets.toml`, dat je niet opent.

## Waar de inhoud staat

- Er is geen rekenkern. De juridische en fiscale inhoud staat in `knowledge_base.py` en gaat via `prompts.py` letterlijk de systeemprompt in. Elke regel daar weegt dus mee in het signaal dat de gebruiker ziet.
- De vindplaats staat in dat bestand bij de regel: `BRONNEN` voor de bronnen en `ACTUELE_FEITEN` voor jaargebonden regels (met status en datum van verificatie). Een nieuwe regel zonder vindplaats voeg je niet toe.
- `KENMERKEN_WERKTABEL` is een eigen hulplijst en geen citaat uit een bron. Houd haar zo, met per regel het gezichtspunt als vindplaats.
- `ACTUELE_FEITEN["controle_uiterlijk"]` is de houdbaarheidsdatum (1 januari 2027). Daarna waarschuwt de app, tenzij de kennisbasis eerst is bijgewerkt.
- Gezichtspunt 8 is het commercieel risico. De btw-, KVK- en IB-vragen horen bij gezichtspunt 9. Neem de oude indeling niet over uit oudere vrijgavenotities.

## Valkuilen

- De controle op modelantwoorden (`analyse_validatie.py`) toetst structuur, geen juridische juistheid. Wijzig je haar, voeg dan een test toe in `tests/test_analyse_validatie.py`.
- Elke inhoudelijke wijziging krijgt een vrijgavenotitie `vrijgave-dba-risicoscan-<datum>.md` in de wortel, zoals de bestaande.
- Er is geen `OPENSTAAND.md`. Open punten staan in de vrijgavenotities.
