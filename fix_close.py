import sys

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'r') as f:
    content = f.read()

target = """    }
        
    sidebarView?.detach()"""

replacement = """    }
        
    fun closeSidebar() {
        sidebarView?.detach()"""

content = content.replace(target, replacement)

# Add closeSidebar() to onDestroy
target_destroy = """    override fun onDestroy() {
        if (this::prefs.isInitialized) {
            prefs.unregisterOnSharedPreferenceChangeListener(prefListener)
        }
        widgetPickerReceiver?.let { unregisterReceiver(it) }
        screenStateReceiver?.let { unregisterReceiver(it) }
        netSpeedManager?.stop()
        callRecorderManager?.stopListening()
        instance = null
        sidebarView = null"""

replacement_destroy = """    override fun onDestroy() {
        if (this::prefs.isInitialized) {
            prefs.unregisterOnSharedPreferenceChangeListener(prefListener)
        }
        widgetPickerReceiver?.let { unregisterReceiver(it) }
        screenStateReceiver?.let { unregisterReceiver(it) }
        netSpeedManager?.stop()
        callRecorderManager?.stopListening()
        instance = null
        closeSidebar()
        sidebarView = null"""

content = content.replace(target_destroy, replacement_destroy)

# We need closeSidebar in WIDGET_PICKER_OPENED? Yes, we already have it in the python script from before! Wait, I removed all occurrences with sed.
# So I need to add it back to widgetPickerReceiver inside FloatingReaderService.kt

target_receiver = """                    if (widgetsGridEditOverlayView?.parent != null) {
                        wasWidgetsGridEditOpen = true
                        widgetsGridEditOverlayView?.detach()
                    }
                } else if (intent.action == "WIDGET_PICKER_CLOSED") {"""

replacement_receiver = """                    if (widgetsGridEditOverlayView?.parent != null) {
                        wasWidgetsGridEditOpen = true
                        widgetsGridEditOverlayView?.detach()
                    }
                    closeSidebar()
                } else if (intent.action == "WIDGET_PICKER_CLOSED") {"""

content = content.replace(target_receiver, replacement_receiver)

# Add closeSidebar() back in onStartCommand when action == "CLOSE_SIDEBAR" if any?
# We'll check if there's an action CLOSE_SIDEBAR
with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'w') as f:
    f.write(content)
