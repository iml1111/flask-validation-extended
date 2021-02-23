from flask import Flask, request
from flask_validation_extended import Validator
from flask_validation_extended.params import  Route, Json, Query, Header, File
from flask_validation_extended.types import List, Dict, All, FileObj
from flask_validation_extended.rules import MinLen, Min, In, ValidationRule, Max, Email, Number, Strip, Ext
app = Flask(__name__)


class CustomRule(ValidationRule):

    @property
    def types(self):
        return int

    def invalid_str(self):
        return "HI, TEST ERROR!"

    def is_valid(self, data) -> bool:
        return True


@app.route("/update/<int:id>", methods=["POST"])
@Validator()
def hello(
        id = Route(optional=True),
        username = Json(rules=In([1,2,3]) , optional=True),
        age = Json(str, rules=Strip() , optional=True),
        nicknames = Json(optional=True),
        password = Json(str, optional=True),
        is_admin = Query(int, default=1, optional=True),
        accept_header = Header('Accept', optional=True),
        test_file = File(rules=Ext('ipynb')),
        test_file2 = File(optional=True)
     ):

    return {
        "id": id,
        "username": username,
        "age": age,
        "nicknames": nicknames,
        "password": password,
        "is_admin": is_admin,
        "accept_header": accept_header,
        "test_file": bool(test_file),
        "test_file2": bool(test_file2)
    }


if __name__ == "__main__":
    app.run(debug=True)

    from werkzeug import FileWrapper