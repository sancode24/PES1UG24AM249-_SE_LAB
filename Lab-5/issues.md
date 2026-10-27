# Lab 5 – Static Code Analysis: Issue Identification

**Student:** Sanjana M Kulkarni  
**SRN:** PES1UG24AM249  
**Project:** Scholarship Eligibility Screener  
**Tools:** Pylint, Bandit, Flake8

## Objective

To identify and correct security vulnerabilities, programming errors, and style violations in the scholarship eligibility screening program using static code analysis.

## Identified Issues and Fixes

| Issue | Type | Original Location | Description | Fix Applied |
|---|---|---|---|---|
| Unsafe `eval()` | Security | `calculate_merit_score()` | Executed a formula string as Python code, creating a code execution risk. | Replaced `eval()` with direct arithmetic. |
| Mutable default argument | Bug | `evaluate_applicant()` | `logs=[]` could share state across function calls. | Replaced with `logs=None` and initialized a new list inside the function. |
| Bare exception handler | Reliability | `load_results()` | `except:` suppressed all exceptions, including unexpected failures. | Used specific exception types and reported errors. |
| Unclosed file resources | Reliability | `persist_results()`, `load_results()` | Files were opened without context managers. | Used `with open(...)` to ensure proper closure. |
| Unused imports | Code quality | Import section | `math` and `sys` were imported but never used. | Removed unnecessary imports. |
| Missing input validation | Logic/security | `evaluate_applicant()` | Invalid GPA, negative credits, and negative income were accepted. | Added range checks and appropriate exceptions. |
| Nonstandard function naming | Style | `printShortlist()` | Function name did not follow PEP 8 snake_case conventions. | Renamed it to `print_shortlist()`. |
| Formatting violations | Style | Multiple locations | Inconsistent blank lines and spacing reduced readability. | Applied consistent PEP 8 formatting. |
| Equality comparison with `True` | Style | `printShortlist()` | Used unnecessary `== True` comparison. | Replaced with a direct Boolean condition. |

## Summary

The updated program improves security by eliminating arbitrary code execution, improves reliability through input validation and safer file handling, and improves maintainability through clearer naming and consistent formatting.

## Verification

The issues above were identified through source-code inspection. Actual Pylint, Bandit, and Flake8 findings and final scores must be confirmed using the generated analysis reports.
