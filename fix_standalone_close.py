with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "r") as f:
    content = f.read()

old_str = """            standaloneSidebarView = SidebarView(this, prefs, windowManager, tempPagesList, listOf(config), 0, onClose = { 
                standaloneSidebarView = null 
            }, onEditPageClicked = null)"""

new_str = """            standaloneSidebarView = SidebarView(this, prefs, windowManager, tempPagesList, listOf(config), 0, onClose = { 
                standaloneSidebarView?.detach()
                standaloneSidebarView = null 
            }, onEditPageClicked = null)"""

content = content.replace(old_str, new_str)

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "w") as f:
    f.write(content)
