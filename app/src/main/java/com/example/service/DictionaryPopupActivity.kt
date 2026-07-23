package com.example.service

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.room.Room
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class DictionaryPopupActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        var query = ""
        if (intent.action == Intent.ACTION_PROCESS_TEXT) {
            query = intent.getCharSequenceExtra(Intent.EXTRA_PROCESS_TEXT)?.toString() ?: ""
        } else if (intent.action == Intent.ACTION_SEND) {
            query = intent.getStringExtra(Intent.EXTRA_TEXT) ?: ""
        }
        
        query = query.trim().split(Regex("\\s+")).firstOrNull()?.replace(Regex("[^a-zA-Z]"), "") ?: ""

        val db = Room.databaseBuilder(applicationContext, DictionaryDatabase::class.java, "dictionary.db").build()

        setContent {
            MaterialTheme(colorScheme = darkColorScheme()) {
                var definition by remember { mutableStateOf<String?>("Loading...") }
                
                LaunchedEffect(query) {
                    if (query.isNotEmpty()) {
                        withContext(Dispatchers.IO) {
                            val res = db.dictionaryDao().getDefinition(query)
                            definition = res?.definition ?: "No definition found for '$query'"
                        }
                    } else {
                        definition = "No word selected."
                    }
                }

                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color(0x88000000))
                        .clickable { finish() },
                    contentAlignment = Alignment.Center
                ) {
                    Card(
                        shape = RoundedCornerShape(12.dp),
                        colors = CardDefaults.cardColors(containerColor = Color(0xFF1E1E2C)),
                        modifier = Modifier
                            .fillMaxWidth(0.85f)
                            .heightIn(min = 100.dp, max = 400.dp)
                            .clickable(enabled = false) {}
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Text(
                                text = if (query.isEmpty()) "Dictionary" else query,
                                fontSize = 18.sp,
                                color = Color.White,
                                modifier = Modifier.padding(bottom = 8.dp)
                            )
                            rememberScrollState().let { scrollState ->
                                Text(
                                    text = definition ?: "",
                                    fontSize = 14.sp,
                                    color = Color.LightGray,
                                    modifier = Modifier.verticalScroll(scrollState)
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}
