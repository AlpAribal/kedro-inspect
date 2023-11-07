import json

from kedro.pipeline import node
from typing_extensions import Any

from kedro_inspect.node import InspectedNode
from kedro_inspect.node_func import NodeFunction


def identity(x) -> Any:
    return x


def test_inspected_node() -> None:
    inputs = ["a"]
    outputs = ["b"]
    orig_node = node(identity, inputs, outputs)
    inspected_node = InspectedNode.from_kedro_node(orig_node)

    assert inspected_node.name is None
    assert inspected_node.tags == set()
    assert inspected_node.confirms == []
    assert inspected_node.namespace is None
    assert inspected_node.inputs == ["a"]
    assert inspected_node.outputs == ["b"]
    assert isinstance(inspected_node.function, NodeFunction)
    assert inspected_node.param_to_input == {"x": ["a"]}

    kedro_node = inspected_node.to_kedro_node()
    assert kedro_node == orig_node

    inspected_node_dict = inspected_node.to_dict()
    assert inspected_node_dict == {
        "name": None,
        "tags": [],
        "confirms": [],
        "namespace": None,
        "inputs": ["a"],
        "outputs": ["b"],
        "function": inspected_node.function.to_dict(),
        "param_to_input": {"x": ["a"]},
    }

    inspected_node_from_dict = InspectedNode.from_dict(inspected_node_dict)
    assert inspected_node_from_dict.to_dict() == inspected_node_dict

    assert json.loads(json.dumps(inspected_node_dict)) == inspected_node_dict
