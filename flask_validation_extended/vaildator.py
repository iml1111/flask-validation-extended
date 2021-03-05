from inspect import signature
from functools import wraps
from flask import request
from .params import Route, Query, Json, Form, File, Header
from .types import type_check, All, FileObj


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
                Query: request.args,
                Form: request.form,
                File: request.files
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
            if param_object.__class__ is Header:
                user_input = request_inputs[Header].get(param_object.header_name)
            elif param_object.__class__ is File:
                user_input = request_inputs[File].getlist(param_name)
                if not user_input:
                    user_input = None
                elif len(user_input) == 1 and user_input[0].filename == "":
                    user_input = None
            else:
                user_input = request_inputs[param_object.__class__].get(param_name)

            # 사용자의 정보가 입력되지 않았으나, default가 명시된 경우, 할당
            if user_input is None and param_object.default is not None:
                user_input = param_object.default

            # 사용자의 인풋 및 default가 모두 없으며,
            # optional이 아닌 경우, 에러 반환
            elif user_input is None and is_required:
                if param_object.__class__ is Header:
                    return self.error_func(
                        f"Required [{param_object_name}] parameter, "
                        f"Header '{param_object.header_name}' not given."
                    )
                else:
                    return self.error_func(
                        f"Required [{param_object_name}] parameter, "
                        f"'{param_name}' not given."
                    )

            # Query, Header, Form, Route의 경우, 타입 변환 시도.
            # 지정된 타입으로의 convert 실패시, 에러 반환
            if (
                param_object.__class__ in {Header, Query, Form, Route} and
                isinstance(user_input, str) and
                param_annotation[0] not in [str, All]
            ):
                user_input, status = self._convert_parameter(user_input, param_annotation[0])
                if not status:
                    return self.error_func(
                        f"In [{param_object_name}] Params, "
                        f"'{param_name}' can't be converted to {param_annotation[0]}."
                    )

            # 사용자 입력값이 None이 아니며, type check에 실패한 경우
            if (
                user_input is not None and
                param_annotation[0] is not FileObj and
                not type_check(user_input, param_annotation)
            ):
                return self.error_func(
                    f"In [{param_object_name}] Params, "
                    f"'{param_name}' is not {[str(i) for i in param_annotation]}."
                )

            # 사용자 입력값이 None이 아니면, 입력된 Rule에 대하여 validation 개시
            if user_input is not None:
                for rule in valid_rules:
                    if not rule.is_valid(user_input):
                        return self.error_func(
                            f'Parameter <{param_name}>: {rule.invalid_str()}'
                        )

            parsed_inputs[param_name] = user_input

        return parsed_inputs

    @staticmethod
    def _convert_parameter(data, annotation):

        if annotation is int:
            try:
                return int(data), True
            except ValueError:
                return data, False

        elif annotation is float:
            try:
                return float(data), True
            except ValueError:
                return data, False

        elif (
            annotation is bool and
            data.lower() in ['true', 'false']
        ):
            return data.lower() == 'true', True

        return data, False

