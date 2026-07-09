import re

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'r') as f:
    content = f.read()

content = content.replace("onCloseSidebar = { onCloseSidebar() }", "onCloseSidebar = closeSidebarCallback")

with open('app/src/main/java/com/example/service/NotificationPageView.kt', 'w') as f:
    f.write(content)

