import re

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "r") as f:
    content = f.read()

content = content.replace(
"""class SidebarAppsManager(
    private val context: Context,
    private val prefs: SharedPreferences,
    private val coroutineScope: CoroutineScope,
    private val pageId: String,
    private val onAppsUpdated: () -> Unit
) {""",
"""class SidebarAppsManager(
    private val context: Context,
    private val prefs: SharedPreferences,
    private val coroutineScope: CoroutineScope,
    private val prefKey: String,
    private val onAppsUpdated: () -> Unit
) {"""
)

content = content.replace('"sidebar_apps_${pageId}"', 'prefKey')

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "w") as f:
    f.write(content)
