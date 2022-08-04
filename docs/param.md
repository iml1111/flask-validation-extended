# Param Documentation

Flask-Validation-Extended supports the following input parameters:

- **Route**: This is the Path parameter supported by Flask., `/users/<int:id>`

- **Query:** It is a `GET` parameter that is entered in the URI.. `/users?id=1235`
- **Form**:  It is an input parameter to be entered in the form.
- **Json**: This is the input parameter entered in the Json Body in the request.
- **Header:** Input parameters entered in the header in the request.
- **File:** This is an input parameter entered as a File type in the Form.

<br>

## Manually Usage

By default, **Route, Query, Form, Json, Param** can be used like this:

```python
parameter_name = Param(annotation, default, rules, optional)
# parameter_name : the name of the parameter
# Param: In which area to search for parameters (Header, Route(URI), Query, Form, Json, File)
# parameter_type: the type of the parameter (single or multiple list)
# default: Set default value when no value is provided
# rules: Additional validation logic for that parameter (single or multiple list)
# optional: Set whether the corresponding parameter is required (True or False)
```

In the case of **Header**, since the standard Header Key value is fixed, the name of the header to be collected must be input separately.

```python
parameter_name = Header(header_name, *args, **kwargs)
# header_name: the name of the header to collect (str)
# The following argument inherits the above args as it is.
```

In case of **File**, annotation and default cannot be input. So, how to use it is as follows.

```python
parameter_name = File(rules, optional)
```

<br>

## annotation (aka parameter_type)

**[default: All]**

After collecting the input from Param through the parameter type, the type of the corresponding value is verified.  

If the corresponding argument is not input, it is judged to be irrelevant no matter what type it comes in.  

Basically, you can use it like this:

```python
Json(str) # input must be str
Json(list) # The input must be a list.
Json(dict) # The input must be a dict (like json).
```

<br>

### Multiple Types

Multiple parameters can be grouped in the form of a list and passed as an argument. 

**In this case, if at least one of the types in the list matches, it is judged as verified**.

```python
Param([int, str, bool]) # It doesn't matter which one of int, str, or bool comes.
```

<br>

### Types by parameter

The types that can be specified are limited according to each Param.

- **Route, Query, Form, Header** supports `int, float, str, bool` as inputs.

- **Json** supports `int, float, str, bool, list, dict`. Furthermore, for complex data types (`list`, `dict`) including multiple data types, type verification for each internal value is possible.
- **File** is a special type of data that only accepts `FileObj`. This cannot be modified at the user level.

<br>

### Input Convert

Since HTTP communication basically recognizes as a string no matter what value is sent to **Header, Query, Form**, etc., it was necessary to additionally change the type in the logic.

In the case of **flask_validation_extended**, if the corresponding input is `str`, but the input annotation is **`int`, `float`, or `bool`**, data conversion to the corresponding type is attempted.

- **If the type conversion is successful**, the logic is executed as it is.
- **If the type conversion fails,** a `400 BAD REQUEST` error is returned.

**(Caution) However, if multiple annotations are entered in the form of a list, ** **Performs data type conversion based on the first annotation among them.**

<br>

### Complex data type (and Custom Type)

In the case of data types for complex data types, only **Json** Param are supported by default.

If you simply declare a type that the corresponding data should be a `list` or `dict`, you can write it as follows.

```python
Json(list) or Json(dict)
```

If you want to go one step further and additionally verify detailed data within the data type,  You can use a combination of custom classes supported by this library.

For more detailed description of annotations, please refer to the **parameter type documentation**.

<br>

## default 

**[default=None]**

If no input is entered in the corresponding Param, it is the default value that is replaced by default. 

**When entering the default value, it must match the specification of the annotation passed along with it.**

<br>

## rules

**[default=None]**

It is an argument that specifies the logic to be verified for the corresponding input parameter.  

If you don't want to specify a rule, basically you don't need to pass any arguments.  All of the codes below mean the same behavior.

```python
Param()
Param(rules=None)
Param(rules=[])
```



 If you want to specify a rule, you can use it as follows.  

The rule registered in the rules argument must be an object that inherits the **ValidationRule class that supports **`flask_validation_extended`.  

How to use is as follows.

```python
from flask_validation_extended.params import Json
from flask_validation_extended.rules import Min, Max, MinLen

# Apply a single rule
# username: Gathered from Body-Json, must be str, and min length must be greater than 5.
username=Json(str, rules=MinLen(5))

# Apply multiple rules (all rules must be satisfied)
# age: collected from Body-Json, must be an int, and must be between 16 and 98
age=Json(int, rules=[Min(18), Max(99)])
```

There are various rules created by default.

 Also, for rules, you can directly **implement custom rules**. Please refer to **Rule Documentation** for more information.

<br>

## optional

**[default=False]**

Determines whether the input parameter is required or not. 

If `True`, if the corresponding input is not input, it will be replaced with the default value or returned as None.

```python
expire=Json(int, optional=True)
```

