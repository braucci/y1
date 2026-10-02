#!/usr/bin/env python3
"""Opt-in Y1 Rockbox refresh patch. Refuses every unknown librockbox.so build."""

import argparse
import hashlib
import struct
from pathlib import Path

ORIGINAL = "f3820e6c7547df588518ae003a5d956e958bf27457dd13efbc1fdad9efd5c1ac"
PATCHED = "725991af7371f2747065a4ee4fba45a49ff4a7c349cbd5d542620c5818a63148"
PATCHES = [
    (0x20758, 0xE3A01064, 0xE3A01003),  # menu list 100 -> 3 ticks
    (0x3B180, 0xE3A01032, 0xE3A01003),  # file list 50 -> 3 ticks
    (0x12785C, 14, 2),                  # SBS minimum update 14 -> 2 ticks
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def patch(source: Path, target: Path) -> None:
    if target.exists():
        raise SystemExit(f"Refusing to overwrite {target}")
    raw = source.read_bytes()
    if sha256(raw) != ORIGINAL:
        raise SystemExit("STOP: unknown Rockbox build. Original SHA-256 does not match; no file was written.")
    if raw[:7] != b"\x7fELF\x01\x01\x01" or struct.unpack_from("<H", raw, 18)[0] != 40:
        raise SystemExit("STOP: not the expected 32-bit little-endian ARM ELF library.")
    phoff = struct.unpack_from("<I", raw, 28)[0]
    phsize, phnum = struct.unpack_from("<HH", raw, 42)

    def file_offset(virtual: int) -> int:
        for i in range(phnum):
            kind, offset, address, _, length, _, _, _ = struct.unpack_from("<8I", raw, phoff + i * phsize)
            if kind == 1 and address <= virtual < address + length:
                return offset + virtual - address
        raise ValueError(f"Could not map virtual address {virtual:x}")

    modified = bytearray(raw)
    for address, expected, replacement in PATCHES:
        offset = file_offset(address)
        if struct.unpack_from("<I", raw, offset)[0] != expected:
            raise SystemExit(f"STOP: instruction mismatch at {address:x}; no file was written.")
        struct.pack_into("<I", modified, offset, replacement)
    if sum(a != b for a, b in zip(raw, modified)) != 3 or sha256(modified) != PATCHED:
        raise SystemExit("STOP: patch verification failed; no file was written.")
    target.write_bytes(modified)
    print(f"Wrote {target}. SHA-256: {PATCHED}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Exact original librockbox.so pulled from your own Y1")
    parser.add_argument("target", type=Path, help="Output filename; must not exist")
    arguments = parser.parse_args()
    patch(arguments.source, arguments.target)
