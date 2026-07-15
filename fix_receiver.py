import sys

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'r') as f:
    content = f.read()

target = """                    if (widgetsGridEditOverlayView?.parent != null) {
                        wasWidgetsGridEditOpen = true
                    }
                } else if (intent.action == "WIDGET_PICKER_CLOSED") {"""

replacement = """                    if (widgetsGridEditOverlayView?.parent != null) {
                        wasWidgetsGridEditOpen = true
                        widgetsGridEditOverlayView?.detach()
                    }
                    closeSidebar()
                } else if (intent.action == "WIDGET_PICKER_CLOSED") {"""

content = content.replace(target, replacement)

# We also need to fix showWidgetsGridEditOverlay() because we removed the manual detach at the start of it.
target_show = """    fun showWidgetsGridEditOverlay(pageId: String) {
        lastWidgetsGridPageId = pageId


        widgetsGridEditOverlayView = WidgetsGridEditOverlayView("""
        
replacement_show = """    fun showWidgetsGridEditOverlay(pageId: String) {
        lastWidgetsGridPageId = pageId
        widgetsGridEditOverlayView?.detach()
        widgetsGridEditOverlayView = WidgetsGridEditOverlayView("""

content = content.replace(target_show, replacement_show)

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'w') as f:
    f.write(content)
