# Param Documentation



Flask-Validate-Extended는 다음과 같은 인풋 파라미터를 지원합니다.

- **Route**: Flask에서 지원하는 Path 파라미터입니다, `/users/<int:id>`

- **Query:** URI에 입력되는 GET 파라미터입니다. `/users?id=1235`
- **Form**: Form에 입력되는 인풋 파라미터입니다.
- **Json**: request에서 Json Body에 입력된 인풋 파라미터입니다.
- **Header:** request에서 헤더에 입력된 인풋 파라미터입니다.
- **File:** Form에서 File type으로 입력된 인풋 파라미터입니다.



## Manually Usage

기본적으로 **Route, Query, Form, Json** Param은 다음과 같이 사용할 수 있습니다.

```python
parameter_name = Param(annotation, default, rules, optional)
# parameter_name : 해당 파라미터의 이름
# Param: 어느 영역에서 파라미터를 조회할 것인가 (헤더, 라우트(URI), 쿼리, 폼, Json, 파일)
# annotation: 해당 파라미터의 타입 (단일 or 복수 리스트)
# default: 값이 오지 않을 경우의 기본 값 설정
# rules: 해당 파라미터에 대한 검증 로직 (단일 or 복수 리스트)
# optional: 해당 파라미터 필수 여부 설정 (True or False)
```

**Header**의 경우, 표준 Header Key 값이 고정되어 있는 특성상, 별도로 수집하고자 하는 header의 이름을 입력받아야 합니다.

```python
parameter_name = Header(header_name, *args, **kwargs)
# header_name: 수집하고자 하는 헤더의 이름 (str)
# 그 뒤의 인자는 그대로 위의 args를 그대로 상속받습니다.
```

**File**의 경우, annotation 및 default를 입력받을 수 없습니다. 따라서 사용방법은 다음과 같습니다.

```python
parameter_name = File(rules, optional)
```



## annotation (aka parameter_type)

**[default: All]**

파라미터 타입을 통해 Param에서 인풋을 수집한 후, 해당 값의 Type을 검증합니다. 

해당 인자가 입력되지 않을 경우, 어떤 타입이 오더라도 무관하다고 판단합니다.

기본적으로 아래와 같이 사용할 수 있습니다.

```python
Json(str) # 인풋이 str이여야 한다
Json(list) # 인풋이 리스트 형태여야 한다.
Json(dict) # 인풋이 dict(like json) 형태여야 한다.
```



### Multiple Types

복수의 파라미터를 리스트의 형태로 묶어서 인자로 넘길 수 있습니다. 

**이 경우, 해당 리스트 내에 타입과 하나라도 매칭이 된다면 검증이 된걸로 판단**합니다.

```python
Param([int, str, bool]) # int, str, bool 중, 어느 것이 오더라도 상관없다.
```



### Types by parameter

각각의 Param에 따라 지정할 수 있는 타입이 제한되어 있습니다.

- **Route, Query, Form, Header**로 들어올 수 있는 인풋으로는 `int, float, str, bool`을 지원합니다.

- **Json**은 `int, float, str, bool, list, dict`를 지원합니다. 거기에 나아가 복수의 데이터를 포함한 복합 자료형(list, dict)에 대하여 각 내부 값에 대한 타입 검증이 가능합니다. 
- **File**은 특수한 형태의 데이터로, 오직  `FileObj`만을 허용합니다. 이는 사용자단에서 수정할 수 없습니다.



### Input Convert

HTTP 통신은 기본적으로 **Header, Query, Form**등에 대하여 어떠한 값을 보내더라도 기본적으로 string으로 인식하기 때문에, 별도로 로직에서 타입을 변경시켜주어야 했습니다.

**flask_validation_extended**의 경우, 해당 인풋이 str이지만 입력된 annotation이 **int, float, bool**인 경우, 해당 타입으로의 데이터 변환을 시도합니다.

- **타입 변환에 성공한 경우,** 그대로 정상적으로 로직이 수행됩니다.
- **타입 변환에 실패한 경우,** 400 BAD REQUEST 에러를 반환합니다.

**(주의사항) 단, 복수의 annotation이 리스트의 형태로 입력된 경우, **
**그 중 가장 첫번째 annotation을 기준으로 데이터 타입 변환을 수행합니다.**



### Complex data type (and Custom Type)

복합 자료형에 대한 데이터 타입의 경우, 기본적으로 **Json** Param에 한하여 지원합니다.

단순히 해당 데이터가 list, dict여야 한다는 타입을 선언할 경우, 아래와 같이 작성할 수 있습니다.

```python
Json(list) # 인풋이 리스트 형태여야 한다.
Json(dict) # 인풋이 dict(like json) 형태여야 한다.
```

여기서 한발 더 나아가, 해당 자료형 내의 세부 데이터에 대한 검증을 추가로 하고 싶다면, 

본 라이브러리에 지원하는 커스텀 클래스를 조합하여 사용할 수 있습니다.

annotation에 관한 더 자세한 설명은 **parameter type documentation**을 참고해주세요.



## default 

**[default=None]**

해당 Param에 인풋이 입력되지 않은 경우, 기본적으로 대체하는 default 값입니다. 

**default 값을 입력시, 반드시 함께 넘어온 annotation의 규격과 일치해야 합니다.**



## rules

**[default=None]**

해당 인풋 파라미터에 대하여, 검증을 수행할 로직을 지정하는 인자입니다.



룰을 지정하고 싶지 않을 경우, 기본적으로 아무 인자도 넘기지 않으면 됩니다. 

기본적으로 아래의 코드는 모두 같은 동작을 의미합니다.

```python
Param()
Param(rules=None)
Param(rules=[])
```



룰을 지정하고 싶을 경우, 아래와 같이 사용할 수 있습니다. rules 인자에 등록되는 룰은 반드시 **flask_validation_extended**에 지원하는 **ValidationRule 클래스를 상속받은 객체**여야만 합니다.

사용방법은 아래와 같습니다.

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

기본적으로 만들어진 다양한 룰들이 존재합니다. 또한 rule의 경우, 직접 **커스텀 룰을 구현**할 수도 있습니다.  자세한 정보는 **Rule Documentation**을 참고해주세요.



## optional

**[default=False]**

해당 인풋 파라미터의 필수 입력 여부를 결정합니다. 

True인 경우, 해당 인풋이 입력되지 않으면 default 값으로 대체되거나 None으로 반환됩니다.

```python
expire=Json(int, optional=True)
```

