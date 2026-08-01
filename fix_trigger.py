with open("app/src/main/java/com/example/service/FloatingTriggerService.kt", "r") as f:
    content = f.read()

import re

# Find executeAction to end of adjustBrightness
pattern = r"private fun executeAction\(targetId: String\) \{.*?\n    override fun onBind"
replacement = """private fun executeAction(targetId: String) {
        val sidebarInstance = SidebarService.instance
        if (sidebarInstance != null) {
            sidebarInstance.executeElementAction(targetId)
        } else {
            // Fallback: try to start SidebarService and hope it catches up, 
            // but in normal usage SidebarService is always running.
            val intent = Intent(this, SidebarService::class.java)
            startService(intent)
        }
    }

    override fun onBind"""

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/service/FloatingTriggerService.kt", "w") as f:
    f.write(new_content)

