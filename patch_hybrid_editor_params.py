import os
import re

with open("app/src/main/java/com/example/HybridGridEditActivity.kt", "r") as f:
    content = f.read()

content = content.replace(
'''fun HybridGridEditor(
    pageId: String,
    prefs: android.content.SharedPreferences,
    appWidgetManager: AppWidgetManager,
    onClose: () -> Unit,
    onAddWidget: () -> Unit
) {''',
'''fun HybridGridEditor(
    pageId: String,
    prefs: android.content.SharedPreferences,
    appWidgetManager: AppWidgetManager,
    appsManager: com.example.service.SidebarAppsManager,
    onClose: () -> Unit,
    onAddWidget: () -> Unit
) {''')

content = content.replace(
'''fun HybridGridEditorCanvas(
    items: List<GridWidgetItem>,
    cols: Int,
    appsManager: com.example.service.SidebarAppsManager,
    appWidgetManager: AppWidgetManager,
    onUpdateItems: (List<GridWidgetItem>) -> Unit
) {''',
'''@Composable
fun HybridGridEditorCanvas(
    items: List<GridWidgetItem>,
    cols: Int,
    appWidgetManager: AppWidgetManager,
    appsManager: com.example.service.SidebarAppsManager,
    onUpdateItems: (List<GridWidgetItem>) -> Unit
) {''')

content = content.replace(
'''fun HybridGridEditorCanvas(
    items: List<GridWidgetItem>,
    cols: Int,
    appWidgetManager: AppWidgetManager,
    onUpdateItems: (List<GridWidgetItem>) -> Unit
) {''',
'''@Composable
fun HybridGridEditorCanvas(
    items: List<GridWidgetItem>,
    cols: Int,
    appWidgetManager: AppWidgetManager,
    appsManager: com.example.service.SidebarAppsManager,
    onUpdateItems: (List<GridWidgetItem>) -> Unit
) {''')

content = content.replace(
'''    fun getHybridWidgetName(context: Context, id: String, appWidgetManager: AppWidgetManager, appsManager: com.example.service.SidebarAppsManager): String {''',
'''fun getHybridWidgetName(context: Context, id: String, appWidgetManager: AppWidgetManager, appsManager: com.example.service.SidebarAppsManager): String {''')

with open("app/src/main/java/com/example/HybridGridEditActivity.kt", "w") as f:
    f.write(content)
