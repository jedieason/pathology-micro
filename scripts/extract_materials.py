#!/usr/bin/env python3
"""Rebuild the reviewed question bank from the two original PDFs. Requires PyMuPDF + Pillow."""
import hashlib, io, json
from pathlib import Path
import fitz
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
 'Microteaching_20260910_Cell Injury and adaptation (1) (2).pdf',
 'Microteaching_20260911_Cell Injury and adaptation (2)_0910renew (1).pdf',
]
# Reviewed 1-based PDF pages; image index refers to get_image_info(xrefs=True).
CASES = [
 dict(id='PA0097', lesson=1, answerPage=21, pages=[15,16,17,19,20], organ='Kidney', diagnosis='Acute tubular necrosis',
 description='1. Tubular epithelial coagulative necrosis\n   ① Dead cells with preserved cellular outlines\n   ② Cytoplasmic eosinophilia, may glassy appearance, may vacuolated\n   ③ Nuclear changes: karyolysis, pyknosis, karyorrhexis\n2. An Inflammatory infiltrate',
 notes='*Acute tubular injury/necrosis\nmainly in proximal convoluted tubule(本片distal也很嚴重)', keywords=['coagulative necrosis','preserved cellular outlines']),
 dict(id='PA0313', lesson=1, answerPage=29, pages=[26,27,28,30], organ='Intestine/colon', acceptedOrgan=['Intestine', 'colon', 'Intestine/colon'], diagnosis='Necrotizing enterocolitis',
 description='1. Coagulative necrosis with hemorrhage – mucosal and transmural (impending perforation)\n2. Chronic changes: strictures, crypt distortion, reactive epithelial cells (本片無)',notes='器官依答案表保留原文 Intestine/colon；作答 Intestine 或 colon 均可。',keywords=['Coagulative necrosis with hemorrhage']),
 dict(id='PA0335', lesson=2, answerPage=15, pages=[9,10,11,12,13,14], organ='Heart', diagnosis='Myocardial infarction, healed',
 description='1. Multifocal fibrosis replacing myocytes (比較久遠的變化, remote)\n   With slightly increased mononuclear inflammatory cells\n2. Granulation tissue, focal (不太好找; 比較近期的變化, recent)\n   Neovascularization (capillary proliferation), hemorrhage\n3. Myocyte vacuolization\n   Especially subendocardial areas (sublethal ischemic changes)\n4. Hypertrophic changes of cardiomyocytes (病人的背景)\n   Increased cell and nuclear size',notes='',keywords=['fibrosis','Granulation tissue','vacuolization','Hypertrophic']),
 dict(id='PA0162', lesson=2, answerPage=31, pages=[22,24,27,29], organ='Cerebrum', diagnosis='Encephalomalacia',
 description='1. Focal liquefactive necrosis\n   Loss of the original structure → Loosening of the tissue\n2. Neutrophil infiltration or “microabscces” may be present\n3. Reactive gliosis\n4. Gitter cells\n   Histiocytes with phagocytosed myelin',notes='',keywords=['liquefactive necrosis','Loosening','microabscces']),
 dict(id='PA0198', lesson=2, answerPage=48, pages=[40,41,42,44,46], organ='Lung', diagnosis='Caseating granulomatous inflammation',
 description='1. Center: Caseous necrosis\n   A structureless collection of lysed cells & amorphous granular debris\n2. Periphery: Granulomatous inflammation\n   ① Epithelioid macrophages\n   ② Langhans giant cells\n   ③ Lymphocytes\n   ④ Fibrosis',notes='',keywords=['Center: Caseous necrosis','Periphery: Granulomatous inflammation']),
 dict(id='PA0081', lesson=2, answerPage=63, pages=[54,57,58,59,61,62], organ='Pancreas', diagnosis='Fat necrosis',
 description='1. Shadowy outlines of necrotic fat cells\n2. Basophilic calcium deposits\n3. Inflammation',
 notes='*本片有 Acute interstitial pancreatitis (traumatic pancreatitis)\nacute inflammatory cell infiltrate into pancreatic parenchyma\nmostly in outer part\nhemorrhage (RBC and fibrin)\ntrauma: by clinical history', keywords=['Shadowy outlines','calcium']),
]

def main():
 docs=[fitz.open(ROOT / s) for s in SOURCES]
 out=[]
 for spec in CASES:
  case={k:v for k,v in spec.items() if k not in ('pages','answerPage')}
  case['keywords']=[{'text':k,'accepted':[k,'microabscess'] if k=='microabscces' else [k]} for k in spec['keywords']]
  case['source']={'file':SOURCES[spec['lesson']-1], 'answerPage':spec['answerPage']}
  case['images']=[]
  for num,pn in enumerate(spec['pages'],1):
   doc=docs[spec['lesson']-1]; page=doc[pn-1]; info=page.get_image_info(xrefs=True)[0]
   raw=doc.extract_image(info['xref'])['image']; im=Image.open(io.BytesIO(raw)).convert('RGB')
   im.thumbnail((2000,2000),Image.Resampling.LANCZOS)
   path=f'assets/images/{spec["id"].lower()}/{num:02d}.webp'
   (ROOT/path).parent.mkdir(parents=True,exist_ok=True)
   im.save(ROOT/path,'WEBP',quality=94,method=6)
   case['images'].append({'src':path,'page':pn,'imageIndex':0,'xref':info['xref'],'bbox':list(info['bbox']),'width':im.width,'height':im.height,'sourceImageSha256':hashlib.sha256(raw).hexdigest()})
  out.append(case)
 bank={'version':1,'title':'Cell injury and adaptation','cases':out}
 (ROOT/'data/cases.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
 print(f'Extracted {len(out)} cases, {sum(len(c["images"]) for c in out)} images.')
if __name__=='__main__': main()
