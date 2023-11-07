from inspect import Parameter

from kedro_inspect.node_func import Argument, NodeFunction


def dummy_func_w_all_param_types(
    pos_only: int, /, a: int, b: int, *args: int, kw_only: int, **kwargs: int
) -> int:
    """To be used in tests."""
    return 1


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
