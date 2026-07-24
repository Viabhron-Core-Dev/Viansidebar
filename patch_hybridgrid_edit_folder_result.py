import os
import re

with open("app/src/main/java/com/example/HybridGridEditActivity.kt", "r") as f:
    content = f.read()

pattern = r'if \(requestCode == 201 && resultCode == Activity\.RESULT_OK && data != null\) \{'

repl = '''if (requestCode == 200 && resultCode == Activity.RESULT_OK && data != null) {
            val updatedFolder = data.getStringExtra("UPDATED_FOLDER")
            val uuid = data.getStringExtra("FOLDER_UUID")
            if (updatedFolder != null && uuid != null) {
                // Update items in prefs directly
                val prefs = getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
                val itemsJson = prefs.getString("sidebar_hybrid_$pageId", "[]")
                val arr = org.json.JSONArray(itemsJson)
                val parsedItems = mutableListOf<com.example.service.GridWidgetItem>()
                for (i in 0 until arr.length()) {
                    val obj = arr.getJSONObject(i)
                    parsedItems.add(com.example.service.GridWidgetItem(
                        id = obj.getString("id"),
                        cols = obj.getInt("cols"),
                        rows = obj.getInt("rows"),
                        x = obj.getInt("x"),
                        y = obj.getInt("y")
                    ))
                }
                
                val index = parsedItems.indexOfFirst { it.id.startsWith("folder:$uuid:") }
                if (index != -1) {
                    parsedItems[index] = parsedItems[index].copy(id = updatedFolder)
                    
                    val newArr = org.json.JSONArray()
                    parsedItems.forEach {
                        val obj = org.json.JSONObject()
                        obj.put("id", it.id)
                        obj.put("cols", it.cols)
                        obj.put("rows", it.rows)
                        obj.put("x", it.x)
                        obj.put("y", it.y)
                        newArr.put(obj)
                    }
                    prefs.edit().putString("sidebar_hybrid_$pageId", newArr.toString()).apply()
                    
                    val bIntent = Intent("ELEMENT_ADDED_TO_HYBRID")
                    bIntent.putExtra("PAGE_ID", pageId)
                    bIntent.setPackage(packageName)
                    sendBroadcast(bIntent)
                }
            }
        } else if (requestCode == 201 && resultCode == Activity.RESULT_OK && data != null) {'''

content = content.replace('if (requestCode == 201 && resultCode == Activity.RESULT_OK && data != null) {', repl)

with open("app/src/main/java/com/example/HybridGridEditActivity.kt", "w") as f:
    f.write(content)
