package com.example

import android.app.Activity
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProviderInfo
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.drawable.BitmapDrawable
import android.graphics.drawable.Drawable
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.example.utils.AppWidgetHelper
import org.json.JSONObject

class WidgetPickerActivity : ComponentActivity() {
    private var appWidgetId = AppWidgetManager.INVALID_APPWIDGET_ID
    private lateinit var appWidgetManager: AppWidgetManager
    private var selectedProvider: AppWidgetProviderInfo? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        appWidgetManager = AppWidgetManager.getInstance(this)
        
        val host = AppWidgetHelper.getHost(this)
        appWidgetId = host.allocateAppWidgetId()

        setContent {
            MaterialTheme(colorScheme = darkColorScheme()) {
                WidgetPickerScreen(
                    providers = appWidgetManager.installedProviders,
                    onWidgetSelected = { provider ->
                        handleWidgetSelected(provider)
                    },
                    onCancel = {
                        AppWidgetHelper.getHost(this).deleteAppWidgetId(appWidgetId)
                        finish()
                    }
                )
            }
        }
    }

    private fun handleWidgetSelected(provider: AppWidgetProviderInfo) {
        selectedProvider = provider
        val allowed = appWidgetManager.bindAppWidgetIdIfAllowed(appWidgetId, provider.provider)
        if (allowed) {
            proceedToConfigureOrFinish()
        } else {
            val intent = Intent(AppWidgetManager.ACTION_APPWIDGET_BIND)
            intent.putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, appWidgetId)
            intent.putExtra(AppWidgetManager.EXTRA_APPWIDGET_PROVIDER, provider.provider)
            try {
                startActivityForResult(intent, 200)
            } catch (e: Exception) {
                Toast.makeText(this, "Failed to bind widget", Toast.LENGTH_SHORT).show()
                finish()
            }
        }
    }

    private fun proceedToConfigureOrFinish() {
        val provider = selectedProvider ?: return
        if (provider.configure != null) {
            val configIntent = Intent(AppWidgetManager.ACTION_APPWIDGET_CONFIGURE)
            configIntent.component = provider.configure
            configIntent.putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, appWidgetId)
            try {
                startActivityForResult(configIntent, 101)
            } catch (e: Exception) {
                finishWithSuccess(appWidgetId)
            }
        } else {
            finishWithSuccess(appWidgetId)
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        
        if (requestCode == 200) {
            if (resultCode == RESULT_OK) {
                proceedToConfigureOrFinish()
            } else {
                Toast.makeText(this, "Widget binding denied", Toast.LENGTH_SHORT).show()
                AppWidgetHelper.getHost(this).deleteAppWidgetId(appWidgetId)
                finish()
            }
        } else if (requestCode == 101) {
            if (resultCode == RESULT_OK) {
                finishWithSuccess(appWidgetId)
            } else {
                AppWidgetHelper.getHost(this).deleteAppWidgetId(appWidgetId)
                finish()
            }
        }
    }
    
    private fun finishWithSuccess(widgetId: Int) {
        val actionType = intent.getStringExtra("ACTION_TYPE") ?: "ADD_ELEMENT"
        
        if (actionType == "ADD_ELEMENT") {
            val info = appWidgetManager.getAppWidgetInfo(widgetId)
            val label = info?.loadLabel(packageManager) ?: "Widget"
            
            val json = JSONObject()
            json.put("widgetId", widgetId)
            json.put("label", label)
            val id = "widget:${widgetId}:${json.toString()}"
            
            val serviceIntent = Intent(this, com.example.service.FloatingReaderService::class.java)
            serviceIntent.action = "ADD_ELEMENT"
            serviceIntent.putExtra("element_id", id)
            
            val folderUuid = intent.getStringExtra("FOLDER_UUID")
            val isElementCallback = intent.getBooleanExtra("IS_ELEMENT_CALLBACK", false)
            
            if (folderUuid != null) {
                serviceIntent.putExtra("FOLDER_UUID", folderUuid)
            }
            if (isElementCallback) {
                serviceIntent.putExtra("IS_ELEMENT_CALLBACK", true)
            }
            startService(serviceIntent)
        } else if (actionType == "CREATE_PAGE") {
            val broadcastIntent = Intent("WIDGET_PAGE_CREATED")
            broadcastIntent.putExtra("WIDGET_ID", widgetId)
            sendBroadcast(broadcastIntent)
        }
        
        finish()
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WidgetPickerScreen(
    providers: List<AppWidgetProviderInfo>,
    onWidgetSelected: (AppWidgetProviderInfo) -> Unit,
    onCancel: () -> Unit
) {
    val context = LocalContext.current
    val pm = context.packageManager
    
    // Group by app name
    val grouped = remember(providers) {
        providers.groupBy { it.loadLabel(pm).toString() }.toSortedMap()
    }

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = Color(0xCC000000)
    ) {
        Box(contentAlignment = Alignment.Center, modifier = Modifier.fillMaxSize().clickable(onClick = onCancel)) {
            Card(
                modifier = Modifier
                    .fillMaxWidth(0.9f)
                    .fillMaxHeight(0.8f)
                    .clickable(enabled = false, onClick = {}), // consume clicks
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = "Choose a Widget",
                        style = MaterialTheme.typography.titleLarge,
                        modifier = Modifier.padding(bottom = 16.dp)
                    )
                    
                    LazyColumn(modifier = Modifier.weight(1f)) {
                        grouped.forEach { (appName, appProviders) ->
                            item {
                                Text(
                                    text = appName,
                                    style = MaterialTheme.typography.titleMedium,
                                    color = MaterialTheme.colorScheme.primary,
                                    modifier = Modifier.padding(vertical = 8.dp, horizontal = 8.dp)
                                )
                            }
                            items(appProviders) { provider ->
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .clickable { onWidgetSelected(provider) }
                                        .padding(vertical = 12.dp, horizontal = 16.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    // Try to load icon
                                    val iconDrawable = provider.loadIcon(context, context.resources.displayMetrics.densityDpi)
                                    if (iconDrawable != null) {
                                        val bitmap = drawableToBitmap(iconDrawable)
                                        Image(
                                            bitmap = bitmap.asImageBitmap(),
                                            contentDescription = null,
                                            modifier = Modifier.size(48.dp)
                                        )
                                        Spacer(modifier = Modifier.width(16.dp))
                                    } else {
                                        Box(modifier = Modifier.size(48.dp).background(Color.Gray, RoundedCornerShape(8.dp)))
                                        Spacer(modifier = Modifier.width(16.dp))
                                    }
                                    
                                    Column {
                                        Text(
                                            text = provider.loadLabel(pm),
                                            style = MaterialTheme.typography.bodyLarge,
                                            maxLines = 1,
                                            overflow = TextOverflow.Ellipsis
                                        )
                                    }
                                }
                            }
                        }
                    }
                    
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
                        TextButton(onClick = onCancel) {
                            Text("Cancel")
                        }
                    }
                }
            }
        }
    }
}

fun drawableToBitmap(drawable: Drawable): Bitmap {
    if (drawable is BitmapDrawable) {
        if (drawable.bitmap != null) {
            return drawable.bitmap
        }
    }
    val bitmap = if (drawable.intrinsicWidth <= 0 || drawable.intrinsicHeight <= 0) {
        Bitmap.createBitmap(1, 1, Bitmap.Config.ARGB_8888)
    } else {
        Bitmap.createBitmap(drawable.intrinsicWidth, drawable.intrinsicHeight, Bitmap.Config.ARGB_8888)
    }
    val canvas = Canvas(bitmap)
    drawable.setBounds(0, 0, canvas.width, canvas.height)
    drawable.draw(canvas)
    return bitmap
}
