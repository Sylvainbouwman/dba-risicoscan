"""
Juridische kennisbasis voor de DBA Risicoscan.
Bronnen: Deliveroo-arrest (HR 24 maart 2023), Uber-arrest (HR 21 februari 2025),
Belastingdienst, SZW-tabel, Rijksoverheid.
"""

NEGEN_GEZICHTSPUNTEN = [
    {
        "nummer": 1,
        "naam": "Aard en duur van de werkzaamheden",
        "toelichting": (
            "Projectmatig werk met een duidelijk eindresultaat wijst op ZZP-schap. "
            "Structurele, doorlopende taken die ook door vaste medewerkers worden uitgevoerd wijzen op loondienst. "
            "Langdurige opdrachten (> 1 jaar, zeker > 2 jaar zonder einddatum) verhogen het risico aanzienlijk."
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
            "(vuistregel: minimaal 1,5x het brutoloon, inclusief vakantiegeld, pensioen en werkgeverslasten) "
            "wijst op ZZP-schap. Een tarief vergelijkbaar met of lager dan cao-loon is een sterk risicosignaal."
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
        "ecli": "ECLI:NL:HR:2025:329",
        "url": "https://uitspraken.rechtspraak.nl/details?id=ECLI:NL:HR:2025:329",
        "inhoud": "Bevestiging en verdere uitwerking Deliveroo-criteria; zwaar gewicht aan inbedding organisatie",
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
