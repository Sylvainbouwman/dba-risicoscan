# Vrijgavenotitie DBA Risicoscan — vindplaats gezichtspunt 4, 5 en 6 — 27-09-2026

**Tool:** DBA Risicoscan, https://dba-risicoscan.streamlit.app/
**Repository:** Sylvainbouwman/dba-risicoscan (publiek)
**Eigenaar:** Sylvain Bouwman
**Datum vrijgave:** 27-09-2026

## Wat is er gewijzigd

Bij gezichtspunt 4 ("Verplichting het werk persoonlijk uit te voeren"), 5 ("Wijze waarop
de contractuele regeling tot stand is gekomen") en 6 ("Wijze waarop de beloning wordt
bepaald en uitbetaald") in `knowledge_base.py` ontbrak een eigen expliciete vindplaats
(ECLI en rechtsoverweging), terwijl de andere zes gezichtspunten die al wel hadden. Bij
elk van de drie is nu een zin toegevoegd die het gezichtspunt aanduidt als het vierde,
vijfde respectievelijk zesde gezichtspunt uit het Deliveroo-arrest (HR 24 maart 2023,
ECLI:NL:HR:2023:443, r.o. 3.2.5).

## Onafhankelijke toets

De agent `bron-controleur` heeft r.o. 3.2.5 zelf opgehaald via data.rechtspraak.nl en de
nummering van alle drie gecontroleerd: juist. Go voor de drie toevoegingen.

Kanttekening van de agent: de vindplaats dekt alleen de nummering, niet de volledige
beschrijvende tekst ervoor. R.o. 3.2.5 noemt de gezichtspunten kort en werkt ze niet
verder uit; de beschrijvende toelichting bij 4, 5 en 6 (net als bij de meeste andere
gezichtspunten) is eigen uitwerking zonder eigen bron. Dat is dezelfde situatie als bij
de bestaande toelichtingen van de overige gezichtspunten en dus geen nieuw gebrek, maar
wel iets om te weten bij een volgende bronronde. Zie de openstaande punten hieronder.

## Testset

37 van 37 tests groen (`python -m unittest discover -s tests`), ongewijzigd; er is geen
nieuwe test toegevoegd omdat dit een tekstuele aanvulling is zonder nieuw gedrag om te
bewaken.

## Openstaande punten

- De beschrijvende tekst bij gezichtspunt 4, 5 en 6 (los van de nieuwe citaatzin) heeft
  nog geen eigen vindplaats buiten r.o. 3.2.5 zelf. Zie `OPENSTAANDE-VRAGEN.md`.
- Bij gezichtspunt 5 kan de slotzin van r.o. 3.2.5 (gewicht van een contractueel beding
  hangt mede af van de mate waarin het daadwerkelijk betekenis heeft) nog als expliciete
  vindplaats voor de modelovereenkomst-opmerking worden toegevoegd.
- Bij gezichtspunt 6 kan de fiscale behandeling explicieter als voorbeeld binnen het
  negende gezichtspunt worden geformuleerd, in plaats van als aparte verwijzing.
