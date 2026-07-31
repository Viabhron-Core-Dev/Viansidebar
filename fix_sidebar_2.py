import re
with open('app/src/main/java/com/example/service/SidebarService.kt', 'r') as f:
    content = f.read()

content = content.replace('TriggerHandleView(this@SidebarService, prefs, windowManager, prefKey.removePrefix("handle_").removeSuffix("_enabled")) { handleId ->', 'TriggerHandleView(this@SidebarService, prefs, windowManager, prefKey.removePrefix("handle_").removeSuffix("_enabled"))')
content = content.replace('TriggerHandleView(this@SidebarService, prefs, windowManager, prefKey.removePrefix("handle_").removeSuffix("_enabled")) { handleId ->', 'TriggerHandleView(this@SidebarService, prefs, windowManager, prefKey.removePrefix("handle_").removeSuffix("_enabled"))')

# Wait, there is probably a trailing brace for the lambda that needs to be removed.
# Let's just find the instantiation and replace the block.
