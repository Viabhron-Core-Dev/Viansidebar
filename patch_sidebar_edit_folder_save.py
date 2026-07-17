import re

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "r") as f:
    content = f.read()

# Change startActivity to startActivityForResult
target1 = """            holder.itemView.setOnClickListener {
                if (id.startsWith("folder:")) {
                    val uuid = id.split(":")[1]
                    val intent = Intent(this@SidebarEditActivity, SidebarEditActivity::class.java).apply {
                        putExtra("FOLDER_UUID", uuid)
                    }
                    startActivity(intent)
                }
            }"""

replacement1 = """            holder.itemView.setOnClickListener {
                if (id.startsWith("folder:")) {
                    val uuid = id.split(":")[1]
                    val intent = Intent(this@SidebarEditActivity, SidebarEditActivity::class.java).apply {
                        putExtra("FOLDER_UUID", uuid)
                    }
                    startActivityForResult(intent, 200)
                }
            }"""

content = content.replace(target1, replacement1)

# Handle onActivityResult for folders
target2 = """    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 100 && resultCode == RESULT_OK) {
            val id = data?.getStringExtra("ELEMENT_ID")
            if (id != null) {
                localIds.add(id)
                adapter.notifyItemInserted(localIds.size - 1)
            }
        }
    }"""

replacement2 = """    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 100 && resultCode == RESULT_OK) {
            val id = data?.getStringExtra("ELEMENT_ID")
            if (id != null) {
                localIds.add(id)
                adapter.notifyItemInserted(localIds.size - 1)
            }
        } else if (requestCode == 200 && resultCode == RESULT_OK) {
            val updatedFolder = data?.getStringExtra("UPDATED_FOLDER")
            val uuid = data?.getStringExtra("FOLDER_UUID")
            if (updatedFolder != null && uuid != null) {
                val index = localIds.indexOfFirst { it.startsWith("folder:$uuid:") }
                if (index != -1) {
                    localIds[index] = updatedFolder
                    adapter.notifyItemChanged(index)
                }
            }
        }
    }"""

content = content.replace(target2, replacement2)

# Change saveIds to also return RESULT_OK when editing folder
target3 = """        if (folderUuid != null) {
            val jsonStr = prefs.getString("sidebar_apps", \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\") ?: return
            val mainArr = JSONArray(jsonStr)
            val newMainArr = JSONArray()
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
                }
                newMainArr.put(item)
            }
            prefs.edit().putString("sidebar_apps", newMainArr.toString()).apply()
            com.example.LogKeeper.writeLog("SidebarEdit", "Saved ${localIds.size} items to folder $folderUuid.")
        } else {"""

replacement3 = """        if (folderUuid != null) {
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

content = content.replace(target3, replacement3)

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "w") as f:
    f.write(content)
