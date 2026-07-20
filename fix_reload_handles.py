with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "r") as f:
    content = f.read()

import re

# Add "handles_list" to the prefListener
old_pref = """        if (key != null && key.startsWith("handle_") && key != "handles_list") {
            triggerHandleViews.forEach { it.updatePosition() }
        }
        when (key) {"""

new_pref = """        if (key != null && key.startsWith("handle_") && key != "handles_list") {
            triggerHandleViews.forEach { it.updatePosition() }
        }
        when (key) {
            "handles_list" -> {
                setupHandles()
            }"""

content = content.replace(old_pref, new_pref)

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "w") as f:
    f.write(content)

