import re

with open("app/src/main/java/com/example/service/VianSideAccessibilityService.kt", "r") as f:
    content = f.read()

# Add isForceStopping to companion object
pattern_companion = r'var instance: VianSideAccessibilityService\? = null\s*private set'
repl_companion = r'var instance: VianSideAccessibilityService? = null\n            private set\n        var isForceStopping = false'
content = re.sub(pattern_companion, repl_companion, content)

# Update onAccessibilityEvent
pattern_event = r'override fun onAccessibilityEvent\(event: AccessibilityEvent\?\) \{\s*\}'
repl_event = r'''override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        if (isForceStopping && event?.packageName != null) {
            val root = rootInActiveWindow ?: return
            
            val okNodes = root.findAccessibilityNodeInfosByText("OK")
            for (node in okNodes) {
                if (node.isClickable) {
                    node.performAction(android.view.accessibility.AccessibilityNodeInfo.ACTION_CLICK)
                    performGlobalAction(GLOBAL_ACTION_BACK)
                    return
                }
            }

            val forceStopNodes = root.findAccessibilityNodeInfosByText("Force stop")
            for (node in forceStopNodes) {
                if (node.isClickable && node.isEnabled) {
                    node.performAction(android.view.accessibility.AccessibilityNodeInfo.ACTION_CLICK)
                    return
                }
            }
        }
    }'''
content = re.sub(pattern_event, repl_event, content)

with open("app/src/main/java/com/example/service/VianSideAccessibilityService.kt", "w") as f:
    f.write(content)
