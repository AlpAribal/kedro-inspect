from dataclasses import dataclass
from inspect import Parameter

from typing_extensions import Any

from kedro_inspect.node_func import Argument, NodeFunction


def dummy_func_w_all_param_types(
    pos_only: int, /, a: int, b: int, *args: int, kw_only: int, **kwargs: int
) -> int:
    """To be used in tests."""
    return 1


class DummyClass:
    """To be used in tests."""

    N_ARGS = 2

    def __init__(self, a: int, b: str) -> None: ...

    def instance_method(self, a: int, b: str) -> None: ...

    @classmethod
    def class_method(cls, a: int, b: str) -> None: ...

    @staticmethod
    def static_method(a: int, b: str) -> None: ...


@dataclass
class DummyDataclass:
    """To be used in tests."""

    a: int
    b: str


def test_argument_to_dict() -> None:
    arg = Argument(name="foo", kind=Parameter.POSITIONAL_ONLY, type_hint=int)
    arg_dict = arg.to_dict()

    assert arg_dict == {
        "name": "foo",
        "kind": "POSITIONAL_ONLY",
        "type_hint": "builtins.int",
    }


def test_argument_from_dict() -> None:
    arg_dict = {"name": "foo", "kind": "POSITIONAL_ONLY", "type_hint": "builtins.int"}
    arg = Argument.from_dict(arg_dict)

    assert arg.name == "foo"
    assert arg.kind == Parameter.POSITIONAL_ONLY
    assert arg.type_hint is int


def test_func_from_callable() -> None:
    """All parameter types are supported."""
    node_func = NodeFunction.from_callable(dummy_func_w_all_param_types)

    assert node_func.func == dummy_func_w_all_param_types
    assert len(node_func.parameters) == 6

    pos_only, arg_a, arg_b, args, kw_only, kwargs = node_func.parameters
    assert isinstance(pos_only, Argument)
    assert pos_only.name == "pos_only"
    assert pos_only.kind == Parameter.POSITIONAL_ONLY
    assert pos_only.type_hint is int

    assert isinstance(arg_a, Argument)
    assert arg_a.name == "a"
    assert arg_a.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert arg_a.type_hint is int

    assert isinstance(arg_b, Argument)
    assert arg_b.name == "b"
    assert arg_b.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert arg_b.type_hint is int

    assert isinstance(args, Argument)
    assert args.name == "args"
    assert args.kind == Parameter.VAR_POSITIONAL
    assert args.type_hint is int

    assert isinstance(kw_only, Argument)
    assert kw_only.name == "kw_only"
    assert kw_only.kind == Parameter.KEYWORD_ONLY
    assert kw_only.type_hint is int

    assert isinstance(kwargs, Argument)
    assert kwargs.name == "kwargs"
    assert kwargs.kind == Parameter.VAR_KEYWORD
    assert kwargs.type_hint is int

    assert node_func.return_value is int


def test_func_to_dict() -> None:
    node_func = NodeFunction.from_callable(dummy_func_w_all_param_types)
    node_func_dict = node_func.to_dict()

    assert node_func_dict == {
        "func": "test_node_func.dummy_func_w_all_param_types",
        "parameters": [
            {
                "name": "pos_only",
                "kind": "POSITIONAL_ONLY",
                "type_hint": "builtins.int",
            },
            {
                "name": "a",
                "kind": "POSITIONAL_OR_KEYWORD",
                "type_hint": "builtins.int",
            },
            {
                "name": "b",
                "kind": "POSITIONAL_OR_KEYWORD",
                "type_hint": "builtins.int",
            },
            {
                "name": "args",
                "kind": "VAR_POSITIONAL",
                "type_hint": "builtins.int",
            },
            {
                "name": "kw_only",
                "kind": "KEYWORD_ONLY",
                "type_hint": "builtins.int",
            },
            {
                "name": "kwargs",
                "kind": "VAR_KEYWORD",
                "type_hint": "builtins.int",
            },
        ],
        "return_value": "builtins.int",
    }


def test_func_from_dict() -> None:
    node_func_dict = {
        "func": "test_node_func.dummy_func_w_all_param_types",
        "parameters": [
            {
                "name": "pos_only",
                "kind": "POSITIONAL_ONLY",
                "type_hint": "builtins.int",
            },
            {
                "name": "a",
                "kind": "POSITIONAL_OR_KEYWORD",
                "type_hint": "builtins.int",
            },
            {
                "name": "b",
                "kind": "POSITIONAL_OR_KEYWORD",
                "type_hint": "builtins.int",
            },
            {
                "name": "args",
                "kind": "VAR_POSITIONAL",
                "type_hint": "builtins.int",
            },
            {
                "name": "kw_only",
                "kind": "KEYWORD_ONLY",
                "type_hint": "builtins.int",
            },
            {
                "name": "kwargs",
                "kind": "VAR_KEYWORD",
                "type_hint": "builtins.int",
            },
        ],
        "return_value": "builtins.int",
    }

    node_func = NodeFunction.from_dict(node_func_dict)

    assert node_func.func == dummy_func_w_all_param_types
    assert len(node_func.parameters) == 6

    pos_only, arg_a, arg_b, args, kw_only, kwargs = node_func.parameters
    assert isinstance(pos_only, Argument)
    assert pos_only.name == "pos_only"
    assert pos_only.kind == Parameter.POSITIONAL_ONLY
    assert pos_only.type_hint is int

    assert isinstance(arg_a, Argument)
    assert arg_a.name == "a"
    assert arg_a.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert arg_a.type_hint is int

    assert isinstance(arg_b, Argument)
    assert arg_b.name == "b"
    assert arg_b.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert arg_b.type_hint is int

    assert isinstance(args, Argument)
    assert args.name == "args"
    assert args.kind == Parameter.VAR_POSITIONAL
    assert args.type_hint is int

    assert isinstance(kw_only, Argument)
    assert kw_only.name == "kw_only"
    assert kw_only.kind == Parameter.KEYWORD_ONLY
    assert kw_only.type_hint is int

    assert isinstance(kwargs, Argument)
    assert kwargs.name == "kwargs"
    assert kwargs.kind == Parameter.VAR_KEYWORD
    assert kwargs.type_hint is int

    assert node_func.return_value is int


def test_func_from_class() -> None:
    """Signature of __init__ is used."""
    node_func = NodeFunction.from_callable(DummyClass)
    assert node_func.func == DummyClass
    assert len(node_func.parameters) == DummyClass.N_ARGS

    a, b = node_func.parameters
    assert isinstance(a, Argument)
    assert a.name == "a"
    assert a.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert a.type_hint is int

    assert isinstance(b, Argument)
    assert b.name == "b"
    assert b.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert b.type_hint is str

    assert node_func.return_value is DummyClass

    assert node_func.to_dict() == {
        "func": "test_node_func.DummyClass",
        "parameters": [
            {
                "name": "a",
                "kind": "POSITIONAL_OR_KEYWORD",
                "type_hint": "builtins.int",
            },
            {
                "name": "b",
                "kind": "POSITIONAL_OR_KEYWORD",
                "type_hint": "builtins.str",
            },
        ],
        "return_value": "test_node_func.DummyClass",
    }


def test_func_from_class_method() -> None:
    node_func = NodeFunction.from_callable(DummyClass.class_method)
    assert node_func.func == DummyClass.class_method
    assert len(node_func.parameters) == DummyClass.N_ARGS

    a, b = node_func.parameters
    assert isinstance(a, Argument)
    assert a.name == "a"
    assert a.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert a.type_hint is int

    assert isinstance(b, Argument)
    assert b.name == "b"
    assert b.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert b.type_hint is str

    assert node_func.return_value is type(None)

    assert node_func.to_dict() == {
        "func": "test_node_func.DummyClass.class_method",
        "parameters": [
            {
                "name": "a",
                "kind": "POSITIONAL_OR_KEYWORD",
                "type_hint": "builtins.int",
            },
            {
                "name": "b",
                "kind": "POSITIONAL_OR_KEYWORD",
                "type_hint": "builtins.str",
            },
        ],
        "return_value": "builtins.NoneType",
    }


def test_func_from_static_method() -> None:
    node_func = NodeFunction.from_callable(DummyClass.static_method)
    assert node_func.func == DummyClass.static_method
    assert len(node_func.parameters) == DummyClass.N_ARGS

    a, b = node_func.parameters
    assert isinstance(a, Argument)
    assert a.name == "a"
    assert a.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert a.type_hint is int

    assert isinstance(b, Argument)
    assert b.name == "b"
    assert b.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert b.type_hint is str

    assert node_func.return_value is type(None)

    assert node_func.to_dict() == {
        "func": "test_node_func.DummyClass.static_method",
        "parameters": [
            {
                "name": "a",
                "kind": "POSITIONAL_OR_KEYWORD",
                "type_hint": "builtins.int",
            },
            {
                "name": "b",
                "kind": "POSITIONAL_OR_KEYWORD",
                "type_hint": "builtins.str",
            },
        ],
        "return_value": "builtins.NoneType",
    }


def test_func_from_bound_instance_method() -> None:
    """Argument 'self' is ignored."""
    dummy_instance = DummyClass(a=1, b="foo")
    node_func = NodeFunction.from_callable(dummy_instance.instance_method)
    assert node_func.func == dummy_instance.instance_method
    assert len(node_func.parameters) == DummyClass.N_ARGS

    a, b = node_func.parameters
    assert isinstance(a, Argument)
    assert a.name == "a"
    assert a.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert a.type_hint is int

    assert isinstance(b, Argument)
    assert b.name == "b"
    assert b.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert b.type_hint is str

    assert node_func.return_value is type(None)


def test_func_from_unbound_method() -> None:
    """`self` is an explicit argument."""
    node_func = NodeFunction.from_callable(DummyClass.instance_method)
    assert node_func.func == DummyClass.instance_method
    assert len(node_func.parameters) == DummyClass.N_ARGS + 1  # +1 for self

    self, a, b = node_func.parameters
    assert isinstance(self, Argument)
    assert self.name == "self"
    assert self.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert self.type_hint is Any

    assert isinstance(a, Argument)
    assert a.name == "a"
    assert a.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert a.type_hint is int

    assert isinstance(b, Argument)
    assert b.name == "b"
    assert b.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert b.type_hint is str

    assert node_func.return_value is type(None)


def test_from_dataclass() -> None:
    node_func = NodeFunction.from_callable(DummyDataclass)
    assert node_func.func == DummyDataclass
    assert len(node_func.parameters) == 2

    a, b = node_func.parameters
    assert isinstance(a, Argument)
    assert a.name == "a"
    assert a.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert a.type_hint is int

    assert isinstance(b, Argument)
    assert b.name == "b"
    assert b.kind == Parameter.POSITIONAL_OR_KEYWORD
    assert b.type_hint is str

    assert node_func.return_value is DummyDataclass

    assert node_func.to_dict() == {
        "func": "test_node_func.DummyDataclass",
        "parameters": [
            {
                "name": "a",
                "kind": "POSITIONAL_OR_KEYWORD",
                "type_hint": "builtins.int",
            },
            {
                "name": "b",
                "kind": "POSITIONAL_OR_KEYWORD",
                "type_hint": "builtins.str",
            },
        ],
        "return_value": "test_node_func.DummyDataclass",
    }
