# Rule Documentation

You can perform validation of each parameter by registering a rule for validation of input parameters. Some rules are created by default, but you can also implement custom rules yourself. Also, when applying the rule, the annotation (parameter type) must be clear.

The basic usage is as follows.

```python
from flask_validation_extended.params import Json
from flask_validation_extended.rules import Min, Max, MinLen

# Apply a single rule
# username: Gathered from Body-Json, must be str, and min length must be greater than 5.
username=Json(str, rules=MinLen(5))

# Apply multiple rules (all rules must be satisfied)
# age: collected from Body-Json, must be an int, and must be between 18 and 99
age=Json(int, rules=[Min(18), Max(99)])
```

<br>

## annotation check 

When applying this rule, annotation (parameter type) must be clear.  

Before all rules are registered, for annotations passed together as arguments, **verify whether all annotations can apply the corresponding rule**.

If there is room for a value that cannot be verified, the rule cannot be applied. Therefore, when using a rule, it is recommended to define the annotation of the relevant Param as clearly as possible.

### example

For example, **Min(5) Rule** is a ruler class that verifies that the input data must be greater than 5. 

**Min** can only perform validation for int and float types. Therefore, it can be used only for Param declared as below.

```python
# Examples of correct rule usage
Json(int, rules=Min(5))
Json(float, rules=Min(5))
Json([int, float], rules=Min(5))
```

As shown below, if an annotation that has a possibility that validation is not possible is input, the corresponding rule cannot be used.

```python
# Examples of wrong rule usage
Json(str, rules=Min(5))
Json(list, rules=Min(5))
Json(All, rules=Min(5))
```

<br>

## Built-in Rules

`flask_validation_extended` basically supports the following rules. (Rules are constantly being added!)


- **MinLen(num: int)** This rule verifies the minimum length of the data length for `str`, `list`, and `dict` types.

- **MaxLen(num: int)**  This rule verifies the maximum length of the data for `str`, `list`, and `dict` types. 

- **Min(num: int, float)** This rule verifies the minimum value of the data for `int` and `float` types.
- **Max(num: int, float)**  This rule verifies the maximum value of the data for `int` and `float` types.
- **In(enum: list, tuple)** For all types, the corresponding data is among the values in the enum list. Verifies that there is a match.
- **Number()** For the `str` type, it verifies whether the corresponding string is a form that can be changed to int.
- **Strip()** For `str` type, verify that the corresponding string is a striped string (there are no left and right spaces).
- **IsoDatetime() **Verifies whether the string ISO Datetime format for the `str` type is present.
- **Datetime(df_format: str)** Verifies whether the entered datetime format for the `str` type matches.

- **Email()**  For the `str` type, it verifies whether the corresponding string is in the form of an email format.
- **PhoneNum()** For the `str` type, it verifies whether the corresponding string is in the form of a phone number format.
- **Regex(pattern: str) **For the `str` type, it verifies whether there is a matching part in the input pattern.
- **Ext(extenstions: str, List(str))** For `FileObj`, verify that the file name ends with one of the extensions entered.
- **MinFileCount(min_num: int**) For `FileObj`, verify the minimum number of the file list.
- **MaxFileCount(max_num: int)** Verifies the maximum number of the file list against `FileObj`.

<br>

## Custom Rule

`flask_validation_extended` has an additional extension function to implement the rules you want. 

In order to implement a custom rule, the `ValidationRule` class of `flask_validation_extended` must be inherited.

```python
from flask_validation_extended.rules import ValidationRule
```

The object is an abstract class and the method below (`is_valid`) must be implemented.

```python
class CustomRule(ValidationRule):

    def is_valid(self, data) -> bool:
        return True
```

The above custom rule is a method that unconditionally returns `True` without considering what data is input. The implemented custom rule can be applied as follows, just like the existing built-in rule.

```python
Route(int, rules=CustomRule())
```

<br>

### type_check

When applied to the corresponding rule, the type check function can be applied. When type check is activated, if data of annotation other than the specified type is passed, an error is returned when the application is executed.

For example, if you do not want the above CustomRule to be registered other than `str`, you can add the code as below.

```python
class CustomRule(ValidationRule):

    @property
    def types(self):
        return str # This rule can only use str

    def is_valid(self, data) -> bool:
        return True
```

Running the below returns an error like this:

```python
Route(int, rules=CustomRule())
"""
flask_validation_extended.exceptions.InvalidRuleAnnotation: 
Rule "CustomRule" is Invalid. This rule's Annotation must be in <class 'str'>,
"""
```

**It is not necessary to use the type check function, but if an input that cannot be validated is passed through the rule, it is recommended to use it because an internal error occurs.**

<br>

### custom error message

If the custom rule verification is not passed, the message below is basically returned to the client.

```
{
    "error": "Parameter <parameter>: doesn't not match the {CustomRule} rule"
}
```

You can customize these error messages by overriding the `invalid_str` method. How to use is as follows.

```python
class CustomRule(ValidationRule):

    @property
    def types(self):
        return All

    def invalid_str(self):
        return "It's Error !!!"

    def is_valid(self, data) -> bool:
        return False

'''
{
    "error": "Parameter <id>: It's Error !!!"
}
'''
```

<br>

## Custom Rule - Example

All built-in rules of `flask_validation_extended` are also implemented in compliance with the above conventions. For example, in the case of `Min() Rule`, it is implemented as follows.

```python
class Min(ValidationRule):

    def __init__(self, num):
        self._num = self._param_validate(num, (int, float))

    @property
    def types(self):
        return (int, float)

    def invalid_str(self):
        return f"must be larger than {self._num}."

    def is_valid(self, data) -> bool:
        return self._num < data
```



