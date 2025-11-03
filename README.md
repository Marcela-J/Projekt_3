# Projekt 3 – Scraper volebních výsledků 2017

Tento projekt stahuje výsledky voleb do Poslanecké sněmovny ČR z roku 2017 pro zvolený územní celek a ukládá je do CSV souboru.

## Požadavky

- Python 3.x
- Knihovny: `requests`, `beautifulsoup4` (viz `requirements.txt`)

## Instalace

1. Vytvořte si virtuální prostředí (doporučeno):

python -m venv venv


2. Aktivujte virtuální prostředí:

venv\Scripts\activate


3. Nainstalujte potřebné knihovny:

pip install -r requirements.txt

## Použití

Program se spouští se dvěma argumenty:

1. URL územního celku na stránkách volby.cz (např. obec nebo okres)
2. Název výstupního CSV souboru

**Příklad spuštění:**
python main.py "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky_benesov.csv

## Výstup

CSV soubor obsahuje následující sloupce:

- `kod` – kód obce
- `nazev` – název obce
- `volici_v_seznamu` – počet voličů v seznamu
- `vydane_obalky` – počet vydaných obálek
- `platne_hlasy` – počet platných hlasů
- Sloupce pro každou kandidující stranu – počet hlasů

Každý řádek CSV odpovídá jedné obci.