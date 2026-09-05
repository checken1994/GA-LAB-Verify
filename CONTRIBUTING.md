# Contributing

1. Create a focused branch.
2. Add or update tests for behavior changes.
3. Do not weaken mandatory tests with skip/xfail/placeholder assertions.
4. Run `python -m unittest discover -s tests -v`.
5. Run `ga-lab verify --repo .` on a clean checkout.
6. Open a pull request with scope, risks and verification notes.
