import re

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'r') as f:
    content = f.read()

target = """    private fun closeSidebar() {
        sidebarView?.close()
        sidebarView = null
    }"""

replacement = """    private fun closeSidebar() {
        sidebarView?.detach()
        sidebarView = null
    }"""

content = content.replace(target, replacement)

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'w') as f:
    f.write(content)

