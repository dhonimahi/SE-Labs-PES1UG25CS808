import pytest
from car_rental_rate import process_rental_fleet, check_fleet_telematics


def test_invalid_input_branches():
    with pytest.raises(ValueError):
        process_rental_fleet(None, 0)
    with pytest.raises(ValueError):
        process_rental_fleet([], -0.01)


def test_confirmation_and_default_value_branches():
    result = process_rental_fleet(
        [{"is_confirmed": False},
         {"is_confirmed": True, "driver_age": 30, "days": 1}], 0
    )
    assert result == {"total_revenue": 40.0, "status": "STANDARD"}


@pytest.mark.parametrize(
    "vehicle_type, expected",
    [("luxury", 120.0), ("suv", 70.0), ("economy", 40.0)],
)
def test_each_vehicle_type_branch(vehicle_type, expected):
    result = process_rental_fleet(
        [{"is_confirmed": True, "vehicle_type": vehicle_type,
          "driver_age": 30, "days": 1}], 0
    )
    assert result["total_revenue"] == expected


def test_days_and_trip_mileage_branches():
    result = process_rental_fleet(
        [{"is_confirmed": True, "days": -1},
         {"is_confirmed": True, "driver_age": 30, "days": 1,
          "trip_segments": [-10, 300, 301]}], 0
    )
    # Economy base 40 + 300*0.20 + 301*0.40
    assert result["total_revenue"] == 220.4


def test_long_trip_young_driver_break_branch():
    result = process_rental_fleet(
        [{"is_confirmed": True, "driver_age": 20, "days": 1,
          "trip_segments": [301, 10]}], 0
    )
    assert result["total_revenue"] == 310.0


def test_driver_age_fee_branches():
    luxury = process_rental_fleet(
        [{"is_confirmed": True, "vehicle_type": "luxury", "driver_age": 24,
          "days": 2}], 0
    )
    non_luxury = process_rental_fleet(
        [{"is_confirmed": True, "vehicle_type": "suv", "driver_age": 25,
          "days": 2}], 0
    )
    assert luxury["total_revenue"] == 340.0
    assert non_luxury["total_revenue"] == 140.0


def test_status_priority_branches():
    high_risk = process_rental_fleet(
        [{"is_confirmed": True, "days": 0} for _ in range(5)], 0
    )
    empty = process_rental_fleet([], 0)
    standard = process_rental_fleet(
        [{"is_confirmed": True, "driver_age": 30, "days": 1}], 0
    )
    assert high_risk["status"] == "HIGH_RISK_AUDIT"
    assert empty["status"] == "EMPTY_BATCH"
    assert standard["status"] == "STANDARD"


def test_telematics_empty_outer_matrix():
    assert check_fleet_telematics([]) == "NO_DATA"


def test_telematics_speeding_streak_reaches_threshold():
    assert check_fleet_telematics([[101, 101]]) == "GROUND_VEHICLE"


def test_telematics_streak_resets_after_safe_speed():
    assert check_fleet_telematics([[101, 100, 101]]) == "SAFE"


def test_telematics_single_speeding_reading_per_vehicle():
    assert check_fleet_telematics([[120], [130]]) == "SAFE"
