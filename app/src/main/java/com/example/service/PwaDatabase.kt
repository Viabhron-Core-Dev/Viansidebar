package com.example.service

import androidx.room.Entity
import androidx.room.PrimaryKey
import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Delete
import androidx.room.Update
import kotlinx.coroutines.flow.Flow

@Entity(tableName = "pwa_entries")
data class PwaEntry(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val name: String,
    val zipPath: String,
    val isLightweight: Boolean,
    val addedAt: Long = System.currentTimeMillis()
)

@Dao
interface PwaDao {
    @Query("SELECT * FROM pwa_entries ORDER BY addedAt DESC")
    fun getAllPwas(): Flow<List<PwaEntry>>

    @Query("SELECT * FROM pwa_entries ORDER BY addedAt DESC")
    fun getAllPwasSync(): List<PwaEntry>

    @Insert
    suspend fun insertPwa(pwa: PwaEntry)

    @Delete
    suspend fun deletePwa(pwa: PwaEntry)

    @Update
    suspend fun updatePwa(pwa: PwaEntry)
}

@Database(entities = [PwaEntry::class], version = 1, exportSchema = false)
abstract class PwaDatabase : RoomDatabase() {
    abstract fun pwaDao(): PwaDao
}
