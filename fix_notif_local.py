import re

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'r') as f:
    content = f.read()

content = content.replace("private fun closeSidebar() { onCloseSidebar.invoke() }", "")
content = content.replace("init {", "init {\n        val closeSidebarCallback = onCloseSidebar")
content = content.replace("onCloseSidebar = { closeSidebar() }", "onCloseSidebar = closeSidebarCallback")

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'w') as f:
    f.write(content)

