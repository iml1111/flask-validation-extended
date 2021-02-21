from inspect import signature
from functools import wraps
from flask import request
from .params import Route, Query, Json, Form, File, Header
from .types import type_check, All


class Validator:
    """
    Main validation class
    """
    def __init__(self, error_function=None):
        self.error_func = error_function if error_function else self.default_error

    @staticmethod
    def default_error(error_message):
        return {"error": error_message}, 400

    def __call__(self, f):
        @wraps(f)
        def nested_func(**kwargs):
            # 모든 리퀘스트 인자 값 호출
            request_inputs = {
                Header: dict(request.headers.items()),
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
            is_required = not param_object.optional
            valid_rules = param_object.rules

            # 지정된 Param 클래스가 아닌 경우, 에러 반환
            if param_object.__class__ not in request_inputs:
                return self.error_func("Invalid parameter type.")

            # Header에서 가져올 데이터의 경우, 별도로 입력받은 header_name으로 호출
            if param_object.__class__ is Header and param_object.header_name:
                user_input = request_inputs[Header].get(param_object.header_name)
            else:
                user_input = request_inputs[param_object.__class__].get(param_name)

            # 사용자의 정보가 입력되지 않았으나, default가 명시된 경우, 할당
            if user_input is None and param_object.default is not None:
                user_input = param_object.default

            # 사용자의 인풋 및 default가 모두 없으며,
            # optional이 아닌 경우, 에러 반환
            elif user_input is None and is_required:
                return self.error_func(
                    f"Required {param_object_name} parameter, "
                    f"'{param_name}' not given."
                )

            # Query, Header, Form, Route의 경우, 타입 변환 시도.
            # 지정된 타입으로의 convert 실패시, 에러 반환
            if (
                param_object.__class__ in {Header, Query, Form, Route} and
                isinstance(user_input, str) and
                param_annotation not in [str, All]
            ):
                if param_annotation is int and user_input.isdecimal():
                    user_input = int(user_input)

                elif (
                    param_annotation is float and
                    user_input.replace('.','',1).isdecimal()
                ):
                    user_input = float(user_input)

                elif (
                    param_annotation is bool and
                    user_input.lower() in ['true', 'false']
                ):
                    user_input = user_input.lower() == 'true'

                else:
                    return self.error_func(
                        f"In '{param_object_name}' Params, "
                        f"'{param_name}' can't be converted to {param_annotation}."
                    )

            # optional이 아니며, type check에 실패한 경우
            if is_required and not type_check(user_input, param_annotation):
                return self.error_func(
                    f"In '{param_object_name}' Params, "
                    f"'{param_name}' is not {param_annotation}."
                )

            # 입력 Rule에 대하여 validation 개시
            if valid_rules:
                pass

            parsed_inputs[param_name] = user_input

        return parsed_inputs

