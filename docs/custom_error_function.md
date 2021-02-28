# Custom Error Function Documentation

flask_validation_extended는 Validate 과정에 실패할 경우, 아래와 같은 포맷의 형태로 클라이언트에게 에러를 리턴합니다.

```python
@staticmethod
    def default_error(error_message):
        return {"error": error_message}, 400
```

**error_message**의 경우, validation 중, 각 세부 과정에 대하여 어느 지점에 실패했는지에 대한 정보가 문자열로 전달됩니다. 



이를 Custom Error function을 구현하여 오버라이딩할 수 있습니다.

커스텀 에러 함수은 위의 error_message를 인자로 받을 수 있는 형태로 아래와 같이 구현합니다.

```python
def custom_error(error_message):
    return {
               "info": "In hello API",
               "error": error_message
           }, 400
```

그 후, Validator 데코레이터 등록시, 해당 클래스의 인자로 함께 등록하면 됩니다.

```python
@app.route("/update/<int:id>", methods=["POST"])
@Validator(custom_error) # 커스텀 에러 함수 등록
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









