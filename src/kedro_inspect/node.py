from __future__ import annotations

import inspect
from collections import defaultdict
from copy import deepcopy
from typing import TYPE_CHECKING, Dict, List, Set

from kedro.pipeline.node import Node as KedroNode
from typing_extensions import Self, TypedDict

from kedro_inspect.node_func import NodeFunction, NodeFunctionDict

if TYPE_CHECKING:
    from inspect import BoundArguments


class InspectedNodeDict(TypedDict):
    name: str | None
    tags: List[str]
    confirms: List[str]
    namespace: str | None
    inputs: List[str] | Dict[str, str] | str | None
    outputs: List[str] | Dict[str, str] | str | None
    function: NodeFunctionDict
    param_to_input: Dict[str, List[str]]


class InspectedNode:
    def __init__(
        self,
        name: str | None,
        tags: Set[str],
        confirms: List[str],
        namespace: str | None,
        inputs: List[str] | Dict[str, str] | str | None,
        outputs: List[str] | Dict[str, str] | str | None,
        function: NodeFunction,
        param_to_input: Dict[str, List[str]],
    ) -> None:
        self.name = name
        self.tags = tags
        self.confirms = confirms
        self.namespace: str | None = namespace
        self.inputs = inputs
        self.outputs = outputs
        self.function = function
        self.param_to_input = param_to_input

    def to_dict(self) -> InspectedNodeDict:
        return {
            "name": self.name,
            "tags": list(self.tags),
            "confirms": self.confirms,
            "namespace": self.namespace,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "function": self.function.to_dict(),
            "param_to_input": self.param_to_input,
        }

    @classmethod
    def from_dict(cls, dct: InspectedNodeDict) -> Self:
        return cls(
            name=dct["name"],
            tags=set(dct["tags"]),
            confirms=dct["confirms"],
            namespace=dct["namespace"],
            inputs=dct["inputs"],
            outputs=dct["outputs"],
            function=NodeFunction.from_dict(dct["function"]),
            param_to_input=dct["param_to_input"],
        )

    def to_kedro_node(self) -> KedroNode:
        return KedroNode(
            func=self.function.func,
            inputs=self.inputs,
            outputs=self.outputs,
            name=self.name,
            tags=self.tags,
            confirms=self.confirms,
            namespace=self.namespace,
        )

    @classmethod
    def from_kedro_node(cls, node: KedroNode) -> Self:
        return cls(
            name=node._name,
            tags=node.tags,
            confirms=node.confirms,
            namespace=node._namespace,
            inputs=deepcopy(node._inputs),
            outputs=deepcopy(node._outputs),
            function=NodeFunction.from_callable(node.func),
            param_to_input=cls.get_param_to_input(node),
        )

    @staticmethod
    def get_bound_datasets_from_node(node: KedroNode) -> BoundArguments:
        sig = inspect.signature(node.func, follow_wrapped=False)
        return (
            sig.bind(**node._inputs)
            if isinstance(node._inputs, dict)
            else sig.bind(*node.inputs)
        )

    @staticmethod
    def get_param_to_input(node: KedroNode) -> Dict[str, List[str]]:
        bound_datasets = InspectedNode.get_bound_datasets_from_node(node)
        p_to_ds = defaultdict(list)
        for param, dataset in bound_datasets.arguments.items():
            if type(dataset) is tuple:
                # real_arg is a VAR_POSITIONAL -> multiple datasets can be bound to it
                p_to_ds[param] = list(dataset)
            elif type(dataset) is dict:
                # real_arg is a VAR_KEYWORD -> multiple datasets can be bound to it
                p_to_ds[param] = list(dataset.values())
            else:
                assert type(dataset) is str
                p_to_ds[param] = [dataset]
        return p_to_ds

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, InspectedNode):
            return NotImplemented
        return self.to_dict() == __value.to_dict()
