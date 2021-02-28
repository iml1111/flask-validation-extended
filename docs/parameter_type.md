# Parameter Type Documentation

Flask-Validate-Extended는 다음과 같은 타입을 지원합니다.

**빌트인 타입**

- **int** (빌트인정수)
- **str** (빌트인 문자열)
- **float** (빌트인 실수)
- **bool** (빌트인 불리언)
- **list** (빌트인 리스트)
- **dict** (빌트인 딕셔너리)

**커스텀 타입**

- **List** (커스텀 타입 리스트)
- **Dict** (커스텀 타입 딕셔너리)
- **FileObj** (커스텀 타입 파일 객체)
- **All** (커스텀 타입 - 모든 타입을 허용)



기본적으로 다음과 같이 사용해볼 수 있습니다.

```python
Json(int) # 인풋이 int이여야 한다
Json(str) # 인풋이 str이여야 한다
Json(float) # 인풋이 float이여야 한다
Json(bool) # 인풋이 bool이여야 한다
```



### [All] parameter

All 파라미터는 라이브러리 내의 자체 클래스로, 모든 타입을 수용하겠다는 것을 의미합니다. 기본적으로 각 Param의 annotation 인자에 default로 지정되어 있으며,  필요시 import 하여 사용할 수 있습니다.

아래의 코드는 모두 같은 의미를 가집니다.

```python
from flask_validation_extended.types import All

Route()
Route(All)
Route([All])
```



### Multiple Types

복수의 파라미터를 리스트의 형태로 묶어서 인자로 넘길 수 있습니다. 

**이 경우, 해당 리스트 내에 타입과 하나라도 매칭이 된다면 검증이 된걸로 판단**합니다.

```python
Param([int, str, bool]) # int, str, bool 중, 어느 것이 오더라도 상관없다.
```



### Complex data type (and Custom Type)

복합 자료형에 대한 데이터 타입의 경우, 기본적으로 **Json** Param에 한하여 지원합니다.

단순히 해당 데이터가 list, dict여야 한다는 타입을 선언할 경우, 아래와 같이 작성할 수 있습니다.

```python
Json(list) # 인풋이 리스트 형태여야 한다.
Json(dict) # 인풋이 dict(like json) 형태여야 한다.
```



여기서 한발 더 나아가, 해당 자료형 내의 세부 데이터에 대한 검증을 추가로 하고 싶다면, 본 라이브러리에 지원하는 커스텀 클래스를 조합하여 사용할 수 있습니다. 사용방법은 아래와 같습니다.

```python
from flask_validation_extended.types import All, List, Dict

# 인풋이 list이기만 하면 상관없다.
# Json(list)와 완전히 동일한 의미입니다.
Json(List())
Json(List(All))

# 인풋이 dict이기만 하면 상관없다.
# Json(dict)와 완전히 동일한 의미입니다.
Json(Dict())
Json(Dict(All))

# str으로 이루어진 list여야 한다.
Json(List(str))
# str or int로 이루어진 list여야 한다.
Json(List([str, int]))

# int로 이루어진 이중 리스트여야 한다.
#Example: [[1,2,3],
#          [2,3,4]]
Json(List(List(int)))

# int 혹은 int-list로 이루어진 list여야 한다.
# Example: [1, [1,2,3], 2, [5,6,7]]
Json(List([int, List(int)]))

# value가 str로 이루어진 Dict로 이루어진 list여야 한다. 
# Example: [{"name":"IML"}, {"name":"HS"}]
Json(List(Dict(str)))
```

커스텀 클래스 **Dict**에 대하여도 사용방법은 완전히 동일하나, **Dict() 클래스의 경우, key/value 중 value에 대해서만 검증을 수행**합니다. key의 경우, 반드시 string인걸로 판단하여 검증을 하지 않습니다.