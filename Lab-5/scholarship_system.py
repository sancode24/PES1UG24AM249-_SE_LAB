
"""Scholarship eligibility screening system."""

import json

INCOME_LIMIT = 800000
CUTOFF = 85
results = {}


def calculate_merit_score(gpa, credits):
    """Calculate the scholarship merit score."""
    return gpa * 10 + credits * 2


def evaluate_applicant(student_id, test_scores, logs=None):
    """Validate and evaluate a scholarship applicant."""
    if logs is None:
        logs = []

    try:
        gpa = float(test_scores["gpa"])
        credits = int(test_scores.get("credits", 0))
        income = float(test_scores.get("income", 0))
    except (KeyError, ValueError, TypeError) as error:
        raise ValueError("Invalid applicant information") from error

    if not 0 <= gpa <= 10:
        raise ValueError("GPA must be between 0 and 10")
    if credits < 0 or income < 0:
        raise ValueError("Credits and income cannot be negative")

    score = calculate_merit_score(gpa, credits)
    eligible = score >= CUTOFF and income < INCOME_LIMIT

    results[student_id] = {
        "score": score,
        "eligible": eligible,
    }
    logs.append(f"{student_id} scored {score}")
    return eligible


def change_formula(new_formula):
    """Allow only the approved merit formula."""
    if new_formula != "gpa * 10 + credits * 2":
        raise ValueError("Unsupported merit formula")


def persist_results(file="scholarships.json"):
    """Save results to a JSON file."""
    with open(file, "w", encoding="utf-8") as data_file:
        json.dump(results, data_file, indent=4)


def load_results(file="scholarships.json"):
    """Load results from a JSON file."""
    global results
    try:
        with open(file, "r", encoding="utf-8") as data_file:
            results = json.load(data_file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not load results: {error}")


def print_shortlist():
    """Display shortlisted scholarship applicants."""
    print("Shortlisted applicants:")
    for student_id, details in results.items():
        if details["eligible"]:
            print(f"  {student_id} score = {details['score']}")


def main():
    """Run the scholarship eligibility screening."""
    applicants = {
        "U001": {"gpa": 9.1, "credits": 4, "income": 450000},
        "U002": {"gpa": 7.2, "credits": 1, "income": 300000},
        "U003": {"gpa": 12.5, "credits": -3, "income": -1},
        "U004": {"gpa": 6.5},
        "U005": {"gpa": 8.4, "credits": 3, "income": 600000},
    }

    formula = input("Merit formula (Enter to keep default): ")
    if formula:
        try:
            change_formula(formula)
        except ValueError as error:
            print(error)

    for student_id, applicant in applicants.items():
        try:
            evaluate_applicant(student_id, applicant)
        except ValueError as error:
            print(f"Skipped {student_id}: {error}")

    persist_results()
    load_results()
    print_shortlist()


if __name__ == "__main__":
    main()
