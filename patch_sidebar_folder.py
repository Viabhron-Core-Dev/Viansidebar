import re

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "r") as f:
    content = f.read()

# 1. Update setOnClickListener for folder
target_click = """            holder.itemView.setOnClickListener {
                if (id.startsWith("folder:")) {
                    val uuid = id.split(":")[1]
                    val intent = Intent(this@SidebarEditActivity, SidebarEditActivity::class.java).apply {
                        putExtra("FOLDER_UUID", uuid)
                    }
                    startActivityForResult(intent, 200)
                }
            }"""
replacement_click = """            holder.itemView.setOnClickListener {
                if (id.startsWith("folder:")) {
                    val uuid = id.split(":")[1]
                    val intent = Intent(this@SidebarEditActivity, SidebarEditActivity::class.java).apply {
                        putExtra("FOLDER_UUID", uuid)
                        putExtra("FOLDER_FULL_ID", id)
                    }
                    startActivityForResult(intent, 200)
                }
            }"""
content = content.replace(target_click, replacement_click)

# 2. Update loadLocalIds
target_load = """    private fun loadLocalIds() {
        localIds.clear()
        val jsonStr = prefs.getString("sidebar_apps", \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\") ?: \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\"
        val arr = JSONArray(jsonStr)
        
        if (folderUuid != null) {
            for (i in 0 until arr.length()) {
                var item = arr.getString(i)
                if (item.startsWith("folder:$folderUuid:")) {
                    try {
                        val parts = item.split(":", limit = 3)
                        val folderDataStr = parts[2]
                        val obj = org.json.JSONObject(folderDataStr)
                        folderName = obj.optString("name", "Folder")
                        folderColor = obj.optString("colorHex", "#444444")
                        folderStyle = obj.optInt("folderStyle", 0)
                        totalCols = obj.optInt("popupColumns", 0)
                        if (totalCols <= 0) totalCols = prefs.getInt("sidebar_columns", 3)
                        totalRows = obj.optInt("popupRows", 0)
                        
                        val itemsArr = obj.optJSONArray("items") ?: org.json.JSONArray()
                        for (j in 0 until itemsArr.length()) {
                            localIds.add(itemsArr.getString(j))
                        }
                    } catch (e: Exception) {}
                    break
                }
            }
        } else {"""

replacement_load = """    private fun loadLocalIds() {
        localIds.clear()
        val fullFolderId = intent.getStringExtra("FOLDER_FULL_ID")
        if (folderUuid != null && fullFolderId != null && fullFolderId.startsWith("folder:")) {
            try {
                val parts = fullFolderId.split(":", limit = 3)
                val folderDataStr = parts[2]
                val obj = org.json.JSONObject(folderDataStr)
                folderName = obj.optString("name", "Folder")
                folderColor = obj.optString("colorHex", "#444444")
                folderStyle = obj.optInt("folderStyle", 0)
                totalCols = obj.optInt("popupColumns", 0)
                if (totalCols <= 0) totalCols = prefs.getInt("sidebar_columns", 3)
                totalRows = obj.optInt("popupRows", 0)
                
                val itemsArr = obj.optJSONArray("items") ?: org.json.JSONArray()
                for (j in 0 until itemsArr.length()) {
                    localIds.add(itemsArr.getString(j))
                }
            } catch (e: Exception) {}
        } else {
            val jsonStr = prefs.getString("sidebar_apps", \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\") ?: \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\"
            val arr = JSONArray(jsonStr)
            for (i in 0 until arr.length()) {
                localIds.add(arr.getString(i))
            }
        }"""
        
# Be careful with the else block in loadLocalIds. The original ends with:
#         } else {
#             for (i in 0 until arr.length()) {
#                 localIds.add(arr.getString(i))
#             }
#         }
#     }
target_load_full = """    private fun loadLocalIds() {
        localIds.clear()
        val jsonStr = prefs.getString("sidebar_apps", \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\") ?: \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\"
        val arr = JSONArray(jsonStr)
        
        if (folderUuid != null) {
            for (i in 0 until arr.length()) {
                var item = arr.getString(i)
                if (item.startsWith("folder:$folderUuid:")) {
                    try {
                        val parts = item.split(":", limit = 3)
                        val folderDataStr = parts[2]
                        val obj = org.json.JSONObject(folderDataStr)
                        folderName = obj.optString("name", "Folder")
                        folderColor = obj.optString("colorHex", "#444444")
                        folderStyle = obj.optInt("folderStyle", 0)
                        totalCols = obj.optInt("popupColumns", 0)
                        if (totalCols <= 0) totalCols = prefs.getInt("sidebar_columns", 3)
                        totalRows = obj.optInt("popupRows", 0)
                        
                        val itemsArr = obj.optJSONArray("items") ?: org.json.JSONArray()
                        for (j in 0 until itemsArr.length()) {
                            localIds.add(itemsArr.getString(j))
                        }
                    } catch (e: Exception) {}
                    break
                }
            }
        } else {
            for (i in 0 until arr.length()) {
                localIds.add(arr.getString(i))
            }
        }
    }"""
content = content.replace(target_load_full, replacement_load + "\n    }")

# 3. Update saveIds
target_save = """    private fun saveIds() {
        val arr = JSONArray()
        localIds.forEach { arr.put(it) }
        
        if (folderUuid != null) {
            val jsonStr = prefs.getString("sidebar_apps", \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\") ?: return
            val mainArr = JSONArray(jsonStr)
            val newMainArr = JSONArray()
            var newItemStr: String? = null
            for (i in 0 until mainArr.length()) {
                var item = mainArr.getString(i)
                if (item.startsWith("folder:$folderUuid:")) {
                    val obj = org.json.JSONObject()
                    obj.put("name", folderName)
                    obj.put("colorHex", folderColor)
                    obj.put("folderStyle", folderStyle)
                    obj.put("popupColumns", totalCols)
                    obj.put("popupRows", totalRows)
                    obj.put("items", arr)
                    item = "folder:$folderUuid:${obj.toString()}"
                    newItemStr = item
                }
                newMainArr.put(item)
            }
            prefs.edit().putString("sidebar_apps", newMainArr.toString()).apply()
            com.example.LogKeeper.writeLog("SidebarEdit", "Saved ${localIds.size} items to folder $folderUuid.")
            
            if (newItemStr != null) {
                val resultIntent = Intent().apply { 
                    putExtra("UPDATED_FOLDER", newItemStr)
                    putExtra("FOLDER_UUID", folderUuid)
                }
                setResult(RESULT_OK, resultIntent)
            }
        } else {"""

replacement_save = """    private fun saveIds() {
        val arr = JSONArray()
        localIds.forEach { arr.put(it) }
        
        if (folderUuid != null) {
            val obj = org.json.JSONObject()
            obj.put("name", folderName)
            obj.put("colorHex", folderColor)
            obj.put("folderStyle", folderStyle)
            obj.put("popupColumns", totalCols)
            obj.put("popupRows", totalRows)
            obj.put("items", arr)
            val newItemStr = "folder:$folderUuid:${obj.toString()}"
            
            val resultIntent = Intent().apply { 
                putExtra("UPDATED_FOLDER", newItemStr)
                putExtra("FOLDER_UUID", folderUuid)
            }
            setResult(RESULT_OK, resultIntent)
            // Removed direct save to prefs; parent grid will save
        } else {"""
content = content.replace(target_save, replacement_save)

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "w") as f:
    f.write(content)
