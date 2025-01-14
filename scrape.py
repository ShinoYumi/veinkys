import random
import requests
import os
import time
from datetime import datetime
from bs4 import BeautifulSoup

def stahni_pdf(url, datum_str, nazev_clanku):
    """
    Stáhne PDF soubor z dané URL a uloží ho s daným názvem a strukturou složek.

    Args:
      url: URL adresa PDF souboru.
      datum_str: Datum článku ve formátu "YYYY-MM-DD".
      nazev_clanku: Název článku.

    Returns:
      bool: True, pokud soubor již existuje, jinak False.
    """
    try:
        print(f"Stahuji soubor: {url}")

        # Simulace webového prohlížeče pro zabránění blokování
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, stream=True, headers=headers)
        response.raise_for_status()  # Vyvolání výjimky v případě chyby

        # Parsování data z řetězce a formátování názvu souboru
        datum = datetime.strptime(datum_str, "%Y-%m-%d")
        mesice = {
            "January": "JAN",
            "February": "FEB",
            "March": "MAR",
            "April": "APR",
            "May": "MAY",
            "June": "JUN",
            "July": "JUL",
            "August": "AUG",
            "September": "SEP",
            "October": "OCT",
            "November": "NOV",
            "December": "DEC"
        }
        nazev_souboru = f"{datum.strftime('%d%b%y').upper()}-{nazev_clanku.replace('-', ' ')}"

        # Vytvoření adresářové struktury rok/měsíc
        rok = datum.strftime("%Y")
        mesic = datum.strftime("%B")
        uloziste = os.path.join(os.getcwd(), rok, mesic)
        os.makedirs(uloziste, exist_ok=True)  # Vytvoření složek, pokud neexistují

        cesta_k_souboru = os.path.join(uloziste, nazev_souboru)

        # Kontrola, zda soubor již existuje
        if os.path.exists(cesta_k_souboru):
            print(f"Soubor {nazev_souboru} již existuje. Nejnovější články staženy! Čekám 12 hodin,")
            return True  # Vrací True, pokud soubor existuje

        # Ukládání souboru po částech
        with open(cesta_k_souboru, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Soubor {nazev_souboru} stažen do {uloziste}")
        return False  # Vrací False, pokud soubor neexistuje

    except requests.exceptions.RequestException as e:
        print(f"Chyba při stahování souboru: {e}")
        return False


def prozkoumej_stranku(url):
    """
    Prozkoumá danou stránku a stáhne všechny dostupné PDF soubory z odkazů /backgrounder/.
    Ukončí procházení, pokud narazí na duplicitní PDF soubor.

    Args:
      url: URL adresa stránky.

    Returns:
      bool: True, pokud byl nalezen duplicitní PDF soubor, jinak False.
    """
    try:
        print(f"Prozkoumávám stránku: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        time.sleep(random.uniform(0.1, 0.3))  # Náhodné zpoždění pro zabránění blokování

        soup = BeautifulSoup(response.content, "html.parser")

        # Nalezení všech odkazů na články začínající /backgrounder/
        clanky = soup.find_all('a', href=lambda href: href and href.startswith('/backgrounder/'))

        nalezeno_duplicitni_pdf = False  # Příznak pro ukončení cyklu

        for clanek in clanky:
            url_clanku = "https://www.understandingwar.org" + clanek['href']
            print(f"Nalezen článek: {url_clanku}")

            # Prozkoumání stránky článku
            try:
                response_clanku = requests.get(url_clanku, headers=headers)
                response_clanku.raise_for_status()
                time.sleep(random.uniform(0.1, 0.3))  # Náhodné zpoždění
            except requests.exceptions.RequestException as e:
                print(f"Chyba při otevírání článku: {e}")
                continue

            soup_clanku = BeautifulSoup(response_clanku.content, "html.parser")

            # Nalezení odkazu na PDF v článku
            pdf_link = soup_clanku.find('a', href=lambda href: href and href.endswith('.pdf'))

            # Extrahování data z článku
            datum_element = soup_clanku.find('span', property="dc:date dc:created")
            if datum_element:
                datum_str = datum_element['content'].split('T')[0]
            else:
                datum_str = datetime.now().strftime("%Y-%m-%d")

            # Extrahování názvu článku
            nazev_clanku_element = soup_clanku.find('h1', class_="title", id="page-title")  
            if nazev_clanku_element:
                nazev_clanku = nazev_clanku_element.text.strip()
            else:
                nazev_clanku = "Neznámý název článku"

            # Stažení PDF, pokud je nalezen odkaz
            if pdf_link:
                url_pdf = pdf_link['href']
                print(f"Nalezen PDF soubor: {url_pdf}")
                if stahni_pdf(url_pdf, datum_str, nazev_clanku):  # Kontrola návratové hodnoty stahni_pdf()
                    nalezeno_duplicitni_pdf = True
                    break  # Ukončení cyklu, pokud je nalezen duplicitní PDF soubor

            if nalezeno_duplicitni_pdf:
                break  # Ukončení cyklu, pokud je nalezen duplicitní PDF soubor na předchozí stránce

        return nalezeno_duplicitni_pdf  # Vrací True, pokud byl nalezen duplicitní PDF soubor

    except requests.exceptions.RequestException as e:
        print(f"Chyba při prozkoumávání stránky: {e}")
        return False  # Vrací False v případě chyby


def main():
    """
    Hlavní funkce pro stahování PDF souborů.
    Spouští se periodicky a prochází všechny dostupné stránky s publikacemi.
    """
    zakladni_url = "https://www.understandingwar.org/publications"
    while True:
        # Zpracování první stránky
        nalezeno_duplicitni_pdf = prozkoumej_stranku(zakladni_url)

        # Zpracování dalších stránek, pouze pokud nebyl nalezen duplicitní PDF soubor
        if not nalezeno_duplicitni_pdf:  
            stranka = 2
            while True:
                dalsi_url = f"{zakladni_url}?page={stranka}"
                response = requests.get(dalsi_url)
                if response.status_code == 200:
                    nalezeno_duplicitni_pdf = prozkoumej_stranku(dalsi_url)  # Kontrola návratové hodnoty
                    if nalezeno_duplicitni_pdf:
                        break  # Ukončení cyklu, pokud je nalezen duplicitní PDF soubor
                    stranka += 1
                else:
                    break  # Ukončení cyklu, pokud další stránka neexistuje

        # Čekání 12 hodin (43200 sekund) před dalším spuštěním
        time.sleep(43200)

if __name__ == "__main__":
    main()
