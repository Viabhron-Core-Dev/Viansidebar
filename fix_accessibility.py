import re

with open("app/src/main/java/com/example/service/VianSideAccessibilityService.kt", "r") as f:
    content = f.read()

target = """    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        // Not used
    }"""

replacement = """    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        if (event == null) return
        
        if (isForceStopping) {
            val rootNode = rootInActiveWindow ?: return
            
            // Try to find and click "Force stop" button
            val forceStopNodes = rootNode.findAccessibilityNodeInfosByText("Force stop")
            var clickedForceStop = false
            for (node in forceStopNodes) {
                if (node.isClickable && node.isEnabled) {
                    node.performAction(android.view.accessibility.AccessibilityNodeInfo.ACTION_CLICK)
                    clickedForceStop = true
                    break
                } else if (node.parent?.isClickable == true && node.parent?.isEnabled == true) {
                    node.parent.performAction(android.view.accessibility.AccessibilityNodeInfo.ACTION_CLICK)
                    clickedForceStop = true
                    break
                }
            }
            
            // Try to find and click "OK" in confirmation dialog
            if (!clickedForceStop) {
                val okNodes = rootNode.findAccessibilityNodeInfosByText("OK")
                for (node in okNodes) {
                    if (node.isClickable && node.isEnabled) {
                        node.performAction(android.view.accessibility.AccessibilityNodeInfo.ACTION_CLICK)
                        break
                    }
                }
            }
        }
    }"""

if target in content:
    content = content.replace(target, replacement)
    
    # ensure import android.view.accessibility.AccessibilityNodeInfo is present if needed, though we used FQDN
    with open("app/src/main/java/com/example/service/VianSideAccessibilityService.kt", "w") as f:
        f.write(content)
else:
    print("Target not found")
