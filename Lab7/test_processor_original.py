from hypothesis import given, strategies as st
from processor_original import sanitize_license_plate, parse_trip_mileage, format_rental_invoice

@given(st.text() | st.none())
def test_sanitize_license_plate_no_crash(s):
    sanitize_license_plate(s)

@given(st.text() | st.none())
def test_parse_trip_mileage_safe(s):
    parse_trip_mileage(s)

@given(st.text() | st.none())
def test_format_rental_invoice_safe(s):
    format_rental_invoice(s)
