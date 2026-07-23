
package com.example.service
import androidx.compose.material.icons.filled.OpenInNew

import android.annotation.SuppressLint
import android.content.Context
import android.content.Intent
import android.widget.FrameLayout
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.platform.ComposeView
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.room.Room
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

@SuppressLint("ViewConstructor")
class DictionaryPageView(
    context: Context,
    private val onCloseSidebar: () -> Unit,
    private val onHeightChanged: (Int) -> Unit
) : FrameLayout(context) {

    private var currentHeightPx: Int = 0

    init {
        addView(ComposeView(context).apply {
            layoutParams = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
            setContent {
                MaterialTheme(colorScheme = darkColorScheme()) {
                    Surface(
                        modifier = Modifier
                            .fillMaxSize()
                            .onSizeChanged { size ->
                                if (currentHeightPx != size.height) {
                                    currentHeightPx = size.height
                                    onHeightChanged(size.height)
                                }
                            },
                        color = Color(0xFF1E1E2C)
                    ) {
                        DictionaryScreen(context = context, onCloseSidebar = onCloseSidebar)
                    }
                }
            }
        })
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DictionaryScreen(context: Context, onCloseSidebar: () -> Unit) {
    val db = remember { Room.databaseBuilder(context, DictionaryDatabase::class.java, "dictionary.db").build() }
    var searchQuery by remember { mutableStateOf("") }
    var searchResults by remember { mutableStateOf<List<DictionaryEntry>>(emptyList()) }
    var selectedEntry by remember { mutableStateOf<DictionaryEntry?>(null) }
    val scope = rememberCoroutineScope()

    LaunchedEffect(searchQuery) {
        if (searchQuery.isNotBlank()) {
            withContext(Dispatchers.IO) {
                searchResults = db.dictionaryDao().searchWords("$searchQuery%")
            }
        } else {
            searchResults = emptyList()
        }
    }

    Column(modifier = Modifier.fillMaxSize().padding(12.dp)) {
        Row(
            modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text("Dictionary", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.White)
            Row {
                IconButton(onClick = { 
                    (context as? FloatingReaderService)?.toggleDictionaryWindow() 
                }, modifier = Modifier.size(28.dp)) {
                    Icon(androidx.compose.material.icons.Icons.Default.OpenInNew, contentDescription = "Pop out", tint = Color.LightGray)
                }
                Spacer(modifier = Modifier.width(8.dp))
                IconButton(onClick = onCloseSidebar, modifier = Modifier.size(28.dp)) {
                    Icon(Icons.Default.Close, contentDescription = "Close", tint = Color.LightGray)
                }
            }
        }

        if (selectedEntry == null) {
            OutlinedTextField(
                value = searchQuery,
                onValueChange = { searchQuery = it },
                placeholder = { Text("Search word...") },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
                singleLine = true,
                modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp),
                textStyle = LocalTextStyle.current.copy(color = Color.White)
            )

            LazyColumn(modifier = Modifier.fillMaxSize()) {
                items(searchResults) { entry ->
                    Text(
                        text = entry.word,
                        fontSize = 16.sp,
                        color = Color.White,
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { selectedEntry = entry }
                            .padding(vertical = 12.dp, horizontal = 8.dp)
                    )
                    Divider(color = Color.DarkGray, thickness = 0.5.dp)
                }
            }
        } else {
            Button(onClick = { selectedEntry = null }, modifier = Modifier.padding(bottom = 8.dp)) {
                Text("Back to search")
            }
            Text(
                text = selectedEntry!!.word,
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold,
                color = Color.White,
                modifier = Modifier.padding(bottom = 8.dp)
            )
            rememberScrollState().let { scrollState ->
                Text(
                    text = selectedEntry!!.definition,
                    fontSize = 14.sp,
                    color = Color.LightGray,
                    modifier = Modifier
                        .fillMaxSize()
                        .verticalScroll(scrollState)
                )
            }
        }
    }
}
