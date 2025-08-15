from typing import List, Dict
from pydantic import BaseModel

class TestStep(BaseModel):
    action: str
    target: str
    value: str = ""
    expected_result: str = ""

class TestCase(BaseModel):
    id: str
    name: str
    description: str
    steps: List[TestStep]
    tags: List[str] = []
    type: str = "functional"  # ui | regression | uat | functional

class UATChecklistItem(BaseModel):
    id: str
    module: str
    feature: str
    requirement: str
    accepted_by: str
    completed: bool = False

# Simple in-memory store (session lifecycle on Streamlit Cloud)
_test_cases: Dict[str, TestCase] = {}

def add_test_case(tc: TestCase) -> None:
    _test_cases[tc.id] = tc

def get_test_case(tc_id: str) -> TestCase | None:
    return _test_cases.get(tc_id)

def list_test_cases(test_type: str | None = None) -> List[TestCase]:
    cases = list(_test_cases.values())
    if test_type:
        cases = [c for c in cases if c.type == test_type]
    # Stable sort by ID then name for consistent UI
    return sorted(cases, key=lambda c: (str(c.id), c.name))

def clear_all_test_cases() -> None:
    _test_cases.clear()

def export_test_cases_json() -> List[dict]:
    return [c.model_dump() for c in list_test_cases()]  # pydantic v2-compatible; v1 also supports .dict()

def stats_overview() -> dict:
    by_type: Dict[str, int] = {}
    for c in _test_cases.values():
        by_type[c.type] = by_type.get(c.type, 0) + 1
    return {"total": len(_test_cases), "by_type": by_type}
