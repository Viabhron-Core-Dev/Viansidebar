import re

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "r") as f:
    content = f.read()

# 1. Add folderUuid property
content = content.replace("val localIds = mutableListOf<String>()",
                          "val localIds = mutableListOf<String>()\n    private var folderUuid: String? = null\n    private var folderName: String = \"Folder\"\n    private var folderColor: String = \"#444444\"\n    private var folderStyle: Int = 0\n    private var totalCols = 3\n    private var totalRows = 3\n")

# 2. Update onCreate loading logic
on_create_target = """        loadLocalIds()

        var totalCols = prefs.getInt("sidebar_columns", 3)"""

on_create_replacement = """        folderUuid = intent.getStringExtra("FOLDER_UUID")
        loadLocalIds()

        if (folderUuid == null) {
            totalCols = prefs.getInt("sidebar_columns", 3)
        }"""
content = content.replace(on_create_target, on_create_replacement)

# 3. Add column controls in header
header_target = """        val btnAdd = Button(this).apply {"""

header_replacement = """        val controlsLayout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            layoutParams = LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f)
            gravity = Gravity.CENTER_VERTICAL
        }
        val colsLayout = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }
        colsLayout.addView(TextView(this).apply { text = "Cols: "; setTextColor(Color.LTGRAY) })
        val btnColMinus = Button(this).apply { text = "-"; layoutParams = LinearLayout.LayoutParams(100, 100); setOnClickListener { if (totalCols > 1) { totalCols--; updateColsDisplay(); updateGrid() } } }
        val tvCols = TextView(this).apply { id = 101; setTextColor(Color.WHITE); setPadding(16, 0, 16, 0); text = totalCols.toString() }
        val btnColPlus = Button(this).apply { text = "+"; layoutParams = LinearLayout.LayoutParams(100, 100); setOnClickListener { totalCols++; updateColsDisplay(); updateGrid() } }
        colsLayout.addView(btnColMinus); colsLayout.addView(tvCols); colsLayout.addView(btnColPlus)
        controlsLayout.addView(colsLayout)
        
        val rowsLayout = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }
        rowsLayout.addView(TextView(this).apply { text = "Rows: "; setTextColor(Color.LTGRAY) })
        val btnRowMinus = Button(this).apply { text = "-"; layoutParams = LinearLayout.LayoutParams(100, 100); setOnClickListener { if (totalRows > 1) { totalRows--; updateRowsDisplay() } } }
        val tvRows = TextView(this).apply { id = 102; setTextColor(Color.WHITE); setPadding(16, 0, 16, 0); text = totalRows.toString() }
        val btnRowPlus = Button(this).apply { text = "+"; layoutParams = LinearLayout.LayoutParams(100, 100); setOnClickListener { totalRows++; updateRowsDisplay() } }
        rowsLayout.addView(btnRowMinus); rowsLayout.addView(tvRows); rowsLayout.addView(btnRowPlus)
        if (folderUuid != null) {
            controlsLayout.addView(rowsLayout)
        }
        headerLayout.addView(controlsLayout)

        val btnAdd = Button(this).apply {"""
content = content.replace(header_target, header_replacement)

# 4. Helper functions for UI
helpers = """    private fun updateColsDisplay() {
        findViewById<TextView>(101)?.text = totalCols.toString()
    }
    private fun updateRowsDisplay() {
        findViewById<TextView>(102)?.text = totalRows.toString()
    }
    private fun updateGrid() {
        if (::recyclerView.isInitialized) {
            recyclerView.layoutManager = GridLayoutManager(this, totalCols)
        }
    }
"""

# Insert helpers before onActivityResult
content = content.replace("    override fun onActivityResult", helpers + "\n    override fun onActivityResult")

# 5. Fix loadLocalIds
load_target = """    private fun loadLocalIds() {
        val jsonStr = prefs.getString("sidebar_apps", \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\") ?: \"\"\"["system:log_keeper", "system:ebook_reader"]\"\"\"
        val arr = JSONArray(jsonStr)
        localIds.clear()
        for (i in 0 until arr.length()) {
            localIds.add(arr.getString(i))
        }
    }"""
load_replacement = """    private fun loadLocalIds() {
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
content = content.replace(load_target, load_replacement)

# 6. Fix saveIds
save_target = """    private fun saveIds() {
        val arr = JSONArray()
        localIds.forEach { arr.put(it) }
        prefs.edit().putString("sidebar_apps", arr.toString()).apply()
        
        com.example.LogKeeper.writeLog("SidebarEdit", "Saved ${localIds.size} items to apps grid.")
        
        val updateIntent = Intent(this, com.example.service.FloatingReaderService::class.java).apply {
            action = "UPDATE_CONFIG"
        }
        startService(updateIntent)
    }"""

save_replacement = """    private fun saveIds() {
        val arr = JSONArray()
        localIds.forEach { arr.put(it) }
        
        if (folderUuid != null) {
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
        } else {
            prefs.edit().putString("sidebar_apps", arr.toString()).apply()
            prefs.edit().putInt("sidebar_columns", totalCols).apply()
            com.example.LogKeeper.writeLog("SidebarEdit", "Saved ${localIds.size} items to apps grid.")
        }
        
        val updateIntent = Intent(this, com.example.service.FloatingReaderService::class.java).apply {
            action = "UPDATE_CONFIG"
        }
        startService(updateIntent)
    }"""
content = content.replace(save_target, save_replacement)

# 7. Update onBindViewHolder
bind_target = """                        if (iconBitmap != null) {
                            holder.iconView.setImageBitmap(iconBitmap)
                        } else {
                            holder.iconView.setImageResource(android.R.drawable.sym_def_app_icon)
                        }"""
bind_replacement = """                        if (iconBitmap != null) {
                            holder.iconView.setImageBitmap(iconBitmap)
                        } else {
                            holder.iconView.setImageResource(android.R.drawable.sym_def_app_icon)
                            if (item is com.example.service.SidebarItem.App) {
                                val loaded = manager.loadIcon(item.packageName)
                                if (loaded != null) {
                                    holder.iconView.setImageBitmap(loaded)
                                }
                            } else if (item is com.example.service.SidebarItem.IntentAction) {
                                try {
                                    val uriStr = item.uri
                                    val pkg = android.content.Intent.parseUri(uriStr, android.content.Intent.URI_INTENT_SCHEME).`package` ?: android.content.Intent.parseUri(uriStr, android.content.Intent.URI_INTENT_SCHEME).component?.packageName ?: ""
                                    val loaded = manager.loadIcon(pkg)
                                    if (loaded != null) {
                                        holder.iconView.setImageBitmap(loaded)
                                    }
                                } catch (e: Exception) {}
                            }
                        }"""
content = content.replace(bind_target, bind_replacement)

# 8. Add setOnClickListener for folders in EditAdapter.onCreateViewHolder or onBindViewHolder
click_target = """            holder.btnRemove.setOnClickListener {"""
click_replacement = """            holder.itemView.setOnClickListener {
                if (id.startsWith("folder:")) {
                    val uuid = id.split(":")[1]
                    val intent = Intent(this@SidebarEditActivity, SidebarEditActivity::class.java).apply {
                        putExtra("FOLDER_UUID", uuid)
                    }
                    startActivity(intent)
                }
            }
            holder.btnRemove.setOnClickListener {"""
content = content.replace(click_target, click_replacement)

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "w") as f:
    f.write(content)
