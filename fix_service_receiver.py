import sys

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'r') as f:
    content = f.read()

target = """        widgetPickerReceiver = object : android.content.BroadcastReceiver() {
            override fun onReceive(context: Context, intent: Intent) {
                if (intent.action == "WIDGET_PICKER_CLOSED") {
                    val pageId = intent.getStringExtra("PAGE_ID")
                    if (pageId != null) {
                        showSidebar()
                        showWidgetsGridEditOverlay(pageId)
                    }
                }
            }
        }
        val widgetFilter = android.content.IntentFilter("WIDGET_PICKER_CLOSED")
        registerReceiver(widgetPickerReceiver, widgetFilter, Context.RECEIVER_NOT_EXPORTED)"""
        
replacement = """        widgetPickerReceiver = object : android.content.BroadcastReceiver() {
            override fun onReceive(context: Context, intent: Intent) {
                if (intent.action == "WIDGET_PICKER_OPENED") {
                    if (sidebarEditOverlayView?.parent != null) {
                        wasSidebarEditOpen = true
                        sidebarEditOverlayView?.detach()
                    }
                    if (widgetsGridEditOverlayView?.parent != null) {
                        wasWidgetsGridEditOpen = true
                        widgetsGridEditOverlayView?.detach()
                    }
                    closeSidebar()
                } else if (intent.action == "WIDGET_PICKER_CLOSED") {
                    val actionType = intent.getStringExtra("ACTION_TYPE")
                    if (actionType == "ADD_TO_WIDGETS_GRID" || wasWidgetsGridEditOpen) {
                        val pageId = intent.getStringExtra("PAGE_ID") ?: lastWidgetsGridPageId
                        if (pageId.isNotEmpty()) {
                            showSidebar()
                            showWidgetsGridEditOverlay(pageId)
                        }
                    } else if (actionType == "ADD_ELEMENT" || wasSidebarEditOpen) {
                        showSidebar()
                        sidebarEditOverlayView?.attach()
                    }
                    wasSidebarEditOpen = false
                    wasWidgetsGridEditOpen = false
                }
            }
        }
        val widgetFilter = android.content.IntentFilter().apply {
            addAction("WIDGET_PICKER_OPENED")
            addAction("WIDGET_PICKER_CLOSED")
        }
        registerReceiver(widgetPickerReceiver, widgetFilter, Context.RECEIVER_NOT_EXPORTED)"""

content = content.replace(target, replacement)

# Add properties
prop_target = """    private var widgetPickerReceiver: android.content.BroadcastReceiver? = null"""
prop_replacement = """    private var widgetPickerReceiver: android.content.BroadcastReceiver? = null
    private var wasSidebarEditOpen = false
    private var wasWidgetsGridEditOpen = false
    private var lastWidgetsGridPageId = "" """

if "wasSidebarEditOpen = false" not in content:
    content = content.replace(prop_target, prop_replacement)
    
# Save lastWidgetsGridPageId
show_grid_target = """    fun showWidgetsGridEditOverlay(pageId: String) {"""
show_grid_replacement = """    fun showWidgetsGridEditOverlay(pageId: String) {
        lastWidgetsGridPageId = pageId"""
        
content = content.replace(show_grid_target, show_grid_replacement)

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'w') as f:
    f.write(content)
