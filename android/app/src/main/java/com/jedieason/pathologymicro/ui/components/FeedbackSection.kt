package com.jedieason.pathologymicro.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.filled.KeyboardArrowUp
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.jedieason.pathologymicro.data.model.CaseItem
import com.jedieason.pathologymicro.data.model.GradingResult
import com.jedieason.pathologymicro.domain.grading.GradingEngine
import com.jedieason.pathologymicro.ui.theme.*

@Composable
fun FeedbackSection(
    caseItem: CaseItem,
    gradingResult: GradingResult?,
    modifier: Modifier = Modifier
) {
    if (gradingResult == null) return

    Column(
        modifier = modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        // Missing keywords warning
        if (gradingResult.missing.isNotEmpty()) {
            Surface(
                color = MissingRedBg,
                shape = RoundedCornerShape(8.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    text = "缺少關鍵字：${gradingResult.missing.joinToString(" · ")}",
                    fontSize = 13.sp,
                    color = IncorrectRed,
                    lineHeight = 18.sp,
                    modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp)
                )
            }
        }

        // Organ answer detail
        ExplanationCard(
            title = "Organ 詳解",
            isCorrect = gradingResult.organ
        ) {
            Text(
                text = caseItem.organ,
                fontSize = 14.sp,
                color = TextDark,
                fontWeight = FontWeight.Medium
            )
        }

        // Diagnosis answer detail
        ExplanationCard(
            title = "Diagnosis 詳解",
            isCorrect = gradingResult.diagnosis
        ) {
            Text(
                text = caseItem.diagnosis,
                fontSize = 14.sp,
                color = TextDark,
                fontWeight = FontWeight.Medium
            )
        }

        // Description answer detail with highlighted keywords
        ExplanationCard(
            title = "Description 詳解",
            isCorrect = gradingResult.description
        ) {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                // Highlighted text
                val highlightedSpans = remember(caseItem) {
                    GradingEngine.highlightedParts(caseItem.description, caseItem.keywords)
                }

                val annotatedString = buildAnnotatedString {
                    for (span in highlightedSpans) {
                        if (span.isHighlighted) {
                            withStyle(
                                SpanStyle(
                                    background = HighlightYellow,
                                    color = TextDark,
                                    fontWeight = FontWeight.SemiBold
                                )
                            ) {
                                append(span.text)
                            }
                        } else {
                            withStyle(SpanStyle(color = TextDark)) {
                                append(span.text)
                            }
                        }
                    }
                }

                Text(
                    text = annotatedString,
                    fontSize = 14.sp,
                    lineHeight = 22.sp
                )

                // Teacher notes
                if (!caseItem.notes.isNullOrBlank()) {
                    HorizontalDivider(color = BorderLine, thickness = 0.8.dp)
                    Text(
                        text = caseItem.notes,
                        fontSize = 12.sp,
                        color = Color(0xFF8B8391),
                        lineHeight = 18.sp
                    )
                }

                // Source info
                Text(
                    text = "${caseItem.id} · 教材 ${caseItem.lesson} · 第 ${caseItem.source.answerPage} 頁",
                    fontSize = 11.sp,
                    color = Color(0xFF938A9D)
                )

                if (caseItem.id == "PA0162") {
                    Text(
                        text = "microabscces 為教材原文；亦接受 microabscess。",
                        fontSize = 11.sp,
                        color = Color(0xFF938A9D)
                    )
                }
            }
        }
    }
}

@Composable
private fun ExplanationCard(
    title: String,
    isCorrect: Boolean,
    content: @Composable () -> Unit
) {
    var expanded by remember(isCorrect) { mutableStateOf(!isCorrect) }

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(10.dp))
            .background(FeedbackBackground)
            .padding(12.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .clickable { expanded = !expanded },
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "$title (${if (expanded) "收合" else "展開"})",
                fontSize = 12.sp,
                fontWeight = FontWeight.Medium,
                color = PurpleAccent
            )
            Icon(
                imageVector = if (expanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown,
                contentDescription = null,
                tint = PurpleAccent,
                modifier = Modifier.size(18.dp)
            )
        }

        AnimatedVisibility(visible = expanded) {
            Box(modifier = Modifier.padding(top = 10.dp)) {
                content()
            }
        }
    }
}
