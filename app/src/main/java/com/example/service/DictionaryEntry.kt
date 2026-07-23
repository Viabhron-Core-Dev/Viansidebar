package com.example.service

import androidx.room.Entity
import androidx.room.PrimaryKey
import androidx.room.Index

@Entity(tableName = "dictionary_entries", indices = [Index(value = ["word"])])
data class DictionaryEntry(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val word: String,
    val definition: String
)
