## About

Here are all the tests regarding Python and Flask code.

## Naming

All files should be named `test_<tested module>.py`

## Requirements

Tests should have:
- `setUpClass()` -> executed before the first test
- `tearDownClass() ` -> executed after the last test
- `setUp()` -> executed before each test
- `tearDown()` -> executed after each test

Tests start with empty database, so the database should be cleared after the tests are executed.

## Running

[Nose 2](https://docs.nose2.io/en/latest/) is the framework used for testing the back-end part of the project.

In `/odyssey` directory:
- `nose2` -> executes all files starting with `test_` in the current directory and all subdirectories
- `nose2 tests.test_<tested module>` -> executes all tests in `./tests/test_<tested module>`
- Adding `-v` flag to both of the previous commands will provide more information about the tests.

## Coverage

Test coverage can be checked with the [Coverage](https://docs.nose2.io/en/latest/plugins/coverage.html) plugin of Nose 2.

How to use:
```
$ coverage run ./tests/test_<tested module>.py
$ coverage report ./flask_<tested module>/*.py
```

Example:
```
$ coverage run ./tests/test_authentication.py
$ coverage report ./flask_authentication/*.py 
|					Name					| Stmts | Miss | Cover |
|-------------------------------------------|-------|------|-------|
|  ./flask_authentication/authentication.py |   44  |   0  |  100% |
```

You can add `-m` flag to `$ coverage report` so that you can see which lines are not tested.

## Reference

For more information and tips you can check out [this link](https://www.patricksoftwareblog.com/unit-testing-a-flask-application/).