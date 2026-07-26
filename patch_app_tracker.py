import re

with open("app/src/main/java/com/example/service/AppTrackerPageView.kt", "r") as f:
    content = f.read()

# We will completely overwrite AppTrackerPageView.kt
new_content = """package com.example.service

import android.annotation.SuppressLint
import android.app.usage.UsageStats
import android.app.usage.UsageStatsManager
import android.content.Context
import android.content.Intent
import android.content.pm.ApplicationInfo
import android.graphics.drawable.Drawable
import android.provider.Settings
import android.widget.FrameLayout
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
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
                        color = Color.Black
                    ) {
                        AppTrackerScreen(context = context, onCloseSidebar = onCloseSidebar)
                    }
                }
            }
        })
    }
}

private fun checkUsageStatsPermission(context: Context): Boolean {
    val appOps = context.getSystemService(Context.APP_OPS_SERVICE) as android.app.AppOpsManager
    val mode = appOps.unsafeCheckOpNoThrow(
        android.app.AppOpsManager.OPSTR_GET_USAGE_STATS,
        android.os.Process.myUid(),
        context.packageName
    )
    return mode == android.app.AppOpsManager.MODE_ALLOWED
}

@Composable
fun AppTrackerScreen(context: Context, onCloseSidebar: () -> Unit) {
    var hasPermission by remember { mutableStateOf(checkUsageStatsPermission(context)) }
    var apps by remember { mutableStateOf<List<TrackedAppInfo>>(emptyList()) }
    var isLoading by remember { mutableStateOf(false) }
    
    val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
    val whitelistCurrent = remember { prefs.getStringSet("app_tracker_whitelist_current", emptySet()) ?: emptySet() }
    
    var showSystemApps by remember { mutableStateOf(false) }
    var selectedPackages by remember { mutableStateOf<Set<String>>(emptySet()) }
    
    DisposableEffect(Unit) {
        hasPermission = checkUsageStatsPermission(context)
        onDispose {}
    }

    LaunchedEffect(hasPermission) {
        if (hasPermission) {
            isLoading = true
            withContext(Dispatchers.IO) {
                val pm = context.packageManager
                val usm = context.getSystemService(Context.USAGE_STATS_SERVICE) as? UsageStatsManager
                val list = mutableListOf<TrackedAppInfo>()
                if (usm != null) {
                    val endTime = System.currentTimeMillis()
                    val startTime = endTime - (1000L * 60 * 60 * 24) // Last 24 hours
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
                apps = list
                selectedPackages = list.map { it.packageName }.toSet()
            }
            isLoading = false
        }
    }

    val filteredApps = remember(apps, showSystemApps) {
        apps.filter { !it.isSystem || showSystemApps }
    }
    
    LaunchedEffect(filteredApps) {
        selectedPackages = filteredApps.map { it.packageName }.toSet()
    }

    Column(modifier = Modifier.fillMaxSize()) {
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

        // Top Buttons Row 1
        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 4.dp, vertical = 2.dp),
            horizontalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            Button(
                onClick = { showSystemApps = !showSystemApps },
                modifier = Modifier.weight(1f).height(36.dp),
                contentPadding = PaddingValues(0.dp),
                shape = RoundedCornerShape(4.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF333333))
            ) {
                Text(if (showSystemApps) "SYSTEM / USER" else "USER ONLY", fontSize = 11.sp)
            }
            Button(
                onClick = {
                    val intent = Intent(context, com.example.AppTrackerSettingsActivity::class.java)
                    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                    context.startActivity(intent)
                    onCloseSidebar()
                },
                modifier = Modifier.weight(1f).height(36.dp),
                contentPadding = PaddingValues(0.dp),
                shape = RoundedCornerShape(4.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF333333))
            ) {
                Text("PREFERENCES", fontSize = 11.sp)
            }
        }
        
        // Top Buttons Row 2
        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 4.dp, vertical = 2.dp),
            horizontalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            Button(
                onClick = { selectedPackages = emptySet() },
                modifier = Modifier.weight(1f).height(36.dp),
                contentPadding = PaddingValues(0.dp),
                shape = RoundedCornerShape(4.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF333333))
            ) {
                Text("DESELECT ALL", fontSize = 11.sp)
            }
            Button(
                onClick = { selectedPackages = filteredApps.map { it.packageName }.toSet() },
                modifier = Modifier.weight(1f).height(36.dp),
                contentPadding = PaddingValues(0.dp),
                shape = RoundedCornerShape(4.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF333333))
            ) {
                Text("SELECT ALL", fontSize = 11.sp)
            }
        }

        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = "${filteredApps.size} ${if (showSystemApps) "System & User" else "User"} App(s) open in background.",
            color = Color.White,
            fontSize = 12.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.align(Alignment.CenterHorizontally).padding(bottom = 8.dp)
        )

        Box(modifier = Modifier.weight(1f)) {
            if (isLoading) {
                CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
            } else {
                LazyVerticalGrid(
                    columns = GridCells.Fixed(4),
                    modifier = Modifier.fillMaxSize().padding(horizontal = 8.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                    contentPadding = PaddingValues(bottom = 80.dp)
                ) {
                    items(filteredApps, key = { it.packageName }) { app ->
                        val isSelected = selectedPackages.contains(app.packageName)
                        AppGridBlock(
                            app = app,
                            isSelected = isSelected,
                            onClick = {
                                val newSet = selectedPackages.toMutableSet()
                                if (isSelected) newSet.remove(app.packageName) else newSet.add(app.packageName)
                                selectedPackages = newSet
                            }
                        )
                    }
                }
            }
            
            SmallFloatingActionButton(
                onClick = {
                    if (selectedPackages.isNotEmpty()) {
                        val intent = Intent(context, com.example.AppTrackerOpenerActivity::class.java).apply {
                            putStringArrayListExtra("packages", ArrayList(selectedPackages.toList()))
                            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                        }
                        context.startActivity(intent)
                        onCloseSidebar()
                    }
                },
                modifier = Modifier.align(Alignment.BottomEnd).padding(16.dp),
                containerColor = MaterialTheme.colorScheme.primary
            ) {
                Icon(Icons.Default.PlayArrow, contentDescription = "Close Selected")
            }
        }
    }
}

@Composable
fun AppGridBlock(app: TrackedAppInfo, isSelected: Boolean, onClick: () -> Unit) {
    val bitmapState = remember(app.icon) {
        try {
            app.icon?.toBitmap(
                width = if (app.icon.intrinsicWidth > 0) app.icon.intrinsicWidth else 96,
                height = if (app.icon.intrinsicHeight > 0) app.icon.intrinsicHeight else 96
            )?.asImageBitmap()
        } catch (e: Exception) { null }
    }
    
    val bgColor = if (isSelected) Color.White else Color(0xFF1E1E1E)
    val textColor = if (isSelected) Color.Black else Color.White
    
    Box(
        modifier = Modifier
            .aspectRatio(1f)
            .clip(RoundedCornerShape(12.dp))
            .background(bgColor)
            .clickable { onClick() }
            .padding(12.dp),
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
                color = textColor,
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold
            )
        }
    }
}

@Composable
fun PermissionBanner(onGrantClick: () -> Unit) {
    Card(
        shape = RoundedCornerShape(10.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF3B2D26)),
        modifier = Modifier.fillMaxWidth().padding(8.dp)
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
"""

with open("app/src/main/java/com/example/service/AppTrackerPageView.kt", "w") as f:
    f.write(new_content)
