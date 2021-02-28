from flask import Flask
from flask_validation_extended import Validator
from flask_validation_extended.params import  Route, Json, Query
from flask_validation_extended.types import List, Dict, All
from flask_validation_extended.rules import MinLen, Min, Max, IsoDatetime, ValidationRule

app = Flask(__name__)

class CustomRule(ValidationRule):

    @property
    def types(self):
        return All

    def invalid_str(self):
        return "It's Error !!!"

    def is_valid(self, data) -> bool:
        return False


def custom_error(error_message):
    return {
               "info": "In hello API",
               "error": error_message
           }, 400


@app.route("/update/<int:id>", methods=["POST"])
@Validator(custom_error)
def hello(
        id=Route(int, rules=CustomRule()),
        username=Json(str, rules=MinLen(5)),
        age=Json(int, rules=Min(5.1)),
        nicknames=Json([str, int]),
        birthday=Json(str, rules=IsoDatetime()),
        expire=Json([str, float, int], default=5, rules=[]),
        is_admin=Query(bool, default=False)
     ):
    return "Update Complete! %s" % locals()


if __name__ == "__main__":
    app.run(debug=True)