#!/usr/bin/env python3
"""Extract reviewed lesson 4 images and append cases to data/cases.json.

python3 scripts/import_lesson4.py
Requires PyMuPDF and Pillow. Original PDFs are never modified.
"""
import hashlib
import io
import json
from pathlib import Path
import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = '病理學 Micro｜0911 Cell Injury and adaptation (4).pdf'
SPECS = [
    (
        'PA0208',
        [12, 18],
        18,
        [(15, 0), (16, 0), (17, 0)],
        'Large intestine',
        'Melanosis coli',
        '1. Yellow-brown ceroid-laden macrophages in the \nlamina propria',
        ['ceroid-laden macrophages'],
    ),
    (
        'PA0211',
        [23, 30],
        29,
        [(26, 0), (27, 0), (28, 0)],
        'Liver',
        'Hemosiderosis',
        '1. Golden yellow-brown, refractile hemosiderin\naccumulation in hepatocytes',
        ['hemosiderin'],
    ),
    (
        'PA0214',
        [31, 41],
        41,
        [(35, 0), (36, 0), (37, 0), (38, 0), (39, 0), (40, 0)],
        'Liver',
        'Obstructive cholestasis',
        '1. Green-brown bile pigments in hepatocytes and \ndilated canaliculi\n2. Portal edema, prominent ductular reaction & \nneutrophil infiltration (“pericholangitis”) (triad of \nobstructive cholestasis)\n3. Swelling of periportal hepatocytes (“feathery \ndegeneration”)',
        ['Green-brown bile pigments', 'Portal edema', 'ductular reaction', 'neutrophil'],
    ),
    (
        'PA0216',
        [42, 48],
        48,
        [(45, 0), (46, 0), (47, 0)],
        'Liver',
        'Malaria pigment',
        '1. Brown-black malaria pigments in macrophages \nand hepatocytes',
        ['Brown-black malaria pigments'],
    ),
]


def main():
    bank_path = ROOT / 'data/cases.json'
    bank = json.loads(bank_path.read_text())
    ids = {s[0] for s in SPECS}
    existing_ids = {c['id'] for c in bank['cases']}
    if ids & existing_ids:
        raise ValueError(f'Cases already exist: {ids & existing_ids}; refusing to overwrite')

    doc = fitz.open(ROOT / 'pdf' / SOURCE)
    cases = []
    seen = set()

    for cid, pages, answer, selections, organ, diagnosis, description, keywords in SPECS:
        case = dict(
            id=cid,
            lesson=4,
            organ=organ,
            diagnosis=diagnosis,
            description=description,
            notes='',
            keywords=[dict(text=t, accepted=[t]) for t in keywords],
            source=dict(file=SOURCE, answerPage=answer, pageRange=pages),
            images=[],
        )

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

            case['images'].append(
                dict(
                    src=path,
                    page=pn,
                    imageIndex=index,
                    xref=info['xref'],
                    bbox=list(info['bbox']),
                    width=im.width,
                    height=im.height,
                    sourceImageSha256=digest,
                )
            )

        cases.append(case)

    bank['cases'].extend(cases)
    bank_path.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(cases)} cases / {len(seen)} images -> {bank_path}')


if __name__ == '__main__':
    main()
