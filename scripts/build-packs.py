#!/usr/bin/env python3
"""Build one deterministic zip per host pack and scan it.

Zips land in dist/ (gitignored). SKILL.md is at the zip root.
Member names are sorted and timestamps are fixed, so a second build
of the same tree is byte-identical on the same zlib. Byte identity
depends on the zlib version that deflates the members.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
import zipfile
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import zipscan

FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def _load_sync():
    path = Path(__file__).resolve().parent / "sync-packs.py"
    spec = importlib.util.spec_from_file_location("sync_packs", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load scripts/sync-packs.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["sync_packs"] = module
    spec.loader.exec_module(module)
    return module


def pack_members(pack_dir: Path) -> dict[str, bytes]:
    if not pack_dir.is_dir():
        raise SystemExit(f"{pack_dir} is missing")
    members: dict[str, bytes] = {}
    for path in pack_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.is_symlink():
            raise SystemExit(f"symlink not packed: {path}")
        rel = path.relative_to(pack_dir).as_posix()
        if "__pycache__" in rel.split("/"):
            continue
        members[rel] = path.read_bytes()
    if "SKILL.md" not in members:
        raise SystemExit(f"{pack_dir} has no SKILL.md")
    return members


def write_deterministic_zip(dest: Path, members: dict[str, bytes]) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w") as zf:
        for name in sorted(members):
            info = zipfile.ZipInfo(filename=name, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 0
            info.external_attr = 0
            info.flag_bits = 0
            zf.writestr(info, members[name], compresslevel=9)


def zip_name(pack: str, version: str) -> str:
    short = pack[: -len("-skill")] if pack.endswith("-skill") else pack
    return f"free-ip-sentinel-{short}-v{version}.zip"


def build(root: Path, dist: Path) -> int:
    sync = _load_sync()
    version = sync.read_version(root)
    packs = sync.read_packs(root)
    failed = False
    for pack in packs:
        members = pack_members(root / pack)
        dest = dist / zip_name(pack, version)
        write_deterministic_zip(dest, members)
        again = dest.with_suffix(dest.suffix + ".again")
        write_deterministic_zip(again, members)
        if again.read_bytes() != dest.read_bytes():
            print(f"FAIL {pack}: zip is not deterministic")
            failed = True
        again.unlink()
        result = zipscan.scan_zip(dest, pack=pack)
        disk_names = sorted(members)
        print(f"{pack}: {dest.name}")
        print(f"  files {result.file_count} uncompressed {result.uncompressed}")
        if disk_names != result.names:
            print(f"FAIL {pack}: zip names differ from the pack tree")
            failed = True
        else:
            print("  pack file list matches zip")
        for name in result.names:
            print(f"  {name}")
        print(zipscan.format_report(result))
        if not result.ok:
            failed = True
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build and scan host-pack zips.")
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--dist", type=Path, default=None)
    args = parser.parse_args(argv)
    root = (args.root or Path(__file__).resolve().parents[1]).resolve()
    dist = (args.dist or (root / "dist")).resolve()
    return build(root, dist)


if __name__ == "__main__":
    sys.exit(main())
