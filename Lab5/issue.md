# Lab 5: Static Code Analysis — Issues and Fixes

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Unsafe `eval()` | Security — Medium | 27 | Can execute arbitrary Python expressions. | Replaced with regular-expression validation and explicit arithmetic operations. |
| Weak random generator | Security — Low | 21 | `random.randint()` is not suitable for security-sensitive randomness. | Replaced with `secrets.randbelow()`. |
| Exception handling with `pass` | Code quality — Low | 33–34 | Can hide unexpected errors. | Removed the unnecessary exception block and validated inputs. |
| Mutable default argument | Code quality | 10 | A shared list can persist across function calls. | Changed `receipts=[]` to `receipts=None` and initialized the list inside the function. |
| Bare exception | Code quality | 16 | Can catch unexpected errors without identifying the cause. | Removed the bare exception and validated inputs. |
| Unsafe file handling | Code quality | 37 | File was opened without an explicit encoding or context manager. | Used `with open(...)` and UTF-8 encoding. |
| Missing docstrings | Code quality | Multiple | Module and functions lacked documentation. | Added docstrings. |
| Naming and unused imports | Code quality | Multiple | Names did not follow conventions and imports were unused. | Renamed `printSales()` to `print_sales()` and removed unused imports. |
| Formatting issues | Style | Multiple | Blank lines and line length did not follow style requirements. | Corrected formatting. |

*Line numbers refer to the original, unmodified program.*
