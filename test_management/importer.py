import json
from typing import List, Tuple
import pandas as pd
from test_management.features import TestCase, TestStep, add_test_case

REQUIRED_COLUMNS = [
    "TestCaseID", "TestCaseName", "Description", "Action",
    "Target", "Value", "ExpectedResult", "Tags", "Type"
]

def _validate_columns(df: pd.DataFrame) -> List[str]:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    return missing

def _parse_df(df: pd.DataFrame) -> Tuple[int, List[str]]:
    errors: List[str] = []
    missing = _validate_columns(df)
    if missing:
        return 0, [f"Missing required column(s): {', '.join(missing)}"]

    grouped = df.groupby("TestCaseID", dropna=False)
    count = 0
    for tc_id, group in grouped:
        try:
            base = group.iloc[0]
            steps = []
            for _, row in group.iterrows():
                steps.append(TestStep(
                    action=str(row.get("Action", "")),
                    target=str(row.get("Target", "")),
                    value="" if pd.isna(row.get("Value")) else str(row.get("Value")),
                    expected_result=str(row.get("ExpectedResult", "")),
                ))
            tc = TestCase(
                id=str(tc_id),
                name=str(base.get("TestCaseName", "")),
                description=str(base.get("Description", "")),
                tags=[t.strip() for t in str(base.get("Tags", "")).split(",") if t.strip()],
                type=str(base.get("Type", "functional")).lower(),
                steps=steps,
            )
            add_test_case(tc)
            count += 1
        except Exception as e:
            errors.append(f"TestCaseID={tc_id}: {e}")
    return count, errors

def import_from_csv(file) -> Tuple[int, List[str]]:
    df = pd.read_csv(file)
    return _parse_df(df)

def import_from_excel(file) -> Tuple[int, List[str]]:
    df = pd.read_excel(file)
    return _parse_df(df)

def import_from_json(file) -> Tuple[int, List[str]]:
    try:
        data = json.load(file)
    except Exception as e:
        return 0, [f"Invalid JSON: {e}"]

    if not isinstance(data, dict) or "test_cases" not in data:
        return 0, ["JSON root must contain 'test_cases' list"]

    count = 0
    errors: List[str] = []
    for item in data.get("test_cases", []):
        try:
            steps = [TestStep(**s) for s in item.get("steps", [])]
            tc = TestCase(
                id=str(item.get("id")),
                name=str(item.get("name")),
                description=str(item.get("description", "")),
                tags=item.get("tags", []),
                type=str(item.get("type", "functional")).lower(),
                steps=steps,
            )
            add_test_case(tc)
            count += 1
        except Exception as e:
            errors.append(f"id={item.get('id')}: {e}")
    return count, errors
