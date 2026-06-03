import copy

import pytest

from src.app import activities

_original_activities = copy.deepcopy(activities)

@pytest.fixture(autouse=True)
def reset_activities():
    yield
    activities.clear()
    activities.update(copy.deepcopy(_original_activities))
