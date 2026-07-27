package com.example.service

import android.annotation.SuppressLint
import android.app.AppOpsManager
import android.app.usage.StorageStatsManager
import android.app.usage.UsageStats
import android.app.usage.UsageStatsManager
import android.content.Context
import android.content.Intent
import android.content.pm.ApplicationInfo
import android.graphics.drawable.Drawable
import android.os.Build
import android.os.Process
import android.os.storage.StorageManager
import android.provider.Settings
import android.text.format.Formatter
import android.widget.FrameLayout
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
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.filled.PlayArrow
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
    val mode = appOps.unsafeCheckOpNoThrow(
        AppOpsManager.OPSTR_GET_USAGE_STATS,
        Process.myUid(),
        context.packageName
    )
    return mode == AppOpsManager.MODE_ALLOWED
}

@Composable
fun AppTrackerScreen(context: Context, onCloseSidebar: () -> Unit) {
    var selectedTab by remember { mutableStateOf(0) }
    var hasPermission by remember { mutableStateOf(checkUsageStatsPermission(context)) }
    
    var recentApps by remember { mutableStateOf<List<TrackedAppInfo>>(emptyList()) }
    var cacheApps by remember { mutableStateOf<List<TrackedAppInfo>>(emptyList()) }
    var isLoadingRecent by remember { mutableStateOf(false) }
    var isLoadingCache by remember { mutableStateOf(false) }
    
    val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
    val whitelistCurrent = remember { prefs.getStringSet("app_tracker_whitelist_current", emptySet()) ?: emptySet() }
    val whitelistCache = remember { prefs.getStringSet("app_tracker_whitelist_cache", emptySet()) ?: emptySet() }
    
    DisposableEffect(Unit) {
        hasPermission = checkUsageStatsPermission(context)
        onDispose {}
    }

    LaunchedEffect(selectedTab, hasPermission) {
        if (selectedTab == 0 && hasPermission) {
            isLoadingRecent = true
            withContext(Dispatchers.IO) {
                val pm = context.packageManager
                val usm = context.getSystemService(Context.USAGE_STATS_SERVICE) as? UsageStatsManager
                val list = mutableListOf<TrackedAppInfo>()
                if (usm != null) {
                    val endTime = System.currentTimeMillis()
                    val startTime = endTime - (1000L * 60 * 60 * 24 * 7)
                    val usageStats = usm.queryUsageStats(UsageStatsManager.INTERVAL_BEST, startTime, endTime)
                    val aggregated = mutableMapOf<String, UsageStats>()
                    for (stat in usageStats) {
                        val existing = aggregated[stat.packageName]
                        if (existing == null || stat.lastTimeUsed > existing.lastTimeUsed) {
                            aggregated[stat.packageName] = stat
                        }
                    }
                    for ((pkgName, stat) in aggregated) {
                        if (stat.lastTimeUsed <= 0 || whitelistCurrent.contains(pkgName) || pkgName == context.packageName) continue
                        try {
                            val appInfo = pm.getApplicationInfo(pkgName, 0)
                            if ((appInfo.flags and ApplicationInfo.FLAG_STOPPED) != 0) continue
                            val label = appInfo.loadLabel(pm).toString()
                            val icon = try { appInfo.loadIcon(pm) } catch (e: Exception) { null }
                            val isSystem = (appInfo.flags and ApplicationInfo.FLAG_SYSTEM) != 0
                            list.add(
                                TrackedAppInfo(
                                    packageName = pkgName,
                                    appName = label,
                                    icon = icon,
                                    isSystem = isSystem,
                                    lastTimeUsed = stat.lastTimeUsed
                                )
                            )
                        } catch (e: Exception) {}
                    }
                    list.sortByDescending { it.lastTimeUsed }
                }
                recentApps = list
            }
            isLoadingRecent = false
        }
    }

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
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O && storageStatsManager != null && storageManager != null) {
                        try {
                            val uuid = appInfo.storageUuid
                            val stats = storageStatsManager.queryStatsForPackage(uuid, pkg.packageName, Process.myUserHandle())
                            cacheSize = stats.cacheBytes
                        } catch (e: Exception) {}
                    }
                    if (cacheSize > 0) {
                        val label = appInfo.loadLabel(pm).toString()
                        val icon = try { appInfo.loadIcon(pm) } catch (e: Exception) { null }
                        val isSystem = (appInfo.flags and ApplicationInfo.FLAG_SYSTEM) != 0
                        list.add(
                            TrackedAppInfo(
                                packageName = pkg.packageName,
                                appName = label,
                                icon = icon,
                                isSystem = isSystem,
                                cacheSize = cacheSize
                            )
                        )
                    }
                }
                list.sortByDescending { it.cacheSize }
                cacheApps = list
            }
            isLoadingCache = false
        }
    }

    Column(modifier = Modifier.fillMaxSize().padding(12.dp)) {
        if (!hasPermission) {
            PermissionBanner(
                onGrantClick = {
                    try {
                        val intent = Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS).apply {
                            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                        }
                        context.startActivity(intent)
                    } catch (e: Exception) { e.printStackTrace() }
                }
            )
            Spacer(modifier = Modifier.height(8.dp))
        }

        Box(modifier = Modifier.weight(1f)) {
            when (selectedTab) {
                0 -> {
                    if (isLoadingRecent) {
                        CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
                    } else {
                        LazyVerticalGrid(
                            columns = GridCells.Fixed(3),
                            modifier = Modifier.fillMaxSize(),
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp),
                            contentPadding = PaddingValues(bottom = 80.dp)
                        ) {
                            items(recentApps, key = { it.packageName }) { app ->
                                AppGridIconItem(app = app, onClick = {
                                    try {
                                        val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
                                            data = android.net.Uri.parse("package:${app.packageName}")
                                            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                        }
                                        context.startActivity(intent)
                                        onCloseSidebar()
                                    } catch (e: Exception) {}
                                })
                            }
                        }
                    }
                }
                1 -> {
                    if (isLoadingCache) {
                        CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
                    } else {
                        LazyColumn(
                            modifier = Modifier.fillMaxSize(),
                            verticalArrangement = Arrangement.spacedBy(6.dp),
                            contentPadding = PaddingValues(bottom = 80.dp)
                        ) {
                            items(cacheApps, key = { it.packageName }) { app ->
                                AppRowItem(
                                    app = app,
                                    subtitle = Formatter.formatShortFileSize(context, app.cacheSize),
                                    onClick = {
                                        try {
                                            val intent = Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
                                                data = android.net.Uri.parse("package:${app.packageName}")
                                                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                            }
                                            context.startActivity(intent)
                                            onCloseSidebar()
                                        } catch (e: Exception) {}
                                    }
                                )
                            }
                        }
                    }
                }
            }

            if (selectedTab == 0 && recentApps.isNotEmpty()) {
                FloatingActionButton(
                    onClick = {
                        val intent = Intent(context, com.example.AppTrackerOpenerActivity::class.java).apply {
                            putStringArrayListExtra("packages", ArrayList(recentApps.map { it.packageName }))
                            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                        }
                        context.startActivity(intent)
                        onCloseSidebar()
                    },
                    modifier = Modifier.align(Alignment.BottomEnd).padding(16.dp)
                ) {
                    Icon(Icons.Default.PlayArrow, contentDescription = "Force Stop All")
                }
            }
        }

        Row(
            modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically
        ) {
            val tabs = listOf("Running", "Cache")
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
fun AppGridIconItem(app: TrackedAppInfo, onClick: () -> Unit) {
    val bitmapState = remember(app.icon) {
        try {
            app.icon?.toBitmap(
                width = if (app.icon.intrinsicWidth > 0) app.icon.intrinsicWidth else 96,
                height = if (app.icon.intrinsicHeight > 0) app.icon.intrinsicHeight else 96
            )?.asImageBitmap()
        } catch (e: Exception) { null }
    }
    Box(
        modifier = Modifier
            .aspectRatio(1f)
            .clip(RoundedCornerShape(16.dp))
            .background(Color(0xFF2B2B3D))
            .clickable { onClick() }
            .padding(12.dp),
        contentAlignment = Alignment.Center
    ) {
        if (bitmapState != null) {
            Image(bitmap = bitmapState, contentDescription = app.appName, modifier = Modifier.fillMaxSize())
        } else {
            Text(app.appName.take(1).uppercase(), color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun AppRowItem(app: TrackedAppInfo, subtitle: String, onClick: () -> Unit) {
    val bitmapState = remember(app.icon) {
        try {
            app.icon?.toBitmap(
                width = if (app.icon.intrinsicWidth > 0) app.icon.intrinsicWidth else 72,
                height = if (app.icon.intrinsicHeight > 0) app.icon.intrinsicHeight else 72
            )?.asImageBitmap()
        } catch (e: Exception) { null }
    }
    Card(
        shape = RoundedCornerShape(8.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF2B2B3D)),
        modifier = Modifier.fillMaxWidth().clickable { onClick() }
    ) {
        Row(
            modifier = Modifier.fillMaxWidth().padding(10.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            if (bitmapState != null) {
                Image(bitmap = bitmapState, contentDescription = app.appName, modifier = Modifier.size(32.dp).clip(CircleShape))
            } else {
                Box(
                    modifier = Modifier.size(32.dp).background(Color.DarkGray, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Text(app.appName.take(1).uppercase(), color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                }
            }
            Spacer(modifier = Modifier.width(10.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(app.appName, fontSize = 14.sp, fontWeight = FontWeight.SemiBold, color = Color.White, maxLines = 1, overflow = TextOverflow.Ellipsis)
                Text(subtitle, fontSize = 12.sp, color = Color.LightGray, maxLines = 1, overflow = TextOverflow.Ellipsis)
            }
            Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(20.dp))
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
            modifier = Modifier.fillMaxWidth().padding(10.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text("Usage Stats Needed", fontWeight = FontWeight.Bold, fontSize = 13.sp, color = Color(0xFFFFB74D))
                Text("Grant Usage Access to track active apps.", fontSize = 11.sp, color = Color.LightGray)
            }
            Spacer(modifier = Modifier.width(8.dp))
            Button(
                onClick = onGrantClick,
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFFF9800)),
                contentPadding = PaddingValues(horizontal = 10.dp, vertical = 4.dp),
                shape = RoundedCornerShape(6.dp)
            ) {
                Text("Grant", fontSize = 11.sp, color = Color.Black)
            }
        }
    }
}
