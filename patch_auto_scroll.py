with open("app/src/main/java/com/example/service/AutoScrollManager.kt", "r") as f:
    content = f.read()

import re

# Add imports
content = content.replace("import android.widget.ImageButton", "import android.widget.ImageButton\nimport android.widget.ImageView\nimport android.view.accessibility.AccessibilityNodeInfo")

# Add isScreenScrollable function
scrollable_func = """    private fun isScreenScrollable(): Boolean {
        val rootNode = service.rootInActiveWindow ?: return false
        val queue = java.util.LinkedList<AccessibilityNodeInfo>()
        queue.add(rootNode)
        var found = false
        while (queue.isNotEmpty()) {
            val node = queue.poll()
            if (node.isScrollable) {
                found = true
                break
            }
            for (i in 0 until node.childCount) {
                val child = node.getChild(i)
                if (child != null) {
                    queue.add(child)
                }
            }
        }
        return found
    }

    private fun showFloatingControls() {"""

content = content.replace("    private fun showFloatingControls() {", scrollable_func)

# Add indicator logic to showFloatingControls
show_controls_old = """        val btnExit = floatingView?.findViewById<ImageButton>(R.id.btn_exit)

        fun updatePlayIcon() {"""

show_controls_new = """        val btnExit = floatingView?.findViewById<ImageButton>(R.id.btn_exit)
        val ivIndicator = floatingView?.findViewById<ImageView>(R.id.iv_scroll_indicator)

        val checkScrollRunnable = object : Runnable {
            override fun run() {
                if (!isRunning) return
                if (isScreenScrollable()) {
                    ivIndicator?.setColorFilter(android.graphics.Color.GREEN)
                } else {
                    ivIndicator?.setColorFilter(android.graphics.Color.RED)
                }
                handler.postDelayed(this, 1000)
            }
        }
        handler.post(checkScrollRunnable)

        fun updatePlayIcon() {"""

content = content.replace(show_controls_old, show_controls_new)

with open("app/src/main/java/com/example/service/AutoScrollManager.kt", "w") as f:
    f.write(content)
