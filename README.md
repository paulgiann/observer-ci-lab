# observer-ci-lab

Minimal Observer-pattern market data -> observers -> broker engine, with pytest + coverage + GitHub Actions.

## Project layout
- trading/: subject, observers, broker, engine
- tests/: pytest suite

## How to run locally (PowerShell, Python 3.11)
From the repo root:

    py -3.11 -m venv .venv
    .\\.venv\\Scripts\\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements.txt

Run tests:
    pytest

Run coverage (must be >= 90%):
    coverage run -m pytest -q
    coverage report --fail-under=90 -m

Optional HTML report:
    coverage html

## CI
GitHub Actions runs the same commands on every push and pull request and fails if coverage < 90%.

## Design notes (brief)
- MarketDataSubject: attach avoids duplicates; detach is idempotent; notify preserves attach order.
- Failure behavior: default propagates the first observer exception; optional continue_on_error mode notifies all then raises NotificationError.
- Engine timing: for each price p_t, observers update first, then engine trades immediately using strategy.last_signal at tick t.
- Observers: VolatilityBreakoutStrategyObserver emits -1/0/+1; RiskObserver flags position limit breaches; LoggerObserver records prices (and can record signals when wired to a strategy).
