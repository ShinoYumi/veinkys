# scrape.py
## Dokumentace ke kódu pro stahování PDF souborů z webu Understanding War

Tento skript slouží k automatickému stahování PDF souborů z webu Understanding War ([https://www.understandingwar.org/publications](https://www.understandingwar.org/publications)) a jejich ukládání do složek podle roku a měsíce. Skript se zaměřuje pouze na články dostupné na  `understandingwar.org/backgrounder`.

## Funkce

### `stahni_pdf(url, datum_str, nazev_clanku)`

Stáhne PDF soubor z dané URL adresy a uloží ho s daným názvem.

**Argumenty:**

* `url`: URL adresa PDF souboru.
* `datum_str`: Datum článku ve formátu "YYYY-MM-DD".
* `nazev_clanku`: Název článku.

**Funkcionalita:**

1. **Odeslání HTTP požadavku:** Odesílá se požadavek na danou URL s hlavičkami simulujícími webový prohlížeč, aby se zabránilo blokování ze strany serveru.
2. **Kontrola odpovědi:** Kontroluje se, zda je požadavek úspěšný (status code 200). Pokud ne, vyvolá se výjimka.
3. **Formátování názvu souboru:** Název souboru se formátuje do tvaru `DDMMYY-Název článku`, kde `DD` je den v měsíci, `MM` je zkratka měsíce v angličtině (JAN, FEB, MAR, ...) a `YY` je rok (dvě číslice).
4. **Vytvoření adresářové struktury:** Vytvoří se adresářová struktura pro ukládání souborů ve formátu `rok/měsíc`.
5. **Kontrola duplicity:** Kontroluje se, zda soubor s daným názvem již existuje. Pokud ano, stahování se přeskočí a funkce vrátí `True`.
6. **Uložení PDF souboru:** Pokud soubor neexistuje, stáhne se a uloží do příslušné složky. Funkce vrátí `False`.
7. **Ošetření chyb:** V případě chyby při stahování se vypíše chybová zpráva a funkce vrátí `False`.

### `prozkoumej_stranku(url)`

Prozkoumá danou stránku a stáhne všechny dostupné PDF soubory z odkazů `/backgrounder/`.

**Argumenty:**

* `url`: URL adresa stránky.

**Funkcionalita:**

1. **Odeslání HTTP požadavku:** Podobně jako u `stahni_pdf()` se odesílá požadavek s hlavičkami prohlížeče.
2. **Kontrola odpovědi:** Kontroluje se úspěšnost požadavku.
3. **Zpoždění:** Zavádí se náhodné zpoždění mezi 100 a 300 ms, aby se předešlo blokování IP adresy za DoS útok.
4. **Parsování HTML:** Pomocí knihovny BeautifulSoup se parsuje HTML kód stránky.
5. **Vyhledání článků:** Vyhledají se všechny odkazy na články začínající `/backgrounder/`.
6. **Procházení článků:** Pro každý nalezený článek se provede:
    * **Získání URL:** Získá se URL adresa článku.
    * **Otevření článku:** Odesílá se požadavek na URL článku a kontroluje se jeho dostupnost.
    * **Zpoždění:** Opět se zavádí náhodné zpoždění.
    * **Parsování HTML článku:** Parsování HTML kódu článku.
    * **Vyhledání PDF:** Vyhledá se odkaz na PDF soubor v článku.
    * **Extrahování data:** Extrahuje se datum článku z HTML kódu.
    * **Extrahování názvu:** Extrahuje se název článku z HTML kódu.
    * **Stažení PDF:** Pokud je nalezen odkaz na PDF, zavolá se funkce `stahni_pdf()` pro stažení souboru. Pokud `stahni_pdf()` vrátí `True` (soubor již existuje), procházení se ukončí a funkce vrátí `True`.
7. **Ošetření chyb:** V případě chyby se vypíše chybová zpráva a funkce vrátí `False`.

### `main()`

Hlavní funkce skriptu.

**Funkcionalita:**

1. **Nastavení URL:** Nastaví se základní URL adresa na `https://www.understandingwar.org/publications`.
2. **Nekonečný cyklus:** V nekonečné smyčce se provádí:
    * **Zpracování stránky:** Zavolá se funkce `prozkoumej_stranku()` pro zpracování první stránky s publikacemi.
    * **Zpracování dalších stránek:** Pokud `prozkoumej_stranku()` nevrátí `True` (nebyl nalezen duplicitní soubor), prochází se další stránky s publikacemi. Pokud `prozkoumej_stranku()` vrátí `True`, cyklus se ukončí.
    * **Čekání:** Po zpracování všech stránek skript čeká 12 hodin (43200 sekund) před dalším spuštěním.

## Použité knihovny

* `requests`: Pro odesílání HTTP požadavků.
* `os`: Pro práci se soubory a adresáři.
* `time`: Pro zpoždění mezi požadavky.
* `datetime`: Pro práci s datem a časem.
* `bs4 (BeautifulSoup)`: Pro parsování HTML kódu. https://pypi.org/project/beautifulsoup4/
* `random`: Pro generování náhodných čísel.

## Spuštění skriptu

Skript lze spustit z příkazového řádku pomocí příkazu `python scrape.py`.
Je nutné nejdříve nainstalovat Python a beatifoulsoup4 (pip install beautifulsoup4)
Testováno na Python ve verzi 3.13.1
