# Dokumentace ke kódu pro stahování PDF souborů z webu Understanding War

Tento skript slouží k automatickému stahování PDF souborů z webu Understanding War ([https://www.understandingwar.org/publications](https://www.understandingwar.org/publications)) a jejich ukládání do složek podle roku a měsíce.

## Funkce

### `stahni_pdf(url, datum_str, nazev_clanku)`

Stáhne PDF soubor z dané URL adresy a uloží ho s daným názvem.

**Argumenty:**

* `url`: URL adresa PDF souboru.
* `datum_str`: Datum článku ve formátu "YYYY-MM-DD".
* `nazev_clanku`: Název článku.

**Funkcionalita:**

1. Odeslání HTTP požadavku na danou URL adresu s hlavičkami simulujícími webový prohlížeč.
2. Kontrola, zda je požadavek úspěšný (status code 200).
3. Formátování názvu souboru ve formátu `DDMMYY-Název článku`, kde:
    * `DD`: Den v měsíci.
    * `MM`: Zkratka měsíce v angličtině (JAN, FEB, MAR, ...).
    * `YY`: Rok (dvě číslice).
4. Vytvoření adresářové struktury pro ukládání souborů ve formátu `rok/měsíc`.
5. Kontrola, zda soubor s daným názvem již existuje. Pokud ano, stahování se přeskočí.
6. Uložení PDF souboru do příslušné složky.

### `prozkoumej_stranku(url)`

Prozkoumá danou stránku a stáhne všechny dostupné PDF soubory.

**Argumenty:**

* `url`: URL adresa stránky.

**Funkcionalita:**

1. Odeslání HTTP požadavku na danou URL adresu s hlavičkami simulujícími webový prohlížeč.
2. Kontrola, zda je požadavek úspěšný (status code 200).
3. Náhodné zpoždění mezi 100 a 300 ms, aby se předešlo blokování IP adresy za DoS útok.
4. Parsování HTML kódu stránky pomocí knihovny BeautifulSoup.
5. Nalezení všech odkazů na články na stránce.
6. Pro každý článek:
    * Získání URL adresy článku.
    * Odeslání HTTP požadavku na URL adresu článku.
    * Náhodné zpoždění mezi 100 a 300 ms.
    * Parsování HTML kódu článku.
    * Nalezení odkazu na PDF soubor v článku.
    * Nalezení data článku v HTML kódu.
    * Získání názvu článku z HTML kódu.
    * Pokud je nalezen odkaz na PDF soubor, zavolá se funkce `stahni_pdf()` pro stažení souboru.

### `main()`

Hlavní funkce skriptu.

**Funkcionalita:**

1. Nastavení základní URL adresy na `https://www.understandingwar.org/publications`.
2. V nekonečné smyčce:
    * Zpracování první stránky s publikacemi.
    * Zpracování dalších stránek s publikacemi (pokud existují).
    * Čekání 12 hodin (43200 sekund).

## Použité knihovny

* `requests`: Pro odesílání HTTP požadavků.
* `os`: Pro práci se soubory a adresáři.
* `time`: Pro zpoždění mezi požadavky.
* `datetime`: Pro práci s datem a časem.
* `bs4 (BeautifulSoup)`: Pro parsování HTML kódu.
* `random`: Pro generování náhodných čísel.

## Spuštění skriptu

Skript lze spustit z příkazového řádku pomocí příkazu `python nazev_skriptu.py`.

## Poznámky

* Skript stahuje PDF soubory dvakrát denně. Pokud je potřeba jiná frekvence, upravte hodnotu v `time.sleep()` v `main()`.
* Skript používá náhodné zpoždění mezi požadavky, aby se předešlo blokování IP adresy.
