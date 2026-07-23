import re

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "r") as f:
    content = f.read()

content = content.replace(
"""            val handleId = intent.getStringExtra("HANDLE_ID") ?: "sidebar"
            val prefKey = "sidebar_apps_" + handleId + "_" + pageId
            val jsonStr = prefs.getString(prefKey, \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\") ?: \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\"
            val arr = JSONArray(jsonStr)""",
"""            val handleId = intent.getStringExtra("HANDLE_ID") ?: "sidebar"
            val prefKey = "sidebar_apps_" + handleId + "_" + pageId
            var jsonStr = prefs.getString(prefKey, null)
            if (jsonStr == null) {
                if (prefKey == "sidebar_apps_sidebar_default_apps") {
                    jsonStr = prefs.getString("sidebar_apps", \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\")
                }
                if (jsonStr == null) {
                    jsonStr = \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\"
                }
            }
            val arr = JSONArray(jsonStr)"""
)

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "w") as f:
    f.write(content)
