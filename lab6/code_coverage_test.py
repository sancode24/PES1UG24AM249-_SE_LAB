import pytest
from amusement_park_ride_access import process_ride_admissions, inspect_safety_restraints


def test_single_adult_family_ride():
    groups = [{"is_open": True, "ride_type": "family", "has_fast_lane": False,
               "patrons": [{"height_cm": 150, "health_warning": False, "is_child": False}]}]
    result = process_ride_admissions(groups, 5.0)
    assert result == {"total_revenue": 10.0, "status": "COMPLETED"}


def test_invalid_input_raises():
    with pytest.raises(ValueError):
        process_ride_admissions("not a list", 5.0)


def test_mixed_groups_completed():
    groups = [
        {"is_open": False, "ride_type": "family", "patrons": []},                       # closed -> skipped
        {"is_open": True, "ride_type": "roller_coaster", "has_fast_lane": True,
         "patrons": [{"height_cm": 160}, {"height_cm": 130, "is_child": True}]},        # 25 + 15 + 5
        {"is_open": True, "ride_type": "water_ride",
         "patrons": [{"height_cm": 0}, {"height_cm": 100},
                     {"height_cm": 150, "health_warning": True}]},                      # 3 rejected, 0
    ]
    result = process_ride_admissions(groups, 5.0)
    assert result == {"total_revenue": 45.0, "status": "COMPLETED"}


def test_unknown_ride_and_coaster_health_break_zero():
    groups = [
        {"is_open": True, "ride_type": "go_kart", "patrons": []},
        {"is_open": True, "ride_type": "roller_coaster",
         "patrons": [{"height_cm": 170}, {"height_cm": 170, "health_warning": True}]},
    ]
    result = process_ride_admissions(groups, 0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}


def test_safety_audit():
    groups = [{"is_open": True, "ride_type": "family",
               "patrons": [{"height_cm": 100}] * 5 + [{"height_cm": 150}]}]
    result = process_ride_admissions(groups, 5.0)
    assert result == {"total_revenue": 10.0, "status": "SAFETY_AUDIT"}


def test_restraints_no_data():
    assert inspect_safety_restraints([]) == "NO_DATA"


def test_restraints_emergency_lock():
    assert inspect_safety_restraints([[1, 0, 1, 0, 0]]) == "EMERGENCY_LOCK"
