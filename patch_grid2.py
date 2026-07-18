import re

with open("app/src/main/java/com/example/service/FolderStyleDialog.kt", "r") as f:
    content = f.read()

target = """        } else if (count == 2) {
            val padding = size * 0.04f"""

replacement = """        } else if (count == 2) {
            val padding = size * 0.015f"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/FolderStyleDialog.kt", "w") as f:
    f.write(content)
