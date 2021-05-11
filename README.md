# Flask-Validate-Extended  ![Python versions](https://img.shields.io/badge/Python-3.6<=@-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Release](https://img.shields.io/badge/release-0.1.5-red)

플라스크로 들어오는 모든 파라미터를 쉽게 검증하세요!

Header, Route, Query, Form, Json, File 등 입력될 수 있는 모든 파라미터에 대하여 validation 기능을 제공합니다.



## Install

**Pip**: `pip install flask_validation_extended` (아직 준비중 입니다!)

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
id: URI 파라미터에 수집하며, int여야 한다.
username: Body-Json에서 수집하며, str이여야 하고, 최소 길이가 5보다 커야 한다.
age: Body-Json에서 수집하며, int여야 하고, 16 ~ 98 사이여야 한다
nicknames: Body-Json에서 수집하며, str으로 구성된 list여야 한다.
birthday: Body-Json에서 수집하며, str이여야 하고, ISO Datetime format이여야 한다.
expire: Body-Json에서 수집하며, int여야 하지만, 반드시 입력받지 않아도 된다.(Optional)
is_admin: Query에서 수집하며, bool이여야 하며, 입력되지 않을 경우, false로 취급한다.
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

1. 적용하고자 하는 flask route 함수에 대하여 Validator() 데코레이터를 등록합니다.
2. 각 argument에 대하여 어느 영역에서 해당 값을 조회하고 검증할 것인지를 Param 객체를 선언하여 등록합니다. 

```python
parameter_name = Param(parameter_type, default, rules, optional)
# parameter_name : 해당 파라미터의 이름
# Param: 어느 영역에서 파라미터를 조회할 것인가 (헤더, 라우트(URI), 쿼리, 폼, Json, 파일)
# parameter_type: 해당 파라미터의 타입 (단일 or 복수 리스트)
# default: 값이 오지 않을 경우의 기본 값 설정
# rules: 해당 파라미터에 대한 검증 로직 (단일 or 복수 리스트)
# optional: 해당 파라미터 필수 여부 설정 (True or False)

'''
해당 usage는 어떤 Param을 사용하느냐에 따라 조금씩 다를 수 있습니다.
자세한 사항은 아래의 Documentation을 참고해주세요.
'''
```

3. 각각의 파라미터에 대하여 다음과 같은 과정을 수행합니다.
   - 지정된 영역에서 해당 이름의 파라미터가 존재하는지 확인.
   - 해당 파라미터가 존재하지 않을 경우, default 값 및 optional 여부를 확인.
   - 해당 파라미터가 지정된 파라미터 타입과 일치하는지 검증.
   - 입력된 룰에 대하여 해당 파라미터가 모두 충족하는지 확인.
   - 해당 파라미터를 route 함수 시작시의 argument로 반환.



## Documentation

- [**Param**](https://github.com/iml1111/flask-validation-extended/blob/main/docs/param.md) 

  인풋 파라미터 수집시, 어떤 영역에 대한 수집을 지원하는지 확인하려면 여기를 클릭하세요.

- [**Parameter Type**](https://github.com/iml1111/flask-validation-extended/blob/main/docs/parameter_type.md)
  
  파라미터 타입 검증시, 어떤 타입의 형태를 지원하는지 확인하려면 여기를 클릭하세요.

- [**Rules**](https://github.com/iml1111/flask-validation-extended/blob/main/docs/rules.md)
  
  파라미터 검증시, 기본적으로 어떠한 Rule을 지원하는지, 또한 커스텀 룰을 등록하는 방법 등을 확인하려면 여기를 클릭하세요.

- [**Custom Error Function**](https://github.com/iml1111/flask-validation-extended/blob/main/docs/custom_error_function.md)
  
  검증 실패시, 커스텀 에러 함수를 정의하려면 여기를 클릭하세요.



# References

https://github.com/d-ganchar/flask_request_validator

https://github.com/Ge0rg3/Flask-Parameter-Validation

