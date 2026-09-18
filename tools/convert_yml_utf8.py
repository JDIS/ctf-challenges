#!/usr/bin/env python3
"""
Recursively convert all .yml files under the `challenges/` folder to UTF-8 (no BOM).
Usage:
  python tools/convert_yml_utf8.py [--root PATH]

Creates a `.bak` backup next to each modified file.
"""
import argparse
import sys
from pathlib import Path

FALLBACKS = ['utf-8', 'cp1252', 'latin-1']

def detect_and_read(path: Path):
    data = path.read_bytes()
    # strip UTF-8 BOM if present
    if data.startswith(b'\xef\xbb\xbf'):
        return data[3:].decode('utf-8'), 'utf-8-bom'
    # try fallbacks
    for enc in FALLBACKS:
        try:
            return data.decode(enc), enc
        except Exception:
            continue
    # last resort: latin-1
    return data.decode('latin-1', errors='replace'), 'latin-1-replaced'

def convert_file(path: Path):
    text, enc = detect_and_read(path)
    # If file already utf-8 and no BOM, nothing to do
    try:
        raw = path.read_bytes()
        if raw.startswith(b'\xef\xbb\xbf'):
            needs = True
        else:
            # try decode as utf-8 to check
            raw.decode('utf-8')
            needs = False
    except Exception:
        needs = True

    if not needs and enc == 'utf-8':
        return False, enc

    # backup
    bak = path.with_suffix(path.suffix + '.bak')
    if not bak.exists():
        path.rename(bak)
        bak.write_text(text, encoding='utf-8')
        # move bak back to original path with utf-8 content
        bak.replace(path)
    else:
        # simple overwrite after creating internal backup name
        backup2 = path.with_suffix(path.suffix + '.bak2')
        path.rename(backup2)
        path.write_text(text, encoding='utf-8')

    return True, enc

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', default='challenges', help='root folder to scan')
    p.add_argument('--force', action='store_true', help='force rewrite files to UTF-8 even if already valid')
    args = p.parse_args()

    root = Path(args.root)
    if not root.exists():
        print('Root does not exist:', root)
        sys.exit(2)

    changed = []
    scanned = 0
    for f in root.rglob('*.yml'):
        scanned += 1
        ok, enc = convert_file(f)
        # if force was requested, always rewrite
        if args.force:
            # read text and write utf-8 forcibly
            text, detected = detect_and_read(f)
            # backup
            bak = f.with_suffix(f.suffix + '.bak')
            if not bak.exists():
                f.rename(bak)
                f.write_text(text, encoding='utf-8')
                changed.append((str(f), detected + '->utf-8 (forced)'))
                print('Force-converted:', f, 'from', detected)
            else:
                backup2 = f.with_suffix(f.suffix + '.bak2')
                f.rename(backup2)
                f.write_text(text, encoding='utf-8')
                changed.append((str(f), detected + '->utf-8 (forced)'))
                print('Force-converted:', f, 'from', detected)
        else:
            if ok:
                changed.append((str(f), enc))
                print('Converted:', f, 'from', enc)
            else:
                print('OK (no change):', f)

    print('\nScanned', scanned, 'files. Converted', len(changed), 'files.')
    if changed:
        print('Files converted:')
        for fn, enc in changed:
            print('-', fn, 'from', enc)

if __name__ == '__main__':
    main()
