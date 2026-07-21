with open("app/src/main/java/com/example/SidebarSettingsScreen.kt", "r") as f:
    content = f.read()

content = content.replace("PageManager.savePages(prefs, newPages)", "PageManager.savePages(prefs, handleId, newPages)")

with open("app/src/main/java/com/example/SidebarSettingsScreen.kt", "w") as f:
    f.write(content)
