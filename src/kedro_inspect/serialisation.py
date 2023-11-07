from __future__ import annotations

import pydoc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Any


def obj_to_fqn(typ: Any) -> str:
    return f"{typ.__module__}.{typ.__qualname__}"


def fqn_to_obj(fqn: str) -> Any:
    obj = pydoc.locate(fqn)
    if obj is None:
        raise ValueError(f"Could not locate object: {fqn}")
    return obj
