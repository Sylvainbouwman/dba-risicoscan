"""
DBA Risicoscan – Streamlit-app
Beoordeling arbeidsrelatie op basis van de negen gezichtspunten (Deliveroo / Uber-arrest).
"""

from __future__ import annotations

import json
import anthropic
import streamlit as st

from knowledge_base import ACTUELE_FEITEN, BRONNEN
from prompts import SYSTEM_PROMPT, bouw_analyse_prompt
from export import genereer_memo

# ---------------------------------------------------------------------------
# Configuratie
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="DBA Risicoscan",
    page_icon="⚖️",
    layout="wide",
)

MODEL = "claude-opus-4-8"

# ---------------------------------------------------------------------------
# Vragenlijst (9 blokken, elk gekoppeld aan een gezichtspunt)
# ---------------------------------------------------------------------------

VRAGENLIJST = [
    {
        "gezichtspunt": 1,
        "naam": "Aard en duur van de werkzaamheden",
        "vragen": [
            {
                "id": "q1_aard",
                "vraag": "Wat is de aard van de werkzaamheden?",
                "opties": [
                    "Projectmatig met duidelijk eindresultaat",
                    "Mix van projectmatig en structureel",
                    "Structurele taken die ook door vaste medewerkers worden gedaan",
                ],
            },
            {
                "id": "q1_duur",
                "vraag": "Hoe lang loopt de opdracht al (of was gepland)?",
                "opties": [
                    "Minder dan 3 maanden",
                    "3 tot 12 maanden",
                    "1 tot 2 jaar",
                    "Meer dan 2 jaar",
                    "Onbepaald / doorlopend zonder einddatum",
                ],
            },
            {
                "id": "q1_einddatum",
                "vraag": "Is er een vaste einddatum afgesproken?",
                "opties": [
                    "Ja, duidelijke einddatum",
                    "Nee, maar opdracht is projectgebonden",
                    "Nee, doorlopend / stilzwijgend verlengd",
                ],
            },
        ],
    },
    {
        "gezichtspunt": 2,
        "naam": "Aansturing en werktijden",
        "vragen": [
            {
                "id": "q2_hoe",
                "vraag": "Wie bepaalt HOE het werk wordt uitgevoerd (werkwijze, methode)?",
                "opties": [
                    "Opdrachtnemer volledig zelf",
                    "Grotendeels opdrachtnemer, met globale richtlijnen",
                    "Opdrachtgever geeft gedetailleerde instructies",
                ],
            },
            {
                "id": "q2_wanneer_waar",
                "vraag": "Wie bepaalt WANNEER en WAAR gewerkt wordt?",
                "opties": [
                    "Opdrachtnemer volledig vrij",
                    "Deels bepaald door opdrachtgever (bijv. verplichte vergaderingen)",
                    "Opdrachtgever schrijft vaste werktijden en/of locatie voor",
                ],
            },
            {
                "id": "q2_beoordeling",
                "vraag": "Vindt er aansturing of beoordeling plaats zoals bij vaste medewerkers?",
                "opties": [
                    "Nee, alleen overleg over opdrachtresultaat",
                    "Incidenteel voortgangsoverleg",
                    "Ja, regelmatige aansturing, beoordeling of functioneringsgesprekken",
                ],
            },
        ],
    },
    {
        "gezichtspunt": 3,
        "naam": "Inbedding in de organisatie",
        "vragen": [
            {
                "id": "q3_locatie",
                "vraag": "Werkt de opdrachtnemer op de locatie van de opdrachtgever?",
                "opties": [
                    "Zelden of nooit (voornamelijk eigen locatie)",
                    "Regelmatig, maar ook op andere locaties",
                    "Altijd of bijna altijd op locatie opdrachtgever",
                ],
            },
            {
                "id": "q3_middelen",
                "vraag": "Maakt de opdrachtnemer gebruik van bedrijfsmiddelen van de opdrachtgever?",
                "opties": [
                    "Nee, uitsluitend eigen middelen",
                    "Deels (bijv. alleen toegang tot systemen)",
                    "Ja, inclusief e-mailadres, telefoon of visitekaartje van opdrachtgever",
                ],
            },
            {
                "id": "q3_team",
                "vraag": "Is de opdrachtnemer onderdeel van een team met vaste medewerkers?",
                "opties": [
                    "Nee, werkt volledig zelfstandig buiten het vaste team",
                    "Deels, voor coördinatie of afstemming",
                    "Ja, volledig geïntegreerd in het team",
                ],
            },
            {
                "id": "q3_vergelijkbaar",
                "vraag": "Zijn er vaste medewerkers die vergelijkbaar werk doen?",
                "opties": [
                    "Nee",
                    "Ja, maar opdrachtnemer doet andere of aanvullende dingen",
                    "Ja, praktisch hetzelfde werk als vaste medewerkers",
                ],
            },
        ],
    },
    {
        "gezichtspunt": 4,
        "naam": "Persoonlijke arbeidsplicht en vervanging",
        "vragen": [
            {
                "id": "q4_vervanging",
                "vraag": "Kan de opdrachtnemer zich laten vervangen?",
                "opties": [
                    "Ja, volledig vrij zonder toestemming van opdrachtgever",
                    "Ja, maar opdrachtgever moet de vervanger goedkeuren",
                    "Nee, vervanging is praktisch niet mogelijk of niet toegestaan",
                ],
            },
            {
                "id": "q4_vervangen_ooit",
                "vraag": "Heeft vervanging ooit daadwerkelijk plaatsgevonden?",
                "opties": [
                    "Ja",
                    "Nee, maar de mogelijkheid bestaat wel",
                    "Nee, nooit en ook praktisch niet mogelijk",
                ],
            },
        ],
    },
    {
        "gezichtspunt": 5,
        "naam": "Totstandkoming van de overeenkomst",
        "vragen": [
            {
                "id": "q5_onderhandeling",
                "vraag": "Hoe is de opdracht tot stand gekomen?",
                "opties": [
                    "Vrije onderhandeling; opdrachtnemer bepaalde mede de voorwaarden",
                    "Standaard contract aangeboden; beperkte onderhandelingsruimte",
                    "Opdrachtgever legde de voorwaarden volledig op",
                ],
            },
            {
                "id": "q5_modelovereenkomst",
                "vraag": "Is er gebruik gemaakt van een modelovereenkomst (goedgekeurd door Belastingdienst)?",
                "opties": [
                    "Nee, eigen opdrachtovereenkomst",
                    "Ja, goedgekeurde modelovereenkomst (goedgekeurd vóór 6 sept 2024)",
                    "Onbekend",
                ],
            },
        ],
    },
    {
        "gezichtspunt": 6,
        "naam": "Wijze van beloning",
        "vragen": [
            {
                "id": "q6_prijsstructuur",
                "vraag": "Hoe is de opdracht geprijsd?",
                "opties": [
                    "Vaste prijs per resultaat of project (geen uren)",
                    "Uurtarief",
                    "Maandelijkse vaste vergoeding",
                ],
            },
            {
                "id": "q6_betaling",
                "vraag": "Hoe vindt betaling plaats?",
                "opties": [
                    "Op factuur met BTW",
                    "Op factuur zonder BTW (bijv. vrijgesteld)",
                    "Zonder factuur of via loonstrook",
                ],
            },
            {
                "id": "q6_loonelementen",
                "vraag": "Zijn er loonelementen aanwezig (vakantiegeld, pensioenopbouw, doorbetaling bij ziekte)?",
                "opties": [
                    "Nee, geen loonelementen",
                    "Één element (bijv. pensioen via opdrachtgever)",
                    "Ja, meerdere loonelementen",
                ],
            },
        ],
    },
    {
        "gezichtspunt": 7,
        "naam": "Hoogte van de beloning",
        "vragen": [
            {
                "id": "q7_tarief_niveau",
                "vraag": "Is het uurtarief duidelijk hoger dan het vergelijkbare cao-uurloon inclusief werkgeverslasten (vuistregel: minimaal 1,5x brutoloon)?",
                "opties": [
                    "Ja, duidelijk hoger (marktconform ZZP-tarief)",
                    "Ongeveer gelijk aan cao-loon inclusief werkgeverslasten",
                    "Lager of vergelijkbaar met cao-loon",
                    "Niet bekend / moeilijk te vergelijken",
                ],
            },
        ],
    },
    {
        "gezichtspunt": 8,
        "naam": "Omzetbelasting en ondernemersstatus",
        "vragen": [
            {
                "id": "q8_btw",
                "vraag": "Brengt de opdrachtnemer BTW in rekening?",
                "opties": [
                    "Ja, altijd",
                    "Nee, BTW-vrijgesteld (bijv. zorg, onderwijs)",
                    "Nee, geen BTW op facturen",
                ],
            },
            {
                "id": "q8_kvk",
                "vraag": "Staat de opdrachtnemer actief ingeschreven bij de KVK?",
                "opties": [
                    "Ja, actieve inschrijving als zelfstandige/ondernemer",
                    "Ja, maar inschrijving is inactief of recent",
                    "Nee",
                ],
            },
            {
                "id": "q8_ib",
                "vraag": "Doet de opdrachtnemer aangifte inkomstenbelasting als ondernemer (winst uit onderneming)?",
                "opties": [
                    "Ja, inclusief zelfstandigenaftrek",
                    "Ja, als resultaat overige werkzaamheden (ROW)",
                    "Nee / onbekend",
                ],
            },
        ],
    },
    {
        "gezichtspunt": 9,
        "naam": "Ondernemersgedrag in het economisch verkeer",
        "vragen": [
            {
                "id": "q9_opdrachtgevers",
                "vraag": "Heeft de opdrachtnemer actief meerdere opdrachtgevers?",
                "opties": [
                    "Ja, 3 of meer actieve opdrachtgevers",
                    "Ja, 2 opdrachtgevers",
                    "Nee, uitsluitend deze opdrachtgever",
                ],
            },
            {
                "id": "q9_presentatie",
                "vraag": "Presenteert de opdrachtnemer zich actief als ondernemer (eigen website, acquisitie, branding)?",
                "opties": [
                    "Ja, actieve eigen bedrijfspresentatie",
                    "Beperkt (bijv. alleen LinkedIn-profiel als ZZP)",
                    "Nee, geen eigen ondernemerspresentatie",
                ],
            },
            {
                "id": "q9_risico",
                "vraag": "Draagt de opdrachtnemer financieel risico bij fouten of tegenvallend resultaat?",
                "opties": [
                    "Ja, volledig aansprakelijk (incl. beroepsaansprakelijkheidsverzekering)",
                    "Deels",
                    "Nee, risico ligt bij opdrachtgever",
                ],
            },
            {
                "id": "q9_investering",
                "vraag": "Heeft de opdrachtnemer geïnvesteerd in eigen bedrijfsmiddelen of gereedschap?",
                "opties": [
                    "Ja, substantiële eigen investering",
                    "Beperkt (bijv. laptop)",
                    "Nee, werkt uitsluitend met middelen van opdrachtgever",
                ],
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# API-client
# ---------------------------------------------------------------------------

def get_client() -> anthropic.Anthropic | None:
    api_key = st.session_state.get("api_key", "")
    if not api_key:
        try:
            api_key = st.secrets["ANTHROPIC_API_KEY"]
        except Exception:
            pass
    if not api_key:
        return None
    return anthropic.Anthropic(api_key=api_key)


def voer_analyse_uit(intake: dict, antwoorden: dict) -> dict | None:
    client = get_client()
    if client is None:
        st.error("Voer eerst een geldige Anthropic API-sleutel in (zie zijbalk).")
        return None

    prompt = bouw_analyse_prompt(intake, antwoorden)

    with st.spinner("Analyse wordt uitgevoerd..."):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
        except anthropic.AuthenticationError:
            st.error("Ongeldige API-sleutel. Controleer de sleutel in de zijbalk.")
            return None
        except Exception as e:
            st.error(f"API-fout: {e}")
            return None

    raw = response.content[0].text.strip()

    # Verwijder eventuele markdown code-blokken
    if raw.startswith("```"):
        lines = raw.splitlines()
        raw = "\n".join(
            line for line in lines if not line.startswith("```")
        ).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        st.error("De analyse kon niet worden verwerkt. Probeer het opnieuw.")
        st.expander("Ruwe API-output (voor diagnose)").code(raw)
        return None


# ---------------------------------------------------------------------------
# Resultaten weergeven
# ---------------------------------------------------------------------------

SIGNAAL_CONFIG = {
    "loondienst": ("Wijst op loondienst", "error"),
    "neutraal": ("Neutraal", "warning"),
    "zzp": ("Wijst op ZZP-schap", "success"),
}

STERKTE_NL = {"zwak": "zwak", "matig": "matig", "sterk": "sterk"}


def toon_resultaten(analyse: dict, intake: dict) -> None:
    st.subheader("Patroon samenvatting")
    st.info(analyse.get("patroon_samenvatting", ""))

    risicosignalen = analyse.get("sterke_risicosignalen", [])
    if risicosignalen:
        st.subheader("Sterke risicosignalen")
        for signaal in risicosignalen:
            st.error(f"- {signaal}")

    st.subheader("Analyse per gezichtspunt")

    for gp in analyse.get("gezichtspunten_analyse", []):
        signaal = gp.get("signaal", "neutraal")
        sterkte = gp.get("sterkte", "")
        label, box_type = SIGNAAL_CONFIG.get(signaal, ("Onbekend", "info"))
        sterkte_label = STERKTE_NL.get(sterkte, sterkte)

        with st.expander(
            f"{gp.get('nummer')}. {gp.get('naam', '')}  —  {label} ({sterkte_label})",
            expanded=(signaal == "loondienst" and sterkte == "sterk"),
        ):
            getattr(st, box_type)(f"**{label}** ({sterkte_label})")
            st.write(gp.get("redenering", ""))
            st.caption(f"Bron: {gp.get('bron', '')}")

    verbeterpunten = analyse.get("verbeterpunten", [])
    if verbeterpunten:
        st.subheader("Verbeterpunten")
        for vp in verbeterpunten:
            with st.expander(f"{vp.get('gezichtspunt', '')}: {vp.get('actie', '')}"):
                st.write(vp.get("toelichting", ""))

    advies = analyse.get("advies_volgende_stap", "")
    if advies:
        st.subheader("Aanbevolen vervolgstap")
        st.success(advies)

    st.subheader("Exporteer als Word-memo")
    memo_buffer = genereer_memo(intake, analyse)
    opdrachtgever = intake.get("opdrachtgever", "opdracht").replace(" ", "_")
    st.download_button(
        label="Download risicomemo (.docx)",
        data=memo_buffer,
        file_name=f"DBA_Risicoscan_{opdrachtgever}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    st.divider()
    st.caption(
        "**Disclaimer:** Dit is een indicatieve risicoanalyse, geen fiscaal of juridisch advies. "
        "De beoordeling van de arbeidsrelatie is voorbehouden aan de Belastingdienst en de rechter, "
        "op basis van alle feiten en omstandigheden en de feitelijke uitvoering van de opdracht. "
        f"Kennisbasis bijgewerkt per {ACTUELE_FEITEN['bijgewerkt']}."
    )


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

def toon_sidebar() -> None:
    with st.sidebar:
        st.title("DBA Risicoscan")
        st.caption(f"Kennisbasis bijgewerkt: {ACTUELE_FEITEN['bijgewerkt']}")

        st.divider()

        if not st.session_state.get("api_key"):
            try:
                st.secrets["ANTHROPIC_API_KEY"]
                st.success("API-sleutel geladen via secrets.")
            except Exception:
                st.session_state["api_key"] = st.text_input(
                    "Anthropic API-sleutel",
                    type="password",
                    placeholder="sk-ant-...",
                    help="Voer je Anthropic API-sleutel in of sla hem op in .streamlit/secrets.toml",
                )

        st.divider()
        st.markdown("**Over deze tool**")
        st.markdown(
            "Beoordeling arbeidsrelatie op basis van de **negen gezichtspunten** "
            "uit het *Deliveroo-arrest* (HR 24 maart 2023) en het *Uber-arrest* "
            "(HR 21 februari 2025)."
        )

        st.markdown("**Belangrijke actualiteiten**")
        st.warning(
            "Normale handhaving hervat per 1 jan 2025. "
            "Modelovereenkomsten bieden geen zekerheid als de praktijk afwijkt.",
            icon="⚠️",
        )
        st.info(
            "Wet VBAR (rechtsvermoeden) is nog **niet** ingevoerd.",
            icon="ℹ️",
        )

        st.divider()
        st.markdown("**Bronnen**")
        for b in BRONNEN.values():
            st.markdown(f"- [{b['naam']}]({b['url']})")


# ---------------------------------------------------------------------------
# Tabbladen
# ---------------------------------------------------------------------------

def tab_intake() -> None:
    st.header("Stap 1: Opdracht")
    st.markdown(
        "Vul de basisgegevens van de concrete opdracht in. "
        "De analyse geldt per opdracht, niet per ZZP'er in het algemeen."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.session_state["intake_opdrachtgever"] = st.text_input(
            "Naam opdrachtgever",
            value=st.session_state.get("intake_opdrachtgever", ""),
        )
        st.session_state["intake_sector"] = st.text_input(
            "Sector / branche",
            value=st.session_state.get("intake_sector", ""),
            placeholder="bijv. bouw, ICT, zorg, onderwijs",
        )
    with col2:
        st.session_state["intake_opdrachtnemer"] = st.text_input(
            "Naam opdrachtnemer / ZZP'er",
            value=st.session_state.get("intake_opdrachtnemer", ""),
        )
        st.session_state["intake_startdatum"] = st.text_input(
            "Startdatum opdracht",
            value=st.session_state.get("intake_startdatum", ""),
            placeholder="bijv. januari 2024",
        )

    st.session_state["intake_werkzaamheden"] = st.text_area(
        "Korte omschrijving van de werkzaamheden",
        value=st.session_state.get("intake_werkzaamheden", ""),
        placeholder="bijv. ontwikkeling en beheer van de website, projectleiding renovatie, financiële rapportages",
        height=80,
    )

    st.info(
        "Let op: een modelovereenkomst biedt geen zekerheid als de feitelijke uitvoering afwijkt. "
        "De Belastingdienst beoordeelt altijd de praktijk.",
        icon="ℹ️",
    )


def tab_vragenlijst() -> None:
    st.header("Stap 2: Vragenlijst")
    st.markdown(
        "Beantwoord alle vragen zo nauwkeurig mogelijk op basis van de **feitelijke situatie**, "
        "niet op basis van contractafspraken alleen."
    )

    if "antwoorden" not in st.session_state:
        st.session_state["antwoorden"] = {}

    for blok in VRAGENLIJST:
        with st.expander(
            f"Gezichtspunt {blok['gezichtspunt']}: {blok['naam']}",
            expanded=True,
        ):
            for q in blok["vragen"]:
                huidige = st.session_state["antwoorden"].get(q["id"], "Selecteer...")
                opties = ["Selecteer..."] + q["opties"]
                idx = opties.index(huidige) if huidige in opties else 0
                antwoord = st.selectbox(
                    q["vraag"],
                    options=opties,
                    index=idx,
                    key=f"sb_{q['id']}",
                )
                st.session_state["antwoorden"][q["id"]] = antwoord


def tab_analyse() -> None:
    st.header("Stap 3: Analyse")

    intake = {
        "opdrachtgever": st.session_state.get("intake_opdrachtgever", ""),
        "opdrachtnemer": st.session_state.get("intake_opdrachtnemer", ""),
        "sector": st.session_state.get("intake_sector", ""),
        "werkzaamheden": st.session_state.get("intake_werkzaamheden", ""),
        "startdatum": st.session_state.get("intake_startdatum", ""),
    }

    antwoorden_geldig = st.session_state.get("antwoorden", {})
    ingevuld = sum(
        1 for v in antwoorden_geldig.values()
        if v and v != "Selecteer..."
    )
    totaal = sum(len(b["vragen"]) for b in VRAGENLIJST)

    st.metric("Vragen beantwoord", f"{ingevuld} / {totaal}")

    if ingevuld < totaal * 0.7:
        st.warning(
            f"Slechts {ingevuld} van de {totaal} vragen zijn beantwoord. "
            "Beantwoord minimaal 70% voor een betrouwbare analyse."
        )

    if not intake.get("opdrachtgever") or not intake.get("opdrachtnemer"):
        st.warning("Vul op tabblad 'Opdracht' minimaal opdrachtgever en opdrachtnemer in.")

    if st.button("Start analyse", type="primary", disabled=(ingevuld == 0)):
        # Bouw leesbare antwoorden-dict op voor de prompt
        antwoorden_prompt: dict[str, str] = {}
        for blok in VRAGENLIJST:
            for q in blok["vragen"]:
                antwoord = antwoorden_geldig.get(q["id"], "")
                if antwoord and antwoord != "Selecteer...":
                    antwoorden_prompt[q["vraag"]] = antwoord

        resultaat = voer_analyse_uit(intake, antwoorden_prompt)
        if resultaat:
            st.session_state["analyse_resultaat"] = resultaat
            st.session_state["analyse_intake"] = intake

    if "analyse_resultaat" in st.session_state:
        st.divider()
        toon_resultaten(
            st.session_state["analyse_resultaat"],
            st.session_state["analyse_intake"],
        )


# ---------------------------------------------------------------------------
# Hoofdpagina
# ---------------------------------------------------------------------------

def main() -> None:
    toon_sidebar()

    st.title("DBA Risicoscan")
    st.markdown(
        "Indicatieve beoordeling van de arbeidsrelatie op basis van de **negen gezichtspunten** "
        "uit het *Deliveroo-arrest* (HR 24 maart 2023) en *Uber-arrest* (HR 21 februari 2025). "
        "Vul de drie stappen hieronder in."
    )

    tab1, tab2, tab3 = st.tabs(["Opdracht", "Vragenlijst", "Analyse & Resultaat"])

    with tab1:
        tab_intake()

    with tab2:
        tab_vragenlijst()

    with tab3:
        tab_analyse()


if __name__ == "__main__":
    main()
