package com.example.service

import android.appwidget.AppWidgetManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.graphics.Color
import android.view.Gravity
import android.view.View
import android.widget.FrameLayout
import android.widget.GridLayout
import android.widget.ScrollView
import com.example.utils.AppWidgetHelper
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import org.json.JSONArray
import org.json.JSONObject

data class GridWidgetItem(
    val id: String,
    var cols: Int = 2,
    var rows: Int = 2
)

class WidgetsGridPageView(
    context: Context,
    private val pageId: String,
    private val onHeightChanged: (Int) -> Unit
) : FrameLayout(context) {

    private val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
    
    private val gridLayout = GridLayout(context).apply {
        layoutParams = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT)
    }

    private val receiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            if (intent?.action == "WIDGET_ADDED_TO_GRID") {
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
        com.example.LogKeeper.writeLog("WidgetsGrid", "Opened widgets grid page")
        val scrollView = ScrollView(context).apply {
            layoutParams = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
            addView(gridLayout)
        }
        addView(scrollView)
        loadWidgets()
    }

    override fun onAttachedToWindow() {
        super.onAttachedToWindow()
        context.registerReceiver(receiver, IntentFilter("WIDGET_ADDED_TO_GRID"), Context.RECEIVER_NOT_EXPORTED)
    }

    override fun onDetachedFromWindow() {
        super.onDetachedFromWindow()
        try {
            context.unregisterReceiver(receiver)
        } catch (e: Exception) {}
    }

    private fun getWidgetItems(): List<GridWidgetItem> {
        val jsonStr = prefs.getString("widgets_grid_$pageId", "[]") ?: "[]"
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
                        obj.optInt("rows", 2)
                    ))
                }
            } else {
                val id = arr.optInt(i, -1)
                if (id != -1) {
                    list.add(GridWidgetItem("widget:$id", 2, 2))
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
            arr.put(obj)
        }
        prefs.edit().putString("widgets_grid_$pageId", arr.toString()).apply()
    }

    private fun addWidgetIdToPrefs(widgetId: Int) {
        val items = getWidgetItems().toMutableList()
        // Default size 2x2
        items.add(GridWidgetItem("widget:$widgetId", 2, 2))
        saveWidgetItems(items)
    }
    
    private fun addElementIdToPrefs(elementId: String) {
        val items = getWidgetItems().toMutableList()
        // Default size 1x1 for elements
        items.add(GridWidgetItem(elementId, 1, 1))
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
        val totalCols = prefs.getInt("widgets_grid_cols_$pageId", 4)
        gridLayout.columnCount = totalCols
        
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
            
            for (item in items) {
                try {
                    if (item.id.startsWith("widget:")) {
                        val wId = item.id.removePrefix("widget:").toIntOrNull() ?: continue
                        val info = appWidgetManager.getAppWidgetInfo(wId)
                        if (info != null) {
                            val hostView = host.createView(context, wId, info)
                            
                            val wCols = minOf(item.cols, totalCols)
                            val wRows = item.rows
                            
                            val params = GridLayout.LayoutParams().apply {
                                width = cellWidth * wCols
                                height = cellHeight * wRows
                                columnSpec = GridLayout.spec(GridLayout.UNDEFINED, wCols)
                                rowSpec = GridLayout.spec(GridLayout.UNDEFINED, wRows)
                            }
                            gridLayout.addView(hostView, params)
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
                                val i = Intent(context, FloatingReaderService::class.java).apply {
                                    action = "LAUNCH_APP"
                                    putExtra("APP_PACKAGE", item.id)
                                }
                                context.startService(i)
                            }
                            
                            val wCols = minOf(item.cols, totalCols)
                            val wRows = item.rows
                            
                            val params = GridLayout.LayoutParams().apply {
                                width = cellWidth * wCols
                                height = cellHeight * wRows
                                columnSpec = GridLayout.spec(GridLayout.UNDEFINED, wCols)
                                rowSpec = GridLayout.spec(GridLayout.UNDEFINED, wRows)
                            }
                            gridLayout.addView(elementView, params)
                        }
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
            onHeightChanged(getCurrentHeightPx())
        }
    }
}
