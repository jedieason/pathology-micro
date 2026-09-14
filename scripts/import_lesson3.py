#!/usr/bin/env python3
"""Extract reviewed lesson 3 images; merge only with an explicitly supplied keyword map.

python3 scripts/import_lesson3.py --keywords path/to/approved-keywords.json
Without --keywords, writes a pending bank outside the live question bank.
Requires PyMuPDF and Pillow. Original PDFs are never modified.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'Microteaching_20260914 Cell Injury and adaptation (3).pdf'
SPECS = [
    ('PA0220', [2, 12], 12, [(8, 0), (9, 0), (10, 0), (11, 0)],
     'Prostate', 'Nodular hyperplasia',
     '1. Nodules of cystically dilated hyperplastic glands'),
    ('PA0074', [13, 22], 22, [(19, 0), (20, 0), (21, 0)],
     'Liver', 'Steatosis (fatty change)', '1. Lipid droplets in hepatocytes'),
    ('PA0017', [23, 32], 32, [(26, 0), (27, 0), (29, 0), (31, 0)],
     'Lung', 'Anthracosis', '1. Dark black pigments in macrophages/histiocytes'),
    ('PA0144', [34, 48], 48, [(42, 0), (43, 2), (44, 1), (45, 0), (45, 1), (47, 0)],
     'Skin', 'Intradermal (melanocytic) nevus',
     '1. Nests & cords of proliferative melanocytes\n2. Brown-black melanin pigmentation\n3. (Adipocytic metaplasia)'),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--keywords', type=Path)
    parser.add_argument('--pending', type=Path, default=ROOT / 'data/lesson3.pending.json')
    args = parser.parse_args()
    approved = json.loads(args.keywords.read_text()) if args.keywords else None
    bank_path = ROOT / 'data/cases.json'
    bank = json.loads(bank_path.read_text())
    ids = {s[0] for s in SPECS}
    if approved is not None:
        if set(approved) != ids:
            raise ValueError('Keyword map must contain exactly the four reviewed case IDs')
        if ids & {c['id'] for c in bank['cases']}:
            raise ValueError('Cases already exist; refusing to overwrite existing answers')
        for cid, _, _, _, _, _, description in SPECS:
            terms = approved[cid]
            if not isinstance(terms, list) or not terms or any(not isinstance(t, str) or not t.strip() or t not in description for t in terms):
                raise ValueError(f'{cid}: provide nonempty exact phrases from the answer table')
    doc = fitz.open(ROOT / 'pdf' / SOURCE)
    cases = []
    seen = set()
    for cid, pages, answer, selections, organ, diagnosis, description in SPECS:
        case = dict(id=cid, lesson=3, organ=organ, diagnosis=diagnosis,
                    description=description, notes='', keywords=[],
                    source=dict(file=SOURCE, answerPage=answer, pageRange=pages), images=[])
        if approved is not None:
            case['keywords'] = [dict(text=t, accepted=[t]) for t in approved[cid]]
            case['notes'] = '本題必答關鍵字由 AI 選定，非原教材螢光標記（使用者授權）。'
            case['source']['keywordBasis'] = 'ai-selected-user-authorized'
        for n, (pn, index) in enumerate(selections, 1):
            info = doc[pn - 1].get_image_info(xrefs=True)[index]
            raw = doc.extract_image(info['xref'])['image']
            digest = hashlib.sha256(raw).hexdigest()
            if digest in seen:
                raise ValueError(f'Duplicate image: {cid} page {pn}')
            seen.add(digest)
            im = Image.open(io.BytesIO(raw)).convert('RGB')
            im.thumbnail((2000, 2000), Image.Resampling.LANCZOS)
            path = f'assets/images/{cid.lower()}/{n:02d}.webp'
            (ROOT / path).parent.mkdir(parents=True, exist_ok=True)
            im.save(ROOT / path, 'WEBP', quality=94, method=6)
            case['images'].append(dict(src=path, page=pn, imageIndex=index,
                xref=info['xref'], bbox=list(info['bbox']), width=im.width,
                height=im.height, sourceImageSha256=digest))
        cases.append(case)
    if approved is None:
        output = dict(status='pending-description-keywords', cases=cases)
        destination = args.pending
    else:
        bank['cases'].extend(cases)
        output, destination = bank, bank_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(cases)} cases / {len(seen)} images -> {destination}')


if __name__ == '__main__':
    main()
