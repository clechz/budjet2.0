# BudJet 2.0

A Django budgeting prototype that moves a Python transaction tracker into a web interface.

The application accepts income and expense entries and displays transaction history. Its transaction records live in CSV; Django's SQLite database supports the framework rather than serving as the transaction ledger.

## What is implemented

- A home page at `/`.
- A transaction-entry form at `/add/`.
- A transaction-history page at `/transactions/`.
- CSV rows containing date, amount, category, description, balance, and session key.
- Session-key filtering in the CSV read and write workflow.

This is a learning prototype. Session filtering is part of the implementation, not a claim of production-grade account isolation.

## Code map

| Path | Purpose |
| --- | --- |
| `budjet/budjetapp/views.py` | Page rendering and form handling |
| `budjet/budjetapp/urls.py` | Application routes |
| `budjet/budjetapp/main/app.py` | CSV storage and balance calculation |
| `budjet/budjetapp/main/data.py` | Transaction input helpers |
| `budjet/budjetapp/templates/` | Django templates |
| `budjet/csv/` | CSV storage directory |
| `budjet/budjet/settings.py` | Django configuration |
| `build.sh` | Dependency installation, static collection, and migrations |

## Local development

Use a disposable local copy and synthetic transaction data.

The checked-in dependency list omits `pandas` and `whitenoise`, both referenced by the application. Install them alongside the existing requirements:

```bash
python -m venv .venv
# Activate .venv using the command for your shell.
python -m pip install -r requirements.txt
python -m pip install pandas whitenoise
```

In your local `budjet/budjet/settings.py`, set:

```python
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
```

Run from the `budjet` directory so the relative `csv/finance_data.csv` path resolves correctly:

```bash
cd budjet
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. These steps explain the expected setup; they do not establish that all transaction flows work correctly.

## Current limitations

- The checked-in settings use a development secret key and have an empty allowed-host list. Production configuration needs separate work.
- CSV creation and missing-file recovery contain calls whose arguments do not match the storage methods. A fresh or missing data file can fail.
- The history reader drops the first data row and can retain empty entries when filtering other sessions.
- Backdated transactions, zero balances, input validation, and concurrent writes need verification and repair.
- Session identifiers and transaction values are printed by debug statements.

The next useful step is a reliable storage and validation pass, followed by a clean synthetic-data demo. The earlier [BudJet CLI](https://github.com/clechz/budjet) shows the original command-line workflow.
