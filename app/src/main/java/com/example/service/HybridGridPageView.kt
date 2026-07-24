package com.example.service

import android.appwidget.AppWidgetManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.graphics.Color
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.widget.FrameLayout
import android.widget.GridLayout
import kotlin.math.max
import android.widget.ScrollView
import android.widget.PopupWindow
import android.widget.TextView
import android.widget.LinearLayout
import androidx.recyclerview.widget.RecyclerView
import androidx.recyclerview.widget.GridLayoutManager

import com.example.utils.AppWidgetHelper
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.json.JSONArray
import org.json.JSONObject


class HybridGridPageView(
    context: Context,
    private val pageId: String,
    private val onHeightChanged: (Int) -> Unit
) : FrameLayout(context) {

    private val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
    
    private val gridLayout = FrameLayout(context).apply {
        layoutParams = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT)
    }

    private val receiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            if (intent?.action == "ELEMENT_ADDED_TO_HYBRID") {
                val targetPageId = intent.getStringExtra("PAGE_ID")
                if (targetPageId == pageId) {
                    val widgetId = intent.getIntExtra("WIDGET_ID", -1)
                    if (widgetId != -1) {
                        addWidgetIdToPrefs(widgetId)
                    }
                    val elementId = intent.getStringExtra("ELEMENT_ID")
                    if (elementId != null) {
                        addElementIdToPrefs(elementId)
                    }
                    loadWidgets()
                }
            }
        }
    }

    init {
        com.example.LogKeeper.writeLog("HybridGrid", "Opened widgets grid page")
        val scrollView = ScrollView(context).apply {
            layoutParams = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
            addView(gridLayout)
        }
        addView(scrollView)
        loadWidgets()
    }

    override fun onAttachedToWindow() {
        super.onAttachedToWindow()
        context.registerReceiver(receiver, IntentFilter("ELEMENT_ADDED_TO_HYBRID"), Context.RECEIVER_NOT_EXPORTED)
    }

    override fun onDetachedFromWindow() {
        super.onDetachedFromWindow()
        try {
            context.unregisterReceiver(receiver)
        } catch (e: Exception) {}
    }

    private fun getWidgetItems(): List<GridWidgetItem> {
        val jsonStr = prefs.getString("hybrid_grid_$pageId", "[]") ?: "[]"
        val arr = JSONArray(jsonStr)
        val list = mutableListOf<GridWidgetItem>()
        for (i in 0 until arr.length()) {
            val obj = arr.optJSONObject(i)
            if (obj != null) {
                val idStr = if (obj.has("id")) {
                    val rawId = obj.get("id")
                    if (rawId is Int) "widget:$rawId" else rawId.toString()
                } else ""
                if (idStr.isNotEmpty()) {
                    list.add(GridWidgetItem(
                        idStr,
                        obj.optInt("cols", 2),
                        obj.optInt("rows", 2),
                        obj.optInt("x", 0),
                        obj.optInt("y", 0)
                    ))
                }
            } else {
                val id = arr.optInt(i, -1)
                if (id != -1) {
                    list.add(GridWidgetItem("widget:$id", 2, 2, 0, 0))
                }
            }
        }
        return list
    }

    private fun saveWidgetItems(items: List<GridWidgetItem>) {
        val arr = JSONArray()
        items.forEach { 
            val obj = JSONObject()
            obj.put("id", it.id)
            obj.put("cols", it.cols)
            obj.put("rows", it.rows)
            obj.put("x", it.x)
            obj.put("y", it.y)
            arr.put(obj)
        }
        prefs.edit().putString("hybrid_grid_$pageId", arr.toString()).apply()
    }

    private fun addWidgetIdToPrefs(widgetId: Int) {
        val items = getWidgetItems().toMutableList()
        // Default size 2x2
        items.add(GridWidgetItem("widget:$widgetId", 2, 2, 0, 0))
        saveWidgetItems(items)
    }
    
    private fun addElementIdToPrefs(elementId: String) {
        val items = getWidgetItems().toMutableList()
        // Default size 1x1 for elements
        items.add(GridWidgetItem(elementId, 1, 1, 0, 0))
        saveWidgetItems(items)
    }

    fun getCurrentHeightPx(): Int {
        if (gridLayout.childCount == 0) {
            val density = context.resources.displayMetrics.density
            return (150 * density).toInt()
        }
        gridLayout.measure(
            View.MeasureSpec.makeMeasureSpec(context.resources.displayMetrics.widthPixels, View.MeasureSpec.AT_MOST),
            View.MeasureSpec.makeMeasureSpec(0, View.MeasureSpec.UNSPECIFIED)
        )
        return gridLayout.measuredHeight
    }

    private fun loadWidgets() {
        gridLayout.removeAllViews()
        val totalCols = prefs.getInt("hybrid_grid_cols_$pageId", 4)
        // FrameLayout, no columnCount needed
        
        // Wait until grid layout has a width to calculate cell sizes
        post {
            val gridWidth = width
            if (gridWidth == 0) {
                // Try again if width is 0
                loadWidgets()
                return@post
            }
            
            val cellWidth = gridWidth / totalCols
            // Make cells square for simplicity, or use a fixed aspect ratio
            val cellHeight = cellWidth 
            
            val items = getWidgetItems()
            val appWidgetManager = AppWidgetManager.getInstance(context)
            val host = AppWidgetHelper.getHost(context)
            
            val appsManager = SidebarAppsManager(context, prefs, CoroutineScope(Dispatchers.IO), "wg_${pageId}") {}
            appsManager.ensureLoaded()
            
            var maxHeight = 0
            for (item in items) {
                try {
                    if (item.id.startsWith("widget:")) {
                        val wId = item.id.removePrefix("widget:").toIntOrNull() ?: continue
                        val info = appWidgetManager.getAppWidgetInfo(wId)
                        if (info != null) {
                            val hostView = host.createView(context, wId, info)
                            
                            val wCols = minOf(item.cols, totalCols)
                            val wRows = item.rows
                            
                            val params = FrameLayout.LayoutParams(cellWidth * wCols, cellHeight * wRows).apply {
                                leftMargin = item.x * cellWidth
                                topMargin = item.y * cellHeight
                            }
                            gridLayout.addView(hostView, params)
                            maxHeight = max(maxHeight, item.y * cellHeight + cellHeight * wRows)
                            
                            hostView.setOnLongClickListener {
                                val actionList = mutableListOf("App Info", "Remove")

                                var popupWindow: PopupWindow? = null
                                val popupLayout = LinearLayout(context).apply {
                                    orientation = LinearLayout.VERTICAL
                                    val pad = (8 * context.resources.displayMetrics.density).toInt()
                                    setPadding(pad, pad, pad, pad)
                                }

                                actionList.forEach { action ->
                                    val actionView = TextView(context).apply {
                                        text = action
                                        setTextColor(Color.WHITE)
                                        setPadding(0, (12 * context.resources.displayMetrics.density).toInt(), 0, (12 * context.resources.displayMetrics.density).toInt())
                                        gravity = Gravity.CENTER
                                        
                                        val shape = android.graphics.drawable.GradientDrawable()
                                        shape.cornerRadius = 8 * context.resources.displayMetrics.density
                                        shape.setColor(Color.parseColor("#333333"))
                                        shape.setStroke(1, Color.LTGRAY)
                                        background = shape
                                        
                                        layoutParams = LinearLayout.LayoutParams(
                                            LinearLayout.LayoutParams.WRAP_CONTENT,
                                            LinearLayout.LayoutParams.WRAP_CONTENT
                                        ).apply {
                                            setMargins(0, 0, 0, (8 * context.resources.displayMetrics.density).toInt())
                                        }
                                        
                                        setOnClickListener {
                                            popupWindow?.dismiss()
                                            when (action) {
                                                "Remove" -> {
                                                    val newItems = items.toMutableList()
                                                    newItems.removeAll { it.id == item.id }
                                                    saveWidgetItems(newItems)
                                                    context.sendBroadcast(Intent("ELEMENT_ADDED_TO_HYBRID").apply { putExtra("PAGE_ID", pageId) })
                                                }
                                                "App Info" -> {
                                                    try {
                                                        val intent = Intent(android.provider.Settings.ACTION_APPLICATION_DETAILS_SETTINGS)
                                                        intent.data = android.net.Uri.parse("package:${info.provider.packageName}")
                                                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                                        context.startActivity(intent)
                                                    } catch (e: Exception) {}
                                                }
                                            }
                                        }
                                    }
                                    popupLayout.addView(actionView)
                                }
                                
                                popupLayout.measure(View.MeasureSpec.UNSPECIFIED, View.MeasureSpec.UNSPECIFIED)
                                popupWindow = PopupWindow(
                                    popupLayout,
                                    (150 * context.resources.displayMetrics.density).toInt(),
                                    LinearLayout.LayoutParams.WRAP_CONTENT,
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
                                hostView.getLocationOnScreen(location)
                                val x = location[0]
                                var y = location[1] - popupLayout.measuredHeight
                                if (y < 0) y = location[1] + hostView.height
                                popupWindow?.showAtLocation(hostView, Gravity.NO_GRAVITY, x, y)
                                true
                            }
                        }
                    } else {
                        val parsed = appsManager.parseId(item.id)
                        if (parsed != null) {
                            val elementView = android.view.LayoutInflater.from(context).inflate(com.example.R.layout.item_sidebar_app, null, false)
                            val icon = elementView.findViewById<android.widget.ImageView>(com.example.R.id.app_icon)
                            val label = elementView.findViewById<android.widget.TextView>(com.example.R.id.app_label)
                            
                            label.text = parsed.label
                            
                            CoroutineScope(Dispatchers.Main).launch {
                                val bmp = appsManager.getIconBitmap(item.id)
                                if (bmp != null) {
                                    icon.setImageBitmap(bmp)
                                }
                            }
                            
                            elementView.setOnClickListener {
                                if (parsed is SidebarItem.App) {
                                    val intent = context.packageManager.getLaunchIntentForPackage(parsed.packageName)
                                    if (intent != null) {
                                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                        try { context.startActivity(intent) } catch (e: Exception) {}
                                    }
                                } else if (parsed is SidebarItem.Folder) {
                                    showFolderPopup(elementView, parsed, appsManager)
                                } else if (parsed is SidebarItem.PopupWidget) {
                                    showWidgetPopup(elementView, parsed)
                                } else if (parsed is SidebarItem.Link) {
                                    try {
                                        val intent = if (parsed.url.startsWith("intent:")) {
                                            Intent.parseUri(parsed.url, Intent.URI_INTENT_SCHEME)
                                        } else {
                                            Intent(Intent.ACTION_VIEW, android.net.Uri.parse(parsed.url))
                                        }
                                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                        context.startActivity(intent)
                                    } catch (e: Exception) {}
                                }
                            }
                            
                            elementView.setOnLongClickListener {
                                val actionList = mutableListOf<String>()
                                if (parsed is SidebarItem.App) {
                                    actionList.add("App Info")
                                }
                                actionList.add("Change Icon")
                                val customIconFile = java.io.File(context.filesDir, "custom_icons/${item.id.replace(Regex("[^a-zA-Z0-9.-]"), "_")}.webp")
                                if (customIconFile.exists()) {
                                    actionList.add("Reset Icon")
                                }
                                actionList.add("Remove")

                                var popupWindow: PopupWindow? = null
                                val popupLayout = LinearLayout(context).apply {
                                    orientation = LinearLayout.VERTICAL
                                    val pad = (8 * context.resources.displayMetrics.density).toInt()
                                    setPadding(pad, pad, pad, pad)
                                }

                                actionList.forEach { action ->
                                    val actionView = TextView(context).apply {
                                        text = action
                                        setTextColor(Color.WHITE)
                                        setPadding(0, (12 * context.resources.displayMetrics.density).toInt(), 0, (12 * context.resources.displayMetrics.density).toInt())
                                        gravity = Gravity.CENTER
                                        
                                        val shape = android.graphics.drawable.GradientDrawable()
                                        shape.cornerRadius = 8 * context.resources.displayMetrics.density
                                        shape.setColor(Color.parseColor("#333333"))
                                        shape.setStroke(1, Color.LTGRAY)
                                        background = shape
                                        
                                        layoutParams = LinearLayout.LayoutParams(
                                            LinearLayout.LayoutParams.WRAP_CONTENT,
                                            LinearLayout.LayoutParams.WRAP_CONTENT
                                        ).apply {
                                            setMargins(0, 0, 0, (8 * context.resources.displayMetrics.density).toInt())
                                        }
                                        
                                        setOnClickListener {
                                            popupWindow?.dismiss()
                                            when (action) {
                                                "Remove" -> {
                                                    // Need to remove from items and save
                                                    val newItems = items.toMutableList()
                                                    newItems.removeAll { it.id == item.id }
                                                    saveWidgetItems(newItems)
                                                    // Trigger reload
                                                    context.sendBroadcast(Intent("ELEMENT_ADDED_TO_HYBRID").apply { putExtra("PAGE_ID", pageId) })
                                                }
                                                "Change Icon" -> {
                                                    val intent = Intent(context, com.example.IconPickerActivity::class.java).apply {
                                                        putExtra("item_id", item.id)
                                                        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                                    }
                                                    context.startActivity(intent)
                                                }
                                                "Reset Icon" -> {
                                                    val file = java.io.File(context.filesDir, "custom_icons/${item.id.replace(Regex("[^a-zA-Z0-9.-]"), "_")}.webp")
                                                    if (file.exists()) file.delete()
                                                    appsManager.iconCache.remove("custom_${item.id}")
                                                    appsManager.iconCache.remove(item.id)
                                                    context.sendBroadcast(Intent("com.example.UPDATE_SIDEBAR_ICONS").apply {
                                                        putExtra("item_id", item.id)
                                                    })
                                                }
                                                "App Info" -> {
                                                    if (parsed is SidebarItem.App) {
                                                        try {
                                                            val intent = Intent(android.provider.Settings.ACTION_APPLICATION_DETAILS_SETTINGS)
                                                            intent.data = android.net.Uri.parse("package:${parsed.packageName}")
                                                            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                                            context.startActivity(intent)
                                                        } catch (e: Exception) {}
                                                    }
                                                }
                                            }
                                        }
                                    }
                                    popupLayout.addView(actionView)
                                }
                                
                                popupLayout.measure(View.MeasureSpec.UNSPECIFIED, View.MeasureSpec.UNSPECIFIED)
                                popupWindow = PopupWindow(
                                    popupLayout,
                                    (150 * context.resources.displayMetrics.density).toInt(),
                                    LinearLayout.LayoutParams.WRAP_CONTENT,
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
                                elementView.getLocationOnScreen(location)
                                val x = location[0]
                                var y = location[1] - popupLayout.measuredHeight
                                if (y < 0) y = location[1] + elementView.height
                                popupWindow?.showAtLocation(elementView, Gravity.NO_GRAVITY, x, y)
                                true
                            }
                            
                            val wCols = minOf(item.cols, totalCols)
                            val wRows = item.rows
                            
                            val params = FrameLayout.LayoutParams(cellWidth * wCols, cellHeight * wRows).apply {
                                leftMargin = item.x * cellWidth
                                topMargin = item.y * cellHeight
                            }
                            gridLayout.addView(elementView, params)
                            maxHeight = max(maxHeight, item.y * cellHeight + cellHeight * wRows)
                        }
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
            gridLayout.layoutParams = FrameLayout.LayoutParams(FrameLayout.LayoutParams.MATCH_PARENT, maxHeight)
            onHeightChanged(getCurrentHeightPx())
        }
    }

    private fun showFolderPopup(anchor: View, folder: SidebarItem.Folder, appsManager: SidebarAppsManager) {
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
                if (parsed is SidebarItem.App) {
                    val intent = context.packageManager.getLaunchIntentForPackage(parsed.packageName)
                    if (intent != null) {
                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                        try { context.startActivity(intent) } catch (e: Exception) {}
                        popupWindow?.dismiss()
                    }
                } else if (parsed is SidebarItem.Link) {
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

    private fun showWidgetPopup(anchor: View, widget: SidebarItem.PopupWidget) {
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
