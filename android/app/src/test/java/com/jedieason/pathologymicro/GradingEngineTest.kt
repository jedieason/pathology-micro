package com.jedieason.pathologymicro

import com.jedieason.pathologymicro.data.model.Answers
import com.jedieason.pathologymicro.data.model.CaseItem
import com.jedieason.pathologymicro.data.model.Keyword
import com.jedieason.pathologymicro.domain.grading.GradingEngine
import org.junit.Assert.*
import org.junit.Test

class GradingEngineTest {

    @Test
    fun normalization_ignores_case_spacing_punctuation_and_fullwidth_differences() {
        assertEquals("kidney", GradingEngine.normalize(" Ｋｉｄｎｅｙ!\n"))
        assertEquals(
            GradingEngine.normalize("Intestine/colon"),
            GradingEngine.normalize("Intestine / COLON")
        )
    }

    @Test
    fun exact_organ_and_diagnosis_do_not_accept_partial_answers_or_synonyms() {
        val caseNec = CaseItem(
            id = "PA0098",
            lesson = 1,
            organ = "Intestine / colon",
            diagnosis = "Necrotizing enterocolitis",
            description = "test"
        )
        val r1 = GradingEngine.grade(
            caseNec,
            Answers(organ = "colon", diagnosis = "Necrotizing enterocolitis", description = "")
        )
        assertFalse(r1.organ)
        assertTrue(r1.diagnosis)

        val caseHeart = CaseItem(
            id = "PA0099",
            lesson = 1,
            organ = "Heart",
            diagnosis = "Myocardial infarction, healed",
            description = "test"
        )
        val r2 = GradingEngine.grade(
            caseHeart,
            Answers(diagnosis = "Myocardial infarction, remote")
        )
        assertFalse(r2.diagnosis)

        val r3 = GradingEngine.grade(
            caseHeart,
            Answers(diagnosis = "MYOCARDIAL-infarction HEALED!!!")
        )
        assertTrue(r3.diagnosis)
    }

    @Test
    fun all_three_fields_are_scored_independently() {
        val testCase = CaseItem(
            id = "PA0097",
            lesson = 1,
            organ = "Kidney",
            diagnosis = "Acute tubular necrosis",
            description = "coagulative necrosis, preserved cellular outlines",
            keywords = listOf(
                Keyword(text = "coagulative necrosis", accepted = listOf("coagulative necrosis")),
                Keyword(text = "preserved cellular outlines", accepted = listOf("preserved cellular outlines"))
            )
        )

        val result = GradingEngine.grade(
            testCase,
            Answers(organ = "wrong", diagnosis = "Acute tubular necrosis", description = testCase.description)
        )
        assertFalse(result.organ)
        assertTrue(result.diagnosis)
        assertTrue(result.description)
        assertEquals(2, result.score)
    }

    @Test
    fun each_highlighted_phrase_is_mandatory() {
        val testCase = CaseItem(
            id = "PA0097",
            lesson = 1,
            organ = "Kidney",
            diagnosis = "Acute tubular necrosis",
            description = "coagulative necrosis, preserved cellular outlines",
            keywords = listOf(
                Keyword(text = "coagulative necrosis", accepted = listOf("coagulative necrosis")),
                Keyword(text = "preserved cellular outlines", accepted = listOf("preserved cellular outlines"))
            )
        )

        // All present (even uppercase)
        val rFull = GradingEngine.grade(
            testCase,
            Answers(description = "COAGULATIVE NECROSIS; PRESERVED CELLULAR OUTLINES")
        )
        assertTrue(rFull.description)
        assertTrue(rFull.missing.isEmpty())

        // Missing one
        val rMissing = GradingEngine.grade(
            testCase,
            Answers(description = "coagulative necrosis only")
        )
        assertFalse(rMissing.description)
        assertTrue(rMissing.missing.contains("preserved cellular outlines"))
    }

    @Test
    fun accepted_synonyms_and_source_typo_accepted() {
        val caseAbscess = CaseItem(
            id = "PA0162",
            lesson = 1,
            organ = "Brain",
            diagnosis = "Brain abscess",
            description = "Liquefactive necrosis, loosening, microabscces",
            keywords = listOf(
                Keyword(
                    text = "microabscces",
                    accepted = listOf("microabscces", "microabscess")
                )
            )
        )

        val rCorrect = GradingEngine.grade(
            caseAbscess,
            Answers(description = "microabscess")
        )
        assertTrue(rCorrect.description)

        val rTypo = GradingEngine.grade(
            caseAbscess,
            Answers(description = "microabscces")
        )
        assertTrue(rTypo.description)
    }

    @Test
    fun empty_answers_never_earn_points() {
        val testCase = CaseItem(
            id = "PA0097",
            lesson = 1,
            organ = "Kidney",
            diagnosis = "Acute tubular necrosis",
            description = "coagulative necrosis",
            keywords = listOf(Keyword(text = "coagulative necrosis", accepted = listOf("coagulative necrosis")))
        )
        val r = GradingEngine.grade(testCase, Answers(organ = "!!!", diagnosis = " ", description = ""))
        assertFalse(r.organ)
        assertFalse(r.diagnosis)
        assertFalse(r.description)
    }

    @Test
    fun highlighted_parts_reconstructs_text() {
        val text = "1. Tubular epithelial coagulative necrosis with preserved cellular outlines."
        val keywords = listOf(
            Keyword(text = "coagulative necrosis", accepted = listOf("coagulative necrosis")),
            Keyword(text = "preserved cellular outlines", accepted = listOf("preserved cellular outlines"))
        )

        val parts = GradingEngine.highlightedParts(text, keywords)
        val reconstructed = parts.joinToString("") { it.text }
        assertEquals(text, reconstructed)
        assertEquals(2, parts.count { it.isHighlighted })
    }

    @Test
    fun accepted_diagnosis_allows_multiple_valid_answers() {
        val testCase = CaseItem(
            id = "PA0096",
            lesson = 6,
            organ = "Kidney",
            diagnosis = "Infarct/Infarction",
            acceptedDiagnosis = listOf("Infarct", "Infarction", "Infract", "Infraction"),
            description = "coagulative necrosis",
            keywords = listOf(Keyword(text = "coagulative necrosis", accepted = listOf("coagulative necrosis")))
        )
        assertTrue(GradingEngine.grade(testCase, Answers(diagnosis = "Infarct")).diagnosis)
        assertTrue(GradingEngine.grade(testCase, Answers(diagnosis = "Infarction")).diagnosis)
        assertTrue(GradingEngine.grade(testCase, Answers(diagnosis = "Infract")).diagnosis)
        assertTrue(GradingEngine.grade(testCase, Answers(diagnosis = "infraction")).diagnosis)
        assertTrue(GradingEngine.grade(testCase, Answers(diagnosis = "Infarct/Infarction")).diagnosis)
        assertFalse(GradingEngine.grade(testCase, Answers(diagnosis = "Necrosis")).diagnosis)
    }
}
