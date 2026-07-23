package com.example.service

import android.annotation.SuppressLint
import android.content.Context
import android.content.Intent
import android.widget.FrameLayout
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.ComposeView
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.room.Room
import com.example.PwaImportActivity
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import androidx.compose.ui.input.pointer.pointerInput

@SuppressLint("ViewConstructor")
class PwaPageView(
    context: Context,
    private val onCloseSidebar: () -> Unit,
    private val onHeightChanged: (Int) -> Unit
) : FrameLayout(context) {

    private val db = Room.databaseBuilder(context.applicationContext, PwaDatabase::class.java, "pwa.db").build()

    init {
        val composeView = ComposeView(context).apply {
            setContent {
                MaterialTheme(colorScheme = darkColorScheme()) {
                    PwaPageContent()
                }
            }
        }
        addView(composeView)
    }

    @OptIn(ExperimentalMaterial3Api::class)
    @Composable
    private fun PwaPageContent() {
        var pwas by remember { mutableStateOf<List<PwaEntry>>(emptyList()) }
        val coroutineScope = rememberCoroutineScope()
        var showDeleteDialog by remember { mutableStateOf<PwaEntry?>(null) }

        LaunchedEffect(Unit) {
            db.pwaDao().getAllPwas().collect { list ->
                pwas = list
            }
        }

        Box(modifier = Modifier.fillMaxSize()) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(16.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("PWA Loader", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Color.White)
                    IconButton(onClick = onCloseSidebar, modifier = Modifier.size(28.dp)) {
                        Icon(Icons.Default.Close, contentDescription = "Close", tint = Color.LightGray)
                    }
                }

                if (pwas.isEmpty()) {
                    Text("No PWAs loaded.", color = Color.Gray, modifier = Modifier.padding(top = 16.dp))
                } else {
                    LazyColumn(modifier = Modifier.weight(1f)) {
                        items(pwas) { pwa ->
                            Card(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 8.dp)
                                    .pointerInput(Unit) {
                                        detectTapGestures(
                                            onLongPress = {
                                                showDeleteDialog = pwa
                                            },
                                            onTap = {
                                                val service = context as? FloatingReaderService
                                                service?.launchPwa(pwa)
                                                onCloseSidebar()
                                            }
                                        )
                                    },
                                colors = CardDefaults.cardColors(containerColor = Color(0xFF2A2A3C))
                            ) {
                                Column(modifier = Modifier.padding(16.dp)) {
                                    Text(pwa.name, fontSize = 18.sp, color = Color.White)
                                    Text(if (pwa.isLightweight) "Floating Window" else "Full Screen", color = Color.Gray, fontSize = 12.sp)
                                }
                            }
                        }
                    }
                }
            }

            FloatingActionButton(
                onClick = {
                    val intent = Intent(context, PwaImportActivity::class.java).apply {
                        flags = Intent.FLAG_ACTIVITY_NEW_TASK
                    }
                    context.startActivity(intent)
                },
                modifier = Modifier
                    .align(Alignment.BottomEnd)
                    .padding(24.dp)
            ) {
                Icon(Icons.Default.Add, contentDescription = "Add PWA")
            }
        }

        if (showDeleteDialog != null) {
            AlertDialog(
                onDismissRequest = { showDeleteDialog = null },
                title = { Text("Delete PWA?") },
                text = { Text("Are you sure you want to delete '${showDeleteDialog?.name}'?") },
                confirmButton = {
                    TextButton(onClick = {
                        coroutineScope.launch(Dispatchers.IO) {
                            try {
                                java.io.File(showDeleteDialog!!.zipPath).delete()
                            } catch (e: Exception) {}
                            db.pwaDao().deletePwa(showDeleteDialog!!)
                            showDeleteDialog = null
                        }
                    }) {
                        Text("Delete")
                    }
                },
                dismissButton = {
                    TextButton(onClick = { showDeleteDialog = null }) {
                        Text("Cancel")
                    }
                }
            )
        }
    }
}
