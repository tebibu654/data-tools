# data-tools

A collection of tools to integrate with the Synthetix [data service](https://github.com/Synthetixio/data).

## setup

To set up this repo, first make sure you have installed [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) using the official installer.

Then, install dependencies and activate the virtual environment:

```bash
poetry install
poetry shell
```

Always make sure this environment has been activated before running any dashboards or API.

Finally, copy the `./streamlit/secrets_example.toml` file and fill it in before running any dashboards.

## tools

- API
  - SynthetixAPI class (in progress)
  - External API wrapper (in progress)
- Dashboards
  - Key metrics (in progress)
  - Deep metrics (in progress)
  - System monitor (in progress)
