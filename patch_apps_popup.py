import re

with open("app/src/main/java/com/example/service/AppsPageView.kt", "r") as f:
    content = f.read()

target = """    private var currentFolderPopup: android.widget.PopupWindow? = null

    private fun showWidgetPopup(anchor: View, widgetId: Int) {
        currentFolderPopup?.dismiss()
        val density = context.resources.displayMetrics.density
        val popupView = FrameLayout(context)
        
        try {
            val appWidgetManager = android.appwidget.AppWidgetManager.getInstance(context)
            val appWidgetInfo = appWidgetManager.getAppWidgetInfo(widgetId)
            
            if (appWidgetInfo != null) {
                com.example.utils.AppWidgetHelper.startListening(context)
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
                
                popupWindow.showAtLocation(anchor, Gravity.NO_GRAVITY, x, y)
            }
        } catch (e: Exception) {
            e.printStackTrace()
            android.widget.Toast.makeText(context, "Failed to load widget", android.widget.Toast.LENGTH_SHORT).show()
        }
    }"""

replacement = """    private var currentFolderPopup: android.widget.PopupWindow? = null
    private var currentOverlayView: View? = null

    private fun showWidgetPopup(anchor: View, widgetId: Int) {
        currentFolderPopup?.dismiss()
        val windowManager = context.getSystemService(Context.WINDOW_SERVICE) as android.view.WindowManager
        currentOverlayView?.let {
            try { windowManager.removeView(it) } catch (e: Exception) {}
        }
        currentOverlayView = null
        
        val density = context.resources.displayMetrics.density
        
        try {
            val appWidgetManager = android.appwidget.AppWidgetManager.getInstance(context)
            val appWidgetInfo = appWidgetManager.getAppWidgetInfo(widgetId)
            
            if (appWidgetInfo != null) {
                com.example.utils.AppWidgetHelper.startListening(context)
                val widgetView = com.example.utils.AppWidgetHelper.getHost(context).createView(context, widgetId, appWidgetInfo)
                
                val padding = (12 * density).toInt()
                val popupContainer = FrameLayout(context)
                popupContainer.setPadding(padding, padding, padding, padding)
                
                val popupOpacity = if (pageConfig?.useCustomSettings == true) pageConfig.transparency else prefs.getFloat("sidebar_transparency", 0.9f)
                val popupBg = android.graphics.drawable.GradientDrawable()
                popupBg.setColor(android.graphics.Color.parseColor("#1A1A1A"))
                popupBg.alpha = (popupOpacity * 255).toInt()
                popupBg.cornerRadius = 16 * density
                popupContainer.background = popupBg
                
                val minWidth = (appWidgetInfo.minWidth * density).toInt()
                val minHeight = (appWidgetInfo.minHeight * density).toInt()
                
                widgetView.minimumWidth = minWidth
                widgetView.minimumHeight = minHeight
                
                popupContainer.addView(widgetView, FrameLayout.LayoutParams(FrameLayout.LayoutParams.WRAP_CONTENT, FrameLayout.LayoutParams.WRAP_CONTENT))
                
                val overlayView = FrameLayout(context)
                overlayView.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                overlayView.setOnClickListener {
                    try { windowManager.removeView(overlayView) } catch (e: Exception) {}
                    currentOverlayView = null
                }
                
                // Block clicks on the container from propagating to the overlay dismiss listener
                popupContainer.setOnClickListener { }
                popupContainer.isClickable = true
                
                val location = IntArray(2)
                anchor.getLocationOnScreen(location)
                val anchorX = location[0]
                val anchorY = location[1]
                val screenWidth = context.resources.displayMetrics.widthPixels
                val screenHeight = context.resources.displayMetrics.heightPixels
                
                popupContainer.measure(View.MeasureSpec.UNSPECIFIED, View.MeasureSpec.UNSPECIFIED)
                val popupWidth = popupContainer.measuredWidth
                val popupHeight = popupContainer.measuredHeight
                
                var x = anchorX
                if (anchorX > screenWidth / 2) {
                    x = anchorX - popupWidth
                } else {
                    x = anchorX + anchor.width
                }
                var y = anchorY
                if (y + popupHeight > screenHeight) y = screenHeight - popupHeight
                if (y < 0) y = 0
                
                val containerParams = FrameLayout.LayoutParams(FrameLayout.LayoutParams.WRAP_CONTENT, FrameLayout.LayoutParams.WRAP_CONTENT).apply {
                    leftMargin = x
                    topMargin = y
                }
                overlayView.addView(popupContainer, containerParams)
                
                val wmParams = android.view.WindowManager.LayoutParams().apply {
                    width = android.view.WindowManager.LayoutParams.MATCH_PARENT
                    height = android.view.WindowManager.LayoutParams.MATCH_PARENT
                    if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                        type = android.view.WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
                    } else {
                        @Suppress("DEPRECATION")
                        type = android.view.WindowManager.LayoutParams.TYPE_PHONE
                    }
                    flags = android.view.WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                            android.view.WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN or
                            android.view.WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS
                    format = android.graphics.PixelFormat.TRANSLUCENT
                }
                
                windowManager.addView(overlayView, wmParams)
                currentOverlayView = overlayView
            }
        } catch (e: Exception) {
            e.printStackTrace()
            android.widget.Toast.makeText(context, "Failed to load widget", android.widget.Toast.LENGTH_SHORT).show()
        }
    }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/AppsPageView.kt", "w") as f:
    f.write(content)
