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
export function formatScore(score) {
  const rounded = Math.round((Number(score) || 0) * 10) / 10;
  return Number.isInteger(rounded) ? String(rounded) : rounded.toFixed(1);
}

export function grade(caseData, answers) {
  const missing = caseData.keywords.filter(keyword => !keyword.accepted.some(term => normalize(answers.description).includes(normalize(term))));
  const acceptedOrgans = getAccepted(caseData.organ, caseData.acceptedOrgan || caseData.acceptedOrgans);
  const acceptedDiagnoses = getAccepted(caseData.diagnosis, caseData.acceptedDiagnosis || caseData.acceptedDiagnoses);
  const normOrgan = normalize(answers.organ);
  const normDiag = normalize(answers.diagnosis);
  const normDesc = normalize(answers.description);

  const organCorrect = !!normOrgan && acceptedOrgans.some(term => normOrgan === normalize(term));
  const diagCorrect = !!normDiag && acceptedDiagnoses.some(term => normDiag === normalize(term));
  const descFull = !!normDesc && caseData.keywords.length > 0 && missing.length === 0;

  const organScore = organCorrect ? 2 : 0;
  const diagScore = diagCorrect ? 5 : 0;
  let descScore = 0;
  if (normDesc && caseData.keywords.length > 0) {
    if (missing.length === 0) {
      descScore = 10;
    } else {
      const hitCount = caseData.keywords.length - missing.length;
      if (hitCount > 0) {
        descScore = Math.round((hitCount / caseData.keywords.length) * 10 * 10) / 10;
      }
    }
  }
  const totalScore = Math.round((organScore + diagScore + descScore) * 10) / 10;

  return {
    organ: organCorrect,
    diagnosis: diagCorrect,
    description: descFull,
    missing: missing.map(k => k.text),
    scores: {
      organ: organScore,
      diagnosis: diagScore,
      description: descScore,
    },
    score: totalScore,
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
