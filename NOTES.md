# A l'Ombre du Vieux Poirier — werknotities

Statische site, vier talen, geen framework. Draft op https://claude.ai/artifact/B4VtZXq9LuDiwuzVTvpW1i (privé).

## Bouwen

    python3 build.py              # schrijft site/ (index.html, fr/, en/, de/, style.css, img/)
    python3 build.py --artifact   # + artifact/index.html (NL-pagina zonder document-skelet, voor claude.ai)

| Wat | Waar |
|---|---|
| Teksten per taal | `content/nl.py`, `fr.py`, `en.py`, `de.py` (zelfde sleutels; `build.py` faalt als er een ontbreekt) |
| Structuur van de pagina | `page.html` (`{placeholders}` uit de content) |
| Document-skelet (head, fonts, hreflang) | `template.html` |
| Stijl | `style.css` |
| Foto's | `img/*.jpg` (klaar voor de site), `img/raw/` (alle originelen van de Wix-site op 1600 px, met Wix-id in de naam) |
| Output | `site/` (upload de inhoud van deze map naar de host) |

Foto's komen van de huidige Wix-site (Sven: hergebruik is ok). Wix levert ze op maximaal 1600 px breed
via de `/v1/fill/` URL; wie de originelen in hogere resolutie wil, vraagt ze aan de fotograaf.

## Beslissingen (Sven, 2026-10-11)

- Talen: NL + FR + EN + DE. NL op `/`, de andere op `/fr/`, `/en/`, `/de/`. Taalkeuze rechtsboven.
- Prijzen: enkel op aanvraag; geen prijstabel, geen kalender. Contactblok vraagt om een prijsvoorstel op maat.
- Elke's telefoon en e-mail (van de huidige Contact-pagina) staan naast die van Yves.

## Nog te doen / te vragen

- `SITE_URL` in `build.py` staat op het huidige domein; pas aan als de site elders komt.
- Vertalingen FR/EN/DE zijn door Claude gemaakt: laten nalezen door Elke en Yves (FR vooral).
- Contactformulier: de Wix-site had er een; nu enkel telefoon, e-mail en Facebook. Een formulier vraagt een dienst (Formspree of de host).
- Hosting en domein: `www.alombreduvieuxpoirier.com` staat nu bij Wix.

## Voor Elke en Yves (niet voor de site)

De toeristische vermeldingen (Visit Wallonia, Cœur de l'Ardenne) tonen nog de oude
capaciteit (12–14 personen, 5 kamers) en de contactgegevens van Johan. Best laten aanpassen.
