# dashboards

This directory contains streamlit dashboards for visualizing Synthetix data.

## structure

Each dashboard is organized like this:

- `app.py`: Main application entry point, con
- `views/`: Page-specific content
- `modules/`: Reusable dashboard components

## features

- Direct page linking via query parameters
- State management using Streamlit
- Server-side data caching
- Shared utilities (charting, formatting, dates, etc.)
- Easy to fork or contribute

## creating a new dashboard

1. Create a new directory under `dashboards/` or copy the `sample` app
2. Add `app.py` as the entry point. This comes with a pre-configured `api` object at `st.session_state.api`
3. Create `views/` for page content, adding each one to the `app.py`
4. (optional) Use `modules/` for reusable components, importing each one in the relevant `views`
5. Utilize shared utilities from `dashboards/utils/`

Refer to existing dashboards for examples of how to structure and implement a rich app. The `key_metrics` dashboard contains examples for usage of the data API, data caching, state management, and more.
