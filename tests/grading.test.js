import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {grade,normalize,highlightedParts,formatScore} from '../assets/grading.js';
const {cases}=JSON.parse(readFileSync(new URL('../data/cases.json',import.meta.url)));
test('normalization ignores case, spacing, punctuation and fullwidth differences',()=>{
  assert.equal(normalize(' Ｋｉｄｎｅｙ!\n'), 'kidney');
  assert.equal(normalize('Intestine / COLON'),normalize('Intestine/colon'));
});
test('exact organ and diagnosis do not accept unauthorized partial answers or synonyms',()=>{
  const heart=cases[2];assert.equal(grade(heart,{diagnosis:'Myocardial infarction, remote'}).diagnosis,false);
  assert.equal(grade(heart,{diagnosis:'MYOCARDIAL-infarction HEALED!!!'}).diagnosis,true);
  const c=cases[1];assert.equal(grade(c,{organ:'stomach',diagnosis:'Necrotizing enterocolitis',description:''}).organ,false);
});
test('all three fields are scored independently',()=>{
 const c=cases[0]; const r=grade(c,{organ:'wrong',diagnosis:c.diagnosis,description:c.description});
 assert.deepEqual([r.organ,r.diagnosis,r.description],[false,true,true]);
});
test('each highlighted phrase is mandatory, including center/periphery',()=>{
 for(const c of cases){
  const full=c.keywords.map(k=>k.text).join('; ');
  assert.equal(grade(c,{description:full.toUpperCase()}).description,true,c.id);
  for(let i=0;i<c.keywords.length;i++){
   const r=grade(c,{description:c.keywords.filter((_,j)=>i!==j).map(k=>k.text).join('; ')});
   assert.equal(r.description,false,c.id);assert.ok(r.missing.includes(c.keywords[i].text));
  }
 }
 const lung=cases[4];assert.equal(grade(lung,{description:'Caseous necrosis. Granulomatous inflammation.'}).description,false);
});
test('source typo and explicitly reviewed correction are both accepted',()=>{
 const c=cases[3];assert.equal(grade(c,{description:'Liquefactive necrosis, loosening, microabscess'}).description,true);
 assert.equal(grade(c,{description:'Liquefactive necrosis, loosening, microabscces'}).description,true);
});
test('multiple accepted answers for diagnosis or organ are supported when explicitly configured',()=>{
  const pa0313=cases.find(c=>c.id==='PA0313');
  assert.ok(pa0313);
  assert.equal(grade(pa0313,{organ:'colon'}).organ,true);
  assert.equal(grade(pa0313,{organ:'Intestine'}).organ,true);
  assert.equal(grade(pa0313,{organ:'Intestine/colon'}).organ,true);

  const pa0074=cases.find(c=>c.id==='PA0074');
  assert.ok(pa0074);
  assert.equal(grade(pa0074,{diagnosis:'Steatosis'}).diagnosis,true);
  assert.equal(grade(pa0074,{diagnosis:'Fatty change'}).diagnosis,true);

  const pa0144=cases.find(c=>c.id==='PA0144');
  assert.ok(pa0144);
  assert.equal(grade(pa0144,{diagnosis:'Intradermal nevus'}).diagnosis,true);
  assert.equal(grade(pa0144,{diagnosis:'Intradermal melanocytic nevus'}).diagnosis,true);

  const pa0017=cases.find(c=>c.id==='PA0017');
  assert.ok(pa0017);
  assert.equal(grade(pa0017,{description:'Dark black pigments in macrophages'}).description,true);
  assert.equal(grade(pa0017,{description:'Dark black pigments in histiocytes'}).description,true);

  const pa0202=cases.find(c=>c.id==='PA0202');
  assert.ok(pa0202);
  assert.equal(grade(pa0202,{description:'fibrinous necrosis, Granulation tissue, Fibrosis'}).description,true);
  assert.equal(grade(pa0202,{description:'fibrinous necrosis, Granulation tissue, scar'}).description,true);

  const pa0096=cases.find(c=>c.id==='PA0096');
  assert.ok(pa0096, 'PA0096 should exist in cases');
  assert.equal(grade(pa0096,{diagnosis:'Infarct'}).diagnosis,true);
  assert.equal(grade(pa0096,{diagnosis:'Infarction'}).diagnosis,true);
  assert.equal(grade(pa0096,{diagnosis:'Infract'}).diagnosis,true);
  assert.equal(grade(pa0096,{diagnosis:'infraction'}).diagnosis,true);
  assert.equal(grade(pa0096,{diagnosis:'Infarct/Infarction'}).diagnosis,true);
  assert.equal(grade(pa0096,{diagnosis:'Infarct / Infarction'}).diagnosis,true);
  assert.equal(grade(pa0096,{diagnosis:'Necrosis'}).diagnosis,false);

  const pa0218=cases.find(c=>c.id==='PA0218');
  assert.ok(pa0218, 'PA0218 should exist in cases');
  assert.equal(grade(pa0218,{diagnosis:'Cytomegalovirus (CMV) infection'}).diagnosis,true);
  assert.equal(grade(pa0218,{diagnosis:'Cytomegaloviral (CMV) nephritis'}).diagnosis,true);
  assert.equal(grade(pa0218,{diagnosis:'Cytomegalovirus infection'}).diagnosis,true);
  assert.equal(grade(pa0218,{diagnosis:'CMV nephritis'}).diagnosis,true);
  assert.equal(grade(pa0218,{diagnosis:'CMV infection'}).diagnosis,true);

  const pa0306=cases.find(c=>c.id==='PA0306');
  assert.ok(pa0306, 'PA0306 should exist in cases');
  assert.equal(grade(pa0306,{organ:'Heart valve'}).organ,true);
  assert.equal(grade(pa0306,{organ:'Heart'}).organ,true);
  assert.equal(grade(pa0306,{organ:'Mitral valve'}).organ,true);
  assert.equal(grade(pa0306,{organ:'Aortic valve'}).organ,true);
  assert.equal(grade(pa0306,{organ:'Kidney'}).organ,false);
  assert.equal(grade(pa0306,{description:'Vegetation'}).description,true);
  assert.equal(grade(pa0306,{description:'Vegetation:'}).description,true);

  const pa0271=cases.find(c=>c.id==='PA0271');
  assert.ok(pa0271, 'PA0271 should exist in cases');
  assert.equal(grade(pa0271,{description:'Molluscum bodies'}).description,true);
  assert.equal(grade(pa0271,{description:'Henderson-Patterson bodies'}).description,true);
  assert.equal(grade(pa0271,{description:'Molluscum bodies (Henderson-Patterson bodies)'}).description,true);

  const pa0255=cases.find(c=>c.id==='PA0255');
  assert.ok(pa0255, 'PA0255 should exist in cases');
  assert.equal(grade(pa0255,{description:'Papillomatosis, Koilocytosis, Acanthosis, Hyperkeratosis, Parakeratosis'}).description,true);
  assert.equal(grade(pa0255,{description:'Papillomatosis, Koilocytosis'}).description,false);

  const pa0251=cases.find(c=>c.id==='PA0251');
  assert.ok(pa0251, 'PA0251 should exist in cases');
  assert.equal(grade(pa0251,{organ:'Ovary'}).organ,true);
  assert.equal(grade(pa0251,{organ:'Ovary (此片被病灶佔滿，其實沒有可供辨認為卵巢之組織)'}).organ,true);
  assert.equal(grade(pa0251,{diagnosis:'Actinomycosis'}).diagnosis,true);
  assert.equal(grade(pa0251,{description:'Sulfur granules, Splendore-Hoeppli phenomenon'}).description,true);
  assert.equal(grade(pa0251,{description:'Sulfur granules'}).description,false);

  const pa0022=cases.find(c=>c.id==='PA0022');
  assert.ok(pa0022, 'PA0022 should exist in cases');
  assert.equal(grade(pa0022,{organ:'Spleen'}).organ,true);
  assert.equal(grade(pa0022,{diagnosis:'Mucormycosis'}).diagnosis,true);
  assert.equal(grade(pa0022,{description:'Aseptate hyphae with wide-angle branching'}).description,true);
  assert.equal(grade(pa0022,{description:'Aseptate hyphae'}).description,false);
  assert.equal(grade(pa0022,{description:'wide angle branching'}).description,false);

  const pa0015=cases.find(c=>c.id==='PA0015');
  assert.ok(pa0015, 'PA0015 should exist in cases');
  assert.equal(grade(pa0015,{organ:'Lung'}).organ,true);
  assert.equal(grade(pa0015,{diagnosis:'Aspergillosis'}).diagnosis,true);
  assert.equal(grade(pa0015,{description:'Fungal hyphae with septa and acute-angle branching'}).description,true);
  assert.equal(grade(pa0015,{description:'septate hyphae with acute-angle branching'}).description,true);
  assert.equal(grade(pa0015,{description:'Fungal hyphae'}).description,false);

  const pa0201=cases.find(c=>c.id==='PA0201');
  assert.ok(pa0201, 'PA0201 should exist in cases');
  assert.equal(grade(pa0201,{organ:'Esophagus'}).organ,true);
  assert.equal(grade(pa0201,{diagnosis:'Candidiasis'}).diagnosis,true);
  assert.equal(grade(pa0201,{description:'Fungal yeasts and pseudohyphae'}).description,true);
  assert.equal(grade(pa0201,{description:'pseudohyphae'}).description,true);
  assert.equal(grade(pa0201,{description:'Chronic inflammation'}).description,false);

  const pa0316=cases.find(c=>c.id==='PA0316');
  assert.ok(pa0316, 'PA0316 should exist in cases');
  assert.equal(grade(pa0316,{description:'thick-walled fungal yeasts, Granulomatous inflammation'}).description,true);
  assert.equal(grade(pa0316,{description:'fungal yeasts, granulomatous'}).description,true);
  assert.equal(grade(pa0316,{description:'thick-walled fungal yeasts'}).description,false);

  const pa0302=cases.find(c=>c.id==='PA0302');
  assert.ok(pa0302, 'PA0302 should exist in cases');
  assert.equal(grade(pa0302,{diagnosis:'Pneumocystis jirovecii pneumonia'}).diagnosis,true);
  assert.equal(grade(pa0302,{diagnosis:'PJP'}).diagnosis,true);
  assert.equal(grade(pa0302,{diagnosis:'Pneumocystis pneumonia'}).diagnosis,true);
  assert.equal(grade(pa0302,{description:'Foamy, granular, eosinophilic exudate'}).description,true);
  assert.equal(grade(pa0302,{description:'eosinophilic foamy exudate'}).description,true);

  const pa0206=cases.find(c=>c.id==='PA0206');
  assert.ok(pa0206, 'PA0206 should exist in cases');
  assert.equal(grade(pa0206,{description:'Ingested red blood cells'}).description,true);
  assert.equal(grade(pa0206,{description:'Ingested RBCs'}).description,true);
  assert.equal(grade(pa0206,{description:'Foamy cytoplasm'}).description,false);

  const pa0354=cases.find(c=>c.id==='PA0354');
  assert.ok(pa0354, 'PA0354 should exist in cases');
  assert.equal(grade(pa0354,{organ:'Oral cavity (mouth floor)'}).organ,true);
  assert.equal(grade(pa0354,{organ:'Oral cavity'}).organ,true);
  assert.equal(grade(pa0354,{organ:'mouth floor'}).organ,true);
  assert.equal(grade(pa0354,{diagnosis:'Herpes virus infection'}).diagnosis,true);
  assert.equal(grade(pa0354,{diagnosis:'HSV infection'}).diagnosis,true);
  assert.equal(grade(pa0354,{description:'herpes infection, Multinucleation, Margination of chromatin, Molding of nuclei'}).description,true);
  assert.equal(grade(pa0354,{description:'herpes infection, multinucleated, Chromatin margination, nuclear molding'}).description,true);
  assert.equal(grade(pa0354,{description:'herpes infection'}).description,false);
});
test('empty answers never earn points',()=>{
 for(const c of cases){const r=grade(c,{organ:'!!!',diagnosis:' ',description:''});assert.equal(r.organ||r.diagnosis||r.description,false);}
});
test('question bank is complete and all marked text and images are traceable',()=>{
 assert.equal(new Set(cases.map(c=>c.id)).size,cases.length);
 for(const c of cases){
  assert.ok(c.images.length>1);assert.ok(c.organ&&c.diagnosis&&c.description&&c.source.answerPage);
  const parts=highlightedParts(c.description,c.keywords);
  assert.equal(parts.map(p=>p.text).join(''),c.description);
  assert.equal(parts.filter(p=>p.highlighted).length,c.keywords.length);
  for(const k of c.keywords){assert.ok(k.accepted.length);assert.ok(k.accepted.every(x=>normalize(x).length));}
  for(const i of c.images){assert.ok(existsSync(new URL('../'+i.src,import.meta.url)));assert.ok(i.page>0&&i.width>0&&i.height>0&&i.sourceImageSha256);}
 }
});
test('scores are calculated based on 17-point scale (organ: 2, diagnosis: 5, description: 10 proportional)',()=>{
  const c=cases[0];
  const perfect=grade(c,{organ:c.organ,diagnosis:c.diagnosis,description:c.description});
  assert.equal(perfect.scores.organ,2);
  assert.equal(perfect.scores.diagnosis,5);
  assert.equal(perfect.scores.description,10);
  assert.equal(perfect.score,17);

  const organOnly=grade(c,{organ:c.organ,diagnosis:'wrong',description:''});
  assert.equal(organOnly.scores.organ,2);
  assert.equal(organOnly.scores.diagnosis,0);
  assert.equal(organOnly.scores.description,0);
  assert.equal(organOnly.score,2);

  const diagOnly=grade(c,{organ:'wrong',diagnosis:c.diagnosis,description:''});
  assert.equal(diagOnly.scores.organ,0);
  assert.equal(diagOnly.scores.diagnosis,5);
  assert.equal(diagOnly.scores.description,0);
  assert.equal(diagOnly.score,5);

  const descHalf=grade(c,{organ:'wrong',diagnosis:'wrong',description:'coagulative necrosis'});
  assert.equal(descHalf.scores.description,5);
  assert.equal(descHalf.score,5);

  const caseWith3Keywords=cases.find(item=>item.keywords.length===3);
  assert.ok(caseWith3Keywords,'Should have at least one case with 3 keywords');
  const kw1=caseWith3Keywords.keywords[0].text;
  const descThird=grade(caseWith3Keywords,{organ:'wrong',diagnosis:'wrong',description:kw1});
  assert.equal(descThird.scores.description,3.3);
  assert.equal(descThird.score,3.3);

  const kw2=caseWith3Keywords.keywords[1].text;
  const descTwoThirds=grade(caseWith3Keywords,{organ:'wrong',diagnosis:'wrong',description:`${kw1} and ${kw2}`});
  assert.equal(descTwoThirds.scores.description,6.7);
  assert.equal(descTwoThirds.score,6.7);

  const kw3=caseWith3Keywords.keywords[2].text;
  const descFullKw=grade(caseWith3Keywords,{organ:'wrong',diagnosis:'wrong',description:`${kw1}, ${kw2}, ${kw3}`});
  assert.equal(descFullKw.scores.description,10);
  assert.equal(descFullKw.score,10);

  const combo=grade(caseWith3Keywords,{organ:caseWith3Keywords.organ,diagnosis:caseWith3Keywords.diagnosis,description:kw1});
  assert.equal(combo.scores.organ,2);
  assert.equal(combo.scores.diagnosis,5);
  assert.equal(combo.scores.description,3.3);
  assert.equal(combo.score,10.3);

  assert.equal(formatScore(17),'17');
  assert.equal(formatScore(10.3),'10.3');
  assert.equal(formatScore(0),'0');
  assert.equal(formatScore(3.3),'3.3');
  assert.equal(formatScore(7.0),'7');
});
