sed -i '/fun showSidebarEditOverlay/i\
    private var widgetsGridEditOverlayView: WidgetsGridEditOverlayView? = null\n\
    fun showWidgetsGridEditOverlay(pageId: String) {\n\
        widgetsGridEditOverlayView?.detach()\n\
        widgetsGridEditOverlayView = WidgetsGridEditOverlayView(\n\
            this, pageId, windowManager,\n\
            onAddClicked = { \n\
                val intent = android.content.Intent(this, com.example.WidgetPickerActivity::class.java).apply {\n\
                    putExtra("ACTION_TYPE", "ADD_TO_WIDGETS_GRID")\n\
                    putExtra("PAGE_ID", pageId)\n\
                    addFlags(android.content.Intent.FLAG_ACTIVITY_NEW_TASK)\n\
                }\n\
                startActivity(intent)\n\
            },\n\
            onClose = { widgetsGridEditOverlayView?.detach() }\n\
        )\n\
        widgetsGridEditOverlayView?.attach()\n\
    }\n' app/src/main/java/com/example/service/FloatingReaderService.kt
