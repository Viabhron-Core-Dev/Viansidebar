with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "r") as f:
    content = f.read()

import re

# Add method
method = """
    private fun reloadHandles() {
        triggerHandleViews.forEach { it.detach() }
        triggerHandleViews.clear()

        val handles = com.example.HandleManager.getHandles(prefs)
        for (handle in handles) {
            if (handle.enabled) {
                val view = TriggerHandleView(this, prefs, windowManager, handle.id) { handleId ->
                    showSidebar()
                }
                view.attach()
                triggerHandleViews.add(view)
            }
        }
    }
"""

content = content.replace("    override fun onCreate() {", method + "\n    override fun onCreate() {")

# Replace setupHandles call
content = content.replace("                setupHandles()", "                reloadHandles()")

# Replace inline creation in onCreate
old_inline = """        val handles = com.example.HandleManager.getHandles(prefs)
        for (handle in handles) {
            if (handle.enabled) {
                val view = TriggerHandleView(this, prefs, windowManager, handle.id) { handleId ->
                    showSidebar()
                }
                view.attach()
                triggerHandleViews.add(view)
            }
        }"""
content = content.replace(old_inline, "        reloadHandles()")

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "w") as f:
    f.write(content)

