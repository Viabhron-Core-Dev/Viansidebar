package com.example.service

import android.annotation.SuppressLint
import android.app.AppOpsManager
import android.app.usage.StorageStatsManager
import android.app.usage.UsageStats
import android.app.usage.UsageStatsManager
import android.content.Context
import android.content.Intent
import android.content.pm.ApplicationInfo
import android.content.pm.PackageManager
import android.graphics.drawable.Drawable
import android.net.Uri
import android.os.Build
import android.os.Process
import android.os.storage.StorageManager
import android.provider.Settings
import android.text.format.Formatter
import android.widget.FrameLayout
import androidx.compose.animation.*
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.platform.ComposeView
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.graphics.drawable.toBitmap
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.text.SimpleDateFormat
import java.util.*

data class TrackedAppInfo(
    val packageName: String,
    val appName: String,
    val icon: Drawable?,
    val isSystem: Boolean,
    val lastTimeUsed: Long = 0L,
    val foregroundTime: Long = 0L,
    val cacheSize: Long = 0L,
    val appSize: Long = 0L,
    val installTime: Long = 0L
)

@SuppressLint("ViewConstructor")
class AppTrackerPageView(
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
                        AppTrackerScreen(context = context, onCloseSidebar = onCloseSidebar)
                    }
                }
            }
        })
    }
}

private fun checkUsageStatsPermission(context: Context): Boolean {
    val appOps = context.getSystemService(Context.APP_OPS_SERVICE) as AppOpsManager
    val mode = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
        appOps.unsafeCheckOpNoThrow(AppOpsManager.OPSTR_GET_USAGE_STATS, Process.myUid(), context.packageName)
    } else {
        @Suppress("DEPRECATION")
        appOps.checkOpNoThrow(AppOpsManager.OPSTR_GET_USAGE_STATS, Process.myUid(), context.packageName)
    }
    return mode == AppOpsManager.MODE_ALLOWED
}

private fun openAppInfo(context: Context, packageName: String) {
    try {
        val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
            data = Uri.parse("package:$packageName")
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        context.startActivity(intent)
    } catch (e: Exception) {
        e.printStackTrace()
    }
}

private fun formatTimeAgo(timeMs: Long): String {
    if (timeMs <= 0) return "Never used"
    val diff = System.currentTimeMillis() - timeMs
    if (diff < 0) return "Just now"
    val seconds = diff / 1000
    val minutes = seconds / 60
    val hours = minutes / 60
    val days = hours / 24

    return when {
        days > 0 -> "${days}d ago"
        hours > 0 -> "${hours}h ago"
        minutes > 0 -> "${minutes}m ago"
        else -> "Just now"
    }
}

private fun formatDuration(millis: Long): String {
    if (millis <= 0) return "0s"
    val seconds = millis / 1000
    val minutes = seconds / 60
    val hours = minutes / 60
    return when {
        hours > 0 -> "${hours}h ${minutes % 60}m"
        minutes > 0 -> "${minutes}m ${seconds % 60}s"
        else -> "${seconds}s"
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AppTrackerScreen(
    context: Context,
    onCloseSidebar: () -> Unit
) {
    LaunchedEffect(Unit) {
        com.example.LogKeeper.writeLog("AppTracker", "Opened app tracker page")
    }
    var selectedTab by remember { mutableStateOf(0) }
    var hasPermission by remember { mutableStateOf(checkUsageStatsPermission(context)) }

    // Tab 1 Data (Recent)
    var recentApps by remember { mutableStateOf<List<TrackedAppInfo>>(emptyList()) }
    val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
    val whitelistCurrent = remember { prefs.getStringSet("app_tracker_whitelist_current", emptySet()) ?: emptySet() }
    val whitelistCache = remember { prefs.getStringSet("app_tracker_whitelist_cache", emptySet()) ?: emptySet() }
    var isLoadingRecent by remember { mutableStateOf(false) }

    // Tab 2 Data (Cache Size)
    var cacheApps by remember { mutableStateOf<List<TrackedAppInfo>>(emptyList()) }
    var isLoadingCache by remember { mutableStateOf(false) }



    // Periodically re-check permission
    DisposableEffect(Unit) {
        hasPermission = checkUsageStatsPermission(context)
        onDispose {}
    }

    // Load Tab 1: Current Apps
    LaunchedEffect(selectedTab, hasPermission) {
        if (selectedTab == 0 && hasPermission) {
            isLoadingRecent = true
            withContext(Dispatchers.IO) {
                val pm = context.packageManager
                val usm = context.getSystemService(Context.USAGE_STATS_SERVICE) as? UsageStatsManager
                val list = mutableListOf<TrackedAppInfo>()

                if (usm != null) {
                    val endTime = System.currentTimeMillis()
                    val startTime = endTime - (1000L * 60 * 60 * 24 * 7) // Last 7 days
                    val usageStats = usm.queryUsageStats(UsageStatsManager.INTERVAL_BEST, startTime, endTime)

                    // Aggregate stats by packageName
                    val aggregated = mutableMapOf<String, UsageStats>()
                    for (stat in usageStats) {
                        val existing = aggregated[stat.packageName]
                        if (existing == null || stat.lastTimeUsed > existing.lastTimeUsed) {
                            aggregated[stat.packageName] = stat
                        }
                    }

                    for ((pkgName, stat) in aggregated) {
                        if (stat.lastTimeUsed <= 0 || whitelistCurrent.contains(pkgName)) continue
                        try {
                            val appInfo = pm.getApplicationInfo(pkgName, 0)
                            // Filter out inactive / launcher-less background services if desired, but keep installed apps
                            val label = appInfo.loadLabel(pm).toString()
                            val icon = try { appInfo.loadIcon(pm) } catch (e: Exception) { null }
                            val isSystem = (appInfo.flags and ApplicationInfo.FLAG_SYSTEM) != 0

                            list.add(
                                TrackedAppInfo(
                                    packageName = pkgName,
                                    appName = label,
                                    icon = icon,
                                    isSystem = isSystem,
                                    lastTimeUsed = stat.lastTimeUsed,
                                    foregroundTime = stat.totalTimeInForeground
                                )
                            )
                        } catch (e: Exception) {
                            // Package not installed or uninstalled
                        }
                    }
                    list.sortByDescending { it.lastTimeUsed }
                }
                recentApps = list
            }
            isLoadingRecent = false
        }
    }

    // Load Tab 2: Cache Size (StorageStatsManager)
    LaunchedEffect(selectedTab, hasPermission) {
        if (selectedTab == 1) {
            isLoadingCache = true
            withContext(Dispatchers.IO) {
                val pm = context.packageManager
                val storageStatsManager = context.getSystemService(Context.STORAGE_STATS_SERVICE) as? StorageStatsManager
                val storageManager = context.getSystemService(Context.STORAGE_SERVICE) as? StorageManager
                val packages = pm.getInstalledPackages(0)
                val list = mutableListOf<TrackedAppInfo>()

                for (pkg in packages) {
                    val appInfo = pkg.applicationInfo ?: continue
                    if (whitelistCache.contains(pkg.packageName)) continue
                    var cacheSize = 0L
                    var appSize = 0L

                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O && storageStatsManager != null && storageManager != null) {
                        try {
                            val uuid = appInfo.storageUuid
                            val stats = storageStatsManager.queryStatsForPackage(uuid, pkg.packageName, Process.myUserHandle())
                            cacheSize = stats.cacheBytes
                            appSize = stats.appBytes + stats.dataBytes
                        } catch (e: Exception) {
                            // Fallback estimation
                            try {
                                val pkgContext = context.createPackageContext(pkg.packageName, 0)
                                val cacheDir = pkgContext.cacheDir
                                cacheSize = cacheDir?.walkTopDown()?.filter { it.isFile }?.map { it.length() }?.sum() ?: 0L
                            } catch (e2: Exception) {
                                cacheSize = 0L
                            }
                        }
                    }

                    val label = appInfo.loadLabel(pm).toString()
                    val icon = try { appInfo.loadIcon(pm) } catch (e: Exception) { null }
                    val isSystem = (appInfo.flags and ApplicationInfo.FLAG_SYSTEM) != 0

                    list.add(
                        TrackedAppInfo(
                            packageName = pkg.packageName,
                            appName = label,
                            icon = icon,
                            isSystem = isSystem,
                            cacheSize = cacheSize,
                            appSize = appSize,
                            installTime = pkg.firstInstallTime
                        )
                    )
                }
                list.sortByDescending { it.cacheSize }
                cacheApps = list
            }
            isLoadingCache = false
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(12.dp)
    ) {
        // Permission Banner if required & missing (for Tab 0 and Tab 1)
        if ((selectedTab == 0 || selectedTab == 1) && !hasPermission) {
            PermissionBanner(
                onGrantClick = {
                    try {
                        val intent = Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS).apply {
                            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                        }
                        context.startActivity(intent)
                    } catch (e: Exception) {
                        e.printStackTrace()
                    }
                }
            )
            Spacer(modifier = Modifier.height(8.dp))
        }

        // Tab Contents
        Box(modifier = Modifier.weight(1f)) {
            val currentList = if (selectedTab == 0) recentApps else cacheApps
            Box(modifier = Modifier.fillMaxSize()) {
            when (selectedTab) {
                0 -> CurrentAppsTab(
                    context = context,
                    apps = recentApps,
                    isLoading = isLoadingRecent
                )
                1 -> CacheAppsTab(
                    context = context,
                    apps = cacheApps,
                    isLoading = isLoadingCache
                )

            }
            FloatingActionButton(
                onClick = {
                    val intent = Intent(context, com.example.AppTrackerOpenerActivity::class.java).apply {
                        putStringArrayListExtra("packages", ArrayList(currentList.map { it.packageName }))
                        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                    }
                    context.startActivity(intent)
                },
                modifier = Modifier.align(Alignment.BottomEnd).padding(16.dp)
            ) {
                Icon(Icons.Default.PlayArrow, contentDescription = "Open App Info Sequential")
            }
            }
        }

        // Pills at the bottom
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 8.dp),
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically
        ) {
            val tabs = listOf("Current", "Cache Size")
            tabs.forEachIndexed { index, title ->
                val isSelected = selectedTab == index
                Box(
                    modifier = Modifier
                        .padding(horizontal = 4.dp)
                        .clip(CircleShape)
                        .background(if (isSelected) MaterialTheme.colorScheme.primary else Color(0xFF2A2A3C))
                        .clickable { selectedTab = index }
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Text(
                        text = title,
                        color = if (isSelected) Color.Black else Color.White,
                        fontSize = 13.sp,
                        fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal
                    )
                }
            }
        }
    }
}

@Composable
fun PermissionBanner(onGrantClick: () -> Unit) {
    Card(
        shape = RoundedCornerShape(10.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF3B2D26)),
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(10.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = "Usage Stats Needed",
                    fontWeight = FontWeight.Bold,
                    fontSize = 13.sp,
                    color = Color(0xFFFFB74D)
                )
                Text(
                    text = "Grant Usage Access to track active apps & cache stats.",
                    fontSize = 11.sp,
                    color = Color.LightGray
                )
            }
            Spacer(modifier = Modifier.width(6.dp))
            Button(
                onClick = onGrantClick,
                shape = RoundedCornerShape(6.dp),
                contentPadding = PaddingValues(horizontal = 10.dp, vertical = 4.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFFF9800))
            ) {
                Text("Grant", fontSize = 11.sp, color = Color.Black)
            }
        }
    }
}

@Composable
fun CurrentAppsTab(
    context: Context,
    apps: List<TrackedAppInfo>,
    isLoading: Boolean
) {
    if (isLoading) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator(color = MaterialTheme.colorScheme.primary)
        }
    } else if (apps.isEmpty()) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Text("No current apps found", color = Color.Gray, fontSize = 13.sp)
        }
    } else {
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.spacedBy(6.dp),
            contentPadding = PaddingValues(vertical = 4.dp)
        ) {
            items(apps, key = { it.packageName }) { app ->
                AppRowItem(
                    app = app,
                    subtitle = "Active: ${formatTimeAgo(app.lastTimeUsed)}" +
                            if (app.foregroundTime > 0) " (${formatDuration(app.foregroundTime)})" else "",
                    onClick = { openAppInfo(context, app.packageName) }
                )
            }
        }
    }
}

@Composable
fun CacheAppsTab(
    context: Context,
    apps: List<TrackedAppInfo>,
    isLoading: Boolean
) {
    if (isLoading) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                CircularProgressIndicator(color = MaterialTheme.colorScheme.primary)
                Spacer(modifier = Modifier.height(12.dp))
                Text("Calculating app cache sizes...", color = Color.LightGray, fontSize = 13.sp)
            }
        }
    } else if (apps.isEmpty()) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Text("No app storage info available", color = Color.Gray, fontSize = 13.sp)
        }
    } else {
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.spacedBy(6.dp),
            contentPadding = PaddingValues(vertical = 4.dp)
        ) {
            items(apps, key = { it.packageName }) { app ->
                AppRowItem(
                    app = app,
                    subtitle = if (app.cacheSize > 0) "Cache: ${Formatter.formatShortFileSize(context, app.cacheSize)}" else "Cache: Minimal",
                    onClick = { openAppInfo(context, app.packageName) }
                )
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AllAppsTab(
    context: Context,
    apps: List<TrackedAppInfo>,
    isLoading: Boolean,
    showSystemApps: Boolean,
    onToggleSystemApps: (Boolean) -> Unit,
    sortBy: String,
    onSortByChange: (String) -> Unit,
    searchQuery: String,
    onSearchQueryChange: (String) -> Unit,
    isSearchOpen: Boolean,
    onToggleSearch: () -> Unit,
    isGridView: Boolean,
    onToggleGridView: () -> Unit
) {
    if (isLoading) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator(color = MaterialTheme.colorScheme.primary)
        }
        return
    }

    // Filter and Sort apps
    val filteredApps = remember(apps, showSystemApps, searchQuery, sortBy) {
        var result = apps.filter { app ->
            if (!showSystemApps && app.isSystem) false
            else if (searchQuery.isNotBlank()) {
                app.appName.contains(searchQuery, ignoreCase = true) ||
                        app.packageName.contains(searchQuery, ignoreCase = true)
            } else true
        }

        result = when (sortBy) {
            "name" -> result.sortedBy { it.appName.lowercase() }
            "time" -> result.sortedByDescending { if (it.lastTimeUsed > 0) it.lastTimeUsed else it.installTime }
            "size" -> result.sortedByDescending { it.cacheSize + it.appSize }
            else -> result
        }
        result
    }

    Column(modifier = Modifier.fillMaxSize()) {
        // Controls Row
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 4.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            // Left Controls: System App Toggle & Sort Chips
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(4.dp),
                modifier = Modifier.weight(1f)
            ) {
                // System App Filter Chip
                FilterChip(
                    selected = showSystemApps,
                    onClick = { onToggleSystemApps(!showSystemApps) },
                    label = { Text("System", fontSize = 10.sp) },
                    modifier = Modifier.height(28.dp)
                )

                // Sort Chip Options
                FilterChip(
                    selected = sortBy == "name",
                    onClick = { onSortByChange("name") },
                    label = { Text("Name", fontSize = 10.sp) },
                    modifier = Modifier.height(28.dp)
                )
                FilterChip(
                    selected = sortBy == "time",
                    onClick = { onSortByChange("time") },
                    label = { Text("Time", fontSize = 10.sp) },
                    modifier = Modifier.height(28.dp)
                )
                FilterChip(
                    selected = sortBy == "size",
                    onClick = { onSortByChange("size") },
                    label = { Text("Size", fontSize = 10.sp) },
                    modifier = Modifier.height(28.dp)
                )
            }

            // Right Controls: Search Toggle & Grid/List View Switch
            Row(verticalAlignment = Alignment.CenterVertically) {
                IconButton(onClick = onToggleSearch, modifier = Modifier.size(28.dp)) {
                    Icon(
                        imageVector = if (isSearchOpen) Icons.Default.SearchOff else Icons.Default.Search,
                        contentDescription = "Search",
                        tint = if (isSearchOpen) MaterialTheme.colorScheme.primary else Color.LightGray,
                        modifier = Modifier.size(18.dp)
                    )
                }
                IconButton(onClick = onToggleGridView, modifier = Modifier.size(28.dp)) {
                    Icon(
                        imageVector = if (isGridView) Icons.Default.List else Icons.Default.GridView,
                        contentDescription = "Toggle View",
                        tint = Color.LightGray,
                        modifier = Modifier.size(18.dp)
                    )
                }
            }
        }

        // Search Bar (if search toggled on)
        AnimatedVisibility(visible = isSearchOpen) {
            OutlinedTextField(
                value = searchQuery,
                onValueChange = onSearchQueryChange,
                placeholder = { Text("Search apps...", fontSize = 12.sp, color = Color.Gray) },
                singleLine = true,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 6.dp),
                textStyle = LocalTextStyle.current.copy(fontSize = 12.sp, color = Color.White),
                trailingIcon = {
                    if (searchQuery.isNotEmpty()) {
                        IconButton(onClick = { onSearchQueryChange("") }) {
                            Icon(Icons.Default.Clear, contentDescription = "Clear", tint = Color.Gray, modifier = Modifier.size(16.dp))
                        }
                    }
                }
            )
        }

        // App List or Grid View
        if (filteredApps.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text("No apps match criteria", color = Color.Gray, fontSize = 13.sp)
            }
        } else if (isGridView) {
            // Grid View (Only Icons)
            LazyVerticalGrid(
                columns = GridCells.Fixed(4),
                modifier = Modifier.fillMaxSize(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp),
                contentPadding = PaddingValues(vertical = 6.dp)
            ) {
                items(filteredApps, key = { it.packageName }) { app ->
                    AppGridIconItem(app = app, onClick = { openAppInfo(context, app.packageName) })
                }
            }
        } else {
            // List View (Tiny Icon + Name + Size)
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                verticalArrangement = Arrangement.spacedBy(6.dp),
                contentPadding = PaddingValues(vertical = 4.dp)
            ) {
                items(filteredApps, key = { it.packageName }) { app ->
                    val sizeText = when {
                        app.cacheSize > 0 || app.appSize > 0 ->
                            Formatter.formatShortFileSize(context, app.cacheSize + app.appSize)
                        else -> "App Info"
                    }
                    AppRowItem(
                        app = app,
                        subtitle = sizeText,
                        iconSizeDp = 24,
                        onClick = { openAppInfo(context, app.packageName) }
                    )
                }
            }
        }
    }
}

@Composable
fun AppRowItem(
    app: TrackedAppInfo,
    subtitle: String,
    extraInfo: String? = null,
    iconSizeDp: Int = 32,
    onClick: () -> Unit
) {
    val bitmapState = remember(app.icon) {
        try {
            app.icon?.toBitmap(
                width = if (app.icon.intrinsicWidth > 0) app.icon.intrinsicWidth else 72,
                height = if (app.icon.intrinsicHeight > 0) app.icon.intrinsicHeight else 72
            )?.asImageBitmap()
        } catch (e: Exception) {
            null
        }
    }

    Card(
        shape = RoundedCornerShape(8.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF2B2B3D)),
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 10.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            if (bitmapState != null) {
                Image(
                    bitmap = bitmapState,
                    contentDescription = app.appName,
                    modifier = Modifier
                        .size(iconSizeDp.dp)
                        .clip(CircleShape)
                )
            } else {
                Box(
                    modifier = Modifier
                        .size(iconSizeDp.dp)
                        .background(Color.DarkGray, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = app.appName.take(1).uppercase(),
                        color = Color.White,
                        fontSize = (iconSizeDp / 2).sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }

            Spacer(modifier = Modifier.width(10.dp))

            Column(modifier = Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = app.appName,
                        fontSize = 13.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = Color.White,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.weight(1f, fill = false)
                    )
                    if (app.isSystem) {
                        Spacer(modifier = Modifier.width(6.dp))
                        Box(
                            modifier = Modifier
                                .background(Color(0xFF4A3B52), RoundedCornerShape(4.dp))
                                .padding(horizontal = 4.dp, vertical = 1.dp)
                        ) {
                            Text("SYS", fontSize = 8.sp, color = Color(0xFFCE93D8), fontWeight = FontWeight.Bold)
                        }
                    }
                }

                Text(
                    text = subtitle,
                    fontSize = 11.sp,
                    color = Color.LightGray,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }

            if (extraInfo != null) {
                Spacer(modifier = Modifier.width(6.dp))
                Text(
                    text = extraInfo,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary
                )
            }

            Spacer(modifier = Modifier.width(4.dp))
            Icon(
                imageVector = Icons.Default.ChevronRight,
                contentDescription = null,
                tint = Color.Gray,
                modifier = Modifier.size(16.dp)
            )
        }
    }
}

@Composable
fun AppGridIconItem(
    app: TrackedAppInfo,
    onClick: () -> Unit
) {
    val bitmapState = remember(app.icon) {
        try {
            app.icon?.toBitmap(
                width = if (app.icon.intrinsicWidth > 0) app.icon.intrinsicWidth else 96,
                height = if (app.icon.intrinsicHeight > 0) app.icon.intrinsicHeight else 96
            )?.asImageBitmap()
        } catch (e: Exception) {
            null
        }
    }

    Box(
        modifier = Modifier
            .aspectRatio(1f)
            .clip(RoundedCornerShape(12.dp))
            .background(Color(0xFF2B2B3D))
            .clickable { onClick() }
            .padding(8.dp),
        contentAlignment = Alignment.Center
    ) {
        if (bitmapState != null) {
            Image(
                bitmap = bitmapState,
                contentDescription = app.appName,
                modifier = Modifier.fillMaxSize()
            )
        } else {
            Text(
                text = app.appName.take(1).uppercase(),
                color = Color.White,
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold
            )
        }
    }
}
