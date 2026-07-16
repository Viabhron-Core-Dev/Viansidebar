package com.example

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.content.pm.ResolveInfo
import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.net.URLEncoder

data class SavedIntentItem(val label: String, val uri: String)

class IntentPickerActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme(colorScheme = darkColorScheme()) {
                IntentPickerScreen(
                    onIntentSelected = { label, uri ->
                        saveIntent(label, uri)
                        val encodedLabel = URLEncoder.encode(label, "UTF-8")
                        val encodedUri = URLEncoder.encode(uri, "UTF-8")
                        val id = "intent:$encodedLabel:$encodedUri"
                        
                        val resultIntent = Intent().apply { putExtra("ELEMENT_ID", id) }
                        setResult(Activity.RESULT_OK, resultIntent)
                        finish()
                    },
                    onBack = { finish() }
                )
            }
        }
    }

    private fun saveIntent(label: String, uri: String) {
        val prefs = getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
        val savedJson = prefs.getString("saved_intents", "[]") ?: "[]"
        val arr = JSONArray(savedJson)
        // check if exists
        for (i in 0 until arr.length()) {
            val obj = arr.getJSONObject(i)
            if (obj.getString("uri") == uri) return
        }
        val newObj = JSONObject().apply {
            put("label", label)
            put("uri", uri)
        }
        arr.put(newObj)
        prefs.edit().putString("saved_intents", arr.toString()).apply()
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun IntentPickerScreen(onIntentSelected: (String, String) -> Unit, onBack: () -> Unit) {
    var showScanAll by remember { mutableStateOf(false) }
    var showAddCustom by remember { mutableStateOf(false) }

    if (showScanAll) {
        ScanAllIntentsScreen(onIntentSelected = onIntentSelected, onBack = { showScanAll = false })
        return
    }

    val context = LocalContext.current
    val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
    var savedIntents by remember { mutableStateOf(emptyList<SavedIntentItem>()) }

    fun loadSaved() {
        val savedJson = prefs.getString("saved_intents", "[]") ?: "[]"
        val arr = JSONArray(savedJson)
        val list = mutableListOf<SavedIntentItem>()
        for (i in 0 until arr.length()) {
            val obj = arr.getJSONObject(i)
            list.add(SavedIntentItem(obj.getString("label"), obj.getString("uri")))
        }
        savedIntents = list
    }

    LaunchedEffect(Unit) {
        loadSaved()
    }

    val commonIntents = listOf(
        SavedIntentItem("Web Search", Intent(Intent.ACTION_WEB_SEARCH).toUri(0)),
        SavedIntentItem("Settings", Intent(android.provider.Settings.ACTION_SETTINGS).toUri(0)),
        SavedIntentItem("Camera", Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE).toUri(0)),
        SavedIntentItem("Dialer", Intent(Intent.ACTION_DIAL).toUri(0)),
        SavedIntentItem("Alarms", Intent(android.provider.AlarmClock.ACTION_SHOW_ALARMS).toUri(0))
    )

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Pick Intent") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, "Back")
                    }
                }
            )
        }
    ) { padding ->
        LazyColumn(modifier = Modifier.padding(padding).fillMaxSize()) {
            item {
                Text("Options", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(16.dp, 8.dp))
                ListItem(
                    headlineContent = { Text("Scan all activities") },
                    supportingContent = { Text("Find any activity on your device") },
                    modifier = Modifier.clickable { showScanAll = true }
                )
                ListItem(
                    headlineContent = { Text("Add custom intent") },
                    supportingContent = { Text("Manually enter a URI") },
                    modifier = Modifier.clickable { showAddCustom = true }
                )
                HorizontalDivider()
            }

            if (savedIntents.isNotEmpty()) {
                item {
                    Text("Saved / Added Intents", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(16.dp, 8.dp))
                }
                items(savedIntents) { item ->
                    ListItem(
                        headlineContent = { Text(item.label) },
                        supportingContent = { Text(item.uri, maxLines = 1) },
                        modifier = Modifier.clickable { onIntentSelected(item.label, item.uri) }
                    )
                }
                item { HorizontalDivider() }
            }

            item {
                Text("Common Intents", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(16.dp, 8.dp))
            }
            items(commonIntents) { item ->
                ListItem(
                    headlineContent = { Text(item.label) },
                    supportingContent = { Text(item.uri, maxLines = 1) },
                    modifier = Modifier.clickable { onIntentSelected(item.label, item.uri) }
                )
            }
        }
    }

    if (showAddCustom) {
        var label by remember { mutableStateOf("") }
        var uri by remember { mutableStateOf("") }
        AlertDialog(
            onDismissRequest = { showAddCustom = false },
            title = { Text("Add Custom Intent") },
            text = {
                Column {
                    OutlinedTextField(
                        value = label,
                        onValueChange = { label = it },
                        label = { Text("Label") },
                        modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)
                    )
                    OutlinedTextField(
                        value = uri,
                        onValueChange = { uri = it },
                        label = { Text("Intent URI") },
                        modifier = Modifier.fillMaxWidth()
                    )
                }
            },
            confirmButton = {
                TextButton(onClick = {
                    if (label.isNotBlank() && uri.isNotBlank()) {
                        onIntentSelected(label, uri)
                        showAddCustom = false
                    }
                }) { Text("Save") }
            },
            dismissButton = {
                TextButton(onClick = { showAddCustom = false }) { Text("Cancel") }
            }
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ScanAllIntentsScreen(onIntentSelected: (String, String) -> Unit, onBack: () -> Unit) {
    val context = LocalContext.current
    var searchQuery by remember { mutableStateOf("") }
    var activities by remember { mutableStateOf<List<ResolveInfo>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }

    LaunchedEffect(Unit) {
        withContext(Dispatchers.IO) {
            val pm = context.packageManager
            val intent = Intent(Intent.ACTION_MAIN, null)
            val list = pm.queryIntentActivities(intent, 0)
            withContext(Dispatchers.Main) {
                activities = list
                isLoading = false
            }
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("All Activities") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(modifier = Modifier.padding(padding).fillMaxSize()) {
            OutlinedTextField(
                value = searchQuery,
                onValueChange = { searchQuery = it },
                label = { Text("Search apps or activities") },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
                modifier = Modifier.fillMaxWidth().padding(16.dp),
                singleLine = true
            )

            if (isLoading) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = androidx.compose.ui.Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else {
                val filtered = remember(searchQuery, activities) {
                    val pm = context.packageManager
                    val query = searchQuery.lowercase()
                    if (query.isEmpty()) {
                        activities
                    } else {
                        activities.filter {
                            val label = it.loadLabel(pm).toString().lowercase()
                            val name = it.activityInfo.name.lowercase()
                            label.contains(query) || name.contains(query)
                        }
                    }
                }

                LazyColumn(modifier = Modifier.weight(1f)) {
                    items(filtered) { info ->
                        val pm = context.packageManager
                        val label = info.loadLabel(pm).toString()
                        val intent = Intent()
                        intent.setClassName(info.activityInfo.packageName, info.activityInfo.name)
                        
                        ListItem(
                            headlineContent = { Text(label) },
                            supportingContent = { Text(info.activityInfo.name, maxLines = 1) },
                            modifier = Modifier.clickable {
                                onIntentSelected(label, intent.toUri(0))
                            }
                        )
                    }
                }
            }
        }
    }
}
