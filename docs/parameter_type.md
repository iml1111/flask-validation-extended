# Parameter Type Documentation

Flask-Validation-Extended supports the following types:

**built-in type**

- **int**
- **str**
- **float**
- **bool**
- **list** 
- **dict** 

**Custom Type**

- **List** 
- **Dict** 
- **FileObj** 
- **All** (Custom Types - accept any type)



Basically, you can try something like this:

```python
Json(int)
Json(str) 
Json(float) 
Json(bool)
```

<br>

### [All] parameter

The `All` parameter is its own class within the library, meaning that it accepts all types. Basically, it is set as default in the annotation parameter of each Param, and can be imported and used if necessary. All of the codes below have the same meaning.

```python
from flask_validation_extended.types import All

Route()
Route(All)
Route([All])
```

<br>

### Multiple Types

Multiple parameters can be grouped in the form of a list and passed as an argument.  

**In this case, if at least one of the types in the list matches, it is judged as verified**.

```python
Param([int, str, bool]) # It doesn't matter which one of int, str, or bool comes.
```

<br>

### Complex data type (and Custom Type)

In the case of data types for complex data types, only **Json** Param are supported by default. If you simply declare a type that the corresponding data should be a list or dict, you can write it as follows.

```python
Json(list) # The input must be a list.
Json(dict) # The input must be a dict (like json).
```

If you want to go one step further and additionally verify detailed data within the data type, you can use a combination of custom classes supported by this library. How to use is as follows.

```python
from flask_validation_extended.types import All, List, Dict

# It doesn't matter as long as the input is a list.
# It has the exact same meaning as Json(list).
Json(List())
Json(List(All))

# It doesn't matter as long as the input is a dict.
# It has the exact same meaning as Json(dict).
Json(Dict())
Json(Dict(All))

# It must be a list of str.
Json(List(str))
# It must be a list of str or int.
Json(List([str, int]))

# It must be a double list of ints.
#Example: [[1,2,3],
#          [2,3,4]]
Json(List(List(int)))

# It must be a list of ints or int-lists.
# Example: [1, [1,2,3], 2, [5,6,7]]
Json(List([int, List(int)]))

# value must be a list of Dicts consisting of str.
# Example: [{"name":"IML"}, {"name":"HS"}]
Json(List(Dict(str)))
```

The usage method is exactly the same for the custom class **Dict**, but in the case of the **Dict() class, only the value among key/value is verified**. In the case of a key, it is determined that it is a string and is not verified.