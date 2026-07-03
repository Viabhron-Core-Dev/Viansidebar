import re
with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'r') as f:
    content = f.read()

new_method = """    fun onFolderItemAdded(folderUuid: String, itemId: String) {
        val editView = sidebarEditOverlayView ?: return
        val localIds = editView.localIds
        for (i in 0 until localIds.size) {
            var item = localIds[i]
            if (item.startsWith("folder:$folderUuid:")) {
                try {
                    val parts = item.split(":", limit = 3)
                    val folderDataStr = parts[2]
                    val obj = org.json.JSONObject(folderDataStr)
                    val itemsArr = obj.optJSONArray("items") ?: org.json.JSONArray()
                    itemsArr.put(itemId)
                    obj.put("items", itemsArr)
                    localIds[i] = "folder:$folderUuid:${obj.toString()}"
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        }
        editView.refresh()
    }"""

content = content.replace("class FloatingReaderService : Service() {", "class FloatingReaderService : Service() {\n\n" + new_method)

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'w') as f:
    f.write(content)
