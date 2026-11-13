# Lab 7 - Fuzz Testing for Input Validation Bugs

**Student:** Sanjana M Kulkarni | **SRN:** PES1UG24AM249

Source: [Assigned amusement park ride access repository](https://github.com/SETAPESU26/L6_L7_11_amusement_park_ride_access/tree/main/Lab%207)

## Files

- `buggy_processor.py` - unchanged original starter for reproducing failures.
- `processor.py` - hardened implementation for the three ride-access functions.
- `test_processor.py` - 7 Hypothesis/pytest tests for crashes, valid values, and boundaries.
- `requirements.txt` - dependencies.

## Reproduce the buggy failure (before)

From this Lab7 directory:

```bash
python -m pip install -r requirements.txt
python buggy_processor.py
```

Enter an invalid rider spec such as `abc` to capture the original exception. For a failing pytest screenshot, temporarily run tests against buggy code **without modifying the submitted fixed implementation**:

```bash
cp processor.py processor_fixed_backup.py
cp buggy_processor.py processor.py
python -m pytest -v test_processor.py
```

Save the failing-test screenshot. Then restore:

```bash
cp processor_fixed_backup.py processor.py
rm processor_fixed_backup.py
```

On Windows PowerShell, replace `cp` with `Copy-Item` and `rm` with `Remove-Item`.

## Run the fixed implementation (after)

```bash
python processor.py
python -m pytest -v test_processor.py
```

Suggested input values for the fixed program: `140:YES`, `48/2.5`, `CST_01`.

## PDF screenshots required by handout

1. Original buggy `processor.py` run (from the preserved `buggy_processor.py`).
2. Failing Hypothesis tests against the buggy program.
3. Fixed `processor.py` successful run.
4. Passing Hypothesis tests against the fixed program.

Take genuine screenshots from the execution environment and combine them into a PDF. Do not present screenshots of unexecuted tests as test results.
