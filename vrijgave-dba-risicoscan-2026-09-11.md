# Vrijgavenotitie DBA Risicoscan — 11-09-2026

**Tool:** DBA Risicoscan, https://dba-risicoscan.streamlit.app/
**Repository:** Sylvainbouwman/dba-risicoscan (publiek)
**Eigenaar:** Sylvain Bouwman
**Datum vrijgave:** 11-09-2026 10:51 CEST
**Status in het register:** beta, `laatst_beoordeeld` staat nog op leeg

## Wat is er gewijzigd

De tool bevat een kennisbasis die letterlijk wordt meegestuurd in elke analyse: negen gezichtspunten, een kenmerkentabel, een bronnenlijst en een blok "actuele stand van zaken". Dat laatste blok bevatte informatie die achterhaald was. Er stond dat de Wet VBAR en de Wet Wtta "nog niet ingevoerd" waren en dat de status "politiek onzeker" was. Dezelfde bewering stond zichtbaar in de zijbalk van de app. Gebruikers hebben dus analyses gekregen waarin het model werkte met een onjuiste stand van de wetgeving.

Vanaf deze versie klopt die stand weer, met de vindplaats per waarde vastgelegd in de code zelf. Voor de gebruiker verandert er zichtbaar twee dingen: de zijbalk meldt niet langer dat het rechtsvermoeden niet is ingevoerd maar dat het op 31 december 2026 ingaat en alleen civielrechtelijk werkt, en de waarschuwing over de handhaving noemt nu ook dat de zachte landing per 1 januari 2027 vervalt. In de analyse zelf verandert de onderbouwing waar het over wetgeving of handhaving gaat.

Daarnaast is één inhoudelijke weging hersteld. Bij gezichtspunt 3 (inbedding in de organisatie) stond dat de Hoge Raad dat gezichtspunt zwaar weegt. Dat staat haaks op de regel hoger in dezelfde prompt dat er geen rangorde geldt, en op het Uber-arrest. Het model werd daarmee gestuurd om de inbedding zwaarder te laten wegen dan de arresten toelaten.

Nieuw is een houdbaarheidsdatum. Wordt de tool na 1 januari 2027 gebruikt zonder dat de kennisbasis is bijgewerkt, dan verschijnt er een rode melding in beeld met het verzoek de beheerder te laten controleren. Dat is de maatregel tegen precies wat hier misging: feiten die ongemerkt verouderen terwijl zij het oordeel blijven sturen.

## Geraakte waarden

| Onderwerp | Oud | Nieuw | Ingangsdatum | Vindplaats |
|---|---|---|---|---|
| Rechtsvermoeden uurtarief | "nog NIET ingevoerd", "politiek onzeker" | Art. 7:610aa BW: ten hoogste EUR 36 per uur geeft een vermoeden van arbeidsovereenkomst; civielrechtelijk, niet fiscaal | Wet in werking 31-12-2026 | Wet 18-06-2026, Stb. 2026, 158; Besluit 13-07-2026, Stb. 2026, 207 |
| Bedrag eerste toepassing | (niet genoemd) | Bewust niet opgenomen: wordt bij ministeriele regeling vastgesteld en die bestaat nog niet | n.v.t. | Art. III, tweede lid Stb. 2026, 158; regeling niet gevonden op 11-09-2026 |
| Wet Wtta | "nog NIET ingevoerd" | Toelatingsstelsel voor uitleners, in werking per 01-01-2027, onderdelen per 01-07-2026 en 01-01-2028 | 01-01-2027 | Wet 12-11-2025, Stb. 2025, 385; Besluit 24-06-2026, Stb. 2026, 159 |
| Zachte landing boetes | "in 2026 worden verzuimboetes nog niet opgelegd" | Idem, aangevuld met: in beginsel eerst een bedrijfsbezoek, en per 01-01-2027 vervallen die elementen | jaargebonden 2026 | Kamerbrief 19-12-2025, dossier 31311; handhavingspagina Belastingdienst |
| Modelovereenkomsten | inhoudelijk juist, zonder vindplaats | ongewijzigd, vindplaats toegevoegd | 06-09-2024 / t/m 31-12-2029 | Belastingdienst, "Geen nieuwe modelovereenkomsten meer" |
| Weging gezichtspunt 3 | "door de Hoge Raad zwaar gewogen" | Geen vast zwaarder gewicht; geen rangorde, wel per situatie verschillend gewicht | n.v.t. | ECLI:NL:HR:2025:319, r.o. 3.3; SZW-toetsingskader juli 2026 |
| Houdbaarheidsdatum | (bestond niet) | 2027-01-01, met zichtbare melding in de app zodra verstreken | n.v.t. | volgt uit de twee ingangsdata hierboven |

Alle bronnen zijn zelf geraadpleegd op 11-09-2026: de Staatsbladen en de kamerbrief als volledige tekst, het SZW-toetsingskader als PDF, de arresten via data.rechtspraak.nl en de Belastingdienstpagina's rechtstreeks.

## Testset

De testsuite telt eenentwintig technische tests, gedraaid met `python -m unittest discover -s tests`: 21 van 21 groen. Acht daarvan zijn met deze wijziging toegevoegd. Zij bewaken dat de achterhaalde beweringen niet terugkeren in de systeemprompt, dat de wet en het inwerkingtredingsbesluit met hun Staatsbladnummer worden genoemd, dat het bedrag van EUR 36 alleen met zijn drie voorbehouden voorkomt, dat het niet-vastgestelde bedrag van 38 euro er juist niet in staat, dat gezichtspunt 3 geen zwaarder gewicht claimt en dat de houdbaarheidsmelding pas vanaf 1 januari 2027 afgaat. Nagemeten op de vorige versie: alle acht falen daar, dus zij betrappen het gebrek werkelijk.

Wat de tests niet afdekken: zij bewijzen dat de juiste tekst in de prompt staat, niet dat het model daar juridisch juist mee omgaat. Het signaal en de sterkte per gezichtspunt komen nog steeds van het model, zonder inhoudelijke regressieset. Er zijn geen tests die een volledige analyse beoordelen.

## Wat de eigenaar moet beoordelen

1. Hoort het bedrag van EUR 36 in de kennisbasis zolang de wet niet in werking is? Het staat er nu in, met drie voorbehouden en een uitdrukkelijk verbod het als drempel bij de negen gezichtspunten te gebruiken. De afweging was: weglaten is veiliger tegen ankering, maar een opdracht die nu wordt beoordeeld loopt vaak door tot na 31 december 2026 en dan moet de gebruiker weten dat er iets verandert.
2. Is de formulering bij gezichtspunt 3 juist? Zij maakt onderscheid tussen een rangorde vooraf, die er niet is, en een gewicht dat per situatie kan verschillen, wat wel kan. Dat onderscheid is subtiel en bepaalt hoe het model de inbedding weegt.
3. Klopt het dat de Wtta in deze tool thuishoort? Die wet gaat over uitleners en niet over de kwalificatie van een zzp-relatie. Zij stond al in de kennisbasis en is nu alleen gecorrigeerd; weglaten is ook verdedigbaar.

## Openstaande punten

- **Het achtste gezichtspunt klopt niet.** De tool noemt bij 8 "Al dan niet betalen van omzetbelasting". In r.o. 3.2.5 van het Deliveroo-arrest is dat "de vraag of degene die de werkzaamheden verricht daarbij commercieel risico loopt"; de fiscale behandeling is daar een deelaspect van gezichtspunt 9. Het commercieel risico ontbreekt daarmee geheel in de vragenlijst en in de prompt, terwijl de tool wel belooft de negen gezichtspunten uit het arrest te volgen. Dit is bewust buiten deze vrijgave gebleven omdat het de vragenlijst en het model raakt en niet alleen een verwijzing.
- **De ministeriele regeling met het uurbedrag bestaat nog niet.** Controleer voor 31 december 2026 of zij is verschenen; dan pas staat vast welk bedrag bij de eerste toepassing geldt.
- **Het uitgebreide beslis- en afwegingskader van de Belastingdienst is nog niet zelf gelezen.** Alleen de verkorte SZW-versie is nagekeken.
- **Het toetsingskader van SZW wordt volgens de vakpers aangepast** omdat formuleringen afwijken van de arresten. Daaruit is daarom alleen de weging overgenomen, en die is onafhankelijk getoetst aan het Uber-arrest.
- Het register vermeldt nog geen `laatst_beoordeeld` en de status staat op beta. Dat bijwerken hoort in `bouwman-tools` en is hier niet gedaan.

## Naschrift 11-09-2026 12:05 CEST — twee openstaande punten gesloten

Later dezelfde dag zijn twee van de openstaande punten hierboven weggewerkt. Zij staan in
een eigen wijziging, omdat het achtste gezichtspunt het model raakt en Sylvain daar eerst
toestemming voor moest geven.

**Het achtste gezichtspunt is hersteld naar het commercieel risico.** De naam, de
toelichting en de vier vragen erbij volgen nu r.o. 3.2.5 van het Deliveroo-arrest
(ECLI:NL:HR:2023:443), met in r.o. 3.1 van het Uber-arrest (ECLI:NL:HR:2025:319) de
nummering van de Hoge Raad zelf: [viii] is het commercieel risico, [ix] het
ondernemersgedrag. De btw-, KVK- en IB-vragen zijn niet geschrapt maar verplaatst naar
gezichtspunt 9, waar de fiscale behandeling volgens die overweging thuishoort. De
vragenlijst telt daardoor 27 vragen in plaats van 25.

**Het uitgebreide beslis- en afwegingskader van de Belastingdienst is nu wel zelf gelezen**
(uitgave april 2026, formulier LH 630-1Z*2PL, acht pagina's, met `pypdf` uitgelezen na
`curl` naar een map buiten de sessiemap). Gezichtspunt 8 staat er woordelijk in en het
kader staat nu als vindplaats in `BRONNEN`. Wat er niet in staat: geen termijn bij
gezichtspunt 1 en geen factor ten opzichte van het cao-loon bij gezichtspunt 7. Daarmee is
het spoor van de twee eerder verwijderde vuistregels afgelopen. De kenmerkentabel die in de
code `SZW_TABEL` heet staat er evenmin in, en ook niet in het SZW-kader van juli 2026; de
herkomst van die tabel blijft dus een openstaand punt en de naam suggereert meer dan er is.

De testsuite staat na die wijziging op 36 tests, alle groen, waarvan vijftien nieuw.
Nagemeten op de commit van vóór die ronde: veertien van de vijftien falen daar.
