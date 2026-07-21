import re

with open("app/src/main/java/com/example/SidebarSettingsScreen.kt", "r") as f:
    content = f.read()
content = content.replace("PageManager.saveDefaultPageIndex(prefs, defaultIndex)", "PageManager.saveDefaultPageIndex(prefs, handleId, defaultIndex)")
with open("app/src/main/java/com/example/SidebarSettingsScreen.kt", "w") as f:
    f.write(content)
