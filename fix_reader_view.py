with open('app/src/main/java/com/example/service/SidebarService.kt', 'r') as f:
    content = f.read()

content = content.replace("""        // readerHandleView = ReaderHandleView(this, prefs, windowManager) {
        //     android.util.Log.d("VianSide", "reader trigger tapped")
        //     toggleReader()
        // }
        // readerHandleView?.attach()""", """        readerHandleView = ReaderHandleView(this, prefs, windowManager)
        if (prefs.getBoolean("reader_handle_enabled", false)) {
            readerHandleView?.attach()
        }""")

content = content.replace("class ReaderHandleView(\n    private val context: Context,\n    private val prefs: SharedPreferences,\n    private val windowManager: WindowManager,\n    private val onTriggerTapped: () -> Unit\n)", "class ReaderHandleView(\n    private val context: Context,\n    private val prefs: SharedPreferences,\n    private val windowManager: WindowManager\n)")
with open('app/src/main/java/com/example/service/SidebarService.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/service/ReaderHandleView.kt', 'r') as f:
    content = f.read()
content = content.replace("class ReaderHandleView(\n    private val context: Context,\n    private val prefs: SharedPreferences,\n    private val windowManager: WindowManager,\n    private val onTriggerTapped: () -> Unit\n)", "class ReaderHandleView(\n    private val context: Context,\n    private val prefs: SharedPreferences,\n    private val windowManager: WindowManager\n)")
content = content.replace("onTriggerTapped()", "com.example.service.FloatingReaderService.instance?.toggleReader()")
with open('app/src/main/java/com/example/service/ReaderHandleView.kt', 'w') as f:
    f.write(content)
