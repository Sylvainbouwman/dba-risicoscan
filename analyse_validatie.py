"""Controleer de structuur van modeluitvoer; dit toetst geen juridische inhoud."""
import json


class OngeldigeAnalyse(ValueError):
    """Het antwoord is niet geschikt om te tonen of te exporteren."""


def _tekst(obj, veld):
    if not isinstance(obj.get(veld), str) or not obj[veld].strip():
        raise OngeldigeAnalyse("Verplicht tekstveld ontbreekt of is leeg.")


def valideer_analyse(analyse):
    if not isinstance(analyse, dict):
        raise OngeldigeAnalyse("Een analyse moet een object zijn.")
    for veld in ("patroon_samenvatting", "advies_volgende_stap"):
        _tekst(analyse, veld)
    punten = analyse.get("gezichtspunten_analyse")
    if not isinstance(punten, list) or len(punten) != 9:
        raise OngeldigeAnalyse("Alle negen gezichtspunten zijn verplicht.")
    nummers = set()
    for punt in punten:
        if not isinstance(punt, dict):
            raise OngeldigeAnalyse("Een gezichtspunt moet een object zijn.")
        nummer = punt.get("nummer")
        if type(nummer) is not int or nummer not in range(1, 10) or nummer in nummers:
            raise OngeldigeAnalyse("Gezichtspunten moeten uniek genummerd zijn van 1 tot 9.")
        nummers.add(nummer)
        for veld in ("naam", "redenering", "bron", "signaal", "sterkte"):
            _tekst(punt, veld)
        if punt["signaal"] not in ("loondienst", "neutraal", "zzp"):
            raise OngeldigeAnalyse("Onbekend signaal.")
        if punt["sterkte"] not in ("zwak", "matig", "sterk"):
            raise OngeldigeAnalyse("Onbekende sterkte.")
    signalen = analyse.get("sterke_risicosignalen")
    if not isinstance(signalen, list) or any(not isinstance(s, str) or not s.strip() for s in signalen):
        raise OngeldigeAnalyse("Risicosignalen moeten een lijst teksten zijn.")
    verbeteringen = analyse.get("verbeterpunten")
    if not isinstance(verbeteringen, list):
        raise OngeldigeAnalyse("Verbeterpunten moeten een lijst zijn.")
    for punt in verbeteringen:
        if not isinstance(punt, dict):
            raise OngeldigeAnalyse("Een verbeterpunt moet een object zijn.")
        for veld in ("gezichtspunt", "actie", "toelichting"):
            _tekst(punt, veld)
    return analyse


def lees_analyse(raw):
    """Accepteer JSON, eventueel in één volledig markdown-codeblok."""
    if not isinstance(raw, str):
        raise OngeldigeAnalyse("Tekst ontbreekt.")
    raw = raw.strip()
    regels = raw.splitlines()
    if regels and regels[0] in ("```", "```json") and regels[-1] == "```":
        raw = "\n".join(regels[1:-1])
    try:
        analyse = json.loads(raw)
    except (ValueError, RecursionError) as exc:
        raise OngeldigeAnalyse("Geen geldig analyse-object.") from exc
    return valideer_analyse(analyse)
