with open("app/src/main/java/com/example/WidgetsGridEditActivity.kt", "r") as f:
    content = f.read()

import_scope = """import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent"""
new_import_scope = """import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers"""
content = content.replace(import_scope, new_import_scope)

# Add manager
old_init = """    private val localItems = mutableListOf<com.example.service.GridWidgetItem>()
    
    override fun onCreate(savedInstanceState: Bundle?) {"""
new_init = """    private val localItems = mutableListOf<com.example.service.GridWidgetItem>()
    private lateinit var manager: com.example.service.SidebarAppsManager
    
    override fun onCreate(savedInstanceState: Bundle?) {
        manager = com.example.service.SidebarAppsManager(this, getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE), CoroutineScope(Dispatchers.IO), "temp") {}
        manager.ensureLoaded()"""
content = content.replace(old_init, new_init)

# Bind Name
old_bind = """            val info = appWidgetManager.getAppWidgetInfo(item.id)
            
            holder.tvName.text = info?.loadLabel(packageManager) ?: "Widget ${item.id} (Unknown)" """
new_bind = """            if (item.id.startsWith("widget:")) {
                val wId = item.id.removePrefix("widget:").toIntOrNull() ?: -1
                val info = appWidgetManager.getAppWidgetInfo(wId)
                holder.tvName.text = info?.loadLabel(packageManager) ?: "Widget ${wId} (Unknown)"
            } else {
                val parsed = manager.parseId(item.id)
                holder.tvName.text = parsed?.label ?: item.id
            }"""
content = content.replace(old_bind, new_bind)

# Remove AppWidget
old_remove = """                    try {
                        AppWidgetHelper.getHost(this@WidgetsGridEditActivity).deleteAppWidgetId(removed.id)
                    } catch (e: Exception) {}"""
new_remove = """                    try {
                        if (removed.id.startsWith("widget:")) {
                            val wId = removed.id.removePrefix("widget:").toIntOrNull() ?: -1
                            AppWidgetHelper.getHost(this@WidgetsGridEditActivity).deleteAppWidgetId(wId)
                        }
                    } catch (e: Exception) {}"""
content = content.replace(old_remove, new_remove)

# Button Add
old_btn = """        val btnAdd = Button(this).apply {
            text = "Add Widget"
            layoutParams = LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT).apply {
                topMargin = 16
            }
            setOnClickListener {
                saveItems() 
                val intent = Intent(this@WidgetsGridEditActivity, WidgetPickerActivity::class.java).apply {
                    putExtra("ACTION_TYPE", "ADD_TO_WIDGETS_GRID")
                    putExtra("PAGE_ID", pageId)
                }
                startActivity(intent)
            }
        }"""
new_btn = """        val btnAdd = Button(this).apply {
            text = "Add Element"
            layoutParams = LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT).apply {
                topMargin = 16
            }
            setOnClickListener {
                saveItems() 
                val intent = Intent(this@WidgetsGridEditActivity, AddElementActivity::class.java)
                startActivityForResult(intent, 201)
            }
        }"""
content = content.replace(old_btn, new_btn)

# Add onActivityResult
old_setup = """        setupItemTouchHelper()
        
        registerReceiver(receiver, android.content.IntentFilter("WIDGET_ADDED_TO_GRID"), Context.RECEIVER_NOT_EXPORTED)
    }"""
new_setup = """        setupItemTouchHelper()
        
        registerReceiver(receiver, android.content.IntentFilter("WIDGET_ADDED_TO_GRID"), Context.RECEIVER_NOT_EXPORTED)
    }
    
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 201 && resultCode == Activity.RESULT_OK && data != null) {
            val elementId = data.getStringExtra("ELEMENT_ID")
            if (elementId != null) {
                // Broadcast that we added to grid so PageView picks it up, or just add it here and reload.
                val intent = Intent("WIDGET_ADDED_TO_GRID")
                intent.putExtra("PAGE_ID", pageId)
                intent.putExtra("ELEMENT_ID", elementId)
                intent.setPackage(packageName)
                sendBroadcast(intent)
                
                // Also update local list immediately
                localItems.add(com.example.service.GridWidgetItem(elementId, 1, 1))
                adapter.notifyItemInserted(localItems.size - 1)
                saveItems()
            }
        }
    }"""
content = content.replace(old_setup, new_setup)

with open("app/src/main/java/com/example/WidgetsGridEditActivity.kt", "w") as f:
    f.write(content)
