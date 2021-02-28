# Rule Documentation

인풋 파라미터에 대한 검증을 위해 룰을 등록하여 각 파라미터의 validation을 수행할 수 있습니다.

룰은 기본적으로 만들어진 것들도 있지만 직접 커스텀 룰을 구현할 수도 있습니다.

또한 해당 룰을 적용시, annotation(parameter type)이 반드시 명확해야만 합니다.



기본 사용법은 아래와 같습니다.

```python
from flask_validation_extended.params import Json
from flask_validation_extended.rules import Min, Max, MinLen

# 단일 룰 적용
# username: Body-Json에서 수집하며, str이여야 하고, 최소 길이가 5보다 커야 한다.
username=Json(str, rules=MinLen(5))

# 복수 룰 적용 (지정된 모든 룰을 충족해야 함)
# age: Body-Json에서 수집하며, int여야 하고, 16 ~ 98 사이여야 한다
age=Json(int, rules=[Min(18), Max(99)])
```



## annotation check 

해당 룰을 적용시, annotation(parameter type)이 반드시 명확해야만 합니다.

모든 룰을 등록되기 전, 함께 인자로 넘어온 annotation에 대하여 

**모든 annotation이 해당 rule을 적용 가능한지를 검증**합니다.

만약 검증이 불가능한 값이 들어올 여지가 있을 경우, 해당 룰은 적용시킬 수 없습니다.

따라서 룰을 사용할 경우, 해당 Param의 annotation을 가능한한 명확히 정의하는 것을 권장합니다. 

### example

예를 들어, **Min(5) Rule**은 입력받은 데이터가 5보다 커야 한다는 것을 검증하는 룰러 클래스입니다.

**Min**은 int, float 타입에 대하여만 validation을 수행 가능합니다. 따라서 아래와 같이 선언된 Param에 대하여서만 사용할 수 있습니다.

```python
# 올바른 룰 사용 예제
Json(int, rules=Min(5))
Json(float, rules=Min(5))
Json([int, float], rules=Min(5))
```

아래와 같이 validation이 불가능한 여지가 있는 annotation이 입력될 경우, 해당 룰을 사용할 수 없습니다.

```python
# 잘못된 룰 사용 예제
Json(str, rules=Min(5))
Json(list, rules=Min(5))
Json(All, rules=Min(5))
```



## Built-in Rules

flask_validation_extended는 기본적으로 아래와 같은 룰을 지원합니다. (룰은 계속해서 추가중입니다!)


- **MinLen(num: int)** str, list, dict 타입에 대하여 해당 데이터의 길이의 최소 길이를 검증하는 룰입니다.

- **MaxLen(num: int)** str, list, dict 타입에 대하여 해당 데이터의 최대 길이를 검증하는 룰입니다.

- **Min(num: int, float)** int, float 타입에 대하여 해당 데이터의 최소값을 검증하는 룰입니다.
- **Max(num: int, float)** int, float 타입에 대하여 해당 데이터의 최대값을 검증하는 룰입니다.
- **In(enum: list, tuple)** 모든 타입에 대하여 해당 데이터가 enum 리스트 안에 있는 값 중 
  일치하는 것이 있는지 검증합니다.
- **Number()** str 타입에 대하여 해당 문자열이 int로 변경가능한 형태인지 검증합니다.
- **Strip()** str 타입에 대하여 해당 문자열이 Striped된 문자열인지(좌우 공백이 없는지) 검증합니다.
- **IsoDatetime()** str 타입에 대하여 해당 문자열 ISO Datetime format을 가지는지 검증합니다.
- **Datetime(df_format: str)** str 타입에 대하여 입력된 datetime format과 일치하는지 검증합니다.

- **Email()** str 타입에 대하여 해당 문자열이 이메일 포맷의 형태인지 검증합니다.
- **PhoneNum()** str 타입에 대하여 해당 문자열이 전화번호 포맷의 형태인지 검증합니다.
- **Regex(pattern: str)** str 타입에 대하여 입력된 pattern에 일치하는 부분이 있는지 검증합니다.
- **Ext(extenstions: str, List(str))** FileObj에 대하여 파일 이름이 입력된 extensions 중에 하나로 끝나는지 검증합니다.
- **MinFileCount(min_num: int**) FileObj에 대하여 해당 파일 리스트의 최소 갯수를 검증합니다.
- **MaxFileCount(max_num: int)**  FileObj에 대하여 해당 파일 리스트의 최대 갯수를 검증합니다.



## Custom Rule

**flask_validation_extended**는 추가적으로 자신이 원하는 룰을 구현하기 위한 확장 기능이 존재합니다.

커스텀룰을 구현하기 위해서는 flask_validation_extended의 ValidationRule 클래스를 상속받아야 합니다.

```python
from flask_validation_extended.rules import ValidationRule
```

해당 객체는 추상화 클래스로 반드시 아래의 메소드(is_valid)가 구현되어야 합니다.

```python
class CustomRule(ValidationRule):

    def is_valid(self, data) -> bool:
        return True
```

위 커스텀룰은 어떤 데이터가 입력되는지를 고려하지 않고 무조건 True를 반환하는 메소드입니다.

구현된 커스텀 룰은 기존의 built-in rule과 마찬가지로 아래와 같이 적용시킬 수 있습니다.

```python
Route(int, rules=CustomRule())
```



### type_check

해당 룰에 적용시, 타입  체크 기능을 적용시킬 수 있습니다. 타입 체크가 활성화되면, 지정된 타입 외의 annotation의 데이터가 넘어올 경우, 어플리케이션 실행시에 에러를 반환합니다.

예를 들어 위의 CustomRule이 str 이외에는 등록되길 원하지 않을 경우, 아래와 같이 코드를 추가해주면 됩니다.

```python
class CustomRule(ValidationRule):

    @property
    def types(self):
        return str # 해당 rule은 str만 사용할 수 있음

    def is_valid(self, data) -> bool:
        return True
```

똑같이 실행을 실행을 하면 아래와 같이 에러를 반환합니다.

```python
Route(int, rules=CustomRule())
"""
flask_validation_extended.exceptions.InvalidRuleAnnotation: 
Rule "CustomRule" is Invalid. This rule's Annotation must be in <class 'str'>,
"""
```

**타입 체크 기능은 반드시 사용하지 않아도 상관없으나, 만일 해당 rule로 validate가 불가능한 인풋이 넘어왔을 경우, 내부에서 에러가 발생하기 때문에 사용하기를 권장합니다.**



### custom error message

커스텀 룰의 검증을 통과하지 못했을 경우, 기본적으로 클라이언트에게는 아래와 같은 message가 반환됩니다.

```
{
    "error": "Parameter <parameter>: doesn't not match the {CustomRule} rule"
}
```

이러한 에러 메시지를 invalid_str 메소드를 오버라이딩하여 커스텀할 수 있습니다. 

사용 방법은 아래와 같습니다.

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



## Custom Rule - Example

flask_validation_extended의 모든 built-in Rule 또한 위의 규약에 준수하여 구현되어 있습니다.

예를 들어 Min() Rule의 경우, 아래와 같이 구현되어 있습니다.

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



