import re

with open("app/src/main/java/com/example/service/AppsPageView.kt", "r") as f:
    content = f.read()

content = content.replace(
"""class AppsPageView(
    context: Context,
    val pageConfig: SidebarPage?,
    private val manager: SidebarAppsManager,
    private val coroutineScope: CoroutineScope,""",
"""class AppsPageView(
    context: Context,
    val handleId: String,
    val pageConfig: SidebarPage?,
    private val manager: SidebarAppsManager,
    private val coroutineScope: CoroutineScope,"""
)

# And fix the column logic
content = content.replace(
    'val columns = if (pageConfig?.useCustomSettings == true) pageConfig.gridColumns else prefs.getInt("sidebar_columns", 3)',
    'val c = prefs.getInt("handle_${handleId}_page_${pageConfig?.id}_columns", -1)\n        val defaultCols = if (handleId == "sidebar" && pageConfig?.id == "default_apps") prefs.getInt("sidebar_columns", 3) else 3\n        val columns = if (pageConfig?.useCustomSettings == true) pageConfig.gridColumns else (if (c != -1) c else defaultCols)'
)
content = content.replace(
    'if (currentSpan == (if (pageConfig?.useCustomSettings == true) pageConfig.gridColumns else prefs.getInt("sidebar_columns", 3)))',
    'if (currentSpan == columns)'
)
content = content.replace(
    'layoutManager = GridLayoutManager(context, columns)',
    'layoutManager = GridLayoutManager(context, columns)' # just to be safe it's unchanged
)

with open("app/src/main/java/com/example/service/AppsPageView.kt", "w") as f:
    f.write(content)
