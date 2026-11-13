"""Validated amusement-park ride access utilities."""
import math
import re


def validate_height_and_fastpass(rider_spec):
    """Return approval and queue status, or a readable validation error."""
    if not isinstance(rider_spec, str):
        return "Invalid rider specification: expected Height:FastPass"
    match = re.fullmatch(r"\s*([+-]?\d+)\s*:\s*(YES|NO)\s*", rider_spec, re.IGNORECASE)
    if not match:
        return "Invalid rider specification: expected Height:FastPass (e.g. 140:YES)"
    height = int(match.group(1))
    if height < 0 or height > 300:
        return "Invalid height: must be between 0 and 300 cm"
    eligible = height >= 120
    has_fastpass = match.group(2).upper() == "YES"
    status = "FastPass Priority" if has_fastpass else "Standard Entry"
    return f"Height {height}cm: {'Approved' if eligible else 'Denied'} ({status})"


def compute_dispatch_throughput(ride_metric_str):
    """Compute riders/min; return None on invalid, unsafe, or undefined input."""
    if not isinstance(ride_metric_str, str):
        return None
    parts = ride_metric_str.split('/')
    if len(parts) != 2:
        return None
    try:
        riders = float(parts[0].strip())
        cycle_mins = float(parts[1].strip())
    except (ValueError, OverflowError):
        return None
    if not (math.isfinite(riders) and math.isfinite(cycle_mins)):
        return None
    if riders < 0 or cycle_mins <= 0:
        return None
    rate = riders / cycle_mins
    if not math.isfinite(rate):
        return None
    return round(rate, 2)


def resolve_safety_restraint_code(zone_code):
    """Resolve a zone prefix; return Unknown restraint code for bad inputs."""
    restraint_types = {
        "CST": "Over-the-Shoulder Harness",
        "WTR": "Lap Bar and Seatbelt",
        "DRP": "Hydraulic Shoulder Vest",
        "WHL": "Manual Safety Bar",
    }
    if not isinstance(zone_code, str):
        return "Unknown restraint code"
    code = zone_code.strip().upper()
    prefix = code[:3]
    return restraint_types.get(prefix, "Unknown restraint code")


def main():
    print("==== Running validate_height_and_fastpass ====")
    r_input = input("Enter rider spec (Height:FastPass, e.g. 140:YES): ")
    print(validate_height_and_fastpass(r_input))
    print("\n==== Running compute_dispatch_throughput ====")
    t_input = input("Enter riders/mins (e.g. 48/2.5): ")
    throughput = compute_dispatch_throughput(t_input)
    print("Throughput (riders/min):", throughput if throughput is not None else "Invalid dispatch metric")
    print("\n==== Running resolve_safety_restraint_code ====")
    z_input = input("Enter ride zone code (e.g. CST_01, WTR_A): ")
    print("Restraint:", resolve_safety_restraint_code(z_input))


if __name__ == "__main__":
    main()
