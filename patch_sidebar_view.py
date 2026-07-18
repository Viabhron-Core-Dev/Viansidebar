import re

with open("app/src/main/java/com/example/service/SidebarView.kt", "r") as f:
    content = f.read()

target = """                if (page is WidgetPageView || page is WidgetsGridPageView) {
                    com.example.utils.AppWidgetHelper.startListening(context)
                } else {
                    com.example.utils.AppWidgetHelper.stopListening()
                }"""

replacement = """                com.example.utils.AppWidgetHelper.startListening(context)"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/SidebarView.kt", "w") as f:
    f.write(content)
