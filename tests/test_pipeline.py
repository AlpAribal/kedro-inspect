from kedro.pipeline import Pipeline, node
from typing_extensions import Any

from kedro_inspect.node import InspectedNode
from kedro_inspect.pipeline import InspectedPipeline


def identity(x) -> Any:
    return x


def test_inspected_pipeline() -> None:
    node1 = node(identity, inputs=["data"], outputs=["result"], tags=["tag1"])
    node2 = node(identity, inputs=["result"], outputs=["output"], tags=["tag2"])
    orig_pipe = Pipeline([node1, node2])

    inspected_pipeline = InspectedPipeline.from_kedro_pipeline(orig_pipe)
    assert len(inspected_pipeline.nodes) == 2
    assert inspected_pipeline.nodes[0] == InspectedNode.from_kedro_node(node1)
    assert inspected_pipeline.nodes[1] == InspectedNode.from_kedro_node(node2)

    kedro_pipeline = inspected_pipeline.to_kedro_pipeline()
    for orig_node, kedro_node in zip(orig_pipe.nodes, kedro_pipeline.nodes):
        assert orig_node == kedro_node

    inspected_pipe_dict = inspected_pipeline.to_dict()
    assert inspected_pipe_dict == {
        "nodes": [
            inspected_pipeline.nodes[0].to_dict(),
            inspected_pipeline.nodes[1].to_dict(),
        ]
    }

    inspected_pipe_from_dict = InspectedPipeline.from_dict(inspected_pipe_dict)
    assert inspected_pipe_from_dict.to_dict() == inspected_pipe_dict
