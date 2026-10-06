#!/usr/bin/env python3
"""Append reviewed NUS Pathweb views. Requires Pillow; never overwrites existing cases.

python3 scripts/import_pathweb.py --tile-cache .test-results/pathweb-source-tiles

The reviewed URLs, rectangles and hashes are in data/imports/pathweb.json.
Use browser-exported original JPEG tiles when NUS rejects direct downloads.
A tile cache uses <slideId>/<pyramidLevel>/<column>_<row>.jpeg.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
from urllib.request import urlopen
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def tile_bytes(tile, cache, sid, level):
    path = cache / sid / str(level) / f"{tile['column']}_{tile['row']}.jpeg"
    if path.exists():
        raw = path.read_bytes()
    else:
        with urlopen(tile['url'], timeout=30) as response:
            raw = response.read()
        if sha(raw) != tile['sha256']:
            raise ValueError(f"Source changed or download blocked: {tile['url']}; use reviewed browser-exported tiles")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    if sha(raw) != tile['sha256']:
        raise ValueError(f'Source hash mismatch: {path}')
    return raw


def assemble(view, spec, cache):
    x, y, columns, rows = view['tileRect']
    size, overlap = 254, 1
    indexed = {(t['column'], t['row']): t for t in view['tiles']}
    assert len(indexed) == columns * rows
    expected = {(x+i, y+j) for j in range(rows) for i in range(columns)}
    if set(indexed) != expected:
        raise ValueError('Missing or extra tiles; refusing to fill gaps')
    pieces, source_raw = [], []
    for j in range(rows):
        for i in range(columns):
            tile = indexed[x+i, y+j]
            raw = tile_bytes(tile, cache, spec['source']['slideId'], view['pyramidLevel'])
            source_raw.append(raw)
            image = Image.open(io.BytesIO(raw)).convert('RGB')
            if image.size != (tile['width'], tile['height']):
                raise ValueError('Tile dimensions changed')
            left, top = overlap if x+i > 0 else 0, overlap if y+j > 0 else 0
            image = image.crop((left, top, min(left+size, image.width), min(top+size, image.height)))
            if (i < columns-1 and image.width != size) or (j < rows-1 and image.height != size):
                raise ValueError('Unexpected partial tile inside a view')
            pieces.append((i, j, image))
    width = (columns-1)*size + pieces[-1][2].width
    height = (rows-1)*size + pieces[-1][2].height
    output = Image.new('RGB', (width, height))
    for i, j, image in pieces:
        output.paste(image, (i*size, j*size))
    return output, sha(b''.join(source_raw))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tile-cache', type=Path, default=ROOT / '.test-results/pathweb-source-tiles')
    parser.add_argument('--case-ids', nargs='+', help='Append only these reviewed IDs when expanding an existing unit')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'data/imports/pathweb.json').read_text())
    path = ROOT / 'data/cases.json'
    bank = json.loads(path.read_text())
    specs = manifest['cases']
    if args.case_ids:
        requested = set(args.case_ids)
        if not requested <= {s['id'] for s in specs}:
            raise ValueError('Unknown requested Pathweb ID')
        specs = [s for s in specs if s['id'] in requested]
    ids = {c['id'] for c in bank['cases']}
    if ids & {s['id'] for s in specs}:
        raise ValueError('Pathweb cases already exist; refusing to overwrite')
    # Validate and assemble every source before writing any public images or question bank.
    assembled = [(spec, [(v, *assemble(v, spec, args.tile_cache)) for v in spec['views']]) for spec in specs]
    additions = []
    for row, (spec, views) in enumerate(assembled):
        case = {k: v for k, v in spec.items() if k != 'views'}
        case['images'] = []
        sid = spec['source']['slideId']
        folder = ROOT / 'assets/images' / f'pathweb-{sid}'
        folder.mkdir(parents=True, exist_ok=True)
        for index, (view, image, digest) in enumerate(views, 1):
            filename = folder / f'{index:02}.webp'
            image.save(filename, 'WEBP', quality=94, method=6)
            x, y, _, _ = view['tileRect']
            case['images'].append({
                'src': str(filename.relative_to(ROOT)), 'width': image.width, 'height': image.height,
                'sourceImageSha256': digest, 'outputSha256': sha(filename.read_bytes()),
                'extractionMethod': 'deepzoom-native-tiles-overlap-removed',
                'pyramidLevel': view['pyramidLevel'], 'tileSize': 254, 'overlap': 1,
                'bbox': [x*254, y*254, x*254+image.width, y*254+image.height],
                'bboxUnit': 'pixels-at-pyramid-level', 'tiles': view['tiles']
            })
        additions.append(case)
    bank['cases'].extend(additions)
    all_pathweb = [c for c in bank['cases'] if c['source'].get('database') == 'NUS Pathweb']
    contact = Image.new('RGB', (1260, 310*len(all_pathweb)), 'white')
    draw = ImageDraw.Draw(contact)
    for row, case in enumerate(all_pathweb):
        for index, item in enumerate(case['images'], 1):
            preview = Image.open(ROOT / item['src']).convert('RGB')
            preview.thumbnail((410, 280))
            ox, oy = (index-1)*420, row*310
            contact.paste(preview, (ox, oy+25))
            draw.text((ox+8, oy+6), f"{case['id']} / {index:02} / level {item['pyramidLevel']}", fill='black')
    contact.save(ROOT / 'docs/pathweb-contact-sheet.jpg', quality=90)
    path.write_text(json.dumps(bank, ensure_ascii=False, indent=2)+'\n')
    print(f"Added {len(additions)} cases, {sum(len(c['images']) for c in additions)} images")


if __name__ == '__main__':
    main()
