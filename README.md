
# ShortLink – URL Shortener

Aplikacja webowa umożliwiająca skracanie długich adresów URL, zarządzanie utworzonymi linkami oraz monitorowanie statystyk ich wykorzystania.

Projekt został stworzony w ramach przedmiotu **Testowanie i jakość oprogramowania II**.

## Technologie

- Python 3.13
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML5
- CSS3
- JavaScript
- pytest
- pytest-cov
- Ruff
- Radon

## Funkcjonalności

- Skracanie adresów URL.
- Automatyczne generowanie krótkich kodów.
- Możliwość definiowania własnych kodów.
- Walidacja adresów URL i kodów.
- Przekierowywanie na oryginalne adresy.
- Zliczanie kliknięć w skrócone linki.
- Dashboard ze statystykami.
- Wyszukiwanie i sortowanie linków.
- Paginacja listy linków.
- Podgląd szczegółów poszczególnych linków.
- Usuwanie utworzonych linków.

## Wymagania

Do uruchomienia projektu potrzebne są:

- Python 3.13 lub nowszy.
- Git (opcjonalnie, jeśli projekt jest pobierany z repozytorium).
- Przeglądarka internetowa.

## Instalacja i uruchomienie

### 1. Pobranie projektu

Sklonuj repozytorium:

```bash
git clone ADRES_REPOZYTORIUM
```

Przejdź do katalogu projektu:

```bash
cd URLShortener
```

Alternatywnie możesz pobrać projekt jako archiwum ZIP i rozpakować go na komputerze.

### 2. Utworzenie środowiska wirtualnego

Windows:

```powershell
py -m venv .venv
```

Aktywuj środowisko:

```powershell
.venv\Scripts\Activate.ps1
```

Jeżeli PowerShell blokuje aktywację skryptu, możesz pominąć aktywację i korzystać bezpośrednio z interpretera znajdującego się w `.venv\Scripts\python.exe`.

### 3. Instalacja zależności

Upewnij się, że znajdujesz się w głównym katalogu projektu, a następnie wykonaj:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Uruchomienie aplikacji

Uruchom serwer Flask:

```powershell
python run.py
```

Aplikacja będzie dostępna pod adresem:

http://127.0.0.1:5000

Aby zakończyć działanie serwera, użyj skrótu `CTRL + C` w terminalu.

## Baza danych

Aplikacja korzysta z SQLite. Baza danych jest tworzona automatycznie podczas uruchamiania aplikacji, jeśli nie istnieje.

Nie jest wymagane ręczne instalowanie ani konfigurowanie serwera bazy danych.

## Uruchamianie testów

Testy można uruchomić poleceniem:

```powershell
python -m pytest -v
```

Uruchomienie testów wraz z raportem pokrycia kodu:

```powershell
python -m pytest -v --cov=app --cov-report=term-missing
```

## Struktura projektu

```text
URLShortener/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── services.py
│   ├── validators.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   └── 404.html
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       ├── script.js
│   │       └── dashboard.js
│   │
│   └── tests/
│
├── config.py
├── run.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Autor

Projekt wykonany w ramach przedmiotu Testowanie i jakość oprogramowania II.
