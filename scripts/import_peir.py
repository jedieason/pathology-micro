#!/usr/bin/env python3
"""Download caption-confirmed PEIR originals and append one question per unique image.

Requires Pillow. No tests or browser automation are run.
python3 scripts/import_peir.py --manifest data/imports/peir.json

Use --manifest .test-results/peir/prepared.json for the initial caption selection.
Existing case IDs stop the import; original JPEGs and API replies remain in an ignored cache.
"""
import argparse
import hashlib
import io
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def fetch(url):
    for attempt in range(3):
        try:
            with urlopen(url, timeout=45) as response:
                return response.read()
        except Exception:
            if attempt == 2:
                raise
            time.sleep(1)


def download(case, cache):
    photo = case['image']
    pid = photo['sourceImageId']
    info_path = cache / f'{pid}-info.json'
    if not info_path.exists():
        info_path.write_bytes(fetch('https://peir.path.uab.edu/library/ws.php?' + urlencode({
            'format': 'json', 'method': 'pwg.images.getInfo', 'image_id': pid})))
    info = json.loads(info_path.read_text())
    if info.get('stat') != 'ok':
        raise ValueError(f'PEIR metadata unavailable for {pid}')
    info = info['result']
    if info['element_url'] != photo['url'] or info['comment'] != case['source']['sourceTitle']:
        raise ValueError(f'Source metadata changed for {pid}; re-review caption before importing')
    raw_path = cache / f'{pid}.jpg'
    if not raw_path.exists():
        raw_path.write_bytes(fetch(photo['url']))
    raw = raw_path.read_bytes()
    if photo.get('sourceImageSha256') and digest(raw) != photo['sourceImageSha256']:
        raise ValueError(f'Source image changed for {pid}')
    image = Image.open(io.BytesIO(raw)).convert('RGB')
    if image.size != (photo['sourceWidth'], photo['sourceHeight']):
        raise ValueError(f'Source dimensions changed for {pid}')
    original_size = image.size
    image.thumbnail((2000, 2000))
    output = io.BytesIO()
    image.save(output, 'WEBP', quality=94, method=6)
    photo.update(sourceImageSha256=digest(raw), outputSha256=digest(output.getvalue()),
                 width=image.width, height=image.height, sourceWidth=original_size[0], sourceHeight=original_size[1],
                 extractionMethod='original-jpeg-to-webp-no-crop')
    case['source']['author'] = info.get('author') or 'PEIR Digital Library'
    case['source']['attribution'] = 'PEIR Digital Library, University of Alabama at Birmingham / ' + case['source']['author']
    case['source']['sourceImageName'] = info.get('name', str(pid))
    return case, output.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=ROOT / 'data/imports/peir.json')
    parser.add_argument('--cache', type=Path, default=ROOT / '.test-results/peir/raw')
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    bank_path = ROOT / 'data/cases.json'
    bank = json.loads(bank_path.read_text())
    if {c['id'] for c in bank['cases']} & {c['id'] for c in manifest['cases']}:
        raise ValueError('PEIR case IDs already exist; refusing to overwrite')
    args.cache.mkdir(parents=True, exist_ok=True)
    results = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        pending = [pool.submit(download, c, args.cache) for c in manifest['cases']]
        for n, future in enumerate(as_completed(pending), 1):
            results.append(future.result())
            if n % 20 == 0:
                print(f'Downloaded {n} / {len(pending)} original images', flush=True)
    # All downloads have completed before publishing assets or appending the bank.
    seen = {}
    additions, unique_specs, duplicates = [], [], []
    for spec, output in sorted(results, key=lambda item: item[0]['image']['sourceImageId']):
        photo = spec['image']
        image_hash = photo['sourceImageSha256']
        if image_hash in seen:
            duplicates.append({'imageId': photo['sourceImageId'], 'duplicateOf': seen[image_hash], 'url': photo['url']})
            continue
        seen[image_hash] = photo['sourceImageId']
        relative = f"assets/images/peir/{photo['sourceImageId']:05}.webp"
        destination = ROOT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(output)
        photo['src'] = relative
        case = {k: v for k, v in spec.items() if k != 'image'}
        case['images'] = [photo]
        additions.append(case)
        unique_specs.append(spec)
    manifest['cases'] = unique_specs
    manifest['duplicates'] = duplicates
    (ROOT / 'data/imports/peir.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    # Re-read before the append so source downloads never replace intervening bank additions.
    bank = json.loads(bank_path.read_text())
    if {c['id'] for c in bank['cases']} & {c['id'] for c in additions}:
        raise ValueError('PEIR IDs were added during download; refusing to overwrite the bank')
    bank['cases'].extend(additions)
    bank_path.write_text(json.dumps(bank, ensure_ascii=False, indent=2)+'\n')
    print(f'Added {len(additions)} PEIR questions / images; omitted {len(duplicates)} byte-identical duplicates', flush=True)


if __name__ == '__main__':
    main()
