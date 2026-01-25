package com.example.dustyjournal.format.QuesttoTask

data class QuestFormat(
    val ID: String,
    val title: String,
    val summary: String,
    val description: String,
    val date: String,
    val startTime: String,
    val endTime: String,
    val tags: List<String>
)