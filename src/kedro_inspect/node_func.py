from __future__ import annotations

import inspect
from dataclasses import dataclass
from inspect import Parameter, _ParameterKind
from typing import Callable, Dict, List

from typing_extensions import (
    Any,
    Self,
    TypedDict,
    get_type_hints,
)

from kedro_inspect.serialisation import fqn_to_obj, obj_to_fqn


def get_type_hints_general(func: Callable) -> Dict[str, Any]:
    # typing.get_type_hints does extra work to get the actual type, whereas
    #   inspect.signature may return just a string
    if inspect.isclass(func):
        # TODO: if TypedDict, then do not use __init__
        typehints = get_type_hints(func.__init__)
        typehints["return"] = func
    else:
        typehints = get_type_hints(func)

    return typehints


class ArgumentDict(TypedDict):
    name: str
    kind: str
    type_hint: str


@dataclass
class Argument:
    name: str
    kind: _ParameterKind
    type_hint: Any

    def to_dict(self) -> ArgumentDict:
        return {
            "name": self.name,
            "kind": self.kind_to_str(self.kind),
            "type_hint": obj_to_fqn(self.type_hint),
        }

    @classmethod
    def from_dict(cls, dct: ArgumentDict) -> Argument:
        return cls(
            name=dct["name"],
            kind=cls.str_to_kind(dct["kind"]),
            type_hint=fqn_to_obj(dct["type_hint"]),
        )

    @staticmethod
    def kind_to_str(kind: Any) -> str:
        return {
            Parameter.POSITIONAL_ONLY: "POSITIONAL_ONLY",
            Parameter.POSITIONAL_OR_KEYWORD: "POSITIONAL_OR_KEYWORD",
            Parameter.VAR_POSITIONAL: "VAR_POSITIONAL",
            Parameter.KEYWORD_ONLY: "KEYWORD_ONLY",
            Parameter.VAR_KEYWORD: "VAR_KEYWORD",
        }[kind]

    @staticmethod
    def str_to_kind(kind_str: str) -> Any:
        return {
            "POSITIONAL_ONLY": Parameter.POSITIONAL_ONLY,
            "POSITIONAL_OR_KEYWORD": Parameter.POSITIONAL_OR_KEYWORD,
            "VAR_POSITIONAL": Parameter.VAR_POSITIONAL,
            "KEYWORD_ONLY": Parameter.KEYWORD_ONLY,
            "VAR_KEYWORD": Parameter.VAR_KEYWORD,
        }[kind_str]


class NodeFunctionDict(TypedDict):
    func: str
    parameters: List[ArgumentDict]
    return_value: str


@dataclass
class NodeFunction:
    func: Callable
    parameters: List[Argument]
    return_value: Any

    @classmethod
    def from_callable(cls, func: Callable) -> Self:
        sig = inspect.signature(func, follow_wrapped=False)
        hints = get_type_hints_general(func)
        return cls(
            func=func,
            parameters=[
                Argument(
                    name=arg.name,
                    kind=arg.kind,
                    type_hint=hints.get(arg.name, Any),
                )
                for arg in sig.parameters.values()
            ],
            return_value=hints.get("return", Any),
        )

    def to_dict(self) -> NodeFunctionDict:
        return {
            "func": obj_to_fqn(self.func),
            "parameters": [arg.to_dict() for arg in self.parameters],
            "return_value": obj_to_fqn(self.return_value),
        }

    @classmethod
    def from_dict(cls, dct: NodeFunctionDict) -> Self:
        return cls(
            func=fqn_to_obj(dct["func"]),
            parameters=[Argument.from_dict(arg) for arg in dct["parameters"]],
            return_value=fqn_to_obj(dct["return_value"]),
        )
