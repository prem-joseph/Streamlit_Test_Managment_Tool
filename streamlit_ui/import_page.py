import streamlit as st
import pandas as pd
from typing import Tuple
from test_management.importer import (
    import_from_csv, import_from_excel, import_from_json, REQUIRED_COLUMNS
)

def _show_requirements():
    st.caption("Required columns (CSV/XLSX):")
    st.code(", ".join(REQUIRED_COLUMNS), language="text")

def _render_examples():
    st.caption("Sample files (open to preview):")
    with st.expander("CSV sample"):
        st.code(open("examples/sample_test_cases.csv", "r", encoding="utf-8").read(), language="csv")
    with st.expander("JSON sample"):
        st.code(open("examples/sample_tool_data.json", "r", encoding="utf-8").read(), language="json")

def run_import_page():
    st.subheader("📥 Import Test Cases")

    _show_requirements()
    _render_examples()

    uploaded_file = st.file_uploader("Choose a file to import", type=["csv", "xlsx", "json"])
    if uploaded_file is None:
        st.info("Upload a CSV/XLSX/JSON file to import test cases.")
        return

    file_type = uploaded_file.name.split(".")[-1].lower()
    with st.spinner("Importing..."):
        try:
            if file_type == "csv":
                count, errors = import_from_csv(uploaded_file)
            elif file_type == "xlsx":
                count, errors = import_from_excel(uploaded_file)
            elif file_type == "json":
                count, errors = import_from_json(uploaded_file)
            else:
                st.error("Unsupported file type.")
                return
        except Exception as e:
            st.error(f"Failed to import file: {e}")
            return

    if count > 0:
        st.success(f"Imported {count} test case(s) from **{uploaded_file.name}**.")
    if errors:
        st.warning("Some rows could not be imported. See details below.")
        for err in errors:
            st.write(f"- {err}")
