import os
import re

with open("app/src/main/java/com/example/HybridGridEditActivity.kt", "r") as f:
    content = f.read()

# Make getHybridWidgetName handle elements using SidebarAppsManager
pattern = r'fun getHybridWidgetName\(context: Context, id: String, appWidgetManager: AppWidgetManager\): String \{([\s\S]*?)fun loadHybridLocalItems'

repl = '''fun getHybridWidgetName(context: Context, id: String, appWidgetManager: AppWidgetManager, appsManager: com.example.service.SidebarAppsManager): String {
    if (id.startsWith("widget:")) {
        val wId = id.removePrefix("widget:").toIntOrNull() ?: return "Unknown Widget"
        val info = appWidgetManager.getAppWidgetInfo(wId)
        return info?.loadLabel(appWidgetManager.context.packageManager) ?: "Widget $wId"
    } else {
        return appsManager.parseId(id)?.label ?: id
    }
}

fun loadHybridLocalItems'''

content = re.sub(pattern, repl, content)

# update usage
content = content.replace(
    'text = getHybridWidgetName(androidx.compose.ui.platform.LocalContext.current, item.id, appWidgetManager),',
    'text = getHybridWidgetName(androidx.compose.ui.platform.LocalContext.current, item.id, appWidgetManager, appsManager),'
)

content = content.replace(
    'appWidgetManager = appWidgetManager,',
    'appWidgetManager = appWidgetManager,\n                        appsManager = appsManager,'
)

content = content.replace(
    'cols: Int,',
    'cols: Int,\n    appsManager: com.example.service.SidebarAppsManager,'
)

# Also need to create appsManager in the activity
content = content.replace(
    'private lateinit var appWidgetManager: AppWidgetManager',
    'private lateinit var appWidgetManager: AppWidgetManager\n    private lateinit var appsManager: com.example.service.SidebarAppsManager'
)

content = content.replace(
    'appWidgetManager = AppWidgetManager.getInstance(this)',
    'appWidgetManager = AppWidgetManager.getInstance(this)\n        appsManager = com.example.service.SidebarAppsManager(this, prefs, kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO), "hg_${pageId}") {}\n        appsManager.ensureLoaded()'
)

with open("app/src/main/java/com/example/HybridGridEditActivity.kt", "w") as f:
    f.write(content)

