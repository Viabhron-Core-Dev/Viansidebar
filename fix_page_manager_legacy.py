import re

with open("app/src/main/java/com/example/utils/PageManager.kt", "r") as f:
    content = f.read()

content = content.replace(
    'val pagesJson = prefs.getString("handle_${handleId}_pages", prefs.getString("sidebar_pages", null))',
    'val legacy = if (handleId == "sidebar") prefs.getString("sidebar_pages", null) else null\n        val pagesJson = prefs.getString("handle_${handleId}_pages", legacy)'
)

with open("app/src/main/java/com/example/utils/PageManager.kt", "w") as f:
    f.write(content)
