# UC_dba-risicoscan — DBA Risicoscan

| | |
|---|---|
| **Eigenaar** | Sylvain Bouwman |
| **Domein** | Fiscaal / Arbeidsrecht / Compliance |
| **Status** | Live |
| **Versie** | v1 — juni 2026 |

## Doel

Een indicatieve beoordeling geven van de arbeidsrelatie met een ZZP'er op basis van de negen gezichtspunten uit het Deliveroo-arrest (HR 24 maart 2023) en het Uber-arrest (HR 21 februari 2025).

## Betrokkenen

| Rol | Toelichting |
|---|---|
| Eigenaar | Sylvain Bouwman |
| Gebruikers | Belastingadviseurs bij Join Administraties en DK Accountants |
| Klant | Opdrachtgever die werkt met ZZP'ers |

## Trigger

Klant werkt met één of meerdere ZZP'ers en wil weten of de arbeidsrelatie het risico loopt als dienstbetrekking te worden aangemerkt (schijnzelfstandigheid).

## As-is situatie

DBA-beoordeling wordt ad-hoc uitgevoerd, sterk afhankelijk van individuele kennis van de adviseur. Geen gestandaardiseerde toets op basis van de actuele jurisprudentie (Deliveroo, Uber). Handhaving door de Belastingdienst is per 2025 hervat — urgentie neemt toe.

## To-be situatie

1. Medewerker opent de tool en doorloopt de negen gezichtspunten uit de arresten
2. Per gezichtspunt wordt de situatie van de klant beoordeeld (dienstbetrekking / zelfstandige / neutraal)
3. Tool genereert een indicatief risicooordeel (laag / midden / hoog)
4. Uitkomst dient als gespreksondersteuning en eerste screening — geen juridisch bindend oordeel

## Live

[dba-risicoscan.streamlit.app](https://dba-risicoscan.streamlit.app)

## Waarde

| | |
|---|---|
| **Kwaliteit** | Gestandaardiseerde toets op basis van actuele jurisprudentie |
| **Tijdwinst** | Snelle eerste screening zonder uitgebreide voorbereiding |
| **Klant** | Vroegtijdige signalering van risico; adviseur kan tijdig bijsturen |
