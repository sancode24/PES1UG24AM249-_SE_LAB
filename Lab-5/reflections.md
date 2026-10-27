# Lab 5 – Static Code Analysis: Reflection

**Name:** Sanjana M Kulkarni  
**SRN:** PES1UG24AM249  
**Project:** Scholarship Eligibility Screener

## 1. What did you learn from using static code analysis tools?

I learned that static code analysis helps identify potential bugs, security vulnerabilities, and coding style violations without executing the program. Pylint checks code quality, Bandit detects insecure coding practices, and Flake8 checks formatting and PEP 8 compliance. Using these tools helps developers write safer, cleaner, and more maintainable code.

## 2. Which issues were most important to fix, and why?

The most important issue was the use of `eval()` because it could execute arbitrary Python expressions, creating a security vulnerability. Other significant problems included mutable default arguments, broad exception handling, and missing input validation. These could cause unexpected behavior, hide errors, or allow invalid applicant information to be processed.

## 3. How did Pylint help improve the program?

Pylint helped identify code quality problems such as unused imports, naming inconsistencies, and mutable default arguments. Fixing these issues improved readability and reduced the risk of unintended behavior. Adding documentation and using clearer function names also made the code easier to understand and maintain.

## 4. How did Bandit help improve security?

Bandit focuses on detecting potentially insecure Python code. The original program used `eval()` to calculate scholarship merit scores. This was replaced with direct arithmetic, preventing arbitrary expression execution. The updated program also validates applicant data to reject invalid GPA, credits, and income values.

## 5. How did Flake8 improve the code?

Flake8 helped guide improvements to Python formatting and style. The updated code follows PEP 8 conventions, including consistent spacing, appropriate blank lines, and snake_case function names. These changes make the program easier to read and support collaboration and maintenance.

## 6. What challenges did you encounter?

One challenge was fixing issues without changing the intended scholarship eligibility logic. Another was understanding how different tools identify different categories of problems. Input validation also required careful handling so that invalid applicants could be rejected without stopping the entire screening process.

## 7. How does static analysis contribute to software quality?

Static analysis detects problems early in development, reducing debugging effort and improving security, reliability, and maintainability. However, static analysis alone cannot guarantee that a program is correct. It should be combined with execution, functional testing, and code review.

## Conclusion

This lab demonstrated the importance of using multiple static analysis tools. Pylint, Bandit, and Flake8 address complementary aspects of software quality. The scholarship screening program was improved by removing unsafe operations, validating inputs, improving exception handling, and applying consistent coding conventions.

**Note:** Final analyzer scores and before-and-after findings will be documented after running the three tools.
