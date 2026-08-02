import re

with open("app/src/main/java/com/example/service/SidebarView.kt", "r") as f:
    content = f.read()

pattern = r"(com\.example\.utils\.AppWidgetHelper\.startListening\(context\))"
replacement = r"\1\n\n                if (::editButton.isInitialized) {\n                    val isEditable = page is AppsPageView || page is WidgetsGridPageView || page is HybridGridPageView || page is AppTrackerPageView\n                    editButton.visibility = if (isEditable) View.VISIBLE else View.INVISIBLE\n                }"

content = re.sub(pattern, replacement, content)

with open("app/src/main/java/com/example/service/SidebarView.kt", "w") as f:
    f.write(content)
