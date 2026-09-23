package com.jedieason.pathologymicro.ui

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowLeft
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.DeleteSweep
import androidx.compose.material.icons.filled.Shuffle
import androidx.compose.material.icons.filled.Sync
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.jedieason.pathologymicro.data.model.CaseItem
import com.jedieason.pathologymicro.data.model.UserRecord
import com.jedieason.pathologymicro.data.repository.CaseRepository
import com.jedieason.pathologymicro.domain.grading.GradingEngine
import com.jedieason.pathologymicro.ui.components.AnswerForm
import com.jedieason.pathologymicro.ui.components.FeedbackSection
import com.jedieason.pathologymicro.ui.components.ImageViewer
import com.jedieason.pathologymicro.ui.components.ZoomDialog
import com.jedieason.pathologymicro.ui.theme.*
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MicroScreen(
    repository: CaseRepository,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    val coroutineScope = rememberCoroutineScope()
    val scrollState = rememberScrollState()

    var cases by remember { mutableStateOf<List<CaseItem>>(emptyList()) }
    var order by remember { mutableStateOf<List<String>>(emptyList()) }
    var records by remember { mutableStateOf<Map<String, UserRecord>>(emptyMap()) }

    var lessonFilter by remember { mutableStateOf("all") }
    var wrongOnly by remember { mutableStateOf(false) }
    var isShuffled by remember { mutableStateOf(false) }
    var currentCaseId by remember { mutableStateOf<String?>(null) }
    var currentImageIndex by remember { mutableIntStateOf(0) }

    var isSyncing by remember { mutableStateOf(false) }
    var showResetDialog by remember { mutableStateOf(false) }
    var showZoomDialog by remember { mutableStateOf(false) }
    var lessonMenuExpanded by remember { mutableStateOf(false) }

    // Helpers
    fun isWrongCase(caseItem: CaseItem): Boolean {
        val r = records[caseItem.id] ?: return false
        if (!r.checked) return false
        val grade = GradingEngine.grade(caseItem, r.answers)
        return !grade.organ || !grade.diagnosis || !grade.description
    }

    val scopedCases = remember(cases, lessonFilter) {
        cases.filter { lessonFilter == "all" || it.lesson.toString() == lessonFilter }
    }

    val wrongCount = remember(scopedCases, records) {
        scopedCases.count { isWrongCase(it) }
    }

    val visibleIds = remember(order, cases, lessonFilter, wrongOnly, records) {
        order.filter { id ->
            val c = cases.find { it.id == id } ?: return@filter false
            val lessonMatch = (lessonFilter == "all" || c.lesson.toString() == lessonFilter)
            val wrongMatch = (!wrongOnly || isWrongCase(c))
            lessonMatch && wrongMatch
        }
    }

    // Auto-select preferred or first
    LaunchedEffect(visibleIds) {
        if (currentCaseId == null || !visibleIds.contains(currentCaseId)) {
            currentCaseId = visibleIds.firstOrNull()
            currentImageIndex = 0
        }
    }

    // Initial load
    LaunchedEffect(Unit) {
        val initialData = repository.loadInitialCases()
        cases = initialData.cases
        order = initialData.cases.map { it.id }
        records = repository.loadRecords()
        currentCaseId = initialData.cases.firstOrNull()?.id

        // Attempt background sync with GitHub
        isSyncing = true
        coroutineScope.launch {
            val syncResult = repository.syncCasesFromRemote()
            isSyncing = false
            syncResult.onSuccess { syncedData ->
                cases = syncedData.cases
                if (!isShuffled) {
                    order = syncedData.cases.map { it.id }
                }
                Toast.makeText(context, "已同步 GitHub 最新題庫 (${syncedData.cases.size} 題)", Toast.LENGTH_SHORT).show()
            }.onFailure {
                // Offline fallback remains active
            }
        }
    }

    val currentCase = remember(cases, currentCaseId) {
        cases.find { it.id == currentCaseId }
    }
    val currentRecord = currentCaseId?.let { records[it] } ?: UserRecord()
    val gradingResult = remember(currentCase, currentRecord) {
        if (currentCase != null && currentRecord.checked) {
            GradingEngine.grade(currentCase, currentRecord.answers)
        } else {
            null
        }
    }
    val currentIndex = currentCaseId?.let { visibleIds.indexOf(it) } ?: -1

    Scaffold(
        topBar = {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color.White)
            ) {
                // Header Bar
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 20.dp, vertical = 14.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // Brand
                    Row(
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Surface(
                            shape = RoundedCornerShape(10.dp),
                            color = PurpleLight,
                            modifier = Modifier.size(34.dp)
                        ) {
                            Box(contentAlignment = Alignment.Center) {
                                Text(
                                    text = "m",
                                    color = PurpleAccent,
                                    fontSize = 24.sp,
                                    fontStyle = FontStyle.Italic,
                                    fontFamily = FontFamily.Serif
                                )
                            }
                        }
                        Spacer(modifier = Modifier.width(10.dp))
                        Text(
                            text = "micro",
                            fontSize = 22.sp,
                            fontWeight = FontWeight.Bold,
                            color = TextDark,
                            letterSpacing = (-0.5).sp
                        )
                        Text(
                            text = ".",
                            fontSize = 22.sp,
                            fontWeight = FontWeight.Bold,
                            color = BrandDot
                        )
                    }

                    // Header actions
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        // Sync button
                        IconButton(
                            onClick = {
                                isSyncing = true
                                coroutineScope.launch {
                                    val res = repository.syncCasesFromRemote()
                                    isSyncing = false
                                    res.onSuccess {
                                        cases = it.cases
                                        if (!isShuffled) order = it.cases.map { c -> c.id }
                                        Toast.makeText(context, "題庫已成功同步！", Toast.LENGTH_SHORT).show()
                                    }.onFailure {
                                        Toast.makeText(context, "連線失敗，目前使用本機題庫", Toast.LENGTH_SHORT).show()
                                    }
                                }
                            }
                        ) {
                            Icon(
                                imageVector = Icons.Default.Sync,
                                contentDescription = "同步 GitHub 題庫",
                                tint = if (isSyncing) PurplePrimary else TextMuted
                            )
                        }

                        // Reset button
                        IconButton(onClick = { showResetDialog = true }) {
                            Icon(
                                imageVector = Icons.Default.DeleteSweep,
                                contentDescription = "重設所有紀錄",
                                tint = TextMuted
                            )
                        }
                    }
                }
                HorizontalDivider(color = BorderLine, thickness = 1.dp)
            }
        },
        containerColor = BackgroundWhite,
        modifier = modifier.fillMaxSize()
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(scrollState)
                .padding(horizontal = 20.dp, vertical = 16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Toolbar
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Left filters (Lesson dropdown + Wrong only chip)
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    // Lesson dropdown
                    Box {
                        OutlinedButton(
                            onClick = { lessonMenuExpanded = true },
                            shape = RoundedCornerShape(20.dp),
                            border = androidx.compose.foundation.BorderStroke(1.dp, BorderLine),
                            contentPadding = PaddingValues(horizontal = 14.dp, vertical = 6.dp)
                        ) {
                            val lessonLabel = if (lessonFilter == "all") "全部教材" else "Lesson $lessonFilter"
                            Text(lessonLabel, fontSize = 13.sp, color = TextDark)
                        }

                        DropdownMenu(
                            expanded = lessonMenuExpanded,
                            onDismissRequest = { lessonMenuExpanded = false }
                        ) {
                            val options = listOf(
                                "all" to "全部教材",
                                "1" to "Cell injury · 01",
                                "2" to "Cell injury · 02",
                                "3" to "Cell injury · 03",
                                "4" to "Cell injury · 04",
                                "5" to "Inflammation · 01",
                                "6" to "Hemodynamic · 01"
                            )
                            options.forEach { (valKey, label) ->
                                DropdownMenuItem(
                                    text = {
                                        Row(
                                            modifier = Modifier.fillMaxWidth(),
                                            horizontalArrangement = Arrangement.SpaceBetween,
                                            verticalAlignment = Alignment.CenterVertically
                                        ) {
                                            Text(label, fontSize = 14.sp)
                                            if (lessonFilter == valKey) {
                                                Icon(
                                                    imageVector = Icons.Default.Check,
                                                    contentDescription = null,
                                                    tint = PurplePrimary,
                                                    modifier = Modifier.size(16.dp)
                                                )
                                            }
                                        }
                                    },
                                    onClick = {
                                        lessonFilter = valKey
                                        lessonMenuExpanded = false
                                        currentImageIndex = 0
                                    }
                                )
                            }
                        }
                    }

                    // Wrong only chip
                    FilterChip(
                        selected = wrongOnly,
                        onClick = {
                            wrongOnly = !wrongOnly
                            currentImageIndex = 0
                        },
                        label = {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text("錯題", fontSize = 13.sp)
                                Spacer(modifier = Modifier.width(4.dp))
                                Text(
                                    text = "$wrongCount",
                                    fontSize = 12.sp,
                                    color = if (wrongOnly) PurpleAccent else TextMuted
                                )
                            }
                        },
                        shape = RoundedCornerShape(20.dp),
                        colors = FilterChipDefaults.filterChipColors(
                            selectedContainerColor = PurpleLight,
                            selectedLabelColor = PurpleAccent
                        )
                    )
                }

                // Shuffle button
                TextButton(
                    onClick = {
                        isShuffled = !isShuffled
                        val newOrder = cases.map { it.id }.toMutableList()
                        if (isShuffled) {
                            newOrder.shuffle()
                        }
                        order = newOrder
                        currentImageIndex = 0
                    }
                ) {
                    Icon(
                        imageVector = Icons.Default.Shuffle,
                        contentDescription = "隨機排序",
                        tint = if (isShuffled) PurplePrimary else TextMuted,
                        modifier = Modifier.size(16.dp)
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(
                        text = if (isShuffled) "已隨機" else "隨機",
                        fontSize = 13.sp,
                        color = if (isShuffled) PurplePrimary else TextMuted
                    )
                }
            }

            // Exercise Section or Empty State
            if (currentCase == null) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 60.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = if (wrongOnly) "沒有錯題，繼續保持！" else "正在載入題目或此教材尚無切片…",
                        color = TextMuted,
                        fontSize = 15.sp
                    )
                }
            } else {
                // Case Meta
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "CASE ${String.format("%02d", currentIndex + 1)}",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        color = TextMuted,
                        letterSpacing = 1.sp
                    )
                    if (currentRecord.checked) {
                        Text(
                            text = "✓",
                            fontSize = 14.sp,
                            fontWeight = FontWeight.Bold,
                            color = PurpleAccent
                        )
                    }
                }

                // Image Viewer
                ImageViewer(
                    images = currentCase.images,
                    currentImageIndex = currentImageIndex,
                    resolveUrl = { repository.resolveImageUrl(it) },
                    onImageIndexChange = { currentImageIndex = it },
                    onOpenZoom = { showZoomDialog = true }
                )

                // Answer Form
                AnswerForm(
                    answers = currentRecord.answers,
                    isChecked = currentRecord.checked,
                    gradingResult = gradingResult,
                    onAnswersChange = { newAnswers ->
                        val updated = records.toMutableMap()
                        updated[currentCase.id] = UserRecord(answers = newAnswers, checked = false)
                        records = updated
                        repository.saveRecords(updated)
                    },
                    onCheckAnswer = {
                        val updated = records.toMutableMap()
                        updated[currentCase.id] = UserRecord(answers = currentRecord.answers, checked = true)
                        records = updated
                        repository.saveRecords(updated)
                    },
                    onRetry = {
                        val updated = records.toMutableMap()
                        updated[currentCase.id] = UserRecord(answers = com.jedieason.pathologymicro.data.model.Answers(), checked = false)
                        records = updated
                        repository.saveRecords(updated)
                    }
                )

                // Feedback Section (if checked)
                if (currentRecord.checked && gradingResult != null) {
                    FeedbackSection(
                        caseItem = currentCase,
                        gradingResult = gradingResult
                    )
                }

                // Question Navigation
                HorizontalDivider(color = BorderLine, thickness = 1.dp, modifier = Modifier.padding(top = 10.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    IconButton(
                        onClick = {
                            if (currentIndex > 0) {
                                currentCaseId = visibleIds[currentIndex - 1]
                                currentImageIndex = 0
                                coroutineScope.launch { scrollState.animateScrollTo(0) }
                            }
                        },
                        enabled = currentIndex > 0
                    ) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.KeyboardArrowLeft,
                            contentDescription = "上一題"
                        )
                    }

                    Text(
                        text = "${currentIndex + 1} / ${visibleIds.size}",
                        fontSize = 13.sp,
                        color = TextMuted
                    )

                    IconButton(
                        onClick = {
                            if (currentIndex < visibleIds.size - 1) {
                                currentCaseId = visibleIds[currentIndex + 1]
                                currentImageIndex = 0
                                coroutineScope.launch { scrollState.animateScrollTo(0) }
                            }
                        },
                        enabled = currentIndex < visibleIds.size - 1
                    ) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.KeyboardArrowRight,
                            contentDescription = "下一題"
                        )
                    }
                }
            }
        }
    }

    // Zoom Dialog
    if (showZoomDialog && currentCase != null) {
        ZoomDialog(
            images = currentCase.images,
            currentImageIndex = currentImageIndex,
            resolveUrl = { repository.resolveImageUrl(it) },
            onImageIndexChange = { currentImageIndex = it },
            onDismiss = { showZoomDialog = false }
        )
    }

    // Reset Confirmation Dialog
    if (showResetDialog) {
        AlertDialog(
            onDismissRequest = { showResetDialog = false },
            title = { Text("重新開始練習？", fontSize = 18.sp, fontWeight = FontWeight.Bold) },
            text = { Text("這將清除此裝置上的所有作答與錯題紀錄。") },
            confirmButton = {
                Button(
                    onClick = {
                        repository.clearRecords()
                        records = emptyMap()
                        showResetDialog = false
                        Toast.makeText(context, "作答紀錄已清除", Toast.LENGTH_SHORT).show()
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = PurplePrimary)
                ) {
                    Text("清除紀錄", color = Color.White)
                }
            },
            dismissButton = {
                TextButton(onClick = { showResetDialog = false }) {
                    Text("取消", color = TextDark)
                }
            }
        )
    }
}
