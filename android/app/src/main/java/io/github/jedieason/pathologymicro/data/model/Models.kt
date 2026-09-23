package io.github.jedieason.pathologymicro.data.model

import com.google.gson.annotations.SerializedName

data class CaseData(
    val version: Int = 1,
    val title: String = "",
    val cases: List<CaseItem> = emptyList()
)

data class CaseItem(
    val id: String,
    val lesson: Int,
    val organ: String,
    val diagnosis: String,
    val description: String,
    val notes: String? = null,
    val keywords: List<Keyword> = emptyList(),
    val source: CaseSource = CaseSource("", 1),
    val images: List<CaseImage> = emptyList()
)

data class Keyword(
    val text: String,
    val accepted: List<String> = emptyList()
)

data class CaseSource(
    val file: String = "",
    @SerializedName("answerPage")
    val answerPage: Int = 1
)

data class CaseImage(
    val src: String,
    val page: Int? = null,
    val width: Int? = null,
    val height: Int? = null
)

data class Answers(
    val organ: String = "",
    val diagnosis: String = "",
    val description: String = ""
)

data class UserRecord(
    val answers: Answers = Answers(),
    val checked: Boolean = false
)

data class GradingResult(
    val organ: Boolean,
    val diagnosis: Boolean,
    val description: Boolean,
    val missing: List<String>
) {
    val score: Int
        get() = (if (organ) 1 else 0) + (if (diagnosis) 1 else 0) + (if (description) 1 else 0)
}

data class HighlightedSpan(
    val text: String,
    val isHighlighted: Boolean
)
