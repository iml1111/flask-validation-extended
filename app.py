from flask import Flask
from flask_validation_extended import Validator
from flask_validation_extended.params import  Route, Json, Query
from flask_validation_extended.types import List, Dict, All
app = Flask(__name__)


@app.route("/update/<int:id>", methods=["POST"])
@Validator()
def hello(
        id = Route(int),
        username = Json(All),
        age = Json(float),
        nicknames = Json(Dict(str, List((int, str))), ["asd", "zxc"]),
        password = Json(int, 5),
        is_admin = Query(str, "asdzxc", optional=True)
     ):
    return str([id, username, age, nicknames, password, is_admin])


if __name__ == "__main__":
    app.run(debug=True)