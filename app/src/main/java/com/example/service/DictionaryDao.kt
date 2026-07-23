package com.example.service

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

@Dao
interface DictionaryDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(entries: List<DictionaryEntry>)

    @Query("SELECT * FROM dictionary_entries WHERE word LIKE :query LIMIT 50")
    suspend fun searchWords(query: String): List<DictionaryEntry>

    @Query("SELECT * FROM dictionary_entries WHERE word = :word LIMIT 1")
    suspend fun getDefinition(word: String): DictionaryEntry?

    @Query("DELETE FROM dictionary_entries")
    suspend fun clearAll()
}
