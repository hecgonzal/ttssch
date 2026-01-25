package com.example.dustyjournal

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.material3.MaterialTheme
import com.example.dustyjournal.screens.QuestLogScreen
import com.example.dustyjournal.viewmodel.TaskViewModel

class MainActivity : ComponentActivity() {

    private val viewModel: TaskViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        // Trigger API load on launch
        viewModel.loadTasks()

        setContent {
            MaterialTheme {
                QuestLogScreen(viewModel)
            }
        }
    }
}