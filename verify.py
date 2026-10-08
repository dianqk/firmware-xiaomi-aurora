#!/usr/bin/env python3
"""Verify the stock payload inventory without accessing a device (Python 3)."""
# SPDX-License-Identifier: MIT
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys


def checksum_entries(path):
    entries = {}
    for line in path.read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        name = name.removeprefix('*')
        if name in entries:
            raise ValueError(f'duplicate checksum entry: {path}: {name}')
        entries[name] = digest
    return entries


def verify(root):
    manifest = json.loads((root / 'SOURCE.json').read_text())
    if manifest['schema_version'] != 1 or manifest['device']['codename'] != 'aurora':
        raise ValueError('unsupported manifest')
    expected = {}
    total = 0
    groups = {}
    for record in manifest['files']:
        name = record['path']
        rel = PurePosixPath(name)
        if (rel.is_absolute() or '..' in rel.parts or len(rel.parts) < 3
                or rel.parts[0] not in manifest['versions'] or str(rel) != name):
            raise ValueError(f'invalid payload path: {name}')
        if name in expected:
            raise ValueError(f'duplicate payload: {name}')
        path = root / name
        if any(p.is_symlink() for p in [path, *path.parents]):
            raise ValueError(f'payload path contains a symlink: {name}')
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if len(data) != record['bytes'] or digest != record['sha256']:
            raise ValueError(f'payload differs: {name}')
        expected[name] = digest
        total += len(data)
        group = '/'.join(rel.parts[:2])
        groups.setdefault(group, {})['/'.join(rel.parts[2:])] = digest

    metadata = {'README.md', 'SHA256SUMS', 'SOURCE.json'}
    actual = {str(p.relative_to(root)) for variant in manifest['versions']
              for p in (root / variant).rglob('*')
              if p.is_file() and p.name not in metadata}
    if actual != set(expected):
        raise ValueError(f'inventory mismatch: {sorted(actual ^ set(expected))}')
    if checksum_entries(root / 'SHA256SUMS') != expected:
        raise ValueError('root checksum manifest differs from SOURCE.json')
    for group, entries in groups.items():
        if checksum_entries(root / group / 'SHA256SUMS') != entries:
            raise ValueError(f'component checksum manifest differs: {group}')

    sensor_sources = json.loads((root / 'android14/sensors/SOURCE.json').read_text())
    for item in sensor_sources['files']:
        matches = [r for r in manifest['files']
                   if r['path'].startswith('android14/sensors/')
                   and r['source'] == item['source']]
        if len(matches) != 1 or matches[0]['sha256'] != item['sha256']:
            raise ValueError(f'sensor provenance mismatch: {item["source"]}')
    print(f'PASS: {len(expected)} unchanged payloads, {total} bytes, '
          f'{len(groups)} component manifests')


if __name__ == '__main__':
    try:
        verify(Path(__file__).resolve().parent)
    except (OSError, ValueError, KeyError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        sys.exit(1)
