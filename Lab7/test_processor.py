"""Hypothesis-based fuzz and correctness tests for all three functions."""
import math

from hypothesis import given, settings, strategies as st
from processor import (
    validate_height_and_fastpass,
    compute_dispatch_throughput,
    resolve_safety_restraint_code,
)


@settings(max_examples=150)
@given(st.text() | st.none())
def test_validate_height_and_fastpass_no_crash(s):
    try:
        result = validate_height_and_fastpass(s)
        assert isinstance(result, str)
    except Exception as exc:
        raise AssertionError(f"Height/FastPass crashed for {s!r}: {exc}") from exc


@settings(max_examples=150)
@given(st.text() | st.none())
def test_compute_dispatch_throughput_safe(s):
    try:
        result = compute_dispatch_throughput(s)
        assert result is None or (isinstance(result, float) and math.isfinite(result))
    except Exception as exc:
        raise AssertionError(f"Throughput crashed for {s!r}: {exc}") from exc


@settings(max_examples=150)
@given(st.text() | st.none())
def test_resolve_safety_restraint_code_safe(s):
    try:
        result = resolve_safety_restraint_code(s)
        assert isinstance(result, str)
    except Exception as exc:
        raise AssertionError(f"Restraint lookup crashed for {s!r}: {exc}") from exc


@given(st.integers(min_value=0, max_value=300), st.booleans())
def test_height_threshold_and_fastpass(height, has_fastpass):
    result = validate_height_and_fastpass(f"{height}:{'YES' if has_fastpass else 'NO'}")
    assert ("Approved" in result) == (height >= 120)
    assert ("FastPass Priority" in result) == has_fastpass


@given(st.integers(min_value=0, max_value=100000),
       st.integers(min_value=1, max_value=10000))
def test_throughput_matches_valid_calculation(riders, minutes):
    assert compute_dispatch_throughput(f"{riders}/{minutes}") == round(riders / minutes, 2)


@given(st.sampled_from(["CST", "WTR", "DRP", "WHL"]), st.text())
def test_known_restraint_prefix(prefix, suffix):
    expected = {
        "CST": "Over-the-Shoulder Harness",
        "WTR": "Lap Bar and Seatbelt",
        "DRP": "Hydraulic Shoulder Vest",
        "WHL": "Manual Safety Bar",
    }
    assert resolve_safety_restraint_code(prefix + suffix) == expected[prefix]


def test_invalid_boundaries():
    assert "Invalid" in validate_height_and_fastpass("-1:YES")
    assert "Invalid" in validate_height_and_fastpass("301:YES")
    assert compute_dispatch_throughput("48/0") is None
    assert compute_dispatch_throughput("nan/2") is None
    assert compute_dispatch_throughput("inf/2") is None
    assert resolve_safety_restraint_code("XYZ") == "Unknown restraint code"
