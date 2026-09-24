import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {grade,normalize,highlightedParts} from '../assets/grading.js';
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
