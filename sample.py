from flask import Flask
from flask_validation_extended import Validator
from flask_validation_extended.params import  Route, Json, Query
from flask_validation_extended.types import List
from flask_validation_extended.rules import MinLen, Min, Max, IsoDatetime

app = Flask(__name__)


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