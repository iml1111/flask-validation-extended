# Advanced Usage

```
This document covers more advanced features.
```

<br>

## Invalidate Validaiton

Sometimes, you may want to temporarily invalidate the validator even if it's a Route function with a validator attached.

If so, you can use the function below.

```python
from flask_validation_extended import invalidate

...
invalidate()
...
```

After the corresponding function is executed, all processing on the validator is not executed in the corresponding context. (**It is only valid in the context in which it is invalidated**)

Usually you will be able to use it in these cases.

- In middleware such as flask's `before_request` function, when disabling the validator under certain conditions
- Or this can be useful when calling another route function from a specific route function.

Like this:

```python
@api.route('/dry/path')
@Validator(bad_request)
def dry_api(
    type=Route(str, rules=In(ALLOWED_TYPES)),
    size=Route(str, rules=In(ALLOWED_SIZES)),
    filename=Route(str),
    dry=Query(bool, default=False),
):
	...

@api.route('/some/path')
@Validator(bad_request)
def some_api(
    path=Route(str, rules=Regex("\.")),
    dry=Query(bool, default=False),
):
    ...
    if dry is True:
        invalidate()
        return dry_api( # Another Route function call
            type=type, size=size,
            filename=path.replace(target, ""),
            dry=dry
        )
    ...
```

