#!/usr/bin/env python3
"""Extract reviewed lesson 6 images and append cases to data/cases.json.

python3 scripts/import_lesson6.py
Requires PyMuPDF and Pillow. Original PDFs are never modified.
"""
import hashlib
import io
import json
from pathlib import Path
import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = '病理學 Micro｜0923 Hemodynamic derangement.pdf'
SPECS = [
    (
        'PA0008',
        [4, 16],
        16,
        [(15, 0), (10, 0), (11, 1), (12, 0), (15, 1)],
        'Spleen',
        'Congestive splenomegaly',
        '1. Red pulp expansion\n2. Red pulp congestion (& fibrosis)\n3. Dilated sinusoids',
        '本題必答關鍵字由 AI 選定，非原教材答案表螢光標記（使用者授權）。',
        [
            ('Red pulp expansion', ['Red pulp expansion']),
            ('Red pulp congestion', ['Red pulp congestion']),
            ('Dilated sinusoids', ['Dilated sinusoids']),
        ],
        'ai-selected-user-authorized',
    ),
    (
        'PA0059',
        [17, 30],
        30,
        [(20, 0), (21, 0), (22, 0), (25, 0), (26, 0), (28, 0)],
        'Anus',
        'Hemorrhoid',
        '1. Dilated and congested submucosal vessels\n2. Thrombosis\n3. Organization & recanalization',
        '本題必答關鍵字由 AI 選定；Organization & recanalization 亦接受 and 拼寫。',
        [
            ('Dilated and congested submucosal vessels', ['Dilated and congested submucosal vessels']),
            ('Thrombosis', ['Thrombosis']),
            ('Organization & recanalization', ['Organization & recanalization', 'Organization and recanalization']),
        ],
        'ai-selected-user-authorized',
    ),
    (
        'PA0076',
        [31, 38],
        38,
        [(35, 0), (36, 0), (37, 0)],
        'Liver',
        'Nutmeg liver',
        '1. Centrilobular [zone 3] congestion (本片主要finding)\n2. Centrilobular [zone 3] hepatocyte necrosis (本片僅局部有)',
        '本題必答關鍵字由 AI 選定，非原教材答案表螢光標記（使用者授權）。',
        [
            ('Centrilobular [zone 3] congestion', ['Centrilobular [zone 3] congestion', 'Centrilobular congestion', 'zone 3 congestion']),
            ('Centrilobular [zone 3] hepatocyte necrosis', ['Centrilobular [zone 3] hepatocyte necrosis', 'Centrilobular hepatocyte necrosis', 'Centrilobular necrosis', 'zone 3 necrosis', 'hepatocyte necrosis']),
        ],
        'ai-selected-user-authorized',
    ),
    (
        'PA0215',
        [39, 51],
        51,
        [(41, 0), (43, 0), (44, 0), (46, 0), (47, 0), (49, 0)],
        'Liver',
        'Cardiac sclerosis',
        '1. Centrilobular congestion\n2. Centrilobular hepatocyte fibrosis',
        '本題必答關鍵字由 AI 選定；Centrilobular hepatocyte fibrosis 亦接受教材投影片標記之 Centrilobular fibrosis。',
        [
            ('Centrilobular congestion', ['Centrilobular congestion']),
            ('Centrilobular hepatocyte fibrosis', ['Centrilobular hepatocyte fibrosis', 'Centrilobular fibrosis']),
        ],
        'ai-selected-user-authorized',
    ),
    (
        'PA0096',
        [52, 63],
        63,
        [(57, 0), (58, 0), (59, 0), (60, 0), (61, 0), (62, 0)],
        'Kidney',
        'Infarct/Infarction',
        '1. Wedge-shaped coagulative necrosis\n- acute tubular necrosis\n2. Thrombosis',
        '診斷依答案表保留原文 Infarct/Infarction。本題必答關鍵字由 AI 依核心特徵選定。',
        [
            ('coagulative necrosis', ['coagulative necrosis', 'Wedge-shaped coagulative necrosis']),
            ('acute tubular necrosis', ['acute tubular necrosis']),
            ('Thrombosis', ['Thrombosis']),
        ],
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
            lesson=6,
            organ=organ,
            diagnosis=diagnosis,
            description=description,
            notes=notes,
            keywords=[dict(text=t, accepted=acc) for t, acc in keywords],
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
