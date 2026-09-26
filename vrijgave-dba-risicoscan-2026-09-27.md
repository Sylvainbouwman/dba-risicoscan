# Vrijgavenotitie DBA Risicoscan — 27-09-2026

**Tool:** DBA Risicoscan, https://dba-risicoscan.streamlit.app/
**Repository:** Sylvainbouwman/dba-risicoscan (publiek)
**Eigenaar:** Sylvain Bouwman
**Datum vrijgave:** 27-09-2026
**Status in het register:** beta, `laatst_beoordeeld` staat nog op leeg

## Wat is er gewijzigd

De kennisbasis bevat een eigen hulplijst (`KENMERKEN_WERKTABEL`, tot 15-09-2026 `SZW_TABEL`) met tweeëntwintig kenmerken die op ZZP-schap of loondienst wijzen. Die lijst ging integraal de systeemprompt in, maar geen enkele regel had een eigen vindplaats: alleen de negen gezichtspunten daarboven hadden dat al. Dat is hetzelfde soort gebrek als eerder bij de twee verwijderde vuistregels en het onjuiste achtste gezichtspunt: een waarde die het oordeel van het model stuurt zonder dat zij ergens op berust.

Elke regel is nu herleid tot een van de negen gezichtspunten uit het Deliveroo-arrest, met dat gezichtspuntnummer als vindplaats. De systeemprompt toont dat nummer voortaan achter elke regel, zodat het model haar niet als eigen gezag kan behandelen maar als toelichting bij een gezichtspunt dat wel een vindplaats heeft. Voor de gebruiker verandert er niets zichtbaars in de app zelf; de wijziging zit in de onderbouwing die het model meekrijgt.

Bij de herleiding kwam een koppelfout aan het licht: de loondienstregel "geïntegreerd in het team; zelfde werk als vaste medewerkers" stond op dezelfde positie als de zzp-regel over ondernemersgedrag (gezichtspunt 9), terwijl zij inhoudelijk bij gezichtspunt 3 (inbedding in de organisatie) hoort. Ook bleken twee regels elk twee gezichtspunten tegelijk te bestrijken; die zijn gesplitst. De toelichting bij gezichtspunt 6 noemde daarnaast zelf ten onrechte de btw, die volgens het arrest bij gezichtspunt 9 hoort; dat is eruit gehaald.

## Geraakte waarden

| Onderwerp | Oud | Nieuw | Vindplaats |
|---|---|---|---|
| Kenmerkentabel, structuur | Twee lijsten van elk 11 regels, per index gepaard, zonder vindplaats | 24 losse regels, elk met een gezichtspunt-nummer (1 t/m 9) als vindplaats | Deliveroo-arrest, ECLI:NL:HR:2023:443, r.o. 3.2.5 |
| "Geïntegreerd in het team; zelfde werk als vaste medewerkers" | Gekoppeld aan gezichtspunt 9 (via de indexpairing) | Gezichtspunt 3 (inbedding) | Toelichting gezichtspunt 3 in de code; inhoudelijk overeenkomend, geen letterlijk citaat |
| "Werkt met materialen, systemen of gereedschap van de opdrachtgever" | Eén regel bij gezichtspunt 8 | Gesplitst: materialen/gereedschap blijft bij gezichtspunt 8, "systemen van de opdrachtgever" is een eigen regel bij gezichtspunt 3 | Toelichting gezichtspunt 3 noemt "systemen van de opdrachtgever" woordelijk |
| "Geen BTW op factuur, of betaling zonder factuur" | Eén regel bij gezichtspunt 9 | Gesplitst: btw blijft bij gezichtspunt 9, "betaling zonder factuur" is een eigen regel bij gezichtspunt 6 | R.o. 3.2.5: fiscale behandeling hoort bij het negende gezichtspunt; wijze van uitbetalen bij het zesde |
| Toelichting gezichtspunt 6 | Noemde btw als voorbeeld ("betaling via factuur met BTW") | Btw verwijderd, met verwijzing naar gezichtspunt 9 | R.o. 3.2.5 noemt fiscale behandeling alleen bij het negende gezichtspunt |

Alle bronnen zijn zelf geraadpleegd: r.o. 3.2.5 van het Deliveroo-arrest (ECLI:NL:HR:2023:443) via data.rechtspraak.nl, opnieuw nagelezen door de agent bron-controleur bij de onafhankelijke toets op 27-09-2026.

## Onafhankelijke toets

De agent `bron-controleur` heeft de 22 oorspronkelijke koppelingen regel voor regel tegen r.o. 3.2.5 getoetst: 19 meteen juist, 3 twijfelachtig, 0 onjuist, 0 te schrappen. De drie twijfelgevallen (de koppelfout en de twee dubbelop-regels) zijn verwerkt zoals hierboven beschreven. De agent gaf een go onder de genoemde voorwaarden; alle vijf voorwaarden zijn doorgevoerd, inclusief het afzwakken van een te stellige uitspraak in de prompttekst over waar een vindplaats te vinden is (niet elk gezichtspunt noemt zelf een ECLI of r.o.) en het rechtzetten van de terminologie in het codecommentaar ("bronverificatie" → "herleiding", "woordelijk" → "inhoudelijk").

## Testset

De testsuite telt zevenendertig technische tests, gedraaid met `python -m unittest discover -s tests`: 37 van 37 groen. Eén nieuwe test bewaakt dat elke regel van de kenmerkentabel een bestaand gezichtspuntnummer als vindplaats heeft.

Wat de tests niet afdekken: zij bewijzen dat de juiste vindplaats in de code en de prompt staat, niet dat het model daar juridisch juist mee omgaat. Dat gold al voor de eerdere vrijgaven.

## Wat de eigenaar moet beoordelen

1. Is de splitsing van "systemen van de opdrachtgever" naar gezichtspunt 3 juist, of hoort dit toch bij gezichtspunt 8 als onderdeel van de bedrijfsmiddelen? Gekozen is voor gezichtspunt 3 omdat de toelichting daar "systemen van de opdrachtgever" letterlijk noemt.
2. Op gezichtspunt 1 en 5 staat bewust geen regel uit de kenmerkentabel, omdat geen van de oorspronkelijke tweeëntwintig regels daar inhoudelijk bij hoorde. Is dat een gemis voor de gebruiker, of is de toelichting bij die twee gezichtspunten op zichzelf voldoende?

## Openstaande punten

- Bij drie van de negen gezichtspunten (4, 5 en 6) noemt de toelichting nog geen eigen vindplaats (ECLI of r.o.), terwijl de andere zes dat wel doen. Zie `OPENSTAANDE-VRAGEN.md`.
- Het bedrag van het rechtsvermoeden bij de eerste toepassing staat nog niet vast; controlemoment vóór 31 december 2026.
- Geen `AGENTS.md`, geen CI-keten en ongepinde dependencies.
- Het register vermeldt nog geen `laatst_beoordeeld` en de status staat op beta. Dat bijwerken hoort in `bouwman-tools` en is hier niet gedaan.
