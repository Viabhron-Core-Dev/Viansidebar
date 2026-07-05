import re

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'r') as f:
    content = f.read()

old_code = """                val miniIcons = item.items.mapNotNull { 
                     if (it.startsWith("app:")) manager.iconCache.get(it.substringAfter("app:")) else null 
                 }"""

new_code = """                val miniIcons = item.items.take(9).mapNotNull { manager.getIconBitmap(it) }"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'w') as f:
    f.write(content)
