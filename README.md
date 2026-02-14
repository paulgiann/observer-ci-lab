# observer-ci-lab

Minimal Observer-pattern market data -> observers -> broker engine, with pytest + coverage + GitHub Actions.

Run locally:
  pip install -r requirements.txt
  pytest
  coverage run -m pytest
  coverage report -m

CI:
GitHub Actions runs tests + coverage and fails if coverage < 90%.
