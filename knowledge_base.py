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

Niet gelukte controle: de PDF "Toelichting Beoordeling arbeidsrelaties, beslis- en
afwegingskader" (Belastingdienst, formulier LH 630-1Z*2PL) bleek niet machinaal te
lezen. Die bron is dus niet zelf nagekeken; zie OPENSTAANDE-VRAGEN.md.
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
            "wijst dit sterk op loondienst. Dit gezichtspunt wordt door de Hoge Raad zwaar gewogen in Deliveroo en Uber."
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
        "naam": "Al dan niet betalen van omzetbelasting",
        "toelichting": (
            "Het in rekening brengen van BTW en het doen van btw-aangifte wijst op ondernemerschap. "
            "KVK-inschrijving en aangifte IB als ondernemer (winst uit onderneming, evt. zelfstandigenaftrek) "
            "versterken dit beeld. Ontbreken van BTW of geen actieve KVK-inschrijving zijn risicosignalen."
        ),
    },
    {
        "nummer": 9,
        "naam": "Gedrag als ondernemer in het economisch verkeer",
        "toelichting": (
            "Actief meerdere opdrachtgevers hebben, investeren in eigen bedrijfsmiddelen, dragen van financieel "
            "risico (aansprakelijkheid bij fouten, no cure no pay), eigen acquisitie, website en branding wijzen "
            "op ondernemerschap. Exclusief voor één opdrachtgever werken is een sterk risicosignaal."
        ),
    },
]

SZW_TABEL = {
    "zzp_kenmerken": [
        "Bepaalt zelf hoe het werk wordt uitgevoerd",
        "Draagt financieel risico (aansprakelijkheid, no cure no pay)",
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
        "Opdrachtgever draagt het financiële risico",
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
        "inhoud": "Normale handhaving hervat per 1 januari 2025; zachte landing boetes in 2026",
    },
    "belastingdienst_model": {
        "naam": "Belastingdienst: Modelovereenkomsten",
        "url": "https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/ondernemen/modelovereenkomsten-in-plaats-van-var/arbeidsrelaties",
        "inhoud": "Geen nieuwe beoordelingen meer since 6 sept 2024; bestaande geldig t/m 31 dec 2029",
    },
    "rijksoverheid_schijnzelfstandigheid": {
        "naam": "Rijksoverheid: Veelgestelde vragen over schijnzelfstandigheid",
        "url": "https://www.rijksoverheid.nl/themas/werk/zelfstandigen-zonder-personeel-zzp/veelgestelde-vragen-schijnzelfstandigheid",
        # Geraadpleegd 11-09-2026. Noemt geen termijn en geen tariefdrempel.
        "inhoud": "Ook bij een hoog uurtarief kan sprake zijn van schijnzelfstandigheid; het tarief is maar een van de criteria",
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

ACTUELE_FEITEN = {
    "handhaving": (
        "Normale handhavingsregels gelden weer per 1 januari 2025. "
        "In 2026 worden verzuimboetes nog niet opgelegd (zachte landing). "
        "Vergrijpboetes (bij evidente schijnzelfstandigheid of kwaadwillendheid) kunnen wel worden opgelegd. "
        "Correctieverplichtingen en naheffingen loonheffingen zijn reeds actief."
    ),
    "modelovereenkomsten": (
        "De Belastingdienst beoordeelt geen nieuwe modelovereenkomsten meer since 6 september 2024. "
        "Bestaande goedgekeurde modelovereenkomsten mogen worden gebruikt tot uiterlijk 31 december 2029. "
        "CRUCIAAL: een modelovereenkomst biedt GEEN zekerheid als de feitelijke uitvoering ervan afwijkt. "
        "De Belastingdienst beoordeelt altijd de feitelijke situatie, niet het papier."
    ),
    "wet_vbar": (
        "De Wet VBAR (rechtsvermoeden arbeidsrelatie) en Wet WTTA zijn nog NIET ingevoerd. "
        "Status: politiek onzeker, behandeling loopt. Niet van toepassing op huidige situaties."
    ),
    "bijgewerkt": "3 juli 2026",
}
