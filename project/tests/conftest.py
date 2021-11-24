# project/tests/conftest.py

import pytest
from app import main
from starlette.testclient import TestClient


@pytest.fixture(scope="module")
def test_app():
    with TestClient(main.app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def test_data_optimization():
    return {
        "customers": ["c1", "c2", "c3", "c4", "c5"],
        "facilities": ["f1", "f2", "f3"],
        "transportation_cost": {
            "c1": {"f1": 4, "f2": 6, "f3": 9},
            "c2": {"f1": 5, "f2": 4, "f3": 7},
            "c3": {"f1": 6, "f2": 3, "f3": 4},
            "c4": {"f1": 8, "f2": 5, "f3": 3},
            "c5": {"f1": 10, "f2": 8, "f3": 4},
        },
        "facility_capacity": {"f1": 500, "f2": 500, "f3": 500},
        "facility_installation_cost": {"f1": 1000, "f2": 1000, "f3": 1000},
        "demand": {"c1": 80, "c2": 270, "c3": 250, "c4": 160, "c5": 180},
    }


@pytest.fixture(scope="module")
def test_data_post(test_data_optimization):
    return {
        **{
            "instance_name": "Facility Location",
            "comment": "Optimization of facility locations for new logistics network",
        },
        **test_data_optimization,
    }


@pytest.fixture(scope="module")
def test_data_post_infeasible(test_data_optimization):
    test_data_optimization["facility_capacity"] = {
        i: 0 for i in test_data_optimization["facilities"]
    }
    return {
        **{
            "instance_name": "Facility Location",
            "comment": "Optimization of facility locations for new logistics network",
        },
        **test_data_optimization,
    }
