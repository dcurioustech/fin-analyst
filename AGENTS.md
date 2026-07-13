# Financial Analysis Bot — Agent Instructions

Intelligent financial analysis assistant for NASDAQ-100 constituents. Natural-language queries drive company profiles, metrics, statements, and peer comparisons. Data comes primarily from Yahoo Finance (`yfinance`); orchestration is LangGraph-based.

For deeper docs see `README.md`, `DEVELOPER_GUIDE.md`, `USER_GUIDE.md`, and `docs/`.

## Architecture

Layered orchestrator design. Prefer extending layers over bypassing them.

| Layer | Path | Role |
|-------|------|------|
| Entry points | `chat_interface.py`, `web_app.py`, `main.py` | CLI chat (recommended), FastAPI web, menu UI |
| Orchestrator | `agents/graph.py`, `agents/nodes.py`, `agents/state.py` | LangGraph workflow & state |
| Interpreter | `agents/interpreter.py` | Parse intent, companies, analysis type |
| Tools | `agents/tools.py` | `@tool` wrappers over analyzers |
| Response | `agents/response_generator.py` | User-facing response formatting |
| Analysis | `analysis/` | Profile, metrics, statements, comparison |
| Data | `services/financial_data_service.py` | Yahoo Finance access, validation, retries |
| Config | `config/settings.py`, `config/gcp_config.py` | App + GCP settings |
| UI helpers | `ui/` | Menu + display formatting |
| Utils | `utils/` | Formatting, validation, errors, viz |

**Request flow:** User input → interpreter → plan → data collection → analysis tools → aggregate → response generation.

**State:** `FinancialOrchestratorState` in `agents/state.py`. Use the helpers there (`create_initial_state`, `update_*`, `set_error`) instead of ad-hoc state mutation.

**Universe boundary:** Only current NASDAQ-100 constituents are supported. The maintained local snapshot and guard functions are in `utils/nasdaq_100.py`; use them for every ticker input and data-service path. Do not bypass the guard with direct Yahoo Finance calls. The snapshot must be refreshed after official index rebalances.

## Setup

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # set GOOGLE_API_KEY at minimum
```

Optional: `./scripts/dev_setup.sh`

**Runtime:** Python 3.12 preferred (see `pyproject.toml` / mypy). Dependencies in `requirements.txt` only — do not invent new top-level packages without updating that file.

## Commands

| Task | Command |
|------|---------|
| Chat (local) | `python3 chat_interface.py` |
| Web | `python3 web_app.py` |
| Menu UI | `python3 main.py` |
| Unit tests | `make test` or `pytest tests/` |
| Integration | `make test-integration` or `pytest integration_tests/` |
| All tests | `make test-all` or `pytest` |
| Coverage | `make test-coverage` |
| CI-like tests | `make ci-test` |
| Format | `make format` (black + isort) |
| Format check | `make format-check` |
| Lint | `make lint` / `make ci-lint` |
| Security | `make ci-security` |
| Docker | `make docker-build` / `make docker-run` |

## Coding conventions

- **Python style:** Black (line length 88 for format; flake8 allows 120), isort profile `black`, type hints where practical.
- **Docstrings:** Module and public function/class docstrings; Args/Returns style as in existing code.
- **Logging:** `logging.getLogger(__name__)`. Prefer structured messages; avoid silent failures.
- **Errors:** Graceful degradation; return structured `{success, error, data}` from tools/services when that pattern already exists. User-facing text goes through the response layer.
- **Tickers:** Normalize with `.upper()`; validate via `FinancialDataService` / `validate_ticker` tool.
- **External I/O:** Keep live API calls in `services/`. Analysis code should not call `yfinance` directly.
- **LangGraph:** New workflow steps belong in `agents/nodes.py` with routing helpers; register nodes/edges in `agents/graph.py`.
- **New analysis capability:** Implement in `analysis/` → expose via `agents/tools.py` → wire interpreter keywords if needed → format in response generator.
- **Secrets:** Never commit `.env` or keys. Use `.env.example` for documented vars only.
- **Do not commit:** `infrastructure/gcp/terraform/terraform.tfstate` secrets, `.terraform/`, venvs, or API keys.

## Testing

- Unit tests: `tests/` (mock external APIs; fixtures in `tests/test_fixtures.py`).
- Integration: `integration_tests/`.
- Markers: `unit`, `integration`, `slow` (see `pyproject.toml`).
- New features need unit tests; workflow/routing changes need integration coverage.
- Prefer pytest; mock `yfinance` / network in unit tests.

## Environment

| Variable | Required | Notes |
|----------|----------|--------|
| `GOOGLE_API_KEY` | Yes (LLM paths) | Google AI / Gemini |
| `ENVIRONMENT` | No | `development` / `staging` / `production` |
| `LOG_LEVEL` | No | Default `INFO` |
| `PORT` | No | Web default `8080` |
| `ALPHA_VANTAGE_API_KEY`, `POLYGON_API_KEY` | No | Optional data sources |
| `PROJECT_ID`, `REGION` | GCP deploy | See `docs/DEPLOYMENT.md` |

## Deployment notes

- Production target: GCP (Cloud Run, Firestore, Redis, Secret Manager). Entry for deploy scripts: `infrastructure/gcp/`.
- Docker: root `Dockerfile`; container listens on `PORT` (default 8080).
- Do not apply Terraform or push to shared cloud without explicit user approval.

## PR / commit expectations

- Branch names: `feature/`, `fix/`, or `chore/` preferred.
- Before PR: tests pass (`make ci-test` or equivalent), format/lint clean for touched code.
- Use `.github/PULL_REQUEST_TEMPLATE.md` checklist.
- Update docs when behavior, env vars, or public APIs change (`docs/API.md`, guides as needed).

## Safety / product constraints

- Educational/research framing: do not present output as personalized investment advice.
- Prefer deterministic rule-based interpreter/response paths unless the task explicitly involves LLM integration.
- Keep financial number formatting consistent with existing `utils/formatters.py` and display helpers.
