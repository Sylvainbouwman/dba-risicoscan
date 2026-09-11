"""Alle invoer is synthetisch; geen netwerk, sleutels of klantbestanden."""
import ast
from contextlib import nullcontext
from datetime import date
from copy import deepcopy
import json
from pathlib import Path
from types import SimpleNamespace
import unittest

from analyse_validatie import OngeldigeAnalyse, lees_analyse, valideer_analyse
from app import kennisbasis_verlopen
from knowledge_base import ACTUELE_FEITEN, BRONNEN, NEGEN_GEZICHTSPUNTEN
from prompts import SYSTEM_PROMPT


def volledig():
    return {
        "gezichtspunten_analyse": [dict(nummer=n, naam=f"Synthetisch punt {n}",
            signaal="neutraal", sterkte="zwak", redenering="Synthetische toelichting.",
            bron="Synthetische bron.") for n in range(1, 10)],
        "patroon_samenvatting": "Synthetisch patroon.",
        "sterke_risicosignalen": [], "verbeterpunten": [],
        "advies_volgende_stap": "Controleer de fictieve invoer.",
    }


class ValidatieTest(unittest.TestCase):
    def test_volledig_en_codeblok(self):
        for prefix, suffix in (("", ""), ("```json\n", "\n```")):
            self.assertEqual(lees_analyse(prefix + json.dumps(volledig()) + suffix), volledig())

    def test_onvolledige_of_afwijkende_structuur_geweigerd(self):
        varianten = [None, [], {}, {**volledig(), "gezichtspunten_analyse": []}]
        for veld in volledig():
            a = volledig(); del a[veld]; varianten.append(a)
        for veld, waarde in (("nummer", True), ("nummer", 2), ("nummer", 10),
                              ("signaal", "onbekend"), ("sterkte", []), ("bron", " "),
                              ("naam", None), ("redenering", {})):
            a = volledig(); a["gezichtspunten_analyse"][0][veld] = waarde; varianten.append(a)
        varianten.extend([{**volledig(), "verbeterpunten": [{}]},
                          {**volledig(), "sterke_risicosignalen": [7]}])
        for a in varianten:
            with self.subTest(a=a), self.assertRaises(OngeldigeAnalyse):
                valideer_analyse(a)

    def test_ongeldige_json(self):
        for raw in ('{', '```json\n{}', 'uitleg\n{}'):
            with self.assertRaises(OngeldigeAnalyse):
                lees_analyse(raw)

    def test_export_weigert_halve_analyse(self):
        from export import genereer_memo
        with self.assertRaises(OngeldigeAnalyse):
            genereer_memo({}, {})
        self.assertTrue(genereer_memo({}, volledig()).getvalue().startswith(b'PK'))

    def test_api_grens_zonder_netwerk(self):
        # Alleen de echte functie compileren: Streamlit start niet en er is geen SDK-call.
        tree = ast.parse(Path('app.py').read_text(encoding='utf-8'))
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'voer_analyse_uit')
        for stop, content, geldig in (
            ('end_turn', [SimpleNamespace(type='text', text=json.dumps(volledig()))], True),
            ('max_tokens', [SimpleNamespace(type='text', text=json.dumps(volledig()))], False),
            ('end_turn', [], False),
            ('end_turn', [SimpleNamespace(type='tool_use')], False),
            ('end_turn', [SimpleNamespace(type='text', text='{}')], False),
        ):
            fouten = []
            response = SimpleNamespace(stop_reason=stop, content=content)
            client = SimpleNamespace(messages=SimpleNamespace(create=lambda **kw: response))
            env = dict(get_client=lambda: client, bouw_analyse_prompt=lambda *a: 'synthetisch',
                st=SimpleNamespace(error=fouten.append, spinner=lambda *a: nullcontext()),
                anthropic=SimpleNamespace(AuthenticationError=RuntimeError), MODEL='test',
                SYSTEM_PROMPT='test', OngeldigeAnalyse=OngeldigeAnalyse, lees_analyse=lees_analyse)
            exec(compile(ast.Module(body=[fn], type_ignores=[]), 'app.py', 'exec'), env)
            resultaat = env['voer_analyse_uit']({}, {})
            self.assertEqual(resultaat is not None, geldig)
            self.assertEqual(bool(fouten), not geldig)

    def test_nieuwe_poging_verwijdert_vorig_resultaat(self):
        tree = ast.parse(Path('app.py').read_text(encoding='utf-8'))
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'tab_analyse')
        blok = next(n for n in ast.walk(fn) if isinstance(n, ast.If)
            and isinstance(n.test, ast.Call) and isinstance(n.test.func, ast.Attribute)
            and n.test.func.attr == 'button')
        state = {'analyse_resultaat': volledig(), 'analyse_intake': {'oud': True}}
        env = {'st': SimpleNamespace(session_state=state)}
        exec(compile(ast.Module(body=deepcopy(blok.body[:2]), type_ignores=[]), 'app.py', 'exec'), env)
        self.assertEqual(state, {})

    def test_oud_onvolledig_resultaat_wordt_niet_getoond(self):
        tree = ast.parse(Path('app.py').read_text(encoding='utf-8'))
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'toon_resultaten')
        fouten = []
        env = dict(st=SimpleNamespace(error=fouten.append), valideer_analyse=valideer_analyse,
                   OngeldigeAnalyse=OngeldigeAnalyse)
        exec(compile(ast.Module(body=[fn], type_ignores=[]), 'app.py', 'exec'), env)
        env['toon_resultaten']({}, {})
        self.assertEqual(len(fouten), 1)


class KennisbasisTest(unittest.TestCase):
    """Bewaakt het bronherstel van 11-09-2026; zie de docstring van knowledge_base.py."""

    def test_systeemprompt_zonder_kwantitatieve_drempel(self):
        # Deze drempels stonden tot 11-09-2026 in de kennisbasis en hebben geen
        # vindplaats in Deliveroo, Uber, de wetsgeschiedenis, de kennisgroep-
        # standpunten of de voorlichting van Belastingdienst en Rijksoverheid.
        verboden = ["1,5", "1.5", "anderhalf", "> 1 jaar", "> 2 jaar",
                    "meer dan 1 jaar", "meer dan 2 jaar", "langer dan een jaar",
                    "langer dan twee jaar", "zonder einddatum) verhogen"]
        for tekst in verboden:
            with self.subTest(tekst=tekst):
                self.assertNotIn(tekst.lower(), SYSTEM_PROMPT.lower())

    def test_duur_en_tarief_noemen_hun_vindplaats(self):
        for nummer in (1, 7):
            toelichting = NEGEN_GEZICHTSPUNTEN[nummer - 1]["toelichting"]
            with self.subTest(gezichtspunt=nummer):
                self.assertIn("ECLI:NL:HR:2023:443", toelichting)
                self.assertIn("r.o. 3.2.5", toelichting)
        self.assertIn("Rijksoverheid", NEGEN_GEZICHTSPUNTEN[6]["toelichting"])

    def test_uber_arrest_heeft_de_juiste_ecli(self):
        # ECLI:NL:HR:2025:329 stond hier eerder en is een strafzaak.
        self.assertEqual(BRONNEN["uber"]["ecli"], "ECLI:NL:HR:2025:319")
        self.assertIn("ECLI:NL:HR:2025:319", BRONNEN["uber"]["url"])
        self.assertNotIn("2025:329", SYSTEM_PROMPT)

    def test_vragenlijst_stuurt_niet_met_een_factor(self):
        vragenlijst = Path('app.py').read_text(encoding='utf-8')
        for tekst in ("1,5x", "1,5 x", "vuistregel: minimaal"):
            with self.subTest(tekst=tekst):
                self.assertNotIn(tekst, vragenlijst)


class GebruiksscenarioTest(unittest.TestCase):
    """Het gebruiksscenario mag geen uitkomst beloven die de tool niet geeft."""

    def test_geen_risicoklasse_belooft(self):
        uc = Path('UC_dba-risicoscan.md').read_text(encoding='utf-8').lower()
        for tekst in ("laag / midden / hoog", "risicooordeel", "risico-oordeel (laag"):
            with self.subTest(tekst=tekst):
                self.assertNotIn(tekst, uc)
        self.assertIn("geen eindoordeel", uc)

    def test_systeemprompt_verbiedt_een_eindoordeel(self):
        self.assertIn("Geef GEEN eindoordeel", SYSTEM_PROMPT)


class ActueleFeitenTest(unittest.TestCase):
    """Bewaakt de bronverificatie van 11-09-2026; zie de docstring van knowledge_base.py.

    ACTUELE_FEITEN gaat via prompts.py letterlijk de systeemprompt in. Tot 11-09-2026
    stond daar dat de Wet VBAR en de Wet Wtta "nog NIET ingevoerd" waren en dat de status
    "politiek onzeker" was. Beide beweringen waren op dat moment onjuist.
    """

    def test_geen_achterhaalde_status_in_de_systeemprompt(self):
        for tekst in ("nog NIET ingevoerd", "politiek onzeker",
                      "Niet van toepassing op huidige situaties"):
            with self.subTest(tekst=tekst):
                self.assertNotIn(tekst.lower(), SYSTEM_PROMPT.lower())

    def test_rechtsvermoeden_noemt_wet_besluit_en_ingangsdatum(self):
        regel = ACTUELE_FEITEN["rechtsvermoeden_uurtarief"]
        # Wet van 18 juni 2026 en het inwerkingtredingsbesluit van 13 juli 2026.
        self.assertIn("Stb. 2026, 158", regel)
        self.assertIn("Stb. 2026, 207", regel)
        self.assertIn("31 december 2026", regel)
        self.assertIn("7:610aa", regel)
        self.assertIn(regel, SYSTEM_PROMPT)

    def test_bedrag_staat_er_alleen_met_zijn_voorbehoud(self):
        # Het bedrag mag in de prompt staan omdat de wet geldend recht is met een
        # vastgestelde ingangsdatum, maar niet als drempel bij de negen gezichtspunten:
        # het vermoeden werkt civielrechtelijk en niet in de fiscale beoordeling.
        regel = ACTUELE_FEITEN["rechtsvermoeden_uurtarief"]
        self.assertIn("EUR 36 per uur", regel)
        self.assertIn("civielrechtelijk", regel)
        self.assertIn("NIET als drempel", regel)
        # Het bedrag uit de voorlichting van het kabinet (38 euro per uur, peildatum
        # 1 januari 2026) is geen vastgesteld bedrag en hoort daarom niet in de
        # kennisbasis; alleen het bedrag uit de wettekst zelf staat erin.
        for tekst in ("38 euro", "EUR 38", "38 per uur", "€ 38"):
            with self.subTest(tekst=tekst):
                self.assertNotIn(tekst, SYSTEM_PROMPT)

    def test_wtta_is_niet_langer_als_niet_ingevoerd_beschreven(self):
        regel = ACTUELE_FEITEN["wtta"]
        self.assertIn("1 januari 2027", regel)
        self.assertIn(regel, SYSTEM_PROMPT)

    def test_handhaving_noemt_het_vervallen_van_de_zachte_landing(self):
        regel = ACTUELE_FEITEN["handhaving"]
        self.assertIn("geen verzuimboetes", regel)
        self.assertIn("ergrijpboetes", regel)
        self.assertIn("1 januari 2027", regel)
        self.assertIn(regel, SYSTEM_PROMPT)

    def test_inbedding_claimt_geen_zwaarder_gewicht(self):
        # Stond haaks op r.o. 3.3 van het Uber-arrest en op de regel hoger in dezelfde
        # systeemprompt dat tussen de gezichtspunten geen rangorde geldt.
        toelichting = NEGEN_GEZICHTSPUNTEN[2]["toelichting"]
        self.assertNotIn("zwaar gewogen", toelichting)
        self.assertIn("geen rangorde", toelichting)
        self.assertIn("r.o. 3.3", toelichting)
        self.assertIn("ECLI:NL:HR:2025:319", toelichting)
        self.assertNotIn("zwaar gewogen", SYSTEM_PROMPT)


class HoudbaarheidTest(unittest.TestCase):
    """De jaargebonden stand mag niet stilzwijgend verouderen."""

    def test_grens_is_een_geldige_datum_na_de_bijwerkdatum(self):
        grens = date.fromisoformat(ACTUELE_FEITEN["controle_uiterlijk"])
        self.assertEqual(grens, date(2027, 1, 1))

    def test_waarschuwt_pas_vanaf_de_grens(self):
        self.assertFalse(kennisbasis_verlopen(date(2026, 12, 31)))
        self.assertTrue(kennisbasis_verlopen(date(2027, 1, 1)))
        self.assertTrue(kennisbasis_verlopen(date(2027, 6, 1)))


if __name__ == '__main__':
    unittest.main()
