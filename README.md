# observer-ci-lab

Observer-pattern market data broadcasting + trading loop with pytest, coverage, and GitHub Actions.

## Design notes (explicit spec alignment)

### MarketDataSubject
- Maintains a list of observers (in attach order).
- attach(observer): adds observer if not already present (avoids duplicates).
- detach(observer): idempotent (no error if missing).
- notify(price): calls observer.update(price) for each observer in attach order.
- Failure behavior:
  - continue_on_error = False (default): propagate the first exception and stop notifying.
  - continue_on_error = True: continue notifying remaining observers, then raise a NotificationError.

### Observers
- VolatilityBreakoutStrategyObserver(window):
  - Stores price history.
  - Computes simple returns r_t = p_t / p_{t-1} - 1.
  - Once enough data exists, compares the latest return to sigma = std(previous window returns, ddof=1).
  - last_signal = +1 if r_t > sigma, -1 if r_t < -sigma, else 0.
  - Non-finite prices (NaN/inf) are ignored (signal set to 0; price not appended).
- RiskObserver(max_position, broker):
  - Reads broker.position and sets breached=True if abs(position) > max_position.
- LoggerObserver(strategy=None):
  - Records all prices and (optionally) strategy.last_signal at update time.

### Broker
- Deterministic market orders (no slippage/fees).
- Validates side in {buy,sell}, qty>0 integer, price>0.
- Raises on insufficient cash/shares.

### Engine timing convention
- For each price p_t:
  1) subject.notify(p_t) updates observers (strategy computes last_signal using p_t).
  2) engine acts immediately on strategy.last_signal at time t using price p_t.

## Run locally
    py -3.11 -m venv .venv
    .\\.venv\\Scripts\\Activate.ps1
    pip install -r requirements.txt
    pytest
    coverage run -m pytest -q
    coverage report --fail-under=90 -m

## CI
- GitHub Actions runs on push and pull_request and enforces coverage >= 90%.
