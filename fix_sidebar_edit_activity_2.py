import re

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "r") as f:
    content = f.read()

content = content.replace(
"""        manager = SidebarAppsManager(this, prefs, serviceScope, pageId) {
            runOnUiThread {
                if (::adapter.isInitialized) {
                    adapter.notifyDataSetChanged()
                }
            }
        }
        
        folderUuid = intent.getStringExtra("FOLDER_UUID")
        pageId = intent.getStringExtra("PAGE_ID") ?: "default_apps\"""",
"""        folderUuid = intent.getStringExtra("FOLDER_UUID")
        pageId = intent.getStringExtra("PAGE_ID") ?: "default_apps"
        val handleId = intent.getStringExtra("HANDLE_ID") ?: "sidebar"
        val prefKey = "sidebar_apps_" + handleId + "_" + pageId
        
        manager = SidebarAppsManager(this, prefs, serviceScope, prefKey) {
            runOnUiThread {
                if (::adapter.isInitialized) {
                    adapter.notifyDataSetChanged()
                }
            }
        }"""
)

# And fix saveIds where it accesses prefs directly!
content = content.replace(
"""        if (folderUuid != null) {
            val resultIntent = Intent()
            resultIntent.putExtra("UPDATED_FOLDER", arr.toString())
            resultIntent.putExtra("FOLDER_UUID", folderUuid)
            setResult(Activity.RESULT_OK, resultIntent)
            // Removed direct save to prefs; parent grid will save
        } else {
            prefs.edit().putString("sidebar_apps_${pageId}", arr.toString()).apply()
            prefs.edit().putInt("sidebar_columns", totalCols).apply()
            prefs.edit().putInt("sidebar_rows", totalRows).apply()
            com.example.LogKeeper.writeLog("SidebarEdit", "Saved ${localIds.size} items to apps grid.")
        }""",
"""        if (folderUuid != null) {
            val resultIntent = Intent()
            resultIntent.putExtra("UPDATED_FOLDER", arr.toString())
            resultIntent.putExtra("FOLDER_UUID", folderUuid)
            setResult(Activity.RESULT_OK, resultIntent)
            // Removed direct save to prefs; parent grid will save
        } else {
            val handleId = intent.getStringExtra("HANDLE_ID") ?: "sidebar"
            val prefKey = "sidebar_apps_" + handleId + "_" + pageId
            prefs.edit().putString(prefKey, arr.toString()).apply()
            prefs.edit().putInt("handle_${handleId}_page_${pageId}_columns", totalCols).apply()
            prefs.edit().putInt("handle_${handleId}_page_${pageId}_rows", totalRows).apply()
            com.example.LogKeeper.writeLog("SidebarEdit", "Saved ${localIds.size} items to apps grid.")
        }"""
)

# Fix loadLocalIds
content = content.replace(
"""        if (folderUuid != null) {
            val fullFolderId = intent.getStringExtra("FOLDER_FULL_ID")
            // ...
        } else {
            val jsonStr = prefs.getString("sidebar_apps_${pageId}", \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\") ?: \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\"
            val arr = JSONArray(jsonStr)""",
"""        if (folderUuid != null) {
            val fullFolderId = intent.getStringExtra("FOLDER_FULL_ID")
            // ...
        } else {
            val handleId = intent.getStringExtra("HANDLE_ID") ?: "sidebar"
            val prefKey = "sidebar_apps_" + handleId + "_" + pageId
            val jsonStr = prefs.getString(prefKey, \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\") ?: \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\"
            val arr = JSONArray(jsonStr)"""
)

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "w") as f:
    f.write(content)
