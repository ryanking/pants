# Copyright 2022 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pants.bsp.spec.base import BuildTargetIdentifier

# -----------------------------------------------------------------------------------------------
# Compile Request
# See https://build-server-protocol.github.io/docs/specification.html#compile-request
# -----------------------------------------------------------------------------------------------


@dataclass(frozen=True)
class CompileParams:
    # A sequence of build targets to compile.
    targets: tuple[BuildTargetIdentifier, ...]

    # A unique identifier generated by the client to identify this request.
    # The server may include this id in triggered notifications or responses.
    origin_id: str | None = None

    # Optional arguments to the compilation process.
    arguments: tuple[str, ...] | None = ()

    @classmethod
    def from_json_dict(cls, d: dict[str, Any]) -> Any:
        return cls(
            targets=tuple(BuildTargetIdentifier.from_json_dict(x) for x in d["targets"]),
            origin_id=d.get("originId"),
            arguments=tuple(d["arguments"]) if "arguments" in d else None,
        )

    def to_json_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"targets": [tgt.to_json_dict() for tgt in self.targets]}
        if self.origin_id is not None:
            result["originId"] = self.origin_id
        if self.arguments is not None:
            result["arguments"] = self.arguments
        return result


@dataclass(frozen=True)
class CompileResult:
    # An optional request id to know the origin of this report.
    origin_id: str | None

    # A status code for the execution.
    status_code: int

    # Kind of data to expect in the `data` field. If this field is not set, the kind of data is not specified.
    data_kind: str | None = None

    # A field containing language-specific information, like products
    # of compilation or compiler-specific metadata the client needs to know.
    data: Any | None = None

    @classmethod
    def from_json_dict(cls, d: dict[str, Any]) -> Any:
        return cls(
            origin_id=d.get("originId"),
            status_code=d["statusCode"],
            data_kind=d.get("dataKind"),
            data=d.get("data"),
        )

    def to_json_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "statusCode": self.status_code,
        }
        if self.origin_id is not None:
            result["originId"] = self.origin_id
        if self.data_kind is not None:
            result["dataKind"] = self.data_kind
        if self.data is not None:
            result["data"] = self.data  # TODO: Enforce to_json_dict available
        return result


@dataclass(frozen=True)
class CompileTask:
    target: BuildTargetIdentifier

    @classmethod
    def from_json_dict(cls, d: dict[str, Any]) -> Any:
        return cls(target=BuildTargetIdentifier.from_json_dict(d["target"]))

    def to_json_dict(self) -> dict[str, Any]:
        return {"target": self.target.to_json_dict()}


@dataclass(frozen=True)
class CompileReport:
    # The build target that was compiled
    target: BuildTargetIdentifier

    # An optional request id to know the origin of this report.
    origin_id: str | None = None

    # The total number of reported errors compiling this target.
    errors: int | None = None

    # The total number of reported warnings compiling the target.
    warnings: int | None = None

    # The total number of milliseconds it took to compile the target.
    time: int | None = None

    # The compilation was a noOp compilation.
    no_op: bool | None = None

    @classmethod
    def from_json_dict(cls, d: dict[str, Any]) -> Any:
        return cls(
            target=BuildTargetIdentifier.from_json_dict(d["target"]),
            origin_id=d.get("originId"),
            errors=d.get("errors"),
            warnings=d.get("warnings"),
            time=d.get("time"),
            no_op=d.get("noOp"),
        )

    def to_json_dict(self) -> dict[str, Any]:
        result = {"target": self.target.to_json_dict()}
        if self.origin_id is not None:
            result["originId"] = self.origin_id
        if self.errors is not None:
            result["errors"] = self.errors
        if self.warnings is not None:
            result["warnings"] = self.warnings
        if self.time is not None:
            result["time"] = self.time
        if self.no_op is not None:
            result["noOp"] = self.no_op
        return result