#!/usr/bin/env python3
"""Extract reviewed lesson 7 images and append cases to data/cases.json.

python3 scripts/import_lesson7.py
Requires PyMuPDF and Pillow. Original PDFs are never modified.
"""
import hashlib
import io
import json
from pathlib import Path
import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = '病理學 Micro｜Infection (1).pdf'
SPECS = [
    (
        'PA0255',
        [5, 23],
        21,
        [(11, 0), (13, 0), (15, 0), (19, 0), (20, 0)],
        'Skin',
        'Condyloma acuminatum',
        '1. Papillomatosis\n2. Koilocytosis\n3. Acanthosis\n4. Hyperkeratosis\n5. Parakeratosis',
        '←2025年解剖病理專科考試。本題必答關鍵字由 AI 依答案表全部病理特徵選定（使用者授權）。',
        [
            ('Papillomatosis', ['Papillomatosis']),
            ('Koilocytosis', ['Koilocytosis']),
            ('Acanthosis', ['Acanthosis']),
            ('Hyperkeratosis', ['Hyperkeratosis']),
            ('Parakeratosis', ['Parakeratosis']),
        ],
        'ai-selected-user-authorized',
    ),
    (
        'PA0271',
        [24, 33],
        33,
        [(27, 0), (28, 1), (29, 0), (29, 1), (32, 0)],
        'Skin',
        'Molluscum contagiosum',
        '1. A cup-like lesion with a crater\n2. Epidermal hyperplasia\n3. Molluscum bodies (Henderson-Patterson bodies) in \nthe crater: large, eosinophilic to basophilic intracytoplasmic \ninclusions that push aside nucleus',
        '',
        [
            (
                'Molluscum bodies (Henderson-Patterson bodies)',
                [
                    'Molluscum bodies (Henderson-Patterson bodies)',
                    'Molluscum bodies',
                    'Henderson-Patterson bodies',
                ],
            ),
        ],
        'source-yellow-highlight',
    ),
    (
        'PA0218',
        [34, 43],
        43,
        [(37, 0), (40, 0), (41, 0), (42, 0), (42, 1)],
        'Kidney',
        'Cytomegalovirus (CMV) infection or Cytomegaloviral (CMV) nephritis',
        '1. Infected cells\n- Cellular and nuclear enlargement\n- Large intranuclear basophilic inclusions with halos/haloes\n- Small cytoplasmic basophilic inclusions\n2. Chronic inflammation \n[此片是慢性發炎，其它案例可能以急性發炎為主要表現]',
        '本題必答關鍵字由 AI 依包含體特徵選定（使用者授權）。作答 Cytomegalovirus (CMV) infection、Cytomegaloviral (CMV) nephritis 或其簡稱均判定正確。',
        [
            (
                'Large intranuclear basophilic inclusions',
                [
                    'Large intranuclear basophilic inclusions',
                    'intranuclear basophilic inclusions',
                    'intranuclear inclusions',
                    'intranuclear basophilic inclusion',
                    'intranuclear inclusion',
                ],
            ),
            (
                'Small cytoplasmic basophilic inclusions',
                [
                    'Small cytoplasmic basophilic inclusions',
                    'cytoplasmic basophilic inclusions',
                    'cytoplasmic inclusions',
                    'cytoplasmic basophilic inclusion',
                    'cytoplasmic inclusion',
                ],
            ),
        ],
        'ai-selected-user-authorized',
        [
            'Cytomegalovirus (CMV) infection',
            'Cytomegaloviral (CMV) nephritis',
            'Cytomegalovirus infection',
            'Cytomegaloviral nephritis',
            'CMV infection',
            'CMV nephritis',
            'Cytomegalovirus (CMV) infection or Cytomegaloviral (CMV) nephritis',
        ],
    ),
    (
        'PA0306',
        [44, 59],
        57,
        [(48, 0), (49, 0), (50, 0), (52, 0), (55, 0), (56, 0)],
        'Heart valve',
        'Infective endocarditis',
        '1. Valve destruction with necrosis\n2. Vegetation: composed of fibrin, bacterial clumps, and \ninflammatory infiltrate (neutrophilic or lymphohistiocytic)\n3. Inflamed granulation tissue\n4. (In chronic lesion): organization and calcification',
        '第 4 頁目錄編號為 PA0306 (4)，投影片內文與切片來源標記為 PA0001 (4)。答案表附註「考試寫 Heart valve 即可（哪個瓣膜無法從組織學判定）」，作答 Heart valve、Heart、Mitral valve 或 Aortic valve 均可。',
        [
            ('Vegetation', ['Vegetation', 'Vegetation:']),
        ],
        'source-yellow-highlight',
        None,
        ['Heart valve', 'Heart', 'Mitral valve', 'Aortic valve'],
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
        if kw_basis == 'ai-selected-user-authorized':
            src_meta['keywordBasis'] = 'ai-selected-user-authorized'

        case = dict(
            id=cid,
            lesson=7,
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

    bank['cases'].extend(cases)
    bank_path.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(cases)} cases / {len(seen)} images -> {bank_path}')


if __name__ == '__main__':
    main()
