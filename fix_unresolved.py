import re

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "r") as f:
    content = f.read()

content = content.replace("private var lastWidgetsGridPageId = \"\"", 'private var lastWidgetsGridPageId = ""\n    private var currentHandleId: String = "sidebar"')

content = content.replace(
"""                val wasAttached = sidebarView?.windowToken != null
                if (wasAttached) {
                    showSidebar(handleId)
                }""",
"""                val wasAttached = sidebarView?.windowToken != null
                if (wasAttached) {
                    showSidebar(currentHandleId)
                }""")

content = content.replace(
"""                        val pageId = intent.getStringExtra("PAGE_ID") ?: lastWidgetsGridPageId
                        if (pageId.isNotEmpty()) {
                            showSidebar(handleId)
                            showWidgetsGridEditOverlay(pageId)
                        }
                    } else if (actionType == "ADD_ELEMENT" || wasSidebarEditOpen) {
                        showSidebar(handleId)""",
"""                        val pageId = intent.getStringExtra("PAGE_ID") ?: lastWidgetsGridPageId
                        if (pageId.isNotEmpty()) {
                            showSidebar(currentHandleId)
                            showWidgetsGridEditOverlay(pageId)
                        }
                    } else if (actionType == "ADD_ELEMENT" || wasSidebarEditOpen) {
                        showSidebar(currentHandleId)"""
)

content = content.replace("private fun showSidebar(handleId: String) {", "private fun showSidebar(handleId: String) {\n        currentHandleId = handleId")

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "w") as f:
    f.write(content)
