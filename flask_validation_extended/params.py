from dataclasses import dataclass
from typing import Any
from .types import All

@dataclass
class Parameter:
    annotation: Any = All
    default: Any = None
    rules: list = None
    optional: bool = False

class Header(Parameter):
    pass

class Route(Parameter):
    pass

class Query(Parameter):
    pass

class Json(Parameter):
    pass

class Form(Parameter):
    pass

class File(Parameter):
    pass
