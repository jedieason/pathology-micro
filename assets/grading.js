/** Exact canonical matching for Organ/Diagnosis; all yellow spans required for Description. */
export function normalize(value) {
  return String(value ?? '').normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{N}]/gu, '');
}
function getAccepted(canonical, explicit) {
  const list = [];
  if (canonical) list.push(canonical);
  if (Array.isArray(explicit)) {
    list.push(...explicit);
  } else if (explicit) {
    list.push(explicit);
  }
  return list;
}
export function grade(caseData, answers) {
  const missing = caseData.keywords.filter(keyword => !keyword.accepted.some(term => normalize(answers.description).includes(normalize(term))));
  const acceptedOrgans = getAccepted(caseData.organ, caseData.acceptedOrgan || caseData.acceptedOrgans);
  const acceptedDiagnoses = getAccepted(caseData.diagnosis, caseData.acceptedDiagnosis || caseData.acceptedDiagnoses);
  const normOrgan = normalize(answers.organ);
  const normDiag = normalize(answers.diagnosis);
  return {
    organ: !!normOrgan && acceptedOrgans.some(term => normOrgan === normalize(term)),
    diagnosis: !!normDiag && acceptedDiagnoses.some(term => normDiag === normalize(term)),
    description: !!normalize(answers.description) && caseData.keywords.length > 0 && missing.length === 0,
    missing: missing.map(k => k.text),
  };
}
export function highlightedParts(text, keywords) {
  const spans = keywords.flatMap(({text:term}) => {
    const found = []; let start = 0, index;
    while ((index = text.toLowerCase().indexOf(term.toLowerCase(), start)) !== -1) {
      found.push([index, index + term.length]); start = index + term.length;
    }
    return found;
  }).sort((a,b) => a[0]-b[0]);
  let cursor=0; const result=[];
  for (const [start,end] of spans) {
    if (start < cursor) continue;
    if (start > cursor) result.push({text:text.slice(cursor,start), highlighted:false});
    result.push({text:text.slice(start,end), highlighted:true}); cursor=end;
  }
  if (cursor < text.length) result.push({text:text.slice(cursor), highlighted:false});
  return result;
}
