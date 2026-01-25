package com.example.dustyjournal.components
import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.AssistChip
import androidx.compose.material3.AssistChipDefaults
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.layout.FlowRow

@Composable
fun QuestEntry(
    title: String,
    summary: String,
    description: String,
    startTime: String,
    endTime: String,
    tags: List<String>
) {
    var expanded by remember { mutableStateOf(false) }

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(12.dp)
            .clickable { expanded = !expanded },
        shape = RoundedCornerShape(16.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 6.dp),
        colors = CardDefaults.cardColors(
            containerColor = Color(0xFFF3E5C8) // parchment tone
        )
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
                .animateContentSize() // smooth expand animation
        ) {

            // Title
            Text(
                text = title,
                style = MaterialTheme.typography.headlineSmall,
                color = Color(0xFF5A3E1B) // warm fantasy brown
            )

            Spacer(Modifier.height(8.dp))

            // Summary (always visible)
            Text(
                text = summary,
                style = MaterialTheme.typography.bodyMedium,
                color = Color(0xFF6B4F2A)
            )

            if (expanded) {
                Spacer(Modifier.height(12.dp))

                // Detailed description
                Text(
                    text = description,
                    style = MaterialTheme.typography.bodyMedium,
                    color = Color(0xFF4A3A22)
                )

                Spacer(Modifier.height(12.dp))

                // Times
                Row(
                    horizontalArrangement = Arrangement.SpaceBetween,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column {
                        Text("Start", style = MaterialTheme.typography.labelSmall)
                        Text(startTime, style = MaterialTheme.typography.bodyMedium)
                    }
                    Column {
                        Text("End", style = MaterialTheme.typography.labelSmall)
                        Text(endTime, style = MaterialTheme.typography.bodyMedium)
                    }
                }

                Spacer(Modifier.height(12.dp))

                // Tags
                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    tags.forEach { tag ->
                        AssistChip(
                            onClick = {},
                            label = { Text(tag) },
                            colors = AssistChipDefaults.assistChipColors(
                                containerColor = Color(0xFFDFC89A),
                                labelColor = Color(0xFF4A3A22)
                            )
                        )
                    }
                }
            }
        }
    }
}