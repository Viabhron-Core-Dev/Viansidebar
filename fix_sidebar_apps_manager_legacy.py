import re

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "r") as f:
    content = f.read()

content = content.replace(
"""    private suspend fun loadActiveApps() = withContext(Dispatchers.IO) {
        var jsonStr = prefs.getString(prefKey, \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\") ?: \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\"
        if (jsonStr == "[]" || jsonStr == \"\"\"["system:log_keeper"]\"\"\") {""",
"""    private suspend fun loadActiveApps() = withContext(Dispatchers.IO) {
        var jsonStr = prefs.getString(prefKey, null)
        if (jsonStr == null) {
            if (prefKey == "sidebar_apps_sidebar_default_apps") {
                jsonStr = prefs.getString("sidebar_apps", \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\")
            }
            if (jsonStr == null) {
                jsonStr = \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\"
            }
        }
        if (jsonStr == "[]" || jsonStr == \"\"\"["system:log_keeper"]\"\"\") {"""
)

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "w") as f:
    f.write(content)
