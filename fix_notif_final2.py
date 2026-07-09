import re

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'r') as f:
    content = f.read()

content = content.replace("private val onCloseSidebar: () -> Unit,", "val myCloseSidebar: () -> Unit,")
content = content.replace("val closeSidebarCallback = onCloseSidebar", "")
content = content.replace("onCloseSidebar = closeSidebarCallback", "onCloseSidebar = myCloseSidebar")

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'w') as f:
    f.write(content)

