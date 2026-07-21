import re

with open("app/src/main/java/com/example/service/SidebarView.kt", "r") as f:
    content = f.read()

content = content.replace("var targetHeight = pageHeightPx + (24 * density)", "var targetHeight = pageHeightPx + (36 * density)")

with open("app/src/main/java/com/example/service/SidebarView.kt", "w") as f:
    f.write(content)
