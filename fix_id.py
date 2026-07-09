import re

with open('app/src/main/java/com/example/PageManagementSettingsScreen.kt', 'r') as f:
    content = f.read()

id_fix = """                        val title = "App Widget"
                        val page = SidebarPage.createDefault(id = "widget:$widgetId", type = "widget", title = title)
                        newPages.add(page)"""

content = content.replace("""                        val title = "App Widget"
                        val page = SidebarPage.createDefault(id = UUID.randomUUID().toString(), type = "widget", title = title)
                        page.id = "widget:$widgetId" // use id to store widget ID
                        newPages.add(page)""", id_fix)

with open('app/src/main/java/com/example/PageManagementSettingsScreen.kt', 'w') as f:
    f.write(content)

