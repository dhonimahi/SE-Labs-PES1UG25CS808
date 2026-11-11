import math

def sanitize_license_plate(plate):
    """
    Sanitizes vehicle license plate input.
    Strips whitespace and removes delimiters ('-', ' ', '_', '#').
    Returns an uppercase string. Handles None, non-strings, and arbitrary text gracefully.
    """
    if plate is None or not isinstance(plate, str):
        return ""
    plate = plate.strip()
    for ch in ['-', ' ', '_', '#']:
        plate = plate.replace(ch, '')
    return plate.upper()

def parse_trip_mileage(mileage_csv):
    """
    Parses a comma-separated string of trip mileages into a list of floats.
    Handles None, empty strings, invalid numeric tokens, negative values,
    and extra whitespace safely without raising uncaught exceptions.
    """
    if mileage_csv is None or not isinstance(mileage_csv, str):
        return []
    
    parts = mileage_csv.split(',')
    mileages = []
    for part in parts:
        cleaned = part.strip()
        if not cleaned:
            continue
        try:
            val = float(cleaned)
            if not math.isnan(val) and not math.isinf(val) and val >= 0:
                mileages.append(val)
        except (ValueError, TypeError):
            continue
    return mileages

def format_rental_invoice(record):
    """
    Formats a rental invoice string from a record formatted as 'Driver:Days:Category'.
    Handles None, missing fields, malformed numbers, negative days,
    and invalid types safely, returning a clear error message instead of crashing.
    """
    if record is None or not isinstance(record, str):
        return "Error: Invalid record input"
    
    parts = record.split(':')
    if len(parts) < 3:
        return "Error: Incomplete record format. Expected 'Driver:Days:Category'"
    
    driver = parts[0].strip()
    if not driver:
        return "Error: Driver name cannot be empty"
    
    try:
        days = int(parts[1].strip())
        if days < 0:
            return "Error: Rental days cannot be negative"
    except (ValueError, TypeError):
        return f"Error: Invalid rental days '{parts[1].strip()}'"
    
    category = parts[2].strip()
    if not category:
        return "Error: Vehicle category cannot be empty"
    
    daily_rate = 50.0 if category.lower() == "suv" else 30.0
    total = days * daily_rate
    return f"Driver {driver} booked {category} for {days} days: Total ${total:.2f}"

def main():
    print("==== Running sanitize_license_plate ====")
    raw_plate = input("Enter license plate with delimiters (-, _, #): ")
    clean_plate = sanitize_license_plate(raw_plate)
    print("Sanitized Plate:", clean_plate)

    print("\n==== Running parse_trip_mileage ====")
    csv_input = input("Enter CSV of mileages (e.g. 100.5, 45.2, 80.0): ")
    mileage_list = parse_trip_mileage(csv_input)
    print("Parsed Mileage List:", mileage_list)

    print("\n==== Running format_rental_invoice ====")
    record_input = input("Enter rental record (Driver:Days:Category): ")
    invoice = format_rental_invoice(record_input)
    print("Rental Invoice:", invoice)

if __name__ == "__main__":
    main()
