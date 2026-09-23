package io.github.jedieason.pathologymicro.ui.components

import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import io.github.jedieason.pathologymicro.data.model.Answers
import io.github.jedieason.pathologymicro.data.model.GradingResult
import io.github.jedieason.pathologymicro.ui.theme.*

@Composable
fun AnswerForm(
    answers: Answers,
    isChecked: Boolean,
    gradingResult: GradingResult?,
    onAnswersChange: (Answers) -> Unit,
    onCheckAnswer: () -> Unit,
    onRetry: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Organ field
        InputFieldWithLabel(
            label = "Organ",
            value = answers.organ,
            placeholder = "器官名稱",
            isChecked = isChecked,
            isCorrect = gradingResult?.organ,
            onValueChange = { onAnswersChange(answers.copy(organ = it)) }
        )

        // Diagnosis field
        InputFieldWithLabel(
            label = "Diagnosis",
            value = answers.diagnosis,
            placeholder = "病理診斷",
            isChecked = isChecked,
            isCorrect = gradingResult?.diagnosis,
            onValueChange = { onAnswersChange(answers.copy(diagnosis = it)) }
        )

        // Description field
        InputFieldWithLabel(
            label = "Description",
            value = answers.description,
            placeholder = "描述你看到的組織變化…",
            isChecked = isChecked,
            isCorrect = gradingResult?.description,
            minLines = 3,
            singleLine = false,
            onValueChange = { onAnswersChange(answers.copy(description = it)) }
        )

        // Actions row
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            // Score indicator
            if (isChecked && gradingResult != null) {
                Text(
                    text = "${gradingResult.score} / 3",
                    fontSize = 14.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = PurpleAccent
                )
            } else {
                Spacer(modifier = Modifier.width(1.dp))
            }

            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                if (isChecked) {
                    OutlinedIconButton(
                        onClick = onRetry,
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier.size(46.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Default.Refresh,
                            contentDescription = "重新作答",
                            tint = TextMuted
                        )
                    }
                }

                Button(
                    onClick = onCheckAnswer,
                    colors = ButtonDefaults.buttonColors(containerColor = PurplePrimary),
                    shape = RoundedCornerShape(14.dp),
                    contentPadding = PaddingValues(horizontal = 24.dp, vertical = 12.dp),
                    modifier = Modifier.height(48.dp)
                ) {
                    Text(
                        text = if (isChecked) "再次檢查" else "檢查答案",
                        fontSize = 15.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = Color.White
                    )
                }
            }
        }
    }
}

@Composable
private fun InputFieldWithLabel(
    label: String,
    value: String,
    placeholder: String,
    isChecked: Boolean,
    isCorrect: Boolean?,
    modifier: Modifier = Modifier,
    minLines: Int = 1,
    singleLine: Boolean = true,
    onValueChange: (String) -> Unit
) {
    val borderColor = when {
        !isChecked || isCorrect == null -> BorderLine
        isCorrect -> CorrectGreen
        else -> IncorrectRed
    }

    Column(modifier = modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 2.dp, vertical = 4.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = label,
                fontSize = 14.sp,
                fontWeight = FontWeight.SemiBold,
                color = TextDark
            )

            if (isChecked && isCorrect != null) {
                Text(
                    text = if (isCorrect) "✓ 正確" else "✕ 錯誤",
                    fontSize = 13.sp,
                    fontWeight = FontWeight.Bold,
                    color = if (isCorrect) CorrectGreen else IncorrectRed
                )
            }
        }

        OutlinedTextField(
            value = value,
            onValueChange = onValueChange,
            placeholder = { Text(placeholder, color = Color(0xFFB0AAB6), fontSize = 15.sp) },
            singleLine = singleLine,
            minLines = minLines,
            shape = RoundedCornerShape(10.dp),
            colors = OutlinedTextFieldDefaults.colors(
                focusedContainerColor = Color.White,
                unfocusedContainerColor = Color.White,
                focusedBorderColor = if (isChecked && isCorrect != null) borderColor else PurplePrimary,
                unfocusedBorderColor = borderColor,
                focusedTextColor = TextDark,
                unfocusedTextColor = TextDark
            ),
            modifier = Modifier.fillMaxWidth()
        )
    }
}
