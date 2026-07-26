package com.example

import android.content.Context
import android.content.pm.ApplicationInfo
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class AppTrackerSettingsActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme(colorScheme = darkColorScheme()) {
                AppTrackerSettingsScreen(onBack = { finish() })
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AppTrackerSettingsScreen(onBack: () -> Unit) {
    val context = androidx.compose.ui.platform.LocalContext.current
    val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
    
    var showSystemApps by remember { mutableStateOf(prefs.getBoolean("app_tracker_show_system", false)) }
    var autoForceStop by remember { mutableStateOf(prefs.getBoolean("app_tracker_auto_force_stop", false)) }
    var whitelistCurrent by remember { mutableStateOf(prefs.getStringSet("app_tracker_whitelist_current", emptySet()) ?: emptySet()) }
    var whitelistCache by remember { mutableStateOf(prefs.getStringSet("app_tracker_whitelist_cache", emptySet()) ?: emptySet()) }
    
    var allApps by remember { mutableStateOf<List<com.example.service.TrackedAppInfo>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    var searchQuery by remember { mutableStateOf("") }
    
    fun saveWhitelistCurrent(set: Set<String>) {
        whitelistCurrent = set
        prefs.edit().putStringSet("app_tracker_whitelist_current", set).apply()
    }
    
    fun saveWhitelistCache(set: Set<String>) {
        whitelistCache = set
        prefs.edit().putStringSet("app_tracker_whitelist_cache", set).apply()
    }

    LaunchedEffect(Unit) {
        withContext(Dispatchers.IO) {
            val pm = context.packageManager
            val packages = pm.getInstalledPackages(0)
            val list = mutableListOf<com.example.service.TrackedAppInfo>()
            for (pkg in packages) {
                val appInfo = pkg.applicationInfo ?: continue
                val label = appInfo.loadLabel(pm).toString()
                val isSystem = (appInfo.flags and ApplicationInfo.FLAG_SYSTEM) != 0
                list.add(
                    com.example.service.TrackedAppInfo(
                        packageName = pkg.packageName,
                        appName = label,
                        icon = null, // don't load icons here to be fast
                        isSystem = isSystem
                    )
                )
            }
            allApps = list.sortedBy { it.appName.lowercase() }
        }
        isLoading = false
    }
    
    val filteredApps = remember(allApps, showSystemApps, searchQuery) {
        allApps.filter { app ->
            if (!showSystemApps && app.isSystem) false
            else if (searchQuery.isNotBlank()) {
                app.appName.contains(searchQuery, ignoreCase = true) ||
                app.packageName.contains(searchQuery, ignoreCase = true)
            } else true
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("App Tracker Edit") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(modifier = Modifier.padding(padding).fillMaxSize()) {
            Row(
                modifier = Modifier.fillMaxWidth().padding(16.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text("Show System Apps")
                Switch(
                    checked = showSystemApps,
                    onCheckedChange = { 
                        showSystemApps = it
                        prefs.edit().putBoolean("app_tracker_show_system", it).apply()
                    }
                )
            }
            
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text("Auto Force Stop (Accessibility)")
                Switch(
                    checked = autoForceStop,
                    onCheckedChange = { 
                        autoForceStop = it
                        prefs.edit().putBoolean("app_tracker_auto_force_stop", it).apply()
                    }
                )
            }
            
            OutlinedTextField(
                value = searchQuery,
                onValueChange = { searchQuery = it },
                label = { Text("Search Apps") },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp)
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            if (isLoading) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else {
                LazyColumn(modifier = Modifier.fillMaxSize()) {
                    items(filteredApps) { app ->
                        val inCurrent = whitelistCurrent.contains(app.packageName)
                        val inCache = whitelistCache.contains(app.packageName)
                        ListItem(
                            headlineContent = { Text(app.appName) },
                            supportingContent = { Text(app.packageName) },
                            trailingContent = {
                                Column(horizontalAlignment = Alignment.End) {
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Text("Skip Current", style = MaterialTheme.typography.bodySmall)
                                        Checkbox(
                                            checked = inCurrent,
                                            onCheckedChange = { checked ->
                                                val newSet = whitelistCurrent.toMutableSet()
                                                if (checked) newSet.add(app.packageName) else newSet.remove(app.packageName)
                                                saveWhitelistCurrent(newSet)
                                            }
                                        )
                                    }
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Text("Skip Cache", style = MaterialTheme.typography.bodySmall)
                                        Checkbox(
                                            checked = inCache,
                                            onCheckedChange = { checked ->
                                                val newSet = whitelistCache.toMutableSet()
                                                if (checked) newSet.add(app.packageName) else newSet.remove(app.packageName)
                                                saveWhitelistCache(newSet)
                                            }
                                        )
                                    }
                                }
                            }
                        )
                        HorizontalDivider()
                    }
                }
            }
        }
    }
}
