# Lab 5: Static Code Analysis — Reflection

## Q1. What is static code analysis?

Static code analysis examines source code without executing the program. It helps identify potential bugs, security vulnerabilities, and code quality problems.

## Q2. What is the difference between Pylint, Bandit, and Flake8?

Pylint checks code quality and potential programming errors. Bandit identifies common Python security vulnerabilities. Flake8 checks Python formatting and compliance with style guidelines.

## Q3. Which issue was most important to fix, and why?

The unsafe use of `eval()` was particularly important because it could execute arbitrary Python expressions. Replacing it with input validation and explicit arithmetic operations reduces this security risk.

## Q4. How did static analysis improve the program?

Static analysis helped identify security vulnerabilities, mutable default arguments, exception-handling problems, unused imports, and formatting issues. Fixing them improved code readability, maintainability, and security.
