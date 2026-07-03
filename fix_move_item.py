import re
with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

old_move = """    fun moveItem(id: String, moveUp: Boolean) {
        (context as? com.example.service.FloatingReaderService)?.onFolderItemAdded(folderUuid, itemId)
        coroutineScope.launch(Dispatchers.IO) {"""

new_move = """    fun moveItem(id: String, moveUp: Boolean) {
        coroutineScope.launch(Dispatchers.IO) {"""

content = content.replace(old_move, new_move)

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)
