import sys

with open('app/src/main/java/com/example/WidgetPickerActivity.kt', 'r') as f:
    content = f.read()

# Add WIDGET_PICKER_OPENED broadcast in onCreate
target_oncreate = """    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        appWidgetManager = AppWidgetManager.getInstance(this)"""
        
replacement_oncreate = """    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        sendBroadcast(Intent("WIDGET_PICKER_OPENED"))
        
        appWidgetManager = AppWidgetManager.getInstance(this)"""
        
content = content.replace(target_oncreate, replacement_oncreate)

# Make sure WIDGET_PICKER_CLOSED sends ACTION_TYPE
target_ondestroy = """    override fun onDestroy() {
        super.onDestroy()
        val actionType = intent.getStringExtra("ACTION_TYPE") ?: ""
        if (actionType == "ADD_TO_WIDGETS_GRID") {
            val pageId = intent.getStringExtra("PAGE_ID") ?: ""
            val broadcastIntent = Intent("WIDGET_PICKER_CLOSED")
            broadcastIntent.putExtra("PAGE_ID", pageId)
            sendBroadcast(broadcastIntent)
        }
    }"""
    
replacement_ondestroy = """    override fun onDestroy() {
        super.onDestroy()
        val actionType = intent.getStringExtra("ACTION_TYPE") ?: ""
        val pageId = intent.getStringExtra("PAGE_ID") ?: ""
        val broadcastIntent = Intent("WIDGET_PICKER_CLOSED")
        broadcastIntent.putExtra("ACTION_TYPE", actionType)
        broadcastIntent.putExtra("PAGE_ID", pageId)
        sendBroadcast(broadcastIntent)
    }"""
    
content = content.replace(target_ondestroy, replacement_ondestroy)

with open('app/src/main/java/com/example/WidgetPickerActivity.kt', 'w') as f:
    f.write(content)
