import re
with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'r') as f:
    content = f.read()

old_add = """            onAddClicked = { 
                 showAddElementOverlayForSelection { id ->
                    sidebarEditOverlayView?.localIds?.add(id)
                    sidebarEditOverlayView?.refresh()
                }
            },"""

new_add = """            onAddClicked = { 
                 showAddElementOverlayForSelection { id ->
                    sidebarEditOverlayView?.localIds?.add(id)
                    sidebarEditOverlayView?.saveCurrentState()
                    sidebarEditOverlayView?.refresh()
                }
            },"""

content = content.replace(old_add, new_add)

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'w') as f:
    f.write(content)
