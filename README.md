# Flask-Validation-Extended  ![Python versions](https://img.shields.io/pypi/pyversions/flask-validation-extended) ![License](https://img.shields.io/badge/license-MIT-green) ![Release](https://img.shields.io/pypi/v/flask-validation-extended)

Easily validate all parameters coming into your flask!

 Provides validation function for all parameters that can be input such as `Header`, `Route`, `Query`, `Form`, `Json`, and `File`.

## Install

**Pip**: `pip install flask-validation-extended`

**Direct:**

- `git clone https://github.com/iml1111/flask-validation-extended`
- `python setup.py install`



## Get Started

```python
from flask import Flask
from flask_validation_extended import Validator
from flask_validation_extended.params import Route, Json, Query
from flask_validation_extended.types import List
from flask_validation_extended.rules import MinLen, Min, Max, IsoDatetime

app = Flask(__name__)

"""
id: Collected in the URI parameter, and must be int.
username: Collected from Body-Json, must be str, and minimum length greater than 5.
age: Collected from Body-Json, it must be an int, and must be between 16 and 98.
nicknames: Collected by Body-Json, it should be a list consisting of str.
birthday: Collected from Body-Json, must be str, and must be in ISO Datetime format.
expire: Collected from Body-Json, and it must be int, but it does not have to be input. (Optional)
is_admin: Collected from Query and must be bool. If it is not input, it is treated as false.
"""
@app.route("/update/<int:id>", methods=["POST"])
@Validator()
def hello(
        id=Route(int),
        username=Json(str, rules=MinLen(5)),
        age=Json(int, rules=[Min(18), Max(99)]),
        nicknames=Json(List(str)),
        birthday=Json(str, rules=IsoDatetime()),
        expire=Json(int, optional=True),
        is_admin=Query(bool, default=False)
     ):
    return "Update Complete! %s" % locals()


if __name__ == "__main__":
    app.run(debug=True)
```



## Simple Usage

1. Register the Validator() decorator for the flask route function you want to apply.
2.  For each argument, declare and register the Param object in which area to search and verify the value.

```python
parameter_name = Param(parameter_type, default, rules, optional)
# parameter_name : the name of the parameter
# Param: In which area to search for parameters (Header, Route(URI), Query, Form, Json, File)
# parameter_type: the type of the parameter (single or multiple list)
# default: Set default value when no value is provided
# rules: Additional validation logic for that parameter (single or multiple list)
# optional: Set whether the corresponding parameter is required (True or False)

'''
The usage may be slightly different depending on which Param is used.
Please refer to the Documentation below for details.
'''
```

3. For each parameter, proceed as follows.
   - Check if a parameter with that name exists in the specified area.
   -  If the parameter does not exist, check the default value and optional.
   - Verifies that the corresponding parameter matches the specified parameter type.
   -  Check whether all relevant parameters for the entered rule are satisfied.
   - The corresponding parameter is returned as an argument at the start of the route function.



## Documentation

- [**Param**](https://github.com/iml1111/flask-validation-extended/blob/main/docs/param.md) 

  When collecting input parameters, click here to see which areas support collection.

- [**Parameter Type**](https://github.com/iml1111/flask-validation-extended/blob/main/docs/parameter_type.md)
  
   Click here to check which types are supported when validating parameter types.

- [**Rules**](https://github.com/iml1111/flask-validation-extended/blob/main/docs/rules.md)
  
  When verifying parameters, click here to check which rules are supported by default and how to register custom rules.

- [**Custom Error Function**](https://github.com/iml1111/flask-validation-extended/blob/main/docs/custom_error_function.md)
  
  If validation fails, click here to define a custom error function.



# References

https://github.com/d-ganchar/flask_request_validator

https://github.com/Ge0rg3/Flask-Parameter-Validation

