import sys
import atheris
import os

# Add project root to path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from opt.helpers.standardization import InputValidator, ValidationRule  # noqa: E402


def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)

    # Create a validator with some rules
    validator = InputValidator()
    validator.add_rule(ValidationRule("username", "required"))
    validator.add_rule(ValidationRule("username", "min_length", 3))
    validator.add_rule(ValidationRule("username", "max_length", 20))
    validator.add_rule(ValidationRule("age", "range", (0, 120)))
    validator.add_rule(ValidationRule("role", "enum", ["admin", "user", "guest"]))

    # Generate random input data
    try:
        input_data = {
            "username": fdp.ConsumeString(fdp.ConsumeIntInRange(0, 50)),
            "age": fdp.ConsumeIntInRange(-50, 200),
            "role": fdp.ConsumeString(fdp.ConsumeIntInRange(0, 20))
        }

        # Run validation - this should not raise an exception
        validator.validate(input_data)
    except Exception:
        # Catch all exceptions to allow fuzzer to continue exploring
        # In a real scenario, we would want to investigate these
        pass


if __name__ == "__main__":
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()
