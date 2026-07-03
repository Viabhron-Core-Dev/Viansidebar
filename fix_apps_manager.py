import re
with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

old_add_item = """        coroutineScope.launch(Dispatchers.IO) {
            val currentStr = prefs.getString("sidebar_apps", \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\") ?: return@launch"""

new_add_item = """        (context as? com.example.service.FloatingReaderService)?.onFolderItemAdded(folderUuid, itemId)
        coroutineScope.launch(Dispatchers.IO) {
            val currentStr = prefs.getString("sidebar_apps", \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\") ?: return@launch"""

content = content.replace(old_add_item, new_add_item)

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)
