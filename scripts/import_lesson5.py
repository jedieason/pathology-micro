#!/usr/bin/env python3
"""Extract reviewed lesson 5 images and append cases to data/cases.json.

python3 scripts/import_lesson5.py
Requires PyMuPDF and Pillow. Original PDFs are never modified.
"""
import hashlib
import io
import json
from pathlib import Path
import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'Microteaching_20260918 Inflammation.pdf'
SPECS = [
    (
        'PA0270',
        [14, 28],
        28,
        [(18, 0), (19, 0), (20, 0), (23, 2), (26, 0), (27, 0)],
        'Appendix',
        'Acute suppurative appendicitis',
        '1. Mucosal and mural neutrophil infiltration, involving muscularis propria\n2. Mucosal ulceration\n3. Luminal and mural abscess\n4. Fibrinous inflammation on the serosal surface',
        '',
        ['Mucosal and mural neutrophil infiltration, involving muscularis propria'],
        'original-yellow-highlight',
    ),
    (
        'PA0044',
        [29, 45],
        45,
        [(31, 0), (32, 0), (36, 0), (37, 0), (40, 0), (43, 0)],
        'Maxillary sinus',
        'Chronic sinusitis',
        '1. Submucosal mixed inflammatory cell infiltrate of \nlymphocytes, plasma cells, and eosinophils\n2. Submucosal edema\n3. Basement membrane thickening (本片僅局部有)',
        '*Organ: Maxillary sinus（教材附註：“Nasal cavity / paranasal sinus / sinonasal tract”）',
        ['mixed', 'edema'],
        'original-yellow-highlight',
    ),
    (
        'PA0143',
        [46, 57],
        57,
        [(49, 0), (50, 0), (51, 0), (52, 0), (53, 0), (56, 0)],
        'Skin',
        'Suture granuloma',
        '1. Center: Suture\n2. Periphery: Granulomatous inflammation\n   1. (Epithelioid) Macrophages/histiocytes\n   2. Multinucleated giant cells\n   3. Lymphocytes, plasma cells\n   4. Fibrosis/scar\n3. Other finding: Fat necrosis',
        '',
        ['Center: Suture', 'Periphery: Granulomatous inflammation'],
        'original-yellow-highlight',
    ),
    (
        'PA0202',
        [58, 73],
        73,
        [(63, 0), (64, 0), (66, 0), (67, 0), (69, 0), (71, 0)],
        'Stomach',
        'Chronic ulcer',
        '1. Mucosa defect with fibrinous necrosis and \nneutrophil\n2. Granulation tissue\n3. Fibrosis/scar\n4. Other finding: Fibrinous inflammation on the serosal \nsurface',
        '本題必答關鍵字由 AI 選定，非原教材螢光標記（使用者授權）。',
        ['fibrinous necrosis', 'Granulation tissue', 'Fibrosis/scar'],
        'ai-selected-user-authorized',
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

    for cid, pages, answer, selections, organ, diagnosis, description, notes, keywords, kw_basis in SPECS:
        src_meta = dict(file=SOURCE, answerPage=answer, pageRange=pages)
        if kw_basis == 'ai-selected-user-authorized':
            src_meta['keywordBasis'] = 'ai-selected-user-authorized'

        case = dict(
            id=cid,
            lesson=5,
            organ=organ,
            diagnosis=diagnosis,
            description=description,
            notes=notes,
            keywords=[dict(text=t, accepted=[t]) for t in keywords],
            source=src_meta,
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
