#!/usr/bin/env python3
"""
Parse Star Rupture .sav files and search the JSON for values.
Usage:
  python parse_sav.py <path-to.sav>                    # load and print root keys
  python parse_sav.py <path-to.sav> "impeller rod"     # find paths where this value appears
  python parse_sav.py <path-to.sav> --key DisplayName  # find paths where key matches
"""

import json
import sys
import zlib
from pathlib import Path


def load_sav(path: str) -> dict:
    """Read .sav file: skip 4-byte header, zlib decompress, parse JSON."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    raw = path.read_bytes()
    if len(raw) < 4:
        raise ValueError("Save file too small")
    compressed = raw[4:]
    # zlib format (header 0x78); use wbits=15 for raw deflate if needed
    try:
        data = zlib.decompress(compressed)
    except zlib.error:
        data = zlib.decompress(compressed, wbits=-zlib.MAX_WBITS)
    return json.loads(data.decode("utf-8", errors="replace"))


def find_value(obj, target: str, path: str = "", results: list | None = None, case_insensitive: bool = True):
    """Recursively find paths where a string value equals target (substring or exact)."""
    if results is None:
        results = []
    target_lower = target.lower() if case_insensitive else target

    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}/{k}" if path else k
            if isinstance(v, str):
                if case_insensitive and v.lower() == target_lower:
                    results.append((p, "value", repr(v)))
                elif not case_insensitive and v == target:
                    results.append((p, "value", repr(v)))
                elif target_lower in (v.lower() if case_insensitive else v):
                    results.append((p, "value (substring)", repr(v)))
            else:
                find_value(v, target, p, results, case_insensitive)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            p = f"{path}[{i}]"
            if isinstance(v, str):
                if case_insensitive and v.lower() == target_lower:
                    results.append((p, "value", repr(v)))
                elif not case_insensitive and v == target:
                    results.append((p, "value", repr(v)))
                elif target_lower in (v.lower() if case_insensitive else v):
                    results.append((p, "value (substring)", repr(v)))
            else:
                find_value(v, target, p, results, case_insensitive)
    return results


def find_key(obj, key_substring: str, path: str = "", results: list | None = None, case_insensitive: bool = True):
    """Recursively find paths where a key name contains key_substring."""
    if results is None:
        results = []
    key_lower = key_substring.lower() if case_insensitive else key_substring

    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}/{k}" if path else k
            if case_insensitive and key_lower in k.lower():
                results.append((p, type(v).__name__, repr(v)[:120]))
            elif not case_insensitive and key_substring in k:
                results.append((p, type(v).__name__, repr(v)[:120]))
            find_key(v, key_substring, p, results, case_insensitive)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            find_key(v, key_substring, f"{path}[{i}]", results, case_insensitive)
    return results


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    sav_path = sys.argv[1]
    search_value = None
    key_filter = None
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--key" and i + 1 < len(sys.argv):
            key_filter = sys.argv[i + 1]
            i += 2
            continue
        if not arg.startswith("-"):
            search_value = arg
        i += 1

    print(f"Loading {sav_path} ...")
    root = load_sav(sav_path)
    print("Loaded. Root keys:", list(root.keys()) if isinstance(root, dict) else type(root))

    if search_value:
        print(f'\nSearching for value "{search_value}" (case-insensitive)...')
        hits = find_value(root, search_value)
        for path, kind, preview in hits:
            print(f"  {path}  [{kind}]  {preview}")
        print(f"Total: {len(hits)} match(es)")

    if key_filter:
        print(f'\nSearching for key containing "{key_filter}"...')
        hits = find_key(root, key_filter)
        for path, typ, preview in hits:
            print(f"  {path}  ({typ})  {preview}")
        print(f"Total: {len(hits)} match(es)")

    if not search_value and not key_filter:
        # Dump structure one level
        if isinstance(root, dict):
            for k, v in root.items():
                t = type(v).__name__
                if isinstance(v, (dict, list)):
                    size = len(v)
                    print(f"  {k}: {t} (len={size})")
                else:
                    print(f"  {k}: {repr(v)[:80]}")


if __name__ == "__main__":
    main()
