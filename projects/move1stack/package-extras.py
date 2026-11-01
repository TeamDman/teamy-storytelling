"""Build local extras from a curated source list. Never upload or publish assets."""
import argparse
import hashlib
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_FILES = ['README.md', 'provenance.json', 'validation-summary.json', 'package.json',
                'package-lock.json', 'bake.py', 'prepare-inputs.py', 'test_prepare_inputs.py',
                'package-extras.py', 'compare.py', 'capture-stills.cjs', 'capture-candidate.cjs',
                'render-orbit.cjs', 'validate-render.cjs', 'validate-video.py', 'render-smoke.cjs',
                'probe-approved-webgl.cjs', 'render.sh', 'runtime-settings.cjs']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', choices=['first', 'source-cutout'], required=True)
    args = parser.parse_args()
    base = ROOT if args.profile == 'first' else ROOT / 'candidates/filtering'
    delivery = base / 'deliverable'
    output = delivery / 'extras.7z'
    if output.exists():
        raise FileExistsError(f'Preserving existing archive: {output}')
    preview = delivery / 'preview.mp4'
    preserved_preview = ROOT / 'previews' / args.profile / 'preview.mp4'
    if not preview.is_file():
        raise FileNotFoundError('Render and validate the preview before packaging')
    if preserved_preview.exists() and preserved_preview.read_bytes() != preview.read_bytes():
        raise FileExistsError('Preserving an existing differing preview')
    with tempfile.TemporaryDirectory(prefix='.extras-', dir=ROOT) as temporary:
        stage = Path(temporary)
        shutil.copy2(delivery / 'preview.mp4', stage / 'preview.mp4')
        shutil.copy2(ROOT / 'README.md', stage / 'README.md')
        source = stage / 'source'
        source.mkdir()
        for name in SOURCE_FILES:
            shutil.copy2(ROOT / name, source / name)
        for name in ['runtime', 'production', 'smoke', 'ground-truth', 'reference-evidence']:
            shutil.copytree(ROOT / name, source / name, ignore=shutil.ignore_patterns(
                '__pycache__', '*.pyc', '*.meta', '*.timestamp-*', 'node_modules'))
        candidate_source = source / 'candidates/filtering'
        candidate_source.mkdir(parents=True)
        for name in ['evaluate.py', 'refinement-summary.json']:
            shutil.copy2(ROOT / 'candidates/filtering' / name, candidate_source / name)
        selected = (['stills', 'comparisons'] if args.profile == 'first'
                    else ['first', 'source-cutout', 'comparisons'])
        for name in selected:
            if (base / name).is_dir():
                shutil.copytree(base / name, stage / name)
        for name in ['comparison-metrics.json', 'all-eight-before-after.png', 'beacon-crops.png',
                     'video-validation.json', 'refinement-summary.json']:
            if (base / name).is_file():
                shutil.copy2(base / name, stage / name)
        entries = []
        for path in sorted(stage.rglob('*')):
            if path.is_symlink():
                raise ValueError('Refusing links in extras')
            if path.is_file():
                entries.append(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(stage).as_posix()}')
        (stage / 'FILES.sha256').write_text('\n'.join(entries) + '\n')
        subprocess.run(['7z', 'a', '-t7z', '-mx=7', str(output), '.'], cwd=stage, check=True)
    subprocess.run(['7z', 't', str(output)], check=True)
    preserved_preview.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(preview, preserved_preview)
    preview.unlink()
    print(output)
    print(preserved_preview)


if __name__ == '__main__':
    main()
