sed -i '/private fun loadWidgets() {/,$d' app/src/main/java/com/example/service/WidgetsGridPageView.kt
cat << 'INNER_EOF' >> app/src/main/java/com/example/service/WidgetsGridPageView.kt
    private fun loadWidgets() {
        widgetsContainer.removeAllViews()
        val ids = getWidgetIds()
        val appWidgetManager = AppWidgetManager.getInstance(context)
        val host = AppWidgetHelper.getHost(context)
        for (widgetId in ids) {
            try {
                val info = appWidgetManager.getAppWidgetInfo(widgetId)
                if (info != null) {
                    val wrapper = LinearLayout(context).apply {
                        orientation = LinearLayout.VERTICAL
                        layoutParams = LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT).apply {
                            setMargins(0, 16, 0, 16)
                        }
                        val hostView = host.createView(context, widgetId, info)
                        addView(hostView, LinearLayout.LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT))
                    }
                    widgetsContainer.addView(wrapper)
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
        post {
            onHeightChanged(getCurrentHeightPx())
        }
    }
}
INNER_EOF
