# Vrijgavenotitie DBA Risicoscan, vervolg vindplaats gezichtspunt 5 en 6, 04-10-2026

**Tool:** DBA Risicoscan, https://dba-risicoscan.streamlit.app/
**Repository:** Sylvainbouwman/dba-risicoscan (publiek)
**Eigenaar:** Sylvain Bouwman
**Datum:** 04-10-2026 (branch, nog niet gemerged)

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

39 van 39 tests groen (`python -m unittest discover -s tests`), waarvan twee nieuw voor deze zinnen.
