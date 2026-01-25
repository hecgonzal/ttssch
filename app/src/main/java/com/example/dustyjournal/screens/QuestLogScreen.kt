package com.example.dustyjournal.screens

import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Surface
import androidx.compose.ui.unit.dp
import com.example.dustyjournal.components.QuestEntry
import com.example.dustyjournal.viewmodel.TaskViewModel


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun QuestLogScreen(viewModel: TaskViewModel) {
    val sampleQuests = listOf(
        QuestData(//Replace with API Input
            title = "Moonlit Forest Expedition",
            summary = "Embark on a nighttime journey through the mystical forest.",
            description = "Venture into the dense, moonlit woods to uncover hidden secrets and face the perils of the night.",
            startTime = "8:00 PM",
            endTime = "10:00 PM",
            tags = listOf("exploration", "night", "magic")
        ),
        QuestData(
            title = "Lost Relic Recovery",
            summary = "Recover an ancient artifact hidden deep within forgotten ruins.",
            description = "Navigate crumbling stone corridors, decipher runes, and avoid ancient traps to retrieve the relic.",
            startTime = "2:00 PM",
            endTime = "4:00 PM",
            tags = listOf("dungeon", "puzzle", "danger")
        )//Replace with API Input//
    )

    Surface(modifier = Modifier.fillMaxSize()) {//Book Vibe
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(12.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(sampleQuests) { quest ->
                QuestEntry(
                    title = quest.title,
                    summary = quest.summary,
                    description = quest.description,
                    startTime = quest.startTime,
                    endTime = quest.endTime,
                    tags = quest.tags
                )
            }
        }
    }
}

data class QuestData(
    val title: String,
    val summary: String,
    val description: String,
    val startTime: String,
    val endTime: String,
    val tags: List<String>
)
