"""Verify pinned, already-materialized Library bundles and install local inputs.

This script does not download files, access credentials, or change network policy.
Use the current Library skill's supported materialization flow first.
"""
import argparse
import hashlib
import json
import shutil
import stat
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
MAX_UNPACKED = 32 * 1024 * 1024


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_entries(archive):
    entries = archive.infolist()
    if sum(entry.file_size for entry in entries) > MAX_UNPACKED:
        raise ValueError('Archive exceeds the input expansion limit')
    seen = set()
    for entry in entries:
        name = entry.filename
        path = PurePosixPath(name)
        if (not name or path.is_absolute() or '..' in path.parts
                or '\\' in name or ':' in name or any(ord(c) < 32 for c in name)):
            raise ValueError(f'Unsafe archive member: {name!r}')
        key = path.as_posix().rstrip('/')
        if key in seen or stat.S_ISLNK(entry.external_attr >> 16):
            raise ValueError(f'Duplicate/link archive member: {name!r}')
        if entry.flag_bits & 1:
            raise ValueError('Encrypted input archives are unsupported')
        seen.add(key)
    return entries


def validate_scene(directory, lock):
    manifest_path = directory / 'scene-manifest.json'
    if digest(manifest_path) != lock['sceneManifestSHA256']:
        raise ValueError('Reconciled scene manifest hash mismatch')
    manifest = json.loads(manifest_path.read_text())
    for asset in manifest['assets']:
        path = PurePosixPath(asset['path'])
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('Unsafe manifest asset path')
        if digest(directory / path) != asset['sha256']:
            raise ValueError(f'Asset hash mismatch: {path}')
    if len(manifest['assets']) != 75:
        raise ValueError('Expected 75 original assets')


def validate_references(directory):
    for line in (directory / 'SHA256SUMS.txt').read_text().splitlines():
        expected, name = line.split('  ', 1)
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or '\\' in name:
            raise ValueError('Unsafe reference checksum path')
        if digest(directory / path) != expected.lower():
            raise ValueError(f'Reference hash mismatch: {name}')
    if len(list((directory / 'reference').glob('figure_*.png'))) != 8:
        raise ValueError('Expected eight reference PNGs')


def install(archive_path, target, record, validate):
    if archive_path.stat().st_size != record['bytes'] or digest(archive_path) != record['sha256']:
        raise ValueError(f'Pinned archive mismatch: {archive_path.name}')
    if target.exists():
        validate(target)
        print(f'Verified existing {target.name}; left unchanged')
        return
    with tempfile.TemporaryDirectory(prefix='.verified-input-', dir=ROOT) as temp:
        staged = Path(temp) / 'input'
        staged.mkdir()
        with zipfile.ZipFile(archive_path) as archive:
            for entry in safe_entries(archive):
                path = staged / PurePosixPath(entry.filename)
                if entry.is_dir():
                    path.mkdir(parents=True, exist_ok=True)
                else:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with archive.open(entry) as source, path.open('xb') as output:
                        shutil.copyfileobj(source, output)
        validate(staged)
        staged.rename(target)
    print(f'Installed verified {target.name}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scene', type=Path)
    parser.add_argument('--references', type=Path)
    parser.add_argument('--verify-existing', action='store_true')
    args = parser.parse_args()
    lock = json.loads((ROOT / 'provenance.json').read_text())
    if args.verify_existing:
        validate_scene(ROOT / 'ground-truth', lock)
        validate_references(ROOT / 'reference-evidence')
        print('75 original assets, scene manifest and eight references verified')
        return
    if args.scene is None or args.references is None:
        parser.error('--scene and --references are required unless --verify-existing is used')
    records = lock['inputs']
    install(args.scene, ROOT / 'ground-truth', records[0], lambda p: validate_scene(p, lock))
    install(args.references, ROOT / 'reference-evidence', records[1], validate_references)


if __name__ == '__main__':
    main()
