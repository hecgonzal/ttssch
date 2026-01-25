package com.example.dustyjournal.components

import com.example.dustyjournal.format.QuesttoTask.TaskFormat
import com.example.dustyjournal.network.RetrofitClient

class TaskRepository {
    suspend fun fetchTasks(): List<TaskFormat> {
        return RetrofitClient.api.getTasks()
    }
}
