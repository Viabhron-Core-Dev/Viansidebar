import os
import re

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "r") as f:
    content = f.read()

methods = '''
    private fun showFolderPopup(anchor: View, folder: com.example.service.SidebarAppsManager.SidebarItem.Folder) {
        val density = context.resources.displayMetrics.density
        val popupView = ScrollView(context)
        val gridLayout = android.widget.GridLayout(context)
        
        val maxCols = if (folder.popupColumns > 0) folder.popupColumns else prefs.getInt("sidebar_columns", 3)
        val validCols = if (maxCols > 0) maxCols else 1
        gridLayout.columnCount = validCols
        val padding = (16 * density).toInt()
        gridLayout.setPadding(padding, padding, padding, padding)
        popupView.addView(gridLayout, FrameLayout.LayoutParams(FrameLayout.LayoutParams.WRAP_CONTENT, FrameLayout.LayoutParams.WRAP_CONTENT))

        val popupOpacity = prefs.getFloat("sidebar_transparency", 0.9f)
        val popupBg = android.graphics.drawable.GradientDrawable()
        popupBg.setColor(Color.parseColor("#1A1A1A"))
        popupBg.alpha = (popupOpacity * 255).toInt()
        popupBg.cornerRadius = 16 * density
        popupView.background = popupBg

        var popupWindow: PopupWindow? = null

        for (itemId in folder.items) {
            val parsed = appsManager.parseId(itemId) ?: continue
            val elementView = android.view.LayoutInflater.from(context).inflate(com.example.R.layout.item_sidebar_app, null, false)
            val icon = elementView.findViewById<android.widget.ImageView>(com.example.R.id.app_icon)
            val label = elementView.findViewById<android.widget.TextView>(com.example.R.id.app_label)
            label.text = parsed.label
            CoroutineScope(Dispatchers.Main).launch {
                val bmp = appsManager.getIconBitmap(itemId)
                if (bmp != null) icon.setImageBitmap(bmp)
            }
            elementView.setOnClickListener {
                if (parsed is com.example.service.SidebarAppsManager.SidebarItem.App) {
                    val intent = context.packageManager.getLaunchIntentForPackage(parsed.packageName)
                    if (intent != null) {
                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                        try { context.startActivity(intent) } catch (e: Exception) {}
                        popupWindow?.dismiss()
                    }
                } else if (parsed is com.example.service.SidebarAppsManager.SidebarItem.Link) {
                    try {
                        val intent = if (parsed.url.startsWith("intent:")) {
                            Intent.parseUri(parsed.url, Intent.URI_INTENT_SCHEME)
                        } else {
                            Intent(Intent.ACTION_VIEW, android.net.Uri.parse(parsed.url))
                        }
                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                        context.startActivity(intent)
                        popupWindow?.dismiss()
                    } catch (e: Exception) {}
                }
            }
            
            val params = android.widget.GridLayout.LayoutParams()
            params.width = (72 * density).toInt()
            params.height = (72 * density).toInt()
            gridLayout.addView(elementView, params)
        }

        popupView.measure(View.MeasureSpec.UNSPECIFIED, View.MeasureSpec.UNSPECIFIED)
        val totalWidth = popupView.measuredWidth
        val totalHeight = popupView.measuredHeight

        popupWindow = PopupWindow(
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
            setBackgroundDrawable(android.graphics.drawable.ColorDrawable(Color.TRANSPARENT))
            isOutsideTouchable = true
        }
        val location = IntArray(2)
        anchor.getLocationOnScreen(location)
        val anchorX = location[0]
        val anchorY = location[1]
        val screenWidth = context.resources.displayMetrics.widthPixels
        val screenHeight = context.resources.displayMetrics.heightPixels
        var x = anchorX
        if (anchorX > screenWidth / 2) {
            x = anchorX - totalWidth
        } else {
            x = anchorX + anchor.width
        }
        var y = anchorY - (totalHeight / 2) + (anchor.height / 2)
        if (y < 0) y = 0
        if (y + totalHeight > screenHeight) y = screenHeight - totalHeight
        popupWindow.showAtLocation(anchor, Gravity.NO_GRAVITY, x, y)
    }

    private fun showWidgetPopup(anchor: View, widget: com.example.service.SidebarAppsManager.SidebarItem.PopupWidget) {
        val density = context.resources.displayMetrics.density
        val popupView = FrameLayout(context)
        
        val padding = (8 * density).toInt()
        popupView.setPadding(padding, padding, padding, padding)

        val popupOpacity = prefs.getFloat("sidebar_transparency", 0.9f)
        val popupBg = android.graphics.drawable.GradientDrawable()
        popupBg.setColor(Color.parseColor("#1A1A1A"))
        popupBg.alpha = (popupOpacity * 255).toInt()
        popupBg.cornerRadius = 16 * density
        popupView.background = popupBg
        
        val appWidgetManager = AppWidgetManager.getInstance(context)
        val host = com.example.utils.AppWidgetHelper.getHost(context)
        val info = appWidgetManager.getAppWidgetInfo(widget.widgetId)
        
        var popupWindow: PopupWindow? = null
        if (info != null) {
            val hostView = host.createView(context, widget.widgetId, info)
            
            val minW = info.minWidth
            val minH = info.minHeight
            val w = if (minW > 0) minW else (200 * density).toInt()
            val h = if (minH > 0) minH else (200 * density).toInt()
            
            val params = FrameLayout.LayoutParams(w, h)
            popupView.addView(hostView, params)
        }

        popupView.measure(View.MeasureSpec.UNSPECIFIED, View.MeasureSpec.UNSPECIFIED)
        val totalWidth = popupView.measuredWidth
        val totalHeight = popupView.measuredHeight

        popupWindow = PopupWindow(
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
            setBackgroundDrawable(android.graphics.drawable.ColorDrawable(Color.TRANSPARENT))
            isOutsideTouchable = true
        }
        val location = IntArray(2)
        anchor.getLocationOnScreen(location)
        val anchorX = location[0]
        val anchorY = location[1]
        val screenWidth = context.resources.displayMetrics.widthPixels
        val screenHeight = context.resources.displayMetrics.heightPixels
        var x = anchorX
        if (anchorX > screenWidth / 2) {
            x = anchorX - totalWidth
        } else {
            x = anchorX + anchor.width
        }
        var y = anchorY - (totalHeight / 2) + (anchor.height / 2)
        if (y < 0) y = 0
        if (y + totalHeight > screenHeight) y = screenHeight - totalHeight
        popupWindow.showAtLocation(anchor, Gravity.NO_GRAVITY, x, y)
    }
}
'''

# insert before last }
idx = content.rfind('}')
if idx != -1:
    content = content[:idx] + methods + content[idx:]
    
with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "w") as f:
    f.write(content)
