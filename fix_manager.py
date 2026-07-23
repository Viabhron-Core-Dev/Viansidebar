with open("app/src/main/java/com/example/WidgetsGridEditActivity.kt", "r") as f:
    content = f.read()

import_scope = """import androidx.activity.ComponentActivity"""
new_import_scope = """import androidx.activity.ComponentActivity
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers"""
content = content.replace(import_scope, new_import_scope)

old_vars = """    val localItems = mutableListOf<GridWidgetItem>()
    private lateinit var appWidgetManager: AppWidgetManager"""
new_vars = """    val localItems = mutableListOf<GridWidgetItem>()
    private lateinit var appWidgetManager: AppWidgetManager
    private lateinit var manager: com.example.service.SidebarAppsManager"""
content = content.replace(old_vars, new_vars)

old_oncreate = """    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)"""
new_oncreate = """    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        manager = com.example.service.SidebarAppsManager(this, getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE), CoroutineScope(Dispatchers.IO), "temp") {}
        manager.ensureLoaded()"""
content = content.replace(old_oncreate, new_oncreate)

with open("app/src/main/java/com/example/WidgetsGridEditActivity.kt", "w") as f:
    f.write(content)
