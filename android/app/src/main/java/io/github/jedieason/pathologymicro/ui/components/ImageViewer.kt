package io.github.jedieason.pathologymicro.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectHorizontalDragGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowLeft
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material.icons.filled.ZoomOutMap
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import io.github.jedieason.pathologymicro.data.model.CaseImage
import io.github.jedieason.pathologymicro.ui.theme.*

@Composable
fun ImageViewer(
    images: List<CaseImage>,
    currentImageIndex: Int,
    resolveUrl: (String) -> String,
    onImageIndexChange: (Int) -> Unit,
    onOpenZoom: () -> Unit,
    modifier: Modifier = Modifier
) {
    if (images.isEmpty()) return

    val currentImage = images.getOrNull(currentImageIndex) ?: images[0]
    val fullUrl = resolveUrl(currentImage.src)

    var totalDrag by remember { mutableFloatStateOf(0f) }

    Card(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(18.dp)),
        colors = CardDefaults.cardColors(containerColor = ViewerBackground),
        shape = RoundedCornerShape(18.dp),
        border = CardDefaults.outlinedCardBorder().copy(brush = androidx.compose.ui.graphics.SolidColor(BorderLine))
    ) {
        Column(modifier = Modifier.fillMaxWidth()) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .aspectRatio(1.1f)
                    .clickable { onOpenZoom() }
                    .pointerInput(images.size) {
                        detectHorizontalDragGestures(
                            onDragStart = { totalDrag = 0f },
                            onDragEnd = {
                                if (totalDrag < -60f && images.size > 1) {
                                    onImageIndexChange((currentImageIndex + 1) % images.size)
                                } else if (totalDrag > 60f && images.size > 1) {
                                    onImageIndexChange((currentImageIndex - 1 + images.size) % images.size)
                                }
                                totalDrag = 0f
                            },
                            onHorizontalDrag = { _, dragAmount ->
                                totalDrag += dragAmount
                            }
                        )
                    }
            ) {
                AsyncImage(
                    model = fullUrl,
                    contentDescription = "切片照片 ${currentImageIndex + 1} / ${images.size}",
                    contentScale = ContentScale.Fit,
                    modifier = Modifier.fillMaxSize()
                )

                // Zoom hint icon
                Surface(
                    shape = CircleShape,
                    color = Color.White.copy(alpha = 0.9f),
                    modifier = Modifier
                        .align(Alignment.TopEnd)
                        .padding(14.dp)
                        .size(34.dp)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(
                            imageVector = Icons.Default.ZoomOutMap,
                            contentDescription = "放大照片",
                            tint = PurpleAccent,
                            modifier = Modifier.size(18.dp)
                        )
                    }
                }

                // Prev / Next arrows
                if (images.size > 1) {
                    IconButton(
                        onClick = {
                            onImageIndexChange((currentImageIndex - 1 + images.size) % images.size)
                        },
                        modifier = Modifier
                            .align(Alignment.CenterStart)
                            .padding(start = 10.dp)
                            .size(38.dp)
                            .background(Color.White.copy(alpha = 0.92f), CircleShape)
                    ) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.KeyboardArrowLeft,
                            contentDescription = "上一張照片",
                            tint = TextDark
                        )
                    }

                    IconButton(
                        onClick = {
                            onImageIndexChange((currentImageIndex + 1) % images.size)
                        },
                        modifier = Modifier
                            .align(Alignment.CenterEnd)
                            .padding(end = 10.dp)
                            .size(38.dp)
                            .background(Color.White.copy(alpha = 0.92f), CircleShape)
                    ) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.KeyboardArrowRight,
                            contentDescription = "下一張照片",
                            tint = TextDark
                        )
                    }
                }
            }

            // Bottom bar
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color.White)
                    .padding(horizontal = 18.dp, vertical = 10.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = String.format("%02d / %02d", currentImageIndex + 1, images.size),
                    fontSize = 12.sp,
                    color = TextMuted
                )

                // Dots
                Row(
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    images.indices.forEach { index ->
                        val isSelected = index == currentImageIndex
                        Box(
                            modifier = Modifier
                                .size(if (isSelected) 8.dp else 6.dp)
                                .clip(CircleShape)
                                .background(if (isSelected) PurplePrimary else BorderLine)
                                .clickable { onImageIndexChange(index) }
                        )
                    }
                }

                Spacer(modifier = Modifier.width(36.dp))
            }
        }
    }
}
