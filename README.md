# Expense Classifier Back End (Datajam 2024)
This project is for Vancouver Datajam 2024.

## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
expense-classifier-be$ pip install -r tests/requirements.txt --user
# unit test
expense-classifier-be$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
expense-classifier-be$ AWS_SAM_STACK_NAME="expense-classifier-be" python -m pytest tests/integration -v
```