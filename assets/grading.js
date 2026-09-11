/** Exact canonical matching for Organ/Diagnosis; all yellow spans required for Description. */
export function normalize(value) {
  return String(value ?? '').normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{N}]/gu, '');
}
export function grade(caseData, answers) {
  const missing = caseData.keywords.filter(keyword => !keyword.accepted.some(term => normalize(answers.description).includes(normalize(term))));
  return {
    organ: !!normalize(answers.organ) && normalize(answers.organ) === normalize(caseData.organ),
    diagnosis: !!normalize(answers.diagnosis) && normalize(answers.diagnosis) === normalize(caseData.diagnosis),
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
