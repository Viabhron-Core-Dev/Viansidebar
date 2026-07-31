with open('app/src/main/java/com/example/service/SidebarService.kt', 'r') as f:
    content = f.read()

content = content.replace("""                val view = TriggerHandleView(this@SidebarService, prefs, windowManager, prefKey.removePrefix("handle_").removeSuffix("_enabled")) { handleId ->
                    showSidebar(handleId)
                }""", '                val view = TriggerHandleView(this@SidebarService, prefs, windowManager, handle.id)')

with open('app/src/main/java/com/example/service/SidebarService.kt', 'w') as f:
    f.write(content)
