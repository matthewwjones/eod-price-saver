# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run tests
pytest

# Run a single test file
pytest test/config/test_instrumentcodeloader.py

# Lint
flake8 src/ test/

# Run the application (from repo root)
EOD_LOADER_API_TOKEN=<token> python -m src.__main__
```

## Architecture

There are two entry points:

- **Local run** — `src/__main__.py` (`if __name__ == "__main__"`) uses `App` (`src/app.py`), which reads instrument codes from `instrument-codes.txt` at the repo root and the API token from `EOD_LOADER_API_TOKEN`
- **Lambda** — `src/__main__.py` (`lambda_handler`) uses `EodPriceLoaderApp` (`src/eodpriceloaderapp.py`), which reads instrument codes from the bundled `instrument-codes.txt` and remaining config from environment variables

### Key classes

- `InstrumentCodeLoader` (`src/config/instrumentcodeloader.py`) — reads newline-separated instrument codes from a file
- `EodLoader` (`src/load/eodloader.py`) — calls the EODHD.com REST API (`/api/eod/{instrument}`) for each instrument; accepts a `load_date` (defaults to today)
- `SesNotifier` (`src/notify/sesnotifier.py`) — formats and sends the prices email via AWS SES

### Lambda environment variables

| Variable | Purpose |
|---|---|
| `EOD_LOADER_API_TOKEN` | EODHD API key |
| `EOD_LOADER_AWS_REGION` | SES region |
| `EOD_LOADER_EMAIL_TO` | Recipient address |
| `EOD_LOADER_EMAIL_FROM` | Verified SES sender address |

### Lambda handler reference
`src.__main__.lambda_handler`
