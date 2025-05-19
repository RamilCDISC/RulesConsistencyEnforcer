# RulesConsistencyEnforcer
Regression testing to ensure consistent CDISC Rules Engine reports before and after updates.

# Rule Regression Tests

This repository contains automatically generated regression tests to validate rule behavior using `core.py`. These tests ensure consistent results after any code updates or logic changes.

## Project Structure
````

├── rule\_regression\_tests/     # Generated pytest test scripts
├── published\_rules/            # Rule JSON files (organized by subfolder)
├── json\_datasets/              # Dataset JSONs and optional XML files (organized by subfolder)
└── README.md                    # This file

````

---

## Prerequisites

- Python 3.12 or later
- `pip` installed
- `core.py` from cdisc rules engine. You will need to have in your root directory the core.py file from rules engine or the executable of the cdisc rules engine



## Running the Regression Tests

Make sure you're in the root directory of the repository.

Then run:

```bash
python -m pytest rule_regression_tests/
```

Each test will:

1. Re-run `core.py validate` with the associated rule and dataset.
2. Generate a new Excel result.
3. Compare it with the previously captured expected result.
4. Raise an error if there's any difference in sheet names, columns, or data.

---


## Notes

* Timestamp columns are ignored during comparison.
* `NaN` values are treated as `None` for consistency.
* Make sure any new Excel files are removed or managed if you're regenerating to avoid picking up old outputs.

---

## Example Test Output

```bash
============================= test session starts =============================
collected 120 items

rule_regression_tests/test_rule_A.py .............                      [ 10%]
rule_regression_tests/test_rule_B.py .............                      [ 20%]
...

========================== 120 passed in 25.31s ==============================
```

---
