package com.example.dustyjournal.Screens

import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.material3.ExperimentalMaterial3Api
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun QuestLogScreen() {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Quest Log") }
            )
        }
    ) { innerPadding ->
        Text(
            text = "Your quests will appear here.",
            modifier = Modifier.fillMaxSize()
        )
    }
}