# Custom Error Function Documentation

`flask_validation_extended` returns an error to the client in the format below when the validation process fails.

```python
@staticmethod
    def default_error(error_message):
        return {"error": error_message}, 400
```

In the case of **error_message**, information about which point failed for each detailed process during validation is delivered as a string.



This can be overridden by implementing a Custom Error function. 

The custom error function is implemented as follows in a form that can receive the above error_message as an argument.

```python
def custom_error(error_message):
    return {
               "info": "In hello API",
               "error": error_message
           }, 400
```

After that, when registering the Validator decorator, register it as an argument of the corresponding class.

```python
@app.route("/update/<int:id>", methods=["POST"])
@Validator(custom_error) # Register custom error function
def hello(
...
    
"""
Example)
{
    "error": "Parameter <id>: It's Error !!!",
    "info": "In hello API"
}
"""
```









