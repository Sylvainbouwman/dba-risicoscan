# Vrijgavenotitie DBA Risicoscan, vervolg vindplaats gezichtspunt 5 en 6, 04-10-2026

**Tool:** DBA Risicoscan, https://dba-risicoscan.streamlit.app/
**Repository:** Sylvainbouwman/dba-risicoscan (publiek)
**Eigenaar:** Sylvain Bouwman
**Datum:** 04-10-2026 (PR #8, gemerged op 04-10-2026)

## Wat is er gewijzigd

Vervolg op de notitie van 27-09-2026 (open punt 6). In `NEGEN_GEZICHTSPUNTEN` in `knowledge_base.py`:

- Gezichtspunt 5: de opmerking over de modelovereenkomst heeft nu een vindplaats, de slotzin van
  r.o. 3.2.5 van HR 24 maart 2023, ECLI:NL:HR:2023:443: het gewicht van een contractueel beding
  hangt mede af van de mate waarin dat beding daadwerkelijk betekenis heeft voor degene die de
  werkzaamheden verricht.
- Gezichtspunt 6: de verwijzing naar het negende gezichtspunt zegt nu dat r.o. 3.2.5 de fiscale
  behandeling als voorbeeld van ondernemersgedrag noemt, en dat het arrest alleen "fiscale
  behandeling" zegt (dat de btw daaronder valt is de indeling van de tool).

## Onafhankelijke toets

De agent `bron-controleur` heeft r.o. 3.2.5 zelf opgehaald en beide zinnen getoetst: juist,
met één kanttekening bij de btw-formulering in gezichtspunt 6. Die is in dezelfde ronde verwerkt.

## Testset

40 van 40 tests groen (`python -m unittest discover -s tests`), waarvan drie nieuw (twee voor de zinnen hierboven, één voor de modelmelding).

## Onderhoud in dezelfde branch (open punten 8, 9 en 10)

- `.github/workflows/tests.yml`: draait de testset op elke push en pull request. Publiceert niets,
  gebruikt geen secrets.
- `requirements.txt`: exact vastgepind op de versies waarmee de tests en de app zijn gedraaid
  (streamlit 1.57.0, anthropic 0.104.1, python-docx 1.2.0).
- `app.py`: bij een ingetrokken model-ID (404 van de API) toont de app een eigen melding aan de
  beheerder in plaats van de algemene foutmelding. Geen automatische terugval op een ander model.
- Testset nu 40 van 40 groen, waarvan één nieuwe test voor die melding.

## Wat de eigenaar moet beoordelen

- Gezichtspunt 6 zegt nu dat het arrest alleen "fiscale behandeling" noemt en dat de btw daaronder
  valt volgens de indeling van de tool. Is die indeling zo gewenst, of moet de btw-vraag elders
  hangen? Zonder reactie blijft de huidige indeling staan.
- De exacte versies in `requirements.txt` zijn gemeten op Python 3.14 lokaal en 3.13 in de CI. Na de
  merge herbouwt Streamlit de live app; die herbouw is niet waargenomen.

## Openstaande punten

- De beschrijvende tekst bij gezichtspunt 4, 5 en 6 heeft buiten r.o. 3.2.5 zelf geen eigen
  vindplaats. Dit is eigen uitwerking, net als bij de meeste andere gezichtspunten.
- Geen inhoudelijke regressieset voor het signaal per gezichtspunt (eigen sessie later).
- Het SZW-toetsingskader van juli 2026 wordt volgens de vakpers aangepast; nog geen nieuwe versie.
