import json
import streamlit as st
from streamlit_option_menu import option_menu
from test_management.features import (
    list_test_cases, export_test_cases_json, clear_all_test_cases, stats_overview
)
from streamlit_ui.import_page import run_import_page

st.set_page_config(page_title="Test Management Tool", layout="wide")

# Sidebar navigation
with st.sidebar:
    choice = option_menu(
        "Menu",
        ["Import Test Cases", "View Test Cases", "Export & Reset", "About"],
        icons=["cloud-upload", "list-task", "box-arrow-down", "info-circle"],
        menu_icon="check2-square",
        default_index=0,
    )

st.title("🧪 Test Management Tool")

if choice == "Import Test Cases":
    run_import_page()

elif choice == "View Test Cases":
    st.subheader("📋 Test Case List")
    cases = list_test_cases()
    if not cases:
        st.info("No test cases imported yet. Use the **Import Test Cases** page to get started.")
    else:
        # KPI cards
        s = stats_overview()
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Cases", s["total"])
        c2.metric("Regression", s["by_type"].get("regression", 0))
        c3.metric("UAT", s["by_type"].get("uat", 0))

        # Filters
        with st.expander("Filters"):
            types = sorted({tc.type for tc in cases})
            type_filter = st.multiselect("Filter by Type", options=types, default=types)
            tag = st.text_input("Filter by Tag (contains)")

        for tc in cases:
            if tc.type not in type_filter:
                continue
            if tag and not any(tag.lower() in t.lower() for t in tc.tags):
                continue
            with st.expander(f"{tc.id} — {tc.name}  •  [{tc.type}]"):
                st.write(f"**Description:** {tc.description}")
                if tc.tags:
                    st.write("**Tags:**", ", ".join(tc.tags))
                st.write("**Steps:**")
                for i, step in enumerate(tc.steps, start=1):
                    st.markdown(f"- **Step {i}:** `{step.action}` on `{step.target}`"
                                f"{' with value `' + step.value + '`' if step.value else ''} "
                                f"→ Expected: `{step.expected_result}`")

elif choice == "Export & Reset":
    st.subheader("📤 Export / ♻️ Reset")
    data = export_test_cases_json()
    st.download_button(
        "Download Test Cases (JSON)",
        data=json.dumps(data, indent=2),
        file_name="test_cases_export.json",
        mime="application/json"
    )

    st.divider()
    st.warning("Reset will remove all in-memory test cases from this session.", icon="⚠️")
    if st.button("Reset All Test Cases", type="primary"):
        clear_all_test_cases()
        st.success("All test cases cleared from memory.")

elif choice == "About":
    st.header("ℹ️ About")
    st.markdown(
        """
This production-ready Streamlit app lets you import and review test cases for **UI**, **Regression**, and **UAT**.

**Highlights**
- Import from **CSV**, **Excel (.xlsx)**, or **JSON** (tool exports)
- In-memory store (session-scoped) suitable for demos and Cloud
- Quick export to JSON; simple filters and metrics

**File Format (CSV/XLSX required columns)**
```
TestCaseID, TestCaseName, Description, Action, Target, Value, ExpectedResult, Tags, Type
```

See sample files under the **examples/** folder in the repo.
"""
    )
