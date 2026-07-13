package com.example.service

import android.content.Context
import android.service.notification.StatusBarNotification
import android.widget.FrameLayout
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import android.app.ActivityOptions
import android.os.Build
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.ComposeView
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.flow.collectLatest
import android.app.PendingIntent
import android.graphics.drawable.Icon
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.foundation.Image
import androidx.core.graphics.drawable.toBitmap
import android.graphics.drawable.BitmapDrawable
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.ExpandMore
import androidx.compose.material.icons.filled.ExpandLess
import androidx.compose.material3.IconButton
import androidx.compose.material.icons.filled.FilterList
import com.example.NotificationHistoryActivity
import android.content.Intent

class NotificationPageView(
    context: Context,
    private val onCloseSidebar: () -> Unit,
    private val onHeightChanged: (Int) -> Unit
) : FrameLayout(context) {

    private var currentHeightPx: Int = 0
    

    init {
        
        addView(ComposeView(context).apply {
            layoutParams = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT)
            setContent {
                MaterialTheme(colorScheme = darkColorScheme()) {
                    Box(modifier = Modifier.fillMaxSize().onSizeChanged { size ->
                        if (currentHeightPx != size.height) {
                            currentHeightPx = size.height
                            onHeightChanged(size.height)
                        }
                    }) {
                        NotificationScreen(context, onCloseSidebar)
                    }
                }
            }
        })
    }

    fun getCurrentHeightPx(): Int {
        val density = context.resources.displayMetrics.density
        return if (currentHeightPx > 0) currentHeightPx else (450 * density).toInt()
    }
}

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun NotificationScreen(context: Context, onCloseSidebar: () -> Unit) {
    LaunchedEffect(Unit) {
        com.example.LogKeeper.writeLog("Sidebar", "Notification page viewed")
    }
    
    val notifications by AppNotificationListener.notifications.collectAsState()
    val prefs = remember { context.getSharedPreferences("NotificationPrefs", Context.MODE_PRIVATE) }
    
    // We store hidden packages in a Set string in SharedPreferences
    var hiddenPackages by remember { 
        mutableStateOf(prefs.getStringSet("hidden_packages", emptySet()) ?: emptySet())
    }
    
    // Filter dialog
    var showFilterDialog by remember { mutableStateOf(false) }
    
    // Check if permission is granted
    val hasPermission = remember { 
        android.provider.Settings.Secure.getString(
            context.contentResolver,
            "enabled_notification_listeners"
        )?.contains(context.packageName) == true
    }

    if (!hasPermission) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.padding(16.dp)) {
                Text("Notification Access Required", color = Color.White)
                Spacer(modifier = Modifier.height(8.dp))
                Button(onClick = {
                    val intent = android.content.Intent("android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS")
                    intent.flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK
                    context.startActivity(intent)
                }) {
                    Text("Grant Permission")
                }
            }
        }
        return
    }

    val visibleNotifications = notifications.filter { !hiddenPackages.contains(it.packageName) }

    Column(modifier = Modifier.fillMaxSize()) {
        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Notifications", style = MaterialTheme.typography.titleMedium, color = Color.White)
            Row {
                IconButton(onClick = { showFilterDialog = true }) {
                    Icon(Icons.Default.FilterList, "Filter Apps", tint = Color.White)
                }
                IconButton(onClick = { 
                    val intent = Intent(context, NotificationHistoryActivity::class.java).apply {
                        flags = Intent.FLAG_ACTIVITY_NEW_TASK
                    }
                    context.startActivity(intent)
                }) {
                    Icon(Icons.Default.History, "History", tint = Color.White)
                }
            }
        }
        
        LazyColumn(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(visibleNotifications, key = { it.key }) { sbn ->
                NotificationItem(context, sbn, onCloseSidebar = onCloseSidebar, onHideApp = { pkg ->
                    val updated = hiddenPackages.toMutableSet().apply { add(pkg) }
                    prefs.edit().putStringSet("hidden_packages", updated).apply()
                    hiddenPackages = updated
                })
            }
            item {
                Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }
    
    if (showFilterDialog) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color.Black.copy(alpha = 0.6f))
                .clickable(
                    interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                    indication = null
                ) { showFilterDialog = false },
            contentAlignment = Alignment.Center
        ) {
            Card(
                modifier = Modifier
                    .fillMaxWidth(0.9f)
                    .fillMaxHeight(0.8f)
                    .padding(16.dp),
                shape = androidx.compose.foundation.shape.RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
            ) {
                Column(modifier = Modifier.padding(24.dp).fillMaxSize()) {
                    Text(
                        text = "Filter Apps in Sidebar",
                        style = MaterialTheme.typography.titleLarge,
                        modifier = Modifier.padding(bottom = 16.dp)
                    )
                    
                    val pm = context.packageManager
                    val appsInList = notifications.map { it.packageName to 
                        try { pm.getApplicationLabel(pm.getApplicationInfo(it.packageName, 0)).toString() } 
                        catch(e: Exception) { it.packageName }
                    }.distinctBy { it.first }
                    
                    LazyColumn(modifier = Modifier.weight(1f)) {
                        items(appsInList) { (pkg, name) ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 4.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Checkbox(
                                    checked = !hiddenPackages.contains(pkg),
                                    onCheckedChange = { checked ->
                                        val newHidden = hiddenPackages.toMutableSet()
                                        if (checked) {
                                            newHidden.remove(pkg)
                                        } else {
                                            newHidden.add(pkg)
                                        }
                                        hiddenPackages = newHidden
                                        prefs.edit().putStringSet("hidden_packages", newHidden).apply()
                                    }
                                )
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(name)
                            }
                        }
                    }
                    
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(top = 16.dp),
                        horizontalArrangement = Arrangement.End
                    ) {
                        TextButton(onClick = { showFilterDialog = false }) {
                            Text("Done")
                        }
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalFoundationApi::class, ExperimentalMaterial3Api::class)
@Composable
fun NotificationItem(context: Context, sbn: StatusBarNotification, onCloseSidebar: () -> Unit, onHideApp: (String) -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    var replyText by remember { mutableStateOf("") }
    
    val notification = sbn.notification
    val title = notification.extras.getString(android.app.Notification.EXTRA_TITLE) ?: "No Title"
    val text = notification.extras.getCharSequence(android.app.Notification.EXTRA_TEXT)?.toString() ?: ""
    
    val pm = context.packageManager
    val appName = try {
        pm.getApplicationLabel(pm.getApplicationInfo(sbn.packageName, 0)).toString()
    } catch (e: Exception) {
        sbn.packageName
    }


            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .combinedClickable(
                        onClick = {
                            try {
                                if (android.os.Build.VERSION.SDK_INT >= 34) {
                                    val options = android.app.ActivityOptions.makeBasic()
                                    options.pendingIntentBackgroundActivityStartMode = android.app.ActivityOptions.MODE_BACKGROUND_ACTIVITY_START_ALLOWED
                                    notification.contentIntent?.send(context, 0, android.content.Intent(), null, null, null, options.toBundle())
                                } else {
                                    notification.contentIntent?.send()
                                }
                                AppNotificationListener.instance?.cancelNotification(sbn.key)
                                onCloseSidebar()
                            } catch (e: Exception) {
                                com.example.LogKeeper.writeLog("Notification", "Failed to open notification content for ${sbn.packageName}: ${e.message}")
                            }
                        },
                        onLongClick = {
                            AppNotificationListener.instance?.cancelNotification(sbn.key)
                        }
                    ),
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = Color(0xFF2A2A2A))
            ) {
                Column(modifier = Modifier.padding(start = 12.dp, end = 12.dp, top = 8.dp, bottom = 12.dp)) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(bottom = 4.dp)
                    ) {
                        Text(
                            text = appName,
                            style = MaterialTheme.typography.labelSmall,
                            color = Color.LightGray,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.weight(1f)
                        )
                        IconButton(
                            onClick = { expanded = !expanded },
                            modifier = Modifier.size(24.dp)
                        ) {
                            Icon(
                                imageVector = if (expanded) Icons.Default.ExpandLess else Icons.Default.ExpandMore,
                                contentDescription = if (expanded) "Collapse" else "Expand",
                                tint = Color.LightGray
                            )
                        }
                    }
                    
                    Text(
                        text = title,
                        style = MaterialTheme.typography.titleMedium,
                        color = Color.White,
                        maxLines = if (expanded) Int.MAX_VALUE else 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    
                    if (text.isNotEmpty()) {
                        Spacer(modifier = Modifier.height(2.dp))
                        Text(
                            text = text,
                            style = MaterialTheme.typography.bodyMedium,
                            color = Color.LightGray,
                            maxLines = if (expanded) Int.MAX_VALUE else 1,
                            overflow = TextOverflow.Ellipsis
                        )
                    }
                    
                    if (!expanded && (text.length > 30 || notification.actions?.isNotEmpty() == true)) {
                        Spacer(modifier = Modifier.height(4.dp))
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(2.dp)
                                .background(Color.Gray.copy(alpha = 0.5f), RoundedCornerShape(1.dp))
                        )
                    }
                    
                    if (expanded && notification.actions != null && notification.actions.isNotEmpty()) {
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        val remoteInputActions = notification.actions.filter { it.remoteInputs?.isNotEmpty() == true }
                        val normalActions = notification.actions.filter { it.remoteInputs.isNullOrEmpty() }
                        
                        if (remoteInputActions.isNotEmpty()) {
                            val replyAction = remoteInputActions.first()
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                OutlinedTextField(
                                    value = replyText,
                                    onValueChange = { replyText = it },
                                    placeholder = { Text(replyAction.title?.toString() ?: "Reply...") },
                                    modifier = Modifier.weight(1f),
                                    singleLine = true,
                                    textStyle = MaterialTheme.typography.bodyMedium.copy(color = Color.White)
                                )
                                Spacer(modifier = Modifier.width(8.dp))
                                Button(
                                    onClick = {
                                        if (replyText.isNotEmpty()) {
                                            try {
                                                val remoteInputs = replyAction.remoteInputs
                                                val intent = android.content.Intent()
                                                val bundle = android.os.Bundle()
                                                for (input in remoteInputs) {
                                                    bundle.putCharSequence(input.resultKey, replyText)
                                                }
                                                android.app.RemoteInput.addResultsToIntent(remoteInputs, intent, bundle)
                                                if (android.os.Build.VERSION.SDK_INT >= 34) {
                                                    val options = android.app.ActivityOptions.makeBasic()
                                                    options.pendingIntentBackgroundActivityStartMode = android.app.ActivityOptions.MODE_BACKGROUND_ACTIVITY_START_ALLOWED
                                                    replyAction.actionIntent.send(context, 0, intent, null, null, null, options.toBundle())
                                                } else {
                                                    replyAction.actionIntent.send(context, 0, intent)
                                                }
                                                replyText = ""
                                            } catch (e: Exception) {
                                                com.example.LogKeeper.writeLog("Notification", "Failed to send reply to ${sbn.packageName}: ${e.message}")
                                            }
                                        }
                                    },
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4CAF50))
                                ) {
                                    Text("Send")
                                }
                            }
                            Spacer(modifier = Modifier.height(8.dp))
                        }
                        
                        if (normalActions.isNotEmpty()) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                normalActions.take(3).forEach { action ->
                                    val actionTitle = action.title?.toString() ?: ""
                                    if (actionTitle.isNotEmpty()) {
                                        Button(
                                            onClick = {
                                                try {
                                                    if (android.os.Build.VERSION.SDK_INT >= 34) {
                                                        val options = android.app.ActivityOptions.makeBasic()
                                                        options.pendingIntentBackgroundActivityStartMode = android.app.ActivityOptions.MODE_BACKGROUND_ACTIVITY_START_ALLOWED
                                                        action.actionIntent.send(context, 0, android.content.Intent(), null, null, null, options.toBundle())
                                                    } else {
                                                        action.actionIntent.send()
                                                    }
                                                    onCloseSidebar()
                                                } catch (e: Exception) {
                                                    com.example.LogKeeper.writeLog("Notification", "Failed to execute action ${actionTitle} for ${sbn.packageName}: ${e.message}")
                                                }
                                            },
                                            modifier = Modifier.weight(1f),
                                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF444444)),
                                            contentPadding = PaddingValues(horizontal = 8.dp, vertical = 4.dp)
                                        ) {
                                            Text(
                                                actionTitle,
                                                maxLines = 1,
                                                overflow = TextOverflow.Ellipsis,
                                                style = MaterialTheme.typography.labelSmall
                                            )
                                        }
                                    }
                                }
                            }
                        }
                    }
                    
                    if (expanded) {
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.End
                        ) {
                            TextButton(
                                onClick = { onHideApp(sbn.packageName) },
                                contentPadding = PaddingValues(horizontal = 8.dp, vertical = 4.dp)
                            ) {
                                Text("Hide App in Sidebar", style = MaterialTheme.typography.labelSmall, color = Color.Gray)
                            }
                        }
                    }
                }
            }
}
