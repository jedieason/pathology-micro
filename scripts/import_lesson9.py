#!/usr/bin/env python3
"""Extract reviewed lesson 9 images and append cases to data/cases.json.

uv run --with pymupdf --with pillow python3 scripts/import_lesson9.py
Requires PyMuPDF and Pillow. Original PDFs are never modified.
"""
import hashlib
import io
import json
from pathlib import Path
import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = '病理學 Micro｜1005 Microteaching_20261005_Infection (3).pdf'
SPECS = [
    (
        'PA0316',
        [3, 16],
        16,
        [(7, 0), (8, 0), (9, 0), (11, 0), (12, 0), (15, 0)],
        'Lung',
        'Cryptococcosis',
        '1. Numerus round to oval, refractile, thick-walled fungal yeasts\n2. Focal necrosis\n3. Granulomatous inflammation (vaguely-formed granuloma / \nmacrophage infiltration with scattered multinucleated giant \ncells)\n4. Infiltration of lymphocytes and plasma cells \n5. Intraalveolar fibrin deposition\n6. Fibrosis',
        '本題答案表無黃色螢光標記，經使用者授權由 AI 依 Take Home Message 與核心特徵選定必答關鍵字。答案表原文第一項拼寫為「Numerus」，已保留原文並相容「Numerous」。',
        [
            (
                'thick-walled fungal yeasts',
                [
                    'thick-walled fungal yeasts',
                    'fungal yeasts',
                    'refractile, thick-walled fungal yeasts',
                    'thick-walled fungal yeast',
                    'fungal yeast',
                ],
            ),
            (
                'Granulomatous inflammation',
                [
                    'Granulomatous inflammation',
                    'granulomatous',
                ],
            ),
        ],
        'ai-selected-user-authorized',
        None,
        None,
    ),
    (
        'PA0302',
        [17, 29],
        28,
        [(22, 0), (23, 0), (24, 0), (25, 0), (26, 0), (27, 0)],
        'Lung',
        'Pneumocystis jirovecii pneumonia',
        '1. Foamy, granular, eosinophilic exudate in the alveolar \nspaces\n2. Interstitial thickening and inflammation\n3. Other finding: focal ossification',
        '',
        [
            (
                'Foamy, granular, eosinophilic exudate',
                [
                    'Foamy, granular, eosinophilic exudate',
                    'foamy, eosinophilic exudate',
                    'foamy eosinophilic exudate',
                    'eosinophilic foamy exudate',
                    'foamy exudate',
                ],
            ),
        ],
        'source-yellow-highlight',
        [
            'Pneumocystis jirovecii pneumonia',
            'Pneumocystis jirovecii pneumonia (PJP)',
            'PJP',
            'Pneumocystis pneumonia',
        ],
        None,
    ),
    (
        'PA0206',
        [30, 40],
        40,
        [(35, 0), (36, 0), (36, 1), (37, 0), (39, 0)],
        'Appendix',
        'Amebiasis',
        '1. Round microorganisms\nFoamy cytoplasm\nRound, eccentric nucleus\nIngested red blood cells\n2. Ulcer with inflamed granulation tissue and acute suppurative \ninflammation (transmural neutrophil infiltration)',
        '答案表註記：←2025年解剖病理專科片試。',
        [
            (
                'Ingested red blood cells',
                [
                    'Ingested red blood cells',
                    'Ingested RBCs',
                    'Ingested red blood cell',
                ],
            ),
        ],
        'source-yellow-highlight',
        None,
        None,
    ),
    (
        'PA0354',
        [41, 55],
        55,
        [(46, 0), (48, 0), (51, 0), (52, 0), (54, 0)],
        'Oral cavity (mouth floor)',
        'Herpes virus infection',
        '1. Cytopathic effects compatible with herpes infection\nMultinucleation\nMargination of chromatin\nMolding of nuclei\n2. Ulcer with neutrophil infiltration and necrotic debris',
        '投影片註明「更新 PA0354 (145)」。原教材答案表塗黃加底線「herpes infection」，經使用者指示擴充 3M 病毒病效應（Multinucleation、Margination of chromatin、Molding of nuclei）為必答關鍵字。作答 Oral cavity、mouth floor、HSV infection 均可。',
        [
            (
                'herpes infection',
                [
                    'herpes infection',
                ],
            ),
            (
                'Multinucleation',
                [
                    'Multinucleation',
                    'multinucleated',
                ],
            ),
            (
                'Margination of chromatin',
                [
                    'Margination of chromatin',
                    'Chromatin margination',
                ],
            ),
            (
                'Molding of nuclei',
                [
                    'Molding of nuclei',
                    'nuclear molding',
                    'molding',
                ],
            ),
        ],
        'source-yellow-highlight-and-user-expanded',
        [
            'Herpes virus infection',
            'Herpes simplex virus infection',
            'HSV infection',
            'Herpes infection',
        ],
        [
            'Oral cavity (mouth floor)',
            'Oral cavity',
            'mouth floor',
            'Oral cavity, mouth floor',
        ],
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
            lesson=9,
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
