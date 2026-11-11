import pytest
from hypothesis import given, settings, strategies as st
from processor import sanitize_license_plate, parse_trip_mileage, format_rental_invoice

@settings(max_examples=500)
@given(st.text() | st.none())
def test_sanitize_license_plate_no_crash(s):
    try:
        result = sanitize_license_plate(s)
        assert isinstance(result, str)
        for ch in ['-', ' ', '_', '#']:
            assert ch not in result
    except Exception as exc:
        pytest.fail(f"sanitize_license_plate crashed on input {s!r} with error: {exc}")

@settings(max_examples=500)
@given(st.text() | st.none())
def test_parse_trip_mileage_safe(s):
    try:
        result = parse_trip_mileage(s)
        assert isinstance(result, list)
        for m in result:
            assert isinstance(m, float)
            assert m >= 0.0
    except Exception as exc:
        pytest.fail(f"parse_trip_mileage crashed on input {s!r} with error: {exc}")

@settings(max_examples=500)
@given(st.text() | st.none())
def test_format_rental_invoice_safe(s):
    try:
        result = format_rental_invoice(s)
        assert isinstance(result, str)
        assert len(result) > 0
    except Exception as exc:
        pytest.fail(f"format_rental_invoice crashed on input {s!r} with error: {exc}")
