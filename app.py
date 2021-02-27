from flask import Flask, request
from flask_validation_extended import Validator
from flask_validation_extended.params import  Route, Json, Query, Header, File, Form
from flask_validation_extended.types import List, Dict, All, FileObj
from flask_validation_extended.rules import MinLen, Min, In, ValidationRule, Max, Email, Number, Strip, Ext, MaxLen, Regex, PhoneNum, MaxFileCount
app = Flask(__name__)


class CustomRule(ValidationRule):

    def invalid_str(self):
        return "must in 1 ~ 100"

    def is_valid(self, data) -> bool:
        for d in data:
            if not (1 <= d <= 10):
                return False
        return True


def c_error(error_message):
    return {"error!!!!": error_message,
            "code":113}, 400

@app.route("/update", methods=["POST"])
@Validator(c_error)
def hello(
        select = Form([str, list])
     ):

    return locals()

@app.route('/file', methods=["POST"])
@Validator()
def hello2(
    test_file=File(rules=[
        Ext('jpeg'), MaxFileCount(5)]),
    test_file2=File(optional=True)
):
    print(test_file)
    print(test_file2)
    return "GOOD!"


if __name__ == "__main__":
    app.run(debug=True)