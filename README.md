# Flask-Validate-Extended  ![Python versions](https://img.shields.io/badge/Python-3.6<=@-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Release](https://img.shields.io/badge/release-not_yet-red)

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
from flask_validation_extended.params import  Route, Json, Query
from flask_validation_extended.types import List
from flask_validation_extended.rules import MinLen, Min, Max, IsoDatetime

app = Flask(__name__)

"""
id: URI 파라미터에 수집하며, int여야 한다.
username: Body-Json에서 수집하며, strd이여야하고, 최소 길이가 5보다 커야 한다.
<작성중>
"""

@app.route("/update/<int:id>", methods=["POST"])
@Validator()
def hello(
        id=Route(int),
        username=Json(str, rules=MinLen(5)),
        age=Json(int, rules=[Min(18), Max(99)]),
        nicknames=Json(List(str)),
        birthday=Json(str, rules=IsoDatetime()),
        expire=Json(int, default=5),
        is_admin=Query(bool, default=False)
     ):
    return "Update Complete! %s" % locals()


if __name__ == "__main__":
    app.run(debug=True)
```



## Usage

1. 적용하고자 하는 flask route 함수에 대하여 Validator() 데코레이터를 등록합니다.
2. 각 argument에 대하여 어느 영역에서 해당 값을 조회하고 검증할 것인지를 Param 객체를 선언하여 등록합니다. 

```python
parameter_name = Param(parameter_type, default, rules, optional)
# parameter_name : 해당 파라미터의 이름
# Param: 어느 영역에서 파라미터를 조회할 것인가 (헤더, 라우트(URI), 쿼리, 폼, Json, 파일)
# parameter_type: 해당 파라미터의 타입
# default: 값이 오지 않을 경우의 기본 값 설정
# rules: 해당 파라미터에 대한 검증 로직 (단일 or 복수 리스트)
# optional: 해당 파라미터 필수 여부 설정
```





# References

https://github.com/d-ganchar/flask_request_validator

https://github.com/Ge0rg3/Flask-Parameter-Validation

