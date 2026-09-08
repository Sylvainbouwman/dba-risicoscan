"""Alle invoer is synthetisch; geen netwerk, sleutels of klantbestanden."""
import ast
from contextlib import nullcontext
from copy import deepcopy
import json
from pathlib import Path
from types import SimpleNamespace
import unittest

from analyse_validatie import OngeldigeAnalyse, lees_analyse, valideer_analyse


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


if __name__ == '__main__':
    unittest.main()
