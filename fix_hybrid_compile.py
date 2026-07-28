import re

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "r") as f:
    content = f.read()

target = """            appsManager.bindIcon(itemId, icon, prefs, CoroutineScope(Dispatchers.Main)) {}"""
replacement = """            CoroutineScope(Dispatchers.Main).launch {
                val bmp = appsManager.getIconBitmap(itemId)
                if (bmp != null) icon.setImageBitmap(bmp)
            }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "w") as f:
    f.write(content)
