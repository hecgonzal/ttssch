package com.example.dustyjournal.network


import com.example.dustyjournal.format.QuesttoTask.TaskFormat
import retrofit2.http.GET

interface TaskApi {

    @GET("tasks")
    suspend fun getTasks(): List<TaskFormat>
}