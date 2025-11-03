"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Marcela Jaškovská
email: fojtikovamarcela@gmail.com
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv

def zkontroluj_argumenty():
    """
    Kontroluje, zda uživatel zadal oba argumenty.
    1. URL územního celku 
    2. Název výstupního CSV
    """
    if len(sys.argv) != 3:
        print("Chyba: Zadejte 2 argumenty: URL a název výstupního CSV souboru.")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]

    if not url.startswith("https://www.volby.cz/"):
        print("Chyba: První argument musí být platná URL na volby.cz.")
        sys.exit(1)

    return url, output_file

def get_obce(url):
    """
    Načte všechny obce z tabulky zadaného územního celku.
    """
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', class_='table')
    if not table:
        print("Tabulka s obcemi nebyla nalezena.")
        return []

    obce = []
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        if len(cols) < 2:
            continue
        kod_tag = cols[0].find('a')
        if kod_tag:
            kod = kod_tag.text.strip()
            odkaz = kod_tag.get('href')
            nazev = cols[1].text.strip()
            plny_odkaz = "https://www.volby.cz/pls/ps2017nss/" + odkaz.lstrip('/')
            obce.append({
                'kod': kod,
                'nazev': nazev,
                'odkaz': plny_odkaz
            })

    return obce

def scrape_vysledky_obce(url):
    """
    Načte výsldky voleb pro jednu obec
    """
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        tab_stat = soup.find('table', class_='table')
        rows = tab_stat.find_all('tr')

        volici_v_seznamu = rows[0].find_all('td')[1].text.strip()
        vydane_obalky = rows[1].find_all('td')[1].text.strip()
        platne_hlasy = rows[2].find_all('td')[1].text.strip()
    except Exception:
        volici_v_seznamu = ''
        vydane_obalky = ''
        platne_hlasy = ''

    hlasy_strany = {}

    tables = soup.find_all('table', class_='table')

    if len(tables) > 1:
        vysledky_tab = tables[1]
        for row in vysledky_tab.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) >= 3:
                nazev_strany = cols[1].text.strip()
                hlasy = cols[2].text.strip()
                hlasy_strany[nazev_strany] = hlasy

    return {
        'volici_v_seznamu': volici_v_seznamu,
        'vydane_obalky': vydane_obalky,
        'platne_hlasy': platne_hlasy,
        'hlasy_strany': hlasy_strany
    }

def uloz_do_csv(soubor, data, strany):
    """
    Uloží výsledky voleb do CSV
    """
    with open(soubor, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        hlavicka = ['kod', 'nazev', 'volici_v_seznamu', 'vydane_obalky', 'platne_hlasy'] + strany
        writer.writerow(hlavicka)

        for radek in data:
            radek_csv = [
                radek['kod'],
                radek['nazev'],
                radek['volici_v_seznamu'],
                radek['vydane_obalky'],
                radek['platne_hlasy']
            ]
            for strana in strany:
                radek_csv.append(radek['hlasy_strany'].get(strana, '0'))
            writer.writerow(radek_csv)

def main():
    """
    Hlavní funkce skriptu:
    - Kontroluje argumenty
    - Načte seznam obcí z územního celku
    - Pro každou obec stáhne výsledky voleb
    - Uloží výsledky do CSV souboru
    """
    url, output_file = zkontroluj_argumenty()

    obce = get_obce(url)
    if not obce:
        print("Nenalezeny žádné obce.")
        sys.exit(1)

    print(f"Nalezeno obcí: {len(obce)}")

    vsechny_strany = set()
    vysledky = []

    for i, obec in enumerate(obce, start=1):
        print(f"Stahuji data pro obec {i}/{len(obce)}: {obec['nazev']}")
        vysledky_obce = scrape_vysledky_obce(obec['odkaz'])
        vsechny_strany.update(vysledky_obce['hlasy_strany'].keys())

        zaznam = {
            'kod': obec['kod'],
            'nazev': obec['nazev'],
            'volici_v_seznamu': vysledky_obce['volici_v_seznamu'],
            'vydane_obalky': vysledky_obce['vydane_obalky'],
            'platne_hlasy': vysledky_obce['platne_hlasy'],
            'hlasy_strany': vysledky_obce['hlasy_strany']
        }
        vysledky.append(zaznam)

    serazene_strany = sorted(vsechny_strany)

    uloz_do_csv(output_file, vysledky, serazene_strany)

    print(f"Data uložena do {output_file}")

if __name__ == "__main__":
    main()
