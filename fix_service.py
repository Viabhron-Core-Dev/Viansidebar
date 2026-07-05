import re

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'r') as f:
    content = f.read()

old_action = """        } else if (id.startsWith("system:")) {"""
new_action = """        } else if (id.startsWith("quicktile:")) {
            val action = id.removePrefix("quicktile:")
            QuickTileHandler.handleQuickTileAction(this, action)
        } else if (id.startsWith("system:")) {"""
content = content.replace(old_action, new_action)

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'w') as f:
    f.write(content)
