import sys

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'r') as f:
    content = f.read()

target = """        widgetsGridEditOverlayView = WidgetsGridEditOverlayView(
            this, pageId, windowManager,
            onAddClicked = { 
                val intent = android.content.Intent(this, com.example.WidgetPickerActivity::class.java).apply {
                    putExtra("ACTION_TYPE", "ADD_TO_WIDGETS_GRID")
                    putExtra("PAGE_ID", pageId)
                    addFlags(android.content.Intent.FLAG_ACTIVITY_NEW_TASK)
                }
                startActivity(intent)
            },
        )"""
        
replacement = """        widgetsGridEditOverlayView = WidgetsGridEditOverlayView(
            this, pageId, windowManager,
            onAddClicked = { 
                val intent = android.content.Intent(this, com.example.WidgetPickerActivity::class.java).apply {
                    putExtra("ACTION_TYPE", "ADD_TO_WIDGETS_GRID")
                    putExtra("PAGE_ID", pageId)
                    addFlags(android.content.Intent.FLAG_ACTIVITY_NEW_TASK)
                }
                startActivity(intent)
            },
            onClose = { widgetsGridEditOverlayView?.detach() }
        )"""

content = content.replace(target, replacement)

target2 = """            onClose = { sidebarEditOverlayView?.detach() }
        , onClose = { widgetsGridEditOverlayView?.detach() })"""

replacement2 = """            onClose = { sidebarEditOverlayView?.detach() }
        )"""

content = content.replace(target2, replacement2)

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'w') as f:
    f.write(content)
