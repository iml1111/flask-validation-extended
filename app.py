from flask import Flask
from flask_validation_extended import Validator
from flask_validation_extended.params import  Route, Json, Query, Header
from flask_validation_extended.types import List, Dict, All
app = Flask(__name__)


@app.route("/update/<int:id>", methods=["POST"])
@Validator()
def hello(
        id = Route(),
        username = Json(),
        age = Json(),
        nicknames = Json(),
        password = Json(),
        is_admin = Query(),
        Accept = Header()
     ):

    print()

    return locals()


if __name__ == "__main__":
    app.run(debug=True)