package com.example.dustyjournal.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.dustyjournal.components.TaskRepository
import com.example.dustyjournal.format.QuesttoTask.QuestFormat
import com.example.dustyjournal.format.QuesttoTask.Converter
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch


class TaskViewModel : ViewModel() {

    private val repo = TaskRepository()

    private val _quests = MutableStateFlow<List<QuestFormat>>(emptyList())
    val quests: StateFlow<List<QuestFormat>> = _quests

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error

    fun loadTasks() {
        _isLoading.value = true
        _error.value = null

        viewModelScope.launch {
            try {
                val tasks = repo.fetchTasks()
                _quests.value = tasks.map { Converter.convertToQuest(it) }
            } catch (e: Exception) {
                _error.value = e.message
            } finally {
                _isLoading.value = false
            }
        }
    }
}