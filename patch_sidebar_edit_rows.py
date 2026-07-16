import re

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "r") as f:
    content = f.read()

target = """            prefs.edit().putString("sidebar_apps", arr.toString()).apply()
            prefs.edit().putInt("sidebar_columns", totalCols).apply()
            com.example.LogKeeper.writeLog("SidebarEdit", "Saved ${localIds.size} items to apps grid.")"""

replacement = """            prefs.edit().putString("sidebar_apps", arr.toString()).apply()
            prefs.edit().putInt("sidebar_columns", totalCols).apply()
            prefs.edit().putInt("sidebar_rows", totalRows).apply()
            com.example.LogKeeper.writeLog("SidebarEdit", "Saved ${localIds.size} items to apps grid.")"""

content = content.replace(target, replacement)

# We should also load sidebar_rows
load_target = """        if (folderUuid == null) {
            totalCols = prefs.getInt("sidebar_columns", 3)
        }"""
load_replacement = """        if (folderUuid == null) {
            totalCols = prefs.getInt("sidebar_columns", 3)
            totalRows = prefs.getInt("sidebar_rows", 3)
        }"""
content = content.replace(load_target, load_replacement)

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "w") as f:
    f.write(content)
