from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Type

from kedro.framework.project import pipelines
from kedro.framework.startup import bootstrap_project

from kedro_inspect.pipeline import InspectedPipeline


class CliArgs(argparse.Namespace):
    """Used to typehint parsed CLI arguments."""

    project_path: Path
    pipeline: str
    indent: int | None
    output: Path | None


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect a Kedro pipeline.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("project_path", type=Path, help="path to the Kedro project")
    parser.add_argument(
        "-p",
        "--pipeline",
        type=str,
        help="name of the pipeline to inspect",
        default="__default__",
    )
    parser.add_argument(
        "-o", "--output", type=Path, help="path to the output file", required=False
    )
    parser.add_argument(
        "--indent", type=int, help="indentation for JSON output", default=None
    )
    return parser


def validate_args_before_bootstrap(args: Type[CliArgs]) -> None:
    if not args.project_path.is_dir():
        raise ValueError(f"Project path {args.project_path} is not a directory.")
    if not args.project_path.exists():
        raise ValueError(f"Project path {args.project_path} does not exist.")
    if args.output is not None and args.output.exists():
        raise ValueError(f"Output path {args.output} already exists.")


def validate_args_after_bootstrap(args: Type[CliArgs]) -> None:
    if args.pipeline not in pipelines:
        raise ValueError(
            f"Pipeline {args.pipeline} not found. "
            f"Available pipelines: {list(pipelines)}"
        )


def main() -> int:
    parser = get_parser()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        return 1

    args = parser.parse_args(namespace=CliArgs)
    validate_args_before_bootstrap(args)

    path = args.project_path.resolve()
    _ = bootstrap_project(path)
    validate_args_after_bootstrap(args)

    pipe = pipelines[args.pipeline]
    inspected = InspectedPipeline.from_kedro_pipeline(pipe)
    js = json.dumps(inspected.to_dict(), indent=args.indent)
    if args.output:
        Path(args.output).write_text(js)
    else:
        print(js)

    return 0


if __name__ == "__main__":
    sys.exit(main())
