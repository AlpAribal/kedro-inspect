from __future__ import annotations

from typing import List

from kedro.pipeline.pipeline import Pipeline as KedroPipeline
from typing_extensions import Self, TypedDict

from kedro_inspect.node import InspectedNode, InspectedNodeDict


class InspectedPipelineDict(TypedDict):
    nodes: List[InspectedNodeDict]


class InspectedPipeline:
    def __init__(self, nodes: List[InspectedNode]) -> None:
        self.nodes = nodes

    def to_dict(self) -> InspectedPipelineDict:
        return {"nodes": [n.to_dict() for n in self.nodes]}

    @classmethod
    def from_dict(cls, dct: InspectedPipelineDict) -> Self:
        return cls(nodes=[InspectedNode.from_dict(node) for node in dct["nodes"]])

    def to_kedro_pipeline(self) -> KedroPipeline:
        return KedroPipeline(nodes=[node.to_kedro_node() for node in self.nodes])

    @classmethod
    def from_kedro_pipeline(cls, pipeline: KedroPipeline) -> Self:
        return cls(
            nodes=[InspectedNode.from_kedro_node(node) for node in pipeline.nodes]
        )

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, InspectedPipeline):
            return NotImplemented
        return self.to_dict() == __value.to_dict()
