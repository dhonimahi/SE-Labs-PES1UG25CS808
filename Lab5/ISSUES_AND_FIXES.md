# Lab 5: Static Code Analysis

## 1. Objective

To improve the quality, security, and formatting of the Retail Point-of-Sale (POS) Python program using Pylint, Bandit, and Flake8.

## 2. Tools Used

- **Pylint:** Detects code quality problems and programming practices that may cause bugs.
- **Bandit:** Detects common security vulnerabilities in Python code.
- **Flake8:** Checks Python formatting and compliance with PEP 8 style guidelines.

## 3. Issues Identified and Fixed

| Issue | Type | Original Problem | Fix Applied |
|---|---|---|---|
| Mutable default argument | Code quality | Using `receipts=[]` can share the same list between function calls. | Changed the default to `None` and initialized the list inside the function. |
| Weak random number generator | Security | `random.randint()` is not suitable when unpredictable values are needed. | Replaced it with `secrets.randbelow()`. |
| Unsafe `eval()` usage | Security | `eval()` can execute arbitrary Python expressions. | Replaced it with a regular-expression check and explicit arithmetic operations. |
| Bare exception | Code quality | A bare `except` can hide unexpected errors. | Removed the broad exception handling and validated products and quantities. |
| Broad exception handling | Code quality | Catching general exceptions can conceal programming errors. | Added explicit validation and handled expected promotion errors. |
| File handling | Code quality | Opening a file without a context manager can leave it open. | Used `with open(...)` and specified UTF-8 encoding. |
| Missing docstrings | Code quality | Functions and the module lacked documentation. | Added a module docstring and function docstrings. |
| Naming and unused imports | Code quality | Some names did not follow Python conventions, and imports were unused. | Used `print_sales()` and removed unused imports. |
| Formatting problems | Style | The original file had line-length, blank-line, and newline issues. | Corrected formatting and standardized line endings. |

**Note:** Original line numbers can be taken from `pylint_before.txt`, `bandit_before.txt`, and `flake8_before.txt`. Line numbers may change after the fixes.

## 4. Verification Results

| Tool | Before | After |
|---|---|---|
| Pylint | 5.65/10 | 10.00/10 |
| Bandit | Reported security findings | No issues identified |
| Flake8 | Reported formatting issues | No issues reported |

## 5. Reflection

### Q1. What is static code analysis?

Static code analysis examines source code without executing the program. It helps identify potential bugs, security vulnerabilities, code quality problems, and formatting issues before deployment.

### Q2. What is the difference between Pylint, Bandit, and Flake8?

Pylint checks code quality, programming practices, and potential errors. Bandit focuses on common Python security vulnerabilities. Flake8 checks formatting and compliance with Python style guidelines.

### Q3. Which issue was most important to fix, and why?

The unsafe use of `eval()` was particularly important because it could execute arbitrary Python expressions. Replacing it with validation and explicit arithmetic operations reduces this security risk.

### Q4. How did static analysis improve the program?

Static analysis helped identify unsafe operations, poor exception handling, mutable default arguments, unused imports, and formatting problems. Fixing these issues improved readability, maintainability, and security.

### Q5. What did you learn from this lab?

I learned how to use Pylint, Bandit, and Flake8 to identify different types of issues, fix the reported problems, and verify the improvements by running the tools again.

## 6. Conclusion

The Retail POS program was updated to address the identified security, code quality, and formatting issues. The final verification achieved a Pylint score of 10.00/10, no issues identified by Bandit, and no Flake8 findings.
