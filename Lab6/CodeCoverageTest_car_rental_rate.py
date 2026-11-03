import pytest
from car_rental_rate import process_rental_fleet, check_fleet_telematics


def test_invalid_rentals_type():
    with pytest.raises(ValueError):
        process_rental_fleet("not a list", 10)


def test_negative_admin_fee():
    with pytest.raises(ValueError):
        process_rental_fleet([], -1)


def test_unconfirmed_rental_is_skipped():
    result = process_rental_fleet([{"is_confirmed": False}], 10)
    assert result == {"total_revenue": 0.0, "status": "EMPTY_BATCH"}


def test_defaults_and_economy_rate():
    result = process_rental_fleet([{"is_confirmed": True}], 10)
    assert result == {"total_revenue": 50.0, "status": "STANDARD"}


@pytest.mark.parametrize(
    "vehicle_type, expected",
    [("luxury", 120.0), ("suv", 70.0), ("economy", 40.0), ("unknown", 40.0)],
)
def test_vehicle_rates(vehicle_type, expected):
    result = process_rental_fleet(
        [{"is_confirmed": True, "vehicle_type": vehicle_type, "driver_age": 30,
          "days": 1}], 0
    )
    assert result["total_revenue"] == expected


def test_nonpositive_days_flagged_and_skipped():
    result = process_rental_fleet(
        [{"is_confirmed": True, "days": 0}], 0
    )
    assert result == {"total_revenue": 0.0, "status": "EMPTY_BATCH"}


def test_negative_miles_flagged_and_skipped():
    result = process_rental_fleet(
        [{"is_confirmed": True, "driver_age": 30, "days": 1,
          "trip_segments": [-5, 100]}], 0
    )
    assert result["total_revenue"] == 60.0


def test_long_trip_surcharge_for_adult_driver():
    result = process_rental_fleet(
        [{"is_confirmed": True, "driver_age": 30, "days": 1,
          "trip_segments": [301]}], 0
    )
    assert result["total_revenue"] == 160.4


def test_long_trip_young_driver_adds_penalty_and_breaks():
    result = process_rental_fleet(
        [{"is_confirmed": True, "driver_age": 20, "days": 1,
          "trip_segments": [301, 50]}], 0
    )
    assert result["total_revenue"] == 310.0


def test_short_trip_cost_and_young_driver_fee():
    result = process_rental_fleet(
        [{"is_confirmed": True, "vehicle_type": "luxury", "driver_age": 24,
          "days": 2, "trip_segments": [100]}], 0
    )
    assert result["total_revenue"] == 360.0


def test_young_non_luxury_driver_fee():
    result = process_rental_fleet(
        [{"is_confirmed": True, "vehicle_type": "suv", "driver_age": 24,
          "days": 2}], 0
    )
    assert result["total_revenue"] == 180.0


def test_high_risk_audit_status():
    rentals = [
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": 0},
    ]
    result = process_rental_fleet(rentals, 0)
    assert result == {"total_revenue": 0.0, "status": "HIGH_RISK_AUDIT"}


def test_telematics_no_data():
    assert check_fleet_telematics([]) == "NO_DATA"


def test_telematics_safe_and_streak_reset():
    assert check_fleet_telematics([[110, 90, 105, 80], [100]]) == "SAFE"


def test_telematics_two_consecutive_speeding_readings():
    assert check_fleet_telematics([[101, 110]]) == "GROUND_VEHICLE"


def test_telematics_streak_resets_between_vehicles():
    assert check_fleet_telematics([[110], [110]]) == "SAFE"
