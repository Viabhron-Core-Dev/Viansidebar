import re

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'r') as f:
    content = f.read()

content = content.replace("private val closeSidebarAction = onCloseSidebar", "private fun closeSidebar() { onCloseSidebar.invoke() }")
content = content.replace("onCloseSidebar = { onCloseSidebar() }", "onCloseSidebar = { closeSidebar() }")

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'w') as f:
    f.write(content)

