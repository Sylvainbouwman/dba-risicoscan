"""
Juridische kennisbasis voor de DBA Risicoscan.
Bronnen: Deliveroo-arrest (HR 24 maart 2023, ECLI:NL:HR:2023:443), Uber-arrest
(HR 21 februari 2025, ECLI:NL:HR:2025:319), Belastingdienst, SZW-tabel, Rijksoverheid.

Bronverificatie 11-09-2026 (2026-09-11 07:05 UTC). De toelichtingen bevatten geen
kwantitatieve drempel meer. Tot die datum stond bij gezichtspunt 1 een termijn
(langer dan een jaar, zeker langer dan twee jaar zonder einddatum) en bij
gezichtspunt 7 een factor (minimaal 1,5x het brutoloon). Beide gingen via
NEGEN_GEZICHTSPUNTEN letterlijk de systeemprompt in en wogen dus mee in het signaal
dat de gebruiker te zien krijgt. Ze zijn verwijderd omdat zij geen vindplaats hebben.
Nagezocht en niet aangetroffen in:

- de volledige tekst van ECLI:NL:HR:2023:443 en ECLI:NL:HR:2025:319, opgehaald via
  data.rechtspraak.nl; de gezichtspunten staan in r.o. 3.2.5 van het Deliveroo-arrest
  en bevatten geen termijn en geen factor;
- de wetsgeschiedenis van het rechtsvermoeden op uurtarief: Stb. 2026, 158 voert
  art. 7:610aa BW in met een bedrag van ten hoogste EUR 36 per uur, dus een absoluut
  bedrag en geen factor ten opzichte van het cao-loon, en die wet is nog niet in
  werking (inwerkingtreding bij koninklijk besluit);
- de kennisgroepstandpunten loonheffingen op kennisgroepen.belastingdienst.nl;
- de voorlichting van Rijksoverheid en Belastingdienst over schijnzelfstandigheid.
  Die zegt over het tarief juist het omgekeerde: ook bij een hoog uurtarief kan
  sprake zijn van schijnzelfstandigheid, want het tarief is maar een van de criteria.

Factoren komen alleen voor in vakliteratuur en op commerciële sites, en dan onderling
tegenstrijdig (1,5x, 2x, 2,5x, of 50 tot 100 procent hoger dan het brutoloon). Dat is
geen grondslag waarop deze tool een risicosignaal mag baseren.

Eerder niet gelukte controle nu wel gelukt (11-09-2026): de PDF "Toelichting Beoordeling
arbeidsrelaties, beslis- en afwegingskader" (Belastingdienst, formulier LH 630-1Z*2PL,
uitgave april 2026) is met curl opgehaald en met pypdf uitgelezen, acht pagina's. Dat is
de primaire uitvoeringsbron waarvan het SZW-toetsingskader van juli 2026 een verkorte
afgeleide is; beide zijn nu zelf gelezen. De uitleg bij de negen gezichtspunten is in
beide woordelijk gelijk. Wat er niet in staat: geen termijn bij gezichtspunt 1 en geen
factor ten opzichte van het cao-loon bij gezichtspunt 7, en ook niet de kenmerkentabel
die hieronder als SZW_TABEL staat. Daarmee is het spoor van de twee verwijderde
vuistregels afgelopen: ook deze bron noemt ze niet.

Bronverificatie ACTUELE_FEITEN 11-09-2026 (2026-09-11 07:28 UTC). Tot die datum zei de
regel "wet_vbar" dat de Wet VBAR en de Wet WTTA "nog NIET ingevoerd" waren en dat de
status "politiek onzeker" was, met bijwerkdatum 3 juli 2026. Beide beweringen waren
achterhaald; de vervangende regels staan hieronder bij ACTUELE_FEITEN, met per regel de
vindplaats en de status. De weging bij gezichtspunt 3 is in dezelfde ronde hersteld: daar
stond dat de Hoge Raad dat gezichtspunt zwaar weegt, wat in strijd is met r.o. 3.3 van het
Uber-arrest en met de regel hoger in dezelfde systeemprompt dat er geen rangorde geldt.

Bronverificatie gezichtspunt 8 en 9, 11-09-2026 (2026-09-11 09:49 UTC). Tot die datum
heette het achtste gezichtspunt hieronder "Al dan niet betalen van omzetbelasting". Dat is
niet het achtste gezichtspunt van de Hoge Raad; het commercieel risico ontbrak daardoor
geheel in de systeemprompt en in de vragenlijst, terwijl de tool wel de belofte doet de
negen gezichtspunten uit het arrest te volgen. Zelf gelezen bewijs:

- ECLI:NL:HR:2023:443 (Deliveroo), r.o. 3.2.5, volledige tekst opgehaald via
  data.rechtspraak.nl. Het achtste gezichtspunt is daar letterlijk "de vraag of degene die
  de werkzaamheden verricht daarbij commercieel risico loopt". De fiscale behandeling is
  geen zelfstandig gezichtspunt maar een van de voorbeelden bij het negende: het gedrag
  als ondernemer in het economisch verkeer, "bijvoorbeeld bij het verwerven van een
  reputatie, bij acquisitie, wat betreft fiscale behandeling, en gelet op het aantal
  opdrachtgevers voor wie hij werkt of heeft gewerkt en de duur waarvoor hij zich
  doorgaans aan een bepaalde opdrachtgever verbindt".
- ECLI:NL:HR:2025:319 (Uber), r.o. 3.1. Daar citeert de Hoge Raad r.o. 3.2.5 van Deliveroo
  en voegt daaraan zelf een nummering toe ("de nummering van omstandigheden in rov. 3.2.5
  is toegevoegd"): [viii] is het commercieel risico en [ix] het gedrag als ondernemer in
  het economisch verkeer. Dat is dus de nummering van de Hoge Raad zelf en niet die van
  een samenvatting. R.o. 3.6.1 noemt het commercieel risico daarbij uitdrukkelijk als een
  omstandigheid binnen de te beoordelen verhouding die op ondernemerschap kan wijzen, en
  r.o. 3.6.2 bepaalt dat het negende gezichtspunt ook ziet op omstandigheden buiten die
  verhouding.
- Toetsingskader Beoordeling arbeidsrelaties, SZW, juli 2026, PDF zelf gelezen met pypdf.
  Gezichtspunt 8 heet daar "Mate waarin de opdrachtnemer bij de opdracht commercieel
  risico loopt", met als elementen de verdeling van risico's tussen opdrachtnemer en
  opdrachtgever bij schade aan derden, ziekte, ongeval en investeringen, en de mate waarin
  de opdrachtnemer verantwoordelijk is voor de kwaliteit van het resultaat (moet hij
  ondermaats werk in eigen tijd en voor eigen rekening herstellen).
- Toelichting Beoordeling arbeidsrelaties - Beslis- en afwegingskader, Belastingdienst,
  uitgave april 2026, formulier LH 630-1Z*2PL, PDF zelf gelezen met pypdf. Dit is de
  primaire uitvoeringsbron waarvan het SZW-kader een verkorte afgeleide is, en de uitleg
  bij gezichtspunt 8 is er woordelijk gelijk aan. Bij gezichtspunt 9 noemt dit kader de
  fiscale behandeling in eigen woorden: "hoe behandelt de Belastingdienst de
  opdrachtnemer". Dat bevestigt dat de btw-, KVK- en IB-vragen bij 9 thuishoren.

Gekozen weg: gezichtspunt 8 is vervangen door het commercieel risico. De btw-, KVK- en
IB-vragen zijn niet geschrapt maar verplaatst naar gezichtspunt 9, omdat de fiscale
behandeling daar volgens r.o. 3.2.5 thuishoort. Zij wegen dus nog mee, maar als deelaspect
van het ondernemersgedrag en niet als zelfstandig gezichtspunt met een eigen negende deel
van de weging. De vragenlijst in app.py telt daardoor 27 vragen in plaats van 25: bij
gezichtspunt 8 staan vier vragen over risicoverdeling, bij gezichtspunt 9 vijf vragen.
"""

NEGEN_GEZICHTSPUNTEN = [
    {
        "nummer": 1,
        "naam": "Aard en duur van de werkzaamheden",
        "toelichting": (
            "Projectmatig werk met een duidelijk eindresultaat wijst op ZZP-schap. "
            "Structurele, doorlopende taken die ook door vaste medewerkers worden uitgevoerd wijzen op loondienst. "
            "Aard en duur is het eerste gezichtspunt uit het Deliveroo-arrest "
            "(HR 24 maart 2023, ECLI:NL:HR:2023:443, r.o. 3.2.5). Een langdurige of doorlopende inzet "
            "zonder einddatum weegt mee, maar noem geen termijn als grens: de arresten en de voorlichting "
            "van Belastingdienst en Rijksoverheid noemen geen aantal maanden of jaren waarboven een "
            "opdracht als dienstbetrekking geldt. Weeg de duur daarom altijd in samenhang met de "
            "andere gezichtspunten."
        ),
    },
    {
        "nummer": 2,
        "naam": "Wijze waarop werkzaamheden en werktijden worden bepaald",
        "toelichting": (
            "Een opdrachtnemer die volledig zelf bepaalt hoe, wanneer en waar hij werkt wijst op ZZP-schap. "
            "Als de opdrachtgever vaste werktijden, locatie en werkwijze voorschrijft wijst dit sterk op loondienst "
            "(gezagselement). Het gezagselement is het kerncriterium van de arbeidsovereenkomst (art. 7:610 BW)."
        ),
    },
    {
        "nummer": 3,
        "naam": "Inbedding van het werk in de organisatie",
        "toelichting": (
            "Als de opdrachtnemer functioneert als onderdeel van het vaste team, gebruik maakt van het e-mailadres, "
            "visitekaartjes of systemen van de opdrachtgever, en vergelijkbaar werk doet als vaste medewerkers, "
            "wijst dit sterk op loondienst. Ook telt mee of het werk een wezenlijk onderdeel vormt van de "
            "bedrijfsvoering van de opdrachtgever. Inbedding is het derde gezichtspunt uit het Deliveroo-arrest "
            "(HR 24 maart 2023, ECLI:NL:HR:2023:443, r.o. 3.2.5). Ken dit gezichtspunt geen vast zwaarder gewicht "
            "toe dan de andere acht: de Hoge Raad heeft tussen de gezichtspunten geen rangorde aangebracht en ziet "
            "daarvoor ook nu geen aanleiding (Uber-arrest, HR 21 februari 2025, ECLI:NL:HR:2025:319, r.o. 3.3). "
            "Dat het gewicht van een gezichtspunt per situatie kan verschillen, is iets anders dan een rangorde vooraf."
        ),
    },
    {
        "nummer": 4,
        "naam": "Verplichting het werk persoonlijk uit te voeren",
        "toelichting": (
            "Als vervanging praktisch onmogelijk is of alleen met toestemming van de opdrachtgever, "
            "wijst dit op loondienst. Een echte ZZP'er kan zich vrij laten vervangen door iemand naar eigen keuze, "
            "en dit moet ook daadwerkelijk zijn voorgekomen of praktisch mogelijk zijn."
        ),
    },
    {
        "nummer": 5,
        "naam": "Wijze waarop de contractuele regeling tot stand is gekomen",
        "toelichting": (
            "Als de opdrachtnemer de voorwaarden vrijelijk kon onderhandelen wijst dit op ZZP-schap. "
            "Als de opdrachtgever een standaardcontract oplegde zonder onderhandelingsruimte, wijst dit meer op "
            "een gezagsverhouding. Let op: een modelovereenkomst biedt geen zekerheid als de feitelijke uitvoering afwijkt."
        ),
    },
    {
        "nummer": 6,
        "naam": "Wijze waarop de beloning wordt bepaald en uitbetaald",
        "toelichting": (
            "Betaling via factuur met BTW op basis van resultaat of vaste prijs wijst op ZZP-schap. "
            "Betaling per uur zonder BTW, of met loonelementen zoals vakantiegeld, pensioenopbouw "
            "of doorbetaling bij ziekte wijst sterk op loondienst."
        ),
    },
    {
        "nummer": 7,
        "naam": "Hoogte van de beloning",
        "toelichting": (
            "Een uurtarief dat duidelijk hoger ligt dan het vergelijkbare cao-uurloon inclusief werkgeverslasten "
            "(vakantiegeld, pensioen en sociale lasten) wijst op ZZP-schap. Een tarief vergelijkbaar met of "
            "lager dan dat cao-loon is een sterk risicosignaal. De hoogte van de beloning is het zevende "
            "gezichtspunt uit het Deliveroo-arrest (HR 24 maart 2023, ECLI:NL:HR:2023:443, r.o. 3.2.5). "
            "Er bestaat geen wettelijke of jurisprudentiële factor ten opzichte van het cao-loon; gebruik "
            "dus geen vuistregel met een vermenigvuldigingsfactor. Ook bij een hoog tarief kan sprake zijn "
            "van schijnzelfstandigheid, want het tarief is maar een van de criteria (Rijksoverheid, "
            "Veelgestelde vragen over schijnzelfstandigheid)."
        ),
    },
    {
        "nummer": 8,
        "naam": "Commercieel risico voor degene die de werkzaamheden verricht",
        "toelichting": (
            "Het achtste gezichtspunt is de vraag of degene die de werkzaamheden verricht daarbij "
            "commercieel risico loopt (Deliveroo-arrest, HR 24 maart 2023, ECLI:NL:HR:2023:443, "
            "r.o. 3.2.5; in het Uber-arrest, HR 21 februari 2025, ECLI:NL:HR:2025:319, r.o. 3.1, "
            "nummert de Hoge Raad deze omstandigheid zelf als [viii]). Het gaat om de verdeling van "
            "risico's tussen opdrachtnemer en opdrachtgever, onder meer bij schade aan derden, ziekte, "
            "ongeval en investeringen, en om de mate waarin de opdrachtnemer verantwoordelijk is voor de "
            "kwaliteit van het resultaat: moet hij ondermaats werk in eigen tijd en voor eigen rekening "
            "herstellen? Ligt het risico bij de opdrachtnemer, dan wijst dat op ZZP-schap; ligt het bij "
            "de opdrachtgever, dan wijst dat op loondienst. Bij een verdeeld risico geldt: hoe meer "
            "risico bij de opdrachtnemer, hoe sterker het signaal naar ZZP-schap (Belastingdienst, "
            "Toelichting Beoordeling arbeidsrelaties – Beslis- en afwegingskader, uitgave april "
            "2026, gezichtspunt 8, woordelijk gelijk in het Toetsingskader Beoordeling "
            "arbeidsrelaties van SZW van juli 2026). LET OP: de fiscale "
            "behandeling hoort niet bij dit gezichtspunt maar bij het negende; weeg btw, KVK en "
            "inkomstenbelasting dus daar en niet hier."
        ),
    },
    {
        "nummer": 9,
        "naam": "Gedrag als ondernemer in het economisch verkeer",
        "toelichting": (
            "Het negende gezichtspunt is of degene die de werkzaamheden verricht zich in het economisch "
            "verkeer als ondernemer gedraagt of kan gedragen, volgens r.o. 3.2.5 van het Deliveroo-arrest "
            "(HR 24 maart 2023, ECLI:NL:HR:2023:443) bijvoorbeeld bij het verwerven van een reputatie, bij "
            "acquisitie, wat betreft fiscale behandeling, en gelet op het aantal opdrachtgevers voor wie "
            "hij werkt of heeft gewerkt en de duur waarvoor hij zich doorgaans aan een bepaalde "
            "opdrachtgever verbindt. De fiscale behandeling valt dus onder dit gezichtspunt en is geen "
            "zelfstandig gezichtspunt: btw in rekening brengen en btw-aangifte doen, een actieve "
            "KVK-inschrijving en aangifte inkomstenbelasting als ondernemer (winst uit onderneming, "
            "eventueel met zelfstandigenaftrek) wijzen op ondernemerschap, en het ontbreken daarvan is een "
            "risicosignaal. Ook eigen acquisitie, website en branding wegen mee; exclusief voor één "
            "opdrachtgever werken is een sterk risicosignaal. Dit gezichtspunt ziet ook op "
            "ondernemerskenmerken buiten de te beoordelen arbeidsrelatie (Uber-arrest, HR 21 februari 2025, "
            "ECLI:NL:HR:2025:319, r.o. 3.6.2) en heeft geen ander gewicht dan de andere acht (r.o. 3.3). "
            "Het dragen van commercieel risico weeg je niet hier maar bij het achtste gezichtspunt."
        ),
    },
]

# Werktabel met kenmerken, per index gepaard: regel n van de ene lijst is de tegenhanger
# van regel n van de andere. Nagelopen op 11-09-2026 bij het herstel van gezichtspunt 8.
# Het financieel risico stond hier al, maar in een vorm die alleen aansprakelijkheid bij
# fouten noemde. De regels zijn gelijkgetrokken met de elementen die bij gezichtspunt 8
# horen: schade aan derden, ziekte, ongeval, investeringen en de verantwoordelijkheid voor
# de kwaliteit van het resultaat (Toetsingskader Beoordeling arbeidsrelaties, SZW, juli
# 2026, gezichtspunt 8). De btw- en KVK-regels blijven staan; zij horen sinds dezelfde
# ronde bij gezichtspunt 9. De herkomst van deze tabel zelf blijft een openstaande vraag.
# Nagemeten op 11-09-2026: de tabel komt niet voor in het beslis- en afwegingskader van de
# Belastingdienst (april 2026) en niet in het toetsingskader van SZW (juli 2026, beide PDF
# zelf uitgelezen). Zij is dus geen citaat uit een officiele bron maar een werktabel, en
# de naam SZW_TABEL suggereert meer herkomst dan er is; zie OPENSTAANDE-VRAGEN.md.
SZW_TABEL = {
    "zzp_kenmerken": [
        "Bepaalt zelf hoe het werk wordt uitgevoerd",
        "Draagt commercieel risico: aansprakelijk bij schade aan derden, geen doorbetaling bij ziekte of ongeval",
        "Herstelt een ondermaats resultaat in eigen tijd en voor eigen rekening (no cure no pay)",
        "Investeert in eigen bedrijfsmiddelen of gereedschap",
        "Heeft meerdere opdrachtgevers (actief)",
        "Kan zich vrij laten vervangen door iemand naar eigen keuze",
        "Bepaalt eigen werktijden en werkplek",
        "Brengt BTW in rekening en doet btw-aangifte",
        "Staat actief ingeschreven bij KVK, heeft eigen branding",
        "Presenteert zich actief als ondernemer (website, acquisitie)",
        "Uurtarief duidelijk hoger dan vergelijkbaar cao-loon incl. werkgeverslasten",
    ],
    "loondienst_kenmerken": [
        "Ontvangt instructies over hoe, wanneer en waar te werken",
        "Opdrachtgever draagt het risico bij schade aan derden, ziekte en ongeval",
        "Een ondermaats resultaat wordt in de tijd en voor rekening van de opdrachtgever hersteld",
        "Werkt met materialen, systemen of gereedschap van de opdrachtgever",
        "Werkt exclusief of vrijwel exclusief voor één opdrachtgever",
        "Moet persoonlijk werken; vervanging niet of nauwelijks toegestaan",
        "Werktijden en locatie worden bepaald door opdrachtgever",
        "Geen BTW op factuur, of betaling zonder factuur",
        "Geen of slapende KVK-inschrijving; geen eigen acquisitie",
        "Geïntegreerd in het team; zelfde werk als vaste medewerkers",
        "Tarief vergelijkbaar met of lager dan cao-loon",
    ],
}

BRONNEN = {
    "deliveroo": {
        "naam": "Hoge Raad: Deliveroo-arrest",
        "datum": "24 maart 2023",
        "ecli": "ECLI:NL:HR:2023:443",
        "url": "https://uitspraken.rechtspraak.nl/details?id=ECLI:NL:HR:2023:443",
        "inhoud": "Vaststelling negen gezichtspunten voor holistische beoordeling arbeidsrelatie",
    },
    "uber": {
        "naam": "Hoge Raad: Uber-arrest (prejudiciële beslissing)",
        "datum": "21 februari 2025",
        # ECLI gecontroleerd 11-09-2026 op data.rechtspraak.nl: zaaknummer 24/00877.
        # ECLI:NL:HR:2025:329 stond hier eerder en is een strafzaak, niet het Uber-arrest.
        "ecli": "ECLI:NL:HR:2025:319",
        "url": "https://uitspraken.rechtspraak.nl/details?id=ECLI:NL:HR:2025:319",
        "inhoud": "Prejudiciële beslissing over het gezichtspunt ondernemerschap; tussen de gezichtspunten geldt geen rangorde (r.o. 3.3) en ook extern ondernemerschap weegt volledig mee",
    },
    "belastingdienst_ar": {
        "naam": "Belastingdienst: Arbeidsrelaties zzp – ja of nee",
        "url": "https://www.belastingdienst.nl/wps/wcm/connect/nl/arbeidsrelaties/arbeidsrelaties",
        "inhoud": "Officieel beoordelingskader Belastingdienst",
    },
    "belastingdienst_handhaving": {
        "naam": "Belastingdienst: Handhaving arbeidsrelaties",
        "url": "https://www.belastingdienst.nl/wps/wcm/connect/nl/arbeidsrelaties/content/handhaving",
        # Geraadpleegd 11-09-2026: "We leggen in 2026 nog geen verzuimboetes op" en
        # "Vanaf 1 januari 2026 kunnen we wel vergrijpboetes opleggen".
        "inhoud": "Normale handhaving hervat per 1 januari 2025; in 2026 geen verzuimboetes, wel vergrijpboetes",
    },
    "kamerbrief_zachte_landing": {
        "naam": "Kamerbrief Gedeeltelijke verlenging zachte landing handhaving schijnzelfstandigheid",
        "datum": "19 december 2025",
        # Dossier 31311. PDF zelf gelezen 11-09-2026 via open.overheid.nl. Letterlijk:
        # de zachte landing wordt in 2026 deels verlengd "door ook in 2026 geen
        # verzuimboetes op te leggen en in beginsel te starten met een bedrijfsbezoek.
        # Pas vanaf 1 januari 2027 zullen ook deze elementen van de zachte landing komen
        # te vervallen."
        "url": "https://www.rijksoverheid.nl/documenten/kamerstukken/2025/12/19/gedeeltelijke-verlenging-zachte-landing-handhaving-schijnzelfstandigheid",
        "inhoud": "Zachte landing in 2026 deels verlengd (geen verzuimboetes, in beginsel bedrijfsbezoek); die elementen vervallen per 1 januari 2027",
    },
    "belastingdienst_model": {
        "naam": "Belastingdienst: Modelovereenkomsten",
        "url": "https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/ondernemen/modelovereenkomsten-in-plaats-van-var/arbeidsrelaties",
        # Geraadpleegd 11-09-2026 op de pagina "Geen nieuwe modelovereenkomsten meer".
        "inhoud": "Sinds 6 september 2024 geen nieuwe beoordelingen; op die datum goedgekeurde overeenkomsten geldig t/m 31 december 2029",
    },
    "rijksoverheid_schijnzelfstandigheid": {
        "naam": "Rijksoverheid: Veelgestelde vragen over schijnzelfstandigheid",
        "url": "https://www.rijksoverheid.nl/themas/werk/zelfstandigen-zonder-personeel-zzp/veelgestelde-vragen-schijnzelfstandigheid",
        # Geraadpleegd 11-09-2026. Noemt geen termijn en geen tariefdrempel.
        "inhoud": "Ook bij een hoog uurtarief kan sprake zijn van schijnzelfstandigheid; het tarief is maar een van de criteria",
    },
    "stb_2026_158": {
        "naam": "Wet invoering rechtsvermoeden van arbeidsovereenkomst op basis van uurtarief",
        "datum": "18 juni 2026, Stb. 2026, 158",
        # Staatsblad zelf gelezen 11-09-2026. Art. I voert art. 7:610aa BW in; art. III
        # regelt inwerkingtreding bij koninklijk besluit en bepaalt dat het toepasselijke
        # bedrag voor de eerste toepassing bij ministeriele regeling wordt vastgesteld.
        "url": "https://zoek.officielebekendmakingen.nl/stb-2026-158.html",
        "inhoud": "Voert art. 7:610aa BW in: wie arbeid verricht tegen ten hoogste EUR 36 per uur wordt vermoed dat krachtens arbeidsovereenkomst te doen; civielrechtelijk vermoeden, geen fiscale beoordelingsregel",
    },
    "stb_2026_207": {
        "naam": "Besluit vaststelling tijdstip inwerkingtreding rechtsvermoeden uurtarief",
        "datum": "13 juli 2026, Stb. 2026, 207",
        # Staatsblad zelf gelezen 11-09-2026; gepubliceerd 15 juli 2026.
        "url": "https://zoek.officielebekendmakingen.nl/stb-2026-207.html",
        "inhoud": "De wet van 18 juni 2026 treedt in werking met ingang van 31 december 2026",
    },
    "wtta": {
        "naam": "Wet toelating terbeschikkingstelling van arbeidskrachten (Wtta)",
        "datum": "12 november 2025, Stb. 2025, 385",
        # Wet en inwerkingtredingsbesluit (Besluit van 24 juni 2026, Stb. 2026, 159)
        # vastgesteld op 11-09-2026 via de SRU-catalogus van officielebekendmakingen.nl.
        # De Wtta gaat over uitleners, niet over de kwalificatie van een zzp-relatie.
        "url": "https://zoek.officielebekendmakingen.nl/stb-2025-385.html",
        "inhoud": "Toelatingsstelsel voor uitleners; in werking per 1 januari 2027 (Besluit van 24 juni 2026, Stb. 2026, 159), met onderdelen per 1 juli 2026 en 1 januari 2028",
    },
    "afwegingskader_belastingdienst": {
        "naam": "Belastingdienst: Toelichting Beoordeling arbeidsrelaties – Beslis- en afwegingskader",
        "datum": "april 2026",
        # PDF zelf gelezen 11-09-2026 (8 pagina's, formulier LH 630-1Z*2PL). Dit is de
        # primaire uitvoeringsbron; het SZW-toetsingskader is er een verkorte afgeleide
        # van. Gezichtspunt 8 staat er woordelijk gelijk in. Eerdere sessies kregen deze
        # PDF niet machinaal uitgelezen; de route die werkt is curl naar een map buiten
        # de sessiemap, daarna pypdf.
        "url": "https://download.belastingdienst.nl/belastingdienst/docs/afwegingskader_dienstbetrekking_lh6301z2pl.pdf",
        "inhoud": "Beslis- en afwegingskader met de uitleg per gezichtspunt; gezichtspunt 8 is de mate waarin de opdrachtnemer bij de opdracht commercieel risico loopt",
    },
    "toetsingskader_szw": {
        "naam": "Ministerie van SZW: Toetsingskader Beoordeling arbeidsrelaties",
        "datum": "juli 2026",
        # PDF zelf gelezen 11-09-2026 (4 pagina's, uitgave SZW juli 2026). Verkorte
        # afgeleide van het beslis- en afwegingskader van de Belastingdienst. Volgens
        # berichtgeving in de vakpers past SZW deze versie aan omdat formuleringen
        # afwijken van de arresten; daarom is hieruit alleen de weging overgenomen, die
        # woordelijk strookt met r.o. 3.3 van het Uber-arrest.
        "url": "https://open.overheid.nl/details/37593cde-4044-4634-93cb-dfbc8375e629",
        "inhoud": "Tussen de negen gezichtspunten geldt geen rangorde; het belang van een gezichtspunt kan per situatie verschillen",
    },
    "webmodule": {
        "naam": "Webmodule Beoordeling Arbeidsrelatie",
        "url": "https://www.webmodulearbeidsrelaties.nl",
        "inhoud": "Indicatief hulpmiddel overheid; niet juridisch bindend",
    },
    "rijksoverheid": {
        "naam": "Rijksoverheid: Van VAR naar Wet DBA (chronologisch overzicht 2026)",
        "url": "https://www.rijksoverheid.nl/onderwerpen/zzp",
        "inhoud": "Actuele stand van zaken en historisch overzicht wetgeving ZZP",
    },
}

# Elke regel hieronder gaat via prompts.py letterlijk de systeemprompt in en weegt dus
# mee in het signaal dat de gebruiker ziet. Daarom staat bij elke regel de vindplaats,
# en waar de regel jaargebonden is of nog geen geldend recht is, ook de status.
# Geverifieerd 11-09-2026 (2026-09-11 07:28 UTC); zie de docstring bovenaan.
ACTUELE_FEITEN = {
    # JAARGEBONDEN, geldt voor 2026. Bron: Kamerbrief 19 december 2025 "Gedeeltelijke
    # verlenging zachte landing handhaving schijnzelfstandigheid" (dossier 31311),
    # bevestigd op de pagina Handhaving arbeidsrelaties van de Belastingdienst.
    # Zie BRONNEN["kamerbrief_zachte_landing"] en BRONNEN["belastingdienst_handhaving"].
    "handhaving": (
        "Normale handhavingsregels gelden weer per 1 januari 2025. "
        "Voor 2026 geldt een gedeeltelijk verlengde zachte landing: er worden geen verzuimboetes opgelegd "
        "en de Belastingdienst start in beginsel met een bedrijfsbezoek. "
        "Vergrijpboetes (bij opzet of grove schuld) kunnen sinds 1 januari 2026 wel worden opgelegd. "
        "Correctieverplichtingen en naheffingen loonheffingen zijn actief: naheffen kan terug tot "
        "1 januari 2025, en bij kwaadwillendheid tot vijf jaar terug. "
        "Per 1 januari 2027 vervallen ook de verzuimboete- en bedrijfsbezoekelementen van de zachte landing."
    ),
    # Bron: Belastingdienst, "Geen nieuwe modelovereenkomsten meer", geraadpleegd
    # 11-09-2026. Letterlijk: "Sinds 6 september 2024 beoordelen we geen nieuwe
    # overeenkomsten meer" en "Goedgekeurde modelovereenkomsten die geldig waren op
    # 6 september 2024, mag u blijven gebruiken tot en met 31 december 2029."
    "modelovereenkomsten": (
        "De Belastingdienst beoordeelt sinds 6 september 2024 geen nieuwe modelovereenkomsten meer. "
        "Modelovereenkomsten die op 6 september 2024 waren goedgekeurd, mogen worden gebruikt "
        "tot en met 31 december 2029. "
        "CRUCIAAL: een modelovereenkomst biedt GEEN zekerheid als de feitelijke uitvoering ervan afwijkt. "
        "De Belastingdienst beoordeelt altijd de feitelijke situatie, niet het papier."
    ),
    # AANGENOMEN WET MET LATERE INGANGSDATUM, nog geen geldend recht op de bijwerkdatum.
    # Wet van 18 juni 2026, Stb. 2026, 158 (BRONNEN["stb_2026_158"]); inwerkingtreding
    # 31 december 2026 bij Besluit van 13 juli 2026, Stb. 2026, 207
    # (BRONNEN["stb_2026_207"]). Het bedrag van EUR 36 staat in de wettekst zelf; het
    # bedrag dat bij de eerste toepassing geldt, wordt op grond van artikel III, tweede
    # lid, bij ministeriele regeling vastgesteld. Die regeling is op 11-09-2026 niet
    # gevonden in Staatsblad of Staatscourant (drie zoekslagen via de SRU-catalogus van
    # officielebekendmakingen.nl). Het kabinet noemt in zijn nieuwsbericht van
    # 6 maart 2026 een bedrag van 38 euro per uur met peildatum 1 januari 2026; dat is
    # voorlichting en geen vastgesteld bedrag, en het staat daarom bewust niet hieronder.
    "rechtsvermoeden_uurtarief": (
        "De Wet invoering rechtsvermoeden van arbeidsovereenkomst op basis van een uurtarief "
        "(wet van 18 juni 2026, Stb. 2026, 158) is aangenomen en gepubliceerd, maar treedt pas "
        "op 31 december 2026 in werking (Besluit van 13 juli 2026, Stb. 2026, 207). "
        "Zij voert artikel 7:610aa BW in: wie tegen een beloning van ten hoogste EUR 36 per uur arbeid "
        "verricht, wordt vermoed dat krachtens arbeidsovereenkomst te doen. Het bedrag dat bij de eerste "
        "toepassing geldt, wordt bij ministeriele regeling vastgesteld en stond op de bijwerkdatum nog niet vast. "
        "BELANGRIJK voor deze analyse: dit rechtsvermoeden werkt alleen civielrechtelijk, tussen werkende en "
        "werkgevende, en verandert niets aan de fiscale beoordeling van de arbeidsrelatie. Gebruik het bedrag "
        "daarom NIET als drempel of vuistregel bij het wegen van de negen gezichtspunten, en noem het alleen "
        "als vooruitblik wanneer de opdracht doorloopt tot na 31 december 2026. "
        "Het verduidelijkingsdeel van het oorspronkelijke wetsvoorstel VBAR is geschrapt; het kabinet "
        "kondigde op 6 maart 2026 een Zelfstandigenwet aan als vervanger, en die is er nog niet."
    ),
    # AANGENOMEN WET, gedeeltelijk in werking. Wet van 12 november 2025, Stb. 2025, 385;
    # inwerkingtreding per 1 januari 2027 bij Besluit van 24 juni 2026, Stb. 2026, 159,
    # met onderdelen per 1 juli 2026 en 1 januari 2028. Zie BRONNEN["wtta"]. Opgenomen
    # omdat de kennisbasis deze wet noemde; zij raakt uitleners en niet de kwalificatie
    # van de arbeidsrelatie zelf.
    "wtta": (
        "De Wet toelating terbeschikkingstelling van arbeidskrachten (Wtta, Stb. 2025, 385) treedt "
        "in werking per 1 januari 2027; enkele onderdelen gelden al sinds 1 juli 2026 en de handhaving "
        "volgt per 1 januari 2028. De Wtta regelt een toelatingsplicht voor het ter beschikking stellen "
        "van arbeidskrachten en gaat dus over uitleners. Zij verandert niets aan de vraag of een "
        "opdrachtnemer zelfstandige of werknemer is; noem haar alleen wanneer de opdracht via een "
        "intermediair loopt."
    ),
    "bijgewerkt": "11 september 2026",
    # Uiterlijke houdbaarheid van de jaargebonden regels hierboven: per 1 januari 2027
    # vervalt de zachte landing en treedt het rechtsvermoeden in werking. De app
    # waarschuwt zichtbaar zodra deze datum is verstreken, zodat een verouderde
    # kennisbasis niet stilzwijgend de systeemprompt in gaat.
    "controle_uiterlijk": "2027-01-01",
}
