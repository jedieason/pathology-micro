#!/usr/bin/env python3
"""Extract reviewed lesson 8 images and append cases to data/cases.json.

uv run --with pymupdf --with pillow python3 scripts/import_lesson8.py
Requires PyMuPDF and Pillow. Original PDFs are never modified.
"""
import hashlib
import io
import json
from pathlib import Path
import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = '病理學 Micro｜1002 Infection (2).pdf'
SPECS = [
    (
        'PA0251',
        [3, 13],
        13,
        [(7, 0), (8, 0), (9, 0), (10, 0)],
        'Ovary (此片被病灶佔滿，其實沒有可供辨認為卵巢之組織)',
        'Actinomycosis',
        '1. Sulfur granules composed of clumped colonies of bacteria \nin center with eosinophilic periphery with club-like \nprojections (Splendore-Hoeppli phenomenon)\n2. Acute and chronic inflammation with abscess formation\n3. May granulomatous inflammation (suppurative \ngranulomatous inflammation)',
        '第 2 頁目錄器官為 Ovary，答案表附註「此片被病灶佔滿，其實沒有可供辨認為卵巢之組織」，作答 Ovary 即可。',
        [
            (
                'Sulfur granules',
                [
                    'Sulfur granules',
                    'Sulfur granule',
                ],
            ),
            (
                'Splendore-Hoeppli phenomenon',
                [
                    'Splendore-Hoeppli phenomenon',
                    'Splendore-Hoeppli',
                    'Splendore Hoeppli phenomenon',
                    'Splendore Hoeppli',
                ],
            ),
        ],
        'source-yellow-highlight',
        None,
        [
            'Ovary',
            'Ovary (此片被病灶佔滿，其實沒有可供辨認為卵巢之組織)',
        ],
    ),
    (
        'PA0022',
        [14, 30],
        30,
        [(18, 0), (20, 0), (22, 0), (23, 0), (25, 0), (29, 0)],
        'Spleen',
        'Mucormycosis',
        '1. Aseptate hyphae with wide-angle branching\n2. Caseating granulomatous inflammation',
        '答案表以粗底線標記 Aseptate 及 wide-angle，Take Home Message 總結重點為 Aseptate hyphae with wide-angle branching。',
        [
            (
                'Aseptate',
                [
                    'Aseptate',
                    'Aseptate hyphae',
                    'non-septate',
                    'nonseptate',
                    'aseptate',
                ],
            ),
            (
                'wide-angle branching',
                [
                    'wide-angle branching',
                    'wide angle branching',
                    'wide-angle',
                    'wide angle',
                    'wide-angled branching',
                    'wide angled branching',
                    'right-angle branching',
                    'right angle branching',
                ],
            ),
        ],
        'source-underlined-take-home-message',
        None,
        None,
    ),
    (
        'PA0015',
        [31, 43],
        43,
        [(35, 0), (36, 0), (37, 0), (38, 0), (39, 0), (40, 0)],
        'Lung',
        'Aspergillosis',
        '1. Fungal hyphae with septa and acute-angle branching\n2. Chronic inflammation\n3. Fibrosis\n4. Anthracosis',
        '答案表第一項具黃色螢光填色與粗底線覆蓋。',
        [
            (
                'Fungal hyphae with septa and acute-angle branching',
                [
                    'Fungal hyphae with septa and acute-angle branching',
                    'Fungal hyphae with septa and acute angle branching',
                    'septa and acute-angle branching',
                    'septa and acute angle branching',
                    'septate hyphae with acute-angle branching',
                    'septate hyphae with acute angle branching',
                    'acute-angle branching',
                    'acute angle branching',
                ],
            ),
        ],
        'source-yellow-highlight',
        None,
        None,
    ),
    (
        'PA0201',
        [45, 56],
        56,
        [(50, 0), (51, 0), (52, 0), (53, 0), (54, 0), (55, 0)],
        'Esophagus',
        'Candidiasis',
        '1. Fungal yeasts and pseudohyphae\n2. Hyperkeratosis, parakeratosis\n3. Chronic inflammation\n4. Bacterial clumps',
        '答案表無黃色螢光標記，必答關鍵字依 Take Home Message 粗底線重點（Yeasts & pseudohyphae）及玻片教學特徵選定。',
        [
            (
                'Fungal yeasts and pseudohyphae',
                [
                    'Fungal yeasts and pseudohyphae',
                    'yeasts and pseudohyphae',
                    'yeast and pseudohyphae',
                    'yeasts & pseudohyphae',
                    'pseudohyphae and yeasts',
                    'pseudohyphae',
                    'pseudohypha',
                ],
            ),
        ],
        'take-home-message-underlined',
        None,
        None,
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

    for item in SPECS:
        cid, pages, answer, selections, organ, diagnosis, description, notes, keywords, kw_basis = item[:10]
        accepted_diag = item[10] if len(item) > 10 and item[10] else None
        accepted_organ = item[11] if len(item) > 11 and item[11] else None
        src_meta = dict(file=SOURCE, answerPage=answer, pageRange=pages)
        if kw_basis != 'source-yellow-highlight':
            src_meta['keywordBasis'] = kw_basis

        case = dict(
            id=cid,
            lesson=8,
            organ=organ,
            diagnosis=diagnosis,
            description=description,
            notes=notes,
            keywords=[dict(text=t, accepted=acc) for t, acc in keywords],
            source=src_meta,
            images=[],
        )
        if accepted_diag:
            case['acceptedDiagnosis'] = accepted_diag
        if accepted_organ:
            case['acceptedOrgan'] = accepted_organ

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

    # Insert lesson 8 before any higher lesson (e.g. lesson 9) if present
    insert_idx = len(bank['cases'])
    for idx, c in enumerate(bank['cases']):
        if c.get('lesson', 0) > 8:
            insert_idx = idx
            break

    bank['cases'][insert_idx:insert_idx] = cases
    bank_path.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(cases)} cases / {len(seen)} images -> {bank_path}')


if __name__ == '__main__':
    main()
