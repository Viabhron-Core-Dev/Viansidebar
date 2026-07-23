import re

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "r") as f:
    content = f.read()

content = content.replace(
"""        if (folderUuid == null) {
            totalCols = prefs.getInt("sidebar_columns", 3)
            totalRows = prefs.getInt("sidebar_rows", 3)
        }""",
"""        if (folderUuid == null) {
            val handleId = intent.getStringExtra("HANDLE_ID") ?: "sidebar"
            val c = prefs.getInt("handle_${handleId}_page_${pageId}_columns", -1)
            if (c == -1) {
                totalCols = if (handleId == "sidebar" && pageId == "default_apps") prefs.getInt("sidebar_columns", 3) else 3
                totalRows = if (handleId == "sidebar" && pageId == "default_apps") prefs.getInt("sidebar_rows", 3) else 3
            } else {
                totalCols = c
                totalRows = prefs.getInt("handle_${handleId}_page_${pageId}_rows", 3)
            }
        }"""
)

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "w") as f:
    f.write(content)
