import {grade, highlightedParts} from './grading.js';
const $ = s => document.querySelector(s);
const fields = ['organ','diagnosis','description'];
const storageKey = 'micro-practice-v1';
let bank=[], records={}, order=[], currentId, imageIndex=0, wrongOnly=false, lesson='all';
let visibleIds=[];
try { const saved=JSON.parse(localStorage.getItem(storageKey)||'{}'); if(saved && typeof saved==='object' && !Array.isArray(saved)) records=saved; } catch { $('#saved').textContent='此瀏覽器無法保留紀錄'; }
function save(){ try{localStorage.setItem(storageKey,JSON.stringify(records));}catch{$('#saved').textContent='此瀏覽器無法保留紀錄';} }
const current = () => bank.find(c=>c.id===currentId);
const record = () => records[currentId] || {};
const isWrong = c => {const r=records[c.id]; return r?.checked && fields.some(f=>!grade(c,r.answers)[f]);};
function updateStats(){
  const scoped=bank.filter(c=>lesson==='all'||String(c.lesson)===lesson);
  $('#wrong-count').textContent=scoped.filter(isWrong).length;
}
function selectList(preferred=currentId){
  visibleIds=order.filter(id=>{const c=bank.find(c=>c.id===id);return (lesson==='all'||String(c.lesson)===lesson)&&(!wrongOnly||isWrong(c));});
  currentId=visibleIds.includes(preferred)?preferred:visibleIds[0];
  imageIndex=0; render();
}
let slideToken=0;
function showPhoto(){
  const c=current(); if(!c)return;
  const item=c.images[imageIndex];
  const img=$('#slide'), slideSpinner=$('#slide-spinner');
  const zoomImg=$('#zoom-image'), zoomSpinner=$('#zoom-spinner');
  const token=++slideToken;

  img.alt=`第 ${visibleIds.indexOf(currentId)+1} 題，切片照片 ${imageIndex+1} / ${c.images.length}`;
  $('#image-count').textContent=`${String(imageIndex+1).padStart(2,'0')} / ${String(c.images.length).padStart(2,'0')}`;
  $('#dots').replaceChildren(...c.images.map((_,i)=>{const b=document.createElement('button');b.type='button';b.setAttribute('aria-label',`照片 ${i+1}`);b.setAttribute('aria-current',String(i===imageIndex));b.onclick=()=>{imageIndex=i;showPhoto();};return b;}));
  for(const id of ['#prev-image','#next-image','#zoom-prev','#zoom-next']) $(id).disabled=c.images.length<2;
  $('#zoom-count').textContent=`切片 ${imageIndex+1} / ${c.images.length}`;

  const setLoaded=(targetImg,spinner)=>{
    if(slideToken!==token)return;
    if(spinner)spinner.hidden=true;
    targetImg.classList.remove('loading');
  };

  const bindImage=(targetImg,spinner,onError)=>{
    targetImg.onload=()=>setLoaded(targetImg,spinner);
    targetImg.onerror=()=>{
      setLoaded(targetImg,spinner);
      if(onError)onError();
    };
    if(targetImg.complete&&targetImg.naturalWidth!==0&&(targetImg.getAttribute('src')===item.src||targetImg.src.endsWith(item.src))){
      setLoaded(targetImg,spinner);
    }else{
      if(spinner)spinner.hidden=false;
      targetImg.classList.add('loading');
      if(targetImg.getAttribute('src')!==item.src) targetImg.src=item.src;
      if(targetImg.complete&&targetImg.naturalWidth!==0){
        setLoaded(targetImg,spinner);
      }
    }
  };

  bindImage(img,slideSpinner,()=>{img.alt='圖片載入失敗，請重新整理';});
  bindImage(zoomImg,zoomSpinner,null);
  zoomImg.classList.remove('expanded');

  // Preload only the next image of the current case.
  new Image().src=c.images[(imageIndex+1)%c.images.length].src;
}
function movePhoto(delta){imageIndex=(imageIndex+delta+current().images.length)%current().images.length;showPhoto();}
function render(){
  updateStats();const c=current();$('#exercise').hidden=!c;$('#empty').hidden=!!c;
  if(!c){$('#empty').textContent=wrongOnly?'沒有錯題，繼續保持。':'此教材尚無題目。';return;}
  const pos=visibleIds.indexOf(currentId);const r=record();
  $('#case-number').textContent=`CASE ${String(pos+1).padStart(2,'0')}`;
  $('#case-state').textContent=r.checked?'✓':'';
  $('#question-position').textContent=`${pos+1} / ${visibleIds.length}`;
  $('#prev-case').disabled=pos===0;$('#next-case').disabled=pos===visibleIds.length-1;
  fields.forEach(f=>{ const v=r.answers?.[f];$(`#${f}`).value=typeof v==='string'?v:''; });
  showPhoto();renderFeedback();
}
function renderFeedback(){
  const c=current(),r=record(),g=r.checked?grade(c,r.answers):null;
  for(const f of fields){
    const field=$(`[data-field="${f}"]`),feedback=field.querySelector('.feedback');
    field.classList.toggle('correct',!!g?.[f]);field.classList.toggle('incorrect',!!g&&!g[f]);
    const result=field.querySelector('.result');
    result.replaceChildren();
    if(g){const symbol=document.createElement('span');symbol.setAttribute('aria-hidden','true');symbol.textContent=g[f]?'✓':'✕';const label=document.createElement('span');label.className='sr-only';label.textContent=g[f]?'正確':'錯誤';result.append(symbol,label);result.title=label.textContent;}else result.removeAttribute('title');
    $(`#${f}`).setAttribute('aria-invalid',String(!!g&&!g[f]));
    feedback.replaceChildren();
    if(!g)continue;
    if(f==='description'&&g.missing.length){const p=document.createElement('p');p.className='missing';p.textContent=`缺少關鍵字：${g.missing.join(' · ')}`;feedback.append(p);}
    const details=document.createElement('details');details.open=!g[f];
    const summary=document.createElement('summary');summary.innerHTML='<span></span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>';
    const updateSummary=()=>{const label=details.open?'收合詳解':'顯示詳解';summary.querySelector('span').textContent=label;summary.setAttribute('aria-label',label);};
    details.addEventListener('toggle',updateSummary);updateSummary();details.append(summary);
    const answer=document.createElement('div');answer.className='answer-text';
    if(f==='description'){
      for(const part of highlightedParts(c.description,c.keywords)){const el=document.createElement(part.highlighted?'mark':'span');el.textContent=part.text;answer.append(el);}
    }else answer.textContent=c[f];
    details.append(answer);
    if(f==='description'){
      if(c.notes){const note=document.createElement('div');note.className='answer-notes';note.textContent=c.notes;details.append(note);}
      const source=document.createElement('div');source.className='source-note';source.textContent=`${c.id} · 教材 ${c.lesson} · 第 ${c.source.answerPage} 頁`;details.append(source);
      if(c.id==='PA0162'){const note=document.createElement('div');note.className='source-note';note.textContent='microabscces 為教材原文；亦接受 microabscess。';details.append(note);}
    }else if(f==='diagnosis'){
      const alts=(c.acceptedDiagnosis||c.acceptedDiagnoses||[]).filter(x=>normalize(x)!==normalize(c.diagnosis));
      const displayAlts=alts.filter(x=>!['infract','infraction'].includes(normalize(x)));
      if(displayAlts.length){const note=document.createElement('div');note.className='source-note';note.textContent=`亦接受：${displayAlts.join(' 或 ')}`;details.append(note);}
    }else if(f==='organ'){
      const alts=(c.acceptedOrgan||c.acceptedOrgans||[]).filter(x=>normalize(x)!==normalize(c.organ));
      if(alts.length){const note=document.createElement('div');note.className='source-note';note.textContent=`亦接受：${alts.join(' 或 ')}`;details.append(note);}
    }
    feedback.append(details);
  }
  $('#score').textContent=g?`${fields.filter(f=>g[f]).length} / 3`:'';
  $('#retry').hidden=!g;$('#check').setAttribute('aria-label',g?'再次檢查':'檢查答案');$('#check').title=g?'再次檢查':'檢查答案';$('#check').textContent=g?'再次檢查':'檢查答案';
}
function answers(){return Object.fromEntries(fields.map(f=>[f,$(`#${f}`).value]));}
$('#answer-form').addEventListener('submit',e=>{e.preventDefault();records[currentId]={answers:answers(),checked:true};save();renderFeedback();updateStats();$('#case-state').textContent='✓';});
$('#answer-form').addEventListener('input',()=>{records[currentId]={answers:answers(),checked:false};save();renderFeedback();updateStats();$('#case-state').textContent='';});
$('#retry').onclick=()=>{records[currentId]={answers:{},checked:false};save();render();$('#organ').focus();};
$('#lesson').onchange=e=>{lesson=e.target.value;syncLessonMenu();selectList();};
const lessonTrigger=$('#lesson-trigger'),lessonMenu=$('#lesson-menu');
function closeLessonMenu(restoreFocus=false){lessonMenu.hidden=true;lessonTrigger.setAttribute('aria-expanded','false');if(restoreFocus)lessonTrigger.focus();}
function syncLessonMenu(){
  $('#lesson-label').textContent=$('#lesson').selectedOptions[0].textContent;
  for(const button of lessonMenu.children)button.setAttribute('aria-checked',String(button.dataset.value===lesson));
}
for(const option of $('#lesson').options){
  const button=document.createElement('button');button.type='button';button.role='menuitemradio';button.dataset.value=option.value;
  const label=document.createElement('span');label.textContent=option.textContent;button.append(label);
  const tick=document.createElement('span');tick.className='lesson-tick';tick.setAttribute('aria-hidden','true');tick.textContent='✓';button.append(tick);
  button.onclick=()=>{$('#lesson').value=option.value;$('#lesson').dispatchEvent(new Event('change'));closeLessonMenu(true);};
  lessonMenu.append(button);
}
syncLessonMenu();
function openLessonMenu(){lessonMenu.hidden=false;lessonTrigger.setAttribute('aria-expanded','true');lessonMenu.querySelector('[aria-checked="true"]').focus();}
lessonTrigger.onclick=()=>{if(lessonMenu.hidden)openLessonMenu();else closeLessonMenu();};
lessonTrigger.addEventListener('keydown',e=>{if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();openLessonMenu();}});
lessonMenu.addEventListener('keydown',e=>{
  const buttons=[...lessonMenu.children],index=buttons.indexOf(document.activeElement);
  if(e.key==='Escape'){e.preventDefault();closeLessonMenu(true);}
  else if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();buttons[(index+(e.key==='ArrowDown'?1:-1)+buttons.length)%buttons.length].focus();}
  else if(e.key==='Home'||e.key==='End'){e.preventDefault();buttons[e.key==='Home'?0:buttons.length-1].focus();}
});
document.addEventListener('click',e=>{if(!e.target.closest('.lesson-picker'))closeLessonMenu();});
document.addEventListener('focusin',e=>{if(!e.target.closest('.lesson-picker'))closeLessonMenu();});
$('#wrong-only').onclick=()=>{wrongOnly=!wrongOnly;$('#wrong-only').setAttribute('aria-pressed',String(wrongOnly));selectList();};
let shuffled=false;
$('#shuffle').onclick=()=>{
  shuffled=!shuffled;
  order=bank.map(c=>c.id);
  if(shuffled){
    for(let i=order.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[order[i],order[j]]=[order[j],order[i]];}
    const eligible=order.filter(id=>{const c=bank.find(c=>c.id===id);return (lesson==='all'||String(c.lesson)===lesson)&&(!wrongOnly||isWrong(c));});
    if(eligible.length>1&&eligible[0]===currentId){const a=order.indexOf(eligible[0]),b=order.indexOf(eligible[1]);[order[a],order[b]]=[order[b],order[a]];}
  }
  $('#shuffle-label').textContent=shuffled?'已隨機':'隨機';
  $('#shuffle').classList.toggle('shuffle-done',shuffled);
  $('#shuffle').setAttribute('aria-pressed',String(shuffled));
  $('#shuffle').title=shuffled?'恢復原始順序':'隨機排序';
  selectList(null);
};
function moveCase(delta){
  // Keep an active wrong-question round stable while corrections are being entered.
  const id=visibleIds[visibleIds.indexOf(currentId)+delta];if(!id)return;
  currentId=id;imageIndex=0;render();$('#case-number').scrollIntoView({behavior:'instant',block:'start'});
}
$('#prev-case').onclick=()=>moveCase(-1);$('#next-case').onclick=()=>moveCase(1);
$('#prev-image').onclick=()=>movePhoto(-1);$('#next-image').onclick=()=>movePhoto(1);
$('.viewer').addEventListener('keydown',e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();movePhoto(e.key==='ArrowLeft'?-1:1);}});
let touchStart=null,suppressClick=false;
$('.viewer').addEventListener('touchstart',e=>{touchStart=e.touches.length===1?{x:e.touches[0].clientX,y:e.touches[0].clientY}:null;},{passive:true});
$('.viewer').addEventListener('touchend',e=>{if(!touchStart)return;const dx=e.changedTouches[0].clientX-touchStart.x,dy=e.changedTouches[0].clientY-touchStart.y;touchStart=null;if(Math.abs(dx)>45&&Math.abs(dx)>Math.abs(dy)*1.4){suppressClick=true;movePhoto(dx<0?1:-1);setTimeout(()=>suppressClick=false,350);}},{passive:true});
$('#open-image').onclick=()=>{if(!suppressClick)$('#zoom-dialog').showModal();};
$('#zoom-close').onclick=()=>$('#zoom-dialog').close();
$('#zoom-prev').onclick=()=>movePhoto(-1);$('#zoom-next').onclick=()=>movePhoto(1);
$('#zoom-image').onclick=()=>$('#zoom-image').classList.toggle('expanded');
$('#zoom-dialog').addEventListener('keydown',e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();movePhoto(e.key==='ArrowLeft'?-1:1);}});
$('#reset').onclick=()=>$('#reset-dialog').showModal();$('#reset-cancel').onclick=()=>$('#reset-dialog').close();
$('#reset-confirm').onclick=()=>{records={};save();$('#reset-dialog').close();selectList();};
try{
  const response=await fetch(new URL('../data/cases.json',import.meta.url));if(!response.ok)throw new Error(`HTTP ${response.status}`);
  const data=await response.json();bank=data.cases;order=bank.map(c=>c.id);
  // Ignore malformed or unrelated saved records; never trust persisted grading results.
  records=Object.fromEntries(Object.entries(records).filter(([id,r])=>order.includes(id)&&r&&typeof r.answers==='object'&&r.answers!==null));
  selectList();
}catch(error){$('#empty').textContent='題庫載入失敗，請重新整理。';console.error(error);}
