# TODO: Header 클래스 추가하기
import typing
from inspect import signature
from functools import wraps
from flask import request
from .params import Route, Query, Json, Form, File
from .types import List, Dict, All


# Main validation class
class Validator:

    @staticmethod
    def default_error(error_message):
        return {"error": error_message}, 400

    def __init__(self, error_function=None):
        self.error_func = error_function if error_function else self.default_error

    def __call__(self, f):
        @wraps(f)
        def nested_func(**kwargs):
            # 모든 리퀘스트 인자 값 호출
            request_inputs = {
                Route: kwargs.copy(),
                Json: request.json or {},
                Query: request.args.to_dict(),
                Form: request.form.to_dict(),
                File: request.files.to_dict()
            }
            parsed_inputs = self.validate_parameters(
                request_inputs, signature(f).parameters
            )
            if isinstance(parsed_inputs, dict):
                return f(**parsed_inputs)
            else:
                return parsed_inputs
        return nested_func

    def validate_parameters(self, request_inputs, function_args):
        parsed_inputs = {}
        for arg in function_args.values():
            param_name = arg.name  # ie. id, username
            param_object = arg.default  # ie. Route(), Json()
            param_annotation = param_object.annotation  # ie. str, int
            param_object_name = param_object.__class__.__name__
            is_optional = param_object.optional

            # 지정된 Param 클래스가 아닌 경우, 에러 반환
            if param_object.__class__ not in request_inputs.keys():
                return self.error_func("Invalid parameter type.")
            user_input = request_inputs[param_object.__class__].get(param_name)

            # 사용자의 정보가 입력되지 않았으나, default가 명시된 경우, 할당
            if user_input is None and param_object.default is not None:
                user_input = param_object.default

            # 사용자의 인풋 및 default가 모두 없으며,
            # optional이 아닌 경우, 에러 반환
            elif user_input is None and not is_optional:

                return self.error_func(
                    f"Required {param_object_name} parameter, "
                    f"'{param_name}' not given."
                )

            if not self.type_check(user_input, param_annotation):
                return self.error_func(
                    f"In {param_object_name}, "
                    f"'{param_name}' is must be {param_annotation}"
                )
            # TODO: Query 파라미터 컨버트
            parsed_inputs[param_name] = user_input

        return parsed_inputs

    def type_check(self, user_input, annotation):
        if isinstance(annotation, Dict):
            if not isinstance(user_input, dict):
                return False
            for key, value in user_input.items():
                if not isinstance(key, annotation.key):
                    return False
                if not self.type_check(value, annotation.value):
                    return False
            return True

        elif isinstance(annotation, List):
            if not isinstance(user_input, list):
                return False
            for item in user_input:
                if not self.type_check(item, annotation.item):
                    return False
            return True

        elif isinstance(annotation, tuple):
                for ann_i in annotation:
                    if self.type_check(user_input, ann_i):
                        return True
                return False

        else:
            return annotation == All or \
                   isinstance(user_input, annotation)

