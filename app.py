from flask import Flask
from flask_validation_extended import Validator
from flask_validation_extended.params import  Route, Json, Query, Header
from flask_validation_extended.types import List, Dict, All
from flask_validation_extended.rules import MinLen, Min, In, ValidationRule
app = Flask(__name__)


class CustomRule(ValidationRule):

    def invalid_str(self):
        return "HI, TEST ERROR!"

    def is_valid(self, data) -> bool:
        return False


@app.route("/update/<int:id>", methods=["POST"])
@Validator()
def hello(
        id = Route(),
        username = Json(int, rules=CustomRule()),
        age = Json(),
        nicknames = Json(),
        password = Json(),
        is_admin = Query(int, default=1, optional=True),
        Accept = Header()
     ):
    return locals()


if __name__ == "__main__":
    app.run(debug=True)