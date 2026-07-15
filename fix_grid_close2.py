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
            }
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

# In case it has a comma:
target2 = """        widgetsGridEditOverlayView = WidgetsGridEditOverlayView(
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

content = content.replace(target, replacement)
content = content.replace(target2, replacement)

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'w') as f:
    f.write(content)
