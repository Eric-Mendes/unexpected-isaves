# Tests
Folder structure:
1. For each module inside `src/unexpected_isaves/`, create a folder inside `tests/`.
2. Each folder inside `tests/` should have 3 folders: `benchmarks/`, `integration_tests/`, `unit_tests/` and `fixtures/` if necessary.

## Running the tests
### Unit tests
```bash
python3 -m unittest discover tests/<module>/unit_tests/
```