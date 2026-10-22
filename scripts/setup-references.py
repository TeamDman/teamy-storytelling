#!/usr/bin/env python3
"""Materialize pinned source references without installing or executing them."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

REPO = Path(__file__).resolve().parents[1]


def git(directory, *args):
    return subprocess.check_output(
        ['git', '-C', str(directory), *args], text=True, stderr=subprocess.PIPE
    ).strip()


def verify(directory, entry):
    if not (directory / '.git').is_dir():
        raise ValueError(f'{directory}: expected a standalone reference checkout; left unchanged')
    if git(directory, 'remote', 'get-url', 'origin') != entry['url']:
        raise ValueError(f'{directory}: origin differs from lock; left unchanged')
    if git(directory, 'status', '--porcelain', '--untracked-files=all'):
        raise ValueError(f'{directory}: local changes exist; left unchanged')
    if git(directory, 'rev-parse', 'HEAD') != entry['commit']:
        raise ValueError(f'{directory}: revision differs from lock; left unchanged; move it aside after review')
    if subprocess.run(['git', '-C', str(directory), 'symbolic-ref', '-q', 'HEAD'],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        raise ValueError(f'{directory}: expected detached HEAD; left unchanged')
    if hashlib.sha256((directory / 'LICENSE').read_bytes()).hexdigest() != entry['license_sha256']:
        raise ValueError(f'{directory}: license digest mismatch')


def ensure(root, entry, check_only=False):
    destination = root / entry['name']
    if destination.exists() or destination.is_symlink():
        if destination.is_symlink():
            raise ValueError(f'{destination}: symlink destination refused; left unchanged')
        verify(destination, entry)
    elif check_only:
        raise ValueError(f'{destination}: missing; run setup-references.py first')
    else:
        root.mkdir(parents=True, exist_ok=True)
        # A failed fetch cannot leave a partial checkout at the canonical path.
        with tempfile.TemporaryDirectory(prefix='.reference-', dir=root) as temp:
            staging = Path(temp) / 'checkout'
            staging.mkdir()
            git(staging, 'init', '--quiet')
            git(staging, 'remote', 'add', 'origin', entry['url'])
            git(staging, 'fetch', '--depth=1', 'origin', entry['commit'])
            git(staging, 'checkout', '--detach', '--quiet', entry['commit'])
            verify(staging, entry)
            staging.rename(destination)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    default_root = Path(os.environ['STORY_ROOT']) / 'references' if 'STORY_ROOT' in os.environ else REPO / '.references'
    parser.add_argument('--root', type=Path, default=default_root)
    parser.add_argument('--check-only', action='store_true', help='Verify existing checkouts without network access')
    args = parser.parse_args()
    lock = json.loads((REPO / 'reference-lock.json').read_text())
    if lock['version'] != 1:
        raise ValueError('Unsupported reference lock version')
    for entry in lock['references']:
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', entry['name']):
            raise ValueError('Invalid reference directory name')
        if not re.fullmatch(r'[0-9a-f]{40}', entry['commit']):
            raise ValueError('Reference must use a full commit SHA')
        path = ensure(args.root.resolve(), entry, args.check_only)
        print(f"{entry['name']}: {entry['commit']} ({entry['license']}) at {path}")


if __name__ == '__main__':
    main()
