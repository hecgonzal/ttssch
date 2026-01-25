package com.example.dustyjournal.format.QuesttoTask
import com.google.gson.annotations.SerializedName

data class TaskFormat(
    @SerializedName("task_id") val taskId: String,
    @SerializedName("task_name") val taskName: String,
    @SerializedName("summary") val taskSummary: String,
    @SerializedName("description") val taskDescription: String,
    @SerializedName("task_date") val taskDate: String,
    @SerializedName("start_time") val taskStartTime: String,
    @SerializedName("end_time") val taskEndTime: String,
    @SerializedName("task_tags") val taskTags: List<String>
)