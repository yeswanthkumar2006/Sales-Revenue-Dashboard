# Revenue Intelligence Suite

A polished Streamlit analytics workspace for sales revenue, product performance, and executive reporting. The app is designed to work immediately with generated sample data and can use PostgreSQL when a `sales` table is configured.

## App Structure

- `main.py` - HOME Page / Growth Command Center with KPIs, trend analysis, category mix, and decision notes.
- `pages/1_Revenue_Explorer.py` - Filtered transaction analysis, exports, and data profiling.
- `pages/2_Product_Portfolio.py` - Product ranking, portfolio matrix, category mix, and focus recommendations.
- `pages/3_Executive_Report_Studio.py` - Leadership-ready report builder with markdown and CSV exports.

## Key Features

- Executive KPI layer for revenue, orders, customers, units, AOV, and growth.
- Sidebar filters for date range, region, category, product, and order revenue.
- Interactive Plotly visuals for trends, rankings, mix, and portfolio positioning.
- Sample-data fallback so the dashboard runs even without a database.
- Clean shared service layer in `src/dashboard_service.py`.
- Exportable transaction data, supporting analysis, and executive summaries.

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run main.py
```

Open the local Streamlit URL shown in your terminal, usually `http://localhost:8501`.

## Optional Database Setup

Create a `.env` file or edit the existing one with:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sales_analytics
DB_USER=user
DB_PASSWORD=password
MAX_DATA_POINTS=100000
```

If the database connection fails or the `sales` table is empty, the app automatically uses generated sample data.

## Project Layout

```text
Revenue Intelligence Suite/
├── main.py                      # HOME Page entry point
├── requirements.txt
├── assets/
│   └── style.css
├── components/
│   ├── charts.py
│   ├── filters.py
│   └── kpi_cards.py
├── data/
│   └── sample_data.py
├── pages/
│   ├── 1_Revenue_Explorer.py
│   ├── 2_Product_Portfolio.py
│   └── 3_Executive_Report_Studio.py
├── scripts/
│   ├── init_db.py
│   └── seed_data.py
├── src/
│   ├── analytics_engine.py
│   ├── dashboard_service.py
│   ├── data_processor.py
│   ├── database.py
│   └── utils.py
└── tests/
    ├── test_analytics_engine.py
    └── test_data_processor.py
```

## Quality Checks

```bash
pytest tests/ -v
python -m compileall main.py pages src components data
```

## Notes

The project keeps business logic in `src/`, generated data in `data/`, reusable Streamlit components in `components/`, and user-facing workflows in `main.py` plus `pages/`. This keeps the dashboard easier to extend without turning the entry point into a large script.
