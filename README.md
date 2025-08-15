# Streamlit Test Management Tool

Production-ready Streamlit app to import and review test cases for **UI**, **Regression**, **UAT**, and more.

## Features
- Import from **CSV**, **Excel (.xlsx)**, or **JSON**
- In-memory store suitable for demos and Streamlit Cloud
- Quick export to JSON, basic filters and metrics
- Sample files under `examples/`

## Run Locally
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy on Streamlit Cloud
1. Push this folder to a GitHub repo
2. In Streamlit Cloud, create a **New app**
3. Select your repo and set **Main file path** to `streamlit_app.py`
4. Deploy

## CSV/XLSX Required Columns
```
TestCaseID, TestCaseName, Description, Action, Target, Value, ExpectedResult, Tags, Type
```

See `examples/sample_test_cases.csv` and `examples/sample_tool_data.json` for ready-to-use templates.
