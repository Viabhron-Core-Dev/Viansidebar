import re

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "r") as f:
    content = f.read()

# Change showSidebar() to showSidebar(handleId: String)
content = content.replace("private fun showSidebar() {", "private fun showSidebar(handleId: String) {")

# Change TriggerHandleView to pass handleId
content = content.replace(
"""                val view = TriggerHandleView(this, prefs, windowManager, handle.id) { handleId ->
                    showSidebar()
                }""",
"""                val view = TriggerHandleView(this, prefs, windowManager, handle.id) { handleId ->
                    showSidebar(handleId)
                }""")

# Any other showSidebar() calls without handleId?
content = content.replace("showSidebar()", 'showSidebar("sidebar")') # default to sidebar handle

# Update rebuildSidebarPages
content = content.replace("private fun rebuildSidebarPages() {", "private fun rebuildSidebarPages(handleId: String) {")
content = content.replace("PageManager.getPages(prefs)", "PageManager.getPages(prefs, handleId)")
content = content.replace("PageManager.getDefaultPageIndex(prefs)", "PageManager.getDefaultPageIndex(prefs, handleId)")

# Inside showSidebar
content = content.replace("rebuildSidebarPages()", "rebuildSidebarPages(handleId)")
content = content.replace("sidebarView = SidebarView(this, prefs, windowManager, sidebarPagesList, PageManager.getPages(prefs), sidebarDefaultIndex", 
                          "sidebarView = SidebarView(this, prefs, windowManager, sidebarPagesList, PageManager.getPages(prefs, handleId), sidebarDefaultIndex")

# We also had an initial rebuildSidebarPages() call in onCreate?
# If so, it might be rebuildSidebarPages("sidebar")
content = content.replace('rebuildSidebarPages("sidebarId")', 'rebuildSidebarPages("sidebar")') # just in case

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "w") as f:
    f.write(content)
