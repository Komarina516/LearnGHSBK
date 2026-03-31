import copy

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

_original_activities = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(_original_activities))
    yield
    activities.clear()
    activities.update(copy.deepcopy(_original_activities))


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client
