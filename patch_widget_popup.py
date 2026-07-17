import re

with open("app/src/main/java/com/example/service/AppsPageView.kt", "r") as f:
    content = f.read()

target = """                } else if (item is SidebarItem.Widget) {
                    WidgetOverlayView(context, item.widgetId)
                    currentFolderPopup?.dismiss()
                    onCloseSidebar()"""

replacement = """                } else if (item is SidebarItem.Widget) {
                    showWidgetPopup(itemView, item.widgetId)
                    // Do not close sidebar, just show popup
                """

content = content.replace(target, replacement)

# Add showWidgetPopup function
new_func = """
    private fun showWidgetPopup(anchor: View, widgetId: Int) {
        currentFolderPopup?.dismiss()
        val density = context.resources.displayMetrics.density
        val popupView = FrameLayout(context)
        
        try {
            val appWidgetManager = android.appwidget.AppWidgetManager.getInstance(context)
            val appWidgetInfo = appWidgetManager.getAppWidgetInfo(widgetId)
            
            if (appWidgetInfo != null) {
                val widgetView = com.example.utils.AppWidgetHelper.getHost(context).createView(context, widgetId, appWidgetInfo)
                
                val padding = (12 * density).toInt()
                popupView.setPadding(padding, padding, padding, padding)
                
                val popupOpacity = if (pageConfig?.useCustomSettings == true) pageConfig.transparency else prefs.getFloat("sidebar_transparency", 0.9f)
                val popupBg = android.graphics.drawable.GradientDrawable()
                popupBg.setColor(android.graphics.Color.parseColor("#1A1A1A"))
                popupBg.alpha = (popupOpacity * 255).toInt()
                popupBg.cornerRadius = 16 * density
                popupView.background = popupBg
                
                // Allow widget to determine its own size, but set a min size based on provider info
                val minWidth = (appWidgetInfo.minWidth * density).toInt()
                val minHeight = (appWidgetInfo.minHeight * density).toInt()
                
                widgetView.minimumWidth = minWidth
                widgetView.minimumHeight = minHeight
                
                popupView.addView(widgetView, FrameLayout.LayoutParams(FrameLayout.LayoutParams.WRAP_CONTENT, FrameLayout.LayoutParams.WRAP_CONTENT))
                
                val popupWindow = android.widget.PopupWindow(
                    popupView,
                    ViewGroup.LayoutParams.WRAP_CONTENT,
                    ViewGroup.LayoutParams.WRAP_CONTENT,
                    true
                ).apply {
                    if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                        windowLayoutType = android.view.WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
                    } else {
                        @Suppress("DEPRECATION")
                        windowLayoutType = android.view.WindowManager.LayoutParams.TYPE_PHONE
                    }
                    setBackgroundDrawable(android.graphics.drawable.ColorDrawable(android.graphics.Color.TRANSPARENT))
                    isOutsideTouchable = true
                }
                
                currentFolderPopup = popupWindow
                
                val location = IntArray(2)
                anchor.getLocationOnScreen(location)
                val anchorX = location[0]
                val anchorY = location[1]
                val screenWidth = context.resources.displayMetrics.widthPixels
                
                popupView.measure(View.MeasureSpec.UNSPECIFIED, View.MeasureSpec.UNSPECIFIED)
                val popupWidth = popupView.measuredWidth
                val popupHeight = popupView.measuredHeight
                
                var x = anchorX
                if (anchorX > screenWidth / 2) {
                    x = anchorX - popupWidth
                } else {
                    x = anchorX + anchor.width
                }
                
                var y = anchorY
                val screenHeight = context.resources.displayMetrics.heightPixels
                if (y + popupHeight > screenHeight) {
                    y = screenHeight - popupHeight
                }
                if (y < 0) y = 0
                
                popupWindow.showAtLocation(anchor, android.view.Gravity.NO_GRAVITY, x, y)
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
"""

content = content.replace("    private fun showFolderPopup", new_func + "\n    private fun showFolderPopup")

with open("app/src/main/java/com/example/service/AppsPageView.kt", "w") as f:
    f.write(content)
