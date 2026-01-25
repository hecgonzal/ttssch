package com.example.dustyjournal.format.QuesttoTask

import android.text.format.DateFormat
import java.util.Calendar

object Converter { //Converts JSON tasks to QuestFormat
    private fun TaskCleanTime(time: String): String {//Ensures time is in 24 hour format, paired with toScreenTime
        if (time.isBlank()) return "00:00"//prevents errors
        val parts = time.split(":")//Create array ex: 12:00 -> [12,00]
        val hour = parts.getOrNull(0)?.toIntOrNull()
            ?: 0 //Checks if input exists, then checks if it can be a number. On fail returns 0
        val minute = parts.getOrNull(1)?.toIntOrNull() ?: 0
        val safeHour = hour.coerceIn(0, 23)
        val safeMinute = minute.coerceIn(0, 59)
        return "%02d:%02d".format(safeHour, safeMinute)
    }

    private fun toScreenTime(time: String): String {
        val parts = TaskCleanTime(time).split(":")
        val hour = parts[0].toInt()
        val minute = parts[1].toInt()
        val calendar = Calendar.getInstance().apply {
            set(Calendar.HOUR_OF_DAY, hour)
            set(Calendar.MINUTE, minute)
        }
        return DateFormat.format("h:mm a", calendar).toString()
    }

    fun convertToQuest(task: TaskFormat): QuestFormat {
        return QuestFormat(
            ID = task.taskId,
            title = task.taskName,
            summary = task.taskSummary,
            description = task.taskDescription.ifBlank { "Clearly no description was needed" },
            date = task.taskDate,
            startTime = toScreenTime(task.taskStartTime),
            endTime = toScreenTime(task.taskEndTime),
            tags = task.taskTags
        )
    }

    private fun toBackendTime(time: String): String {
        val trimmed = time.trim().uppercase()
        val parts = trimmed.split(" ")
        val timePart = parts[0]
        val ampm = parts.getOrNull(1) ?: "AM"
        val hourMinute = timePart.split(":")
        val hour12 = hourMinute[0].toIntOrNull() ?: 0
        val minute = hourMinute[1].toIntOrNull() ?: 0
        val hour24 = when {
            ampm == "AM" && hour12 == 12 -> 0
            ampm == "PM" && hour12 != 12 -> hour12 + 12
            else -> hour12
        }
        return "%02d:%02d".format(hour24, minute)
    }

    fun convertToTask(quest: QuestFormat): TaskFormat { //Call upon when saving user inputs
        return TaskFormat(
            taskId = quest.ID,
            taskName = quest.title,
            taskSummary = quest.summary,
            taskDescription = quest.description,
            taskDate = quest.date,
            taskStartTime = toBackendTime(quest.startTime),
            taskEndTime = toBackendTime(quest.endTime),
            taskTags = quest.tags
        )
    }
}