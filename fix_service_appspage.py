import re

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'r') as f:
    content = f.read()

old_appspage = """                    p = AppsPageView(this, appsManager, serviceScope,
                        onCloseSidebar = { sidebarView?.detach() },"""
new_appspage = """                    p = AppsPageView(this, config, appsManager, serviceScope,
                        onCloseSidebar = { sidebarView?.detach() },"""
content = content.replace(old_appspage, new_appspage)

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'w') as f:
    f.write(content)
