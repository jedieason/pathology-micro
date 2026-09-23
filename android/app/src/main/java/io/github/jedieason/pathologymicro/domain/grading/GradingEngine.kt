package io.github.jedieason.pathologymicro.domain.grading

import io.github.jedieason.pathologymicro.data.model.Answers
import io.github.jedieason.pathologymicro.data.model.CaseItem
import io.github.jedieason.pathologymicro.data.model.GradingResult
import io.github.jedieason.pathologymicro.data.model.HighlightedSpan
import io.github.jedieason.pathologymicro.data.model.Keyword
import java.text.Normalizer

object GradingEngine {

    fun normalize(value: String?): String {
        val nonNull = value ?: ""
        val nfkc = Normalizer.normalize(nonNull, Normalizer.Form.NFKC)
        return nfkc.lowercase().replace(Regex("[^\\p{L}\\p{N}]"), "")
    }

    fun grade(caseItem: CaseItem, answers: Answers): GradingResult {
        val normOrgan = normalize(answers.organ)
        val normDiag = normalize(answers.diagnosis)
        val normDesc = normalize(answers.description)

        val missing = caseItem.keywords.filter { kw ->
            kw.accepted.none { term ->
                normDesc.contains(normalize(term))
            }
        }.map { it.text }

        val organCorrect = normOrgan.isNotEmpty() && normOrgan == normalize(caseItem.organ)
        val diagCorrect = normDiag.isNotEmpty() && normDiag == normalize(caseItem.diagnosis)
        val descCorrect = normDesc.isNotEmpty() && caseItem.keywords.isNotEmpty() && missing.isEmpty()

        return GradingResult(
            organ = organCorrect,
            diagnosis = diagCorrect,
            description = descCorrect,
            missing = missing
        )
    }

    fun highlightedParts(text: String, keywords: List<Keyword>): List<HighlightedSpan> {
        val lowerText = text.lowercase()
        val spans = mutableListOf<Pair<Int, Int>>()

        for (kw in keywords) {
            val term = kw.text.lowercase()
            if (term.isEmpty()) continue
            var start = 0
            while (true) {
                val index = lowerText.indexOf(term, start)
                if (index == -1) break
                spans.add(Pair(index, index + term.length))
                start = index + term.length
            }
        }

        spans.sortBy { it.first }

        var cursor = 0
        val result = mutableListOf<HighlightedSpan>()
        for ((start, end) in spans) {
            if (start < cursor) continue
            if (start > cursor) {
                result.add(HighlightedSpan(text = text.substring(cursor, start), isHighlighted = false))
            }
            result.add(HighlightedSpan(text = text.substring(start, end), isHighlighted = true))
            cursor = end
        }
        if (cursor < text.length) {
            result.add(HighlightedSpan(text = text.substring(cursor), isHighlighted = false))
        }
        return result
    }
}
