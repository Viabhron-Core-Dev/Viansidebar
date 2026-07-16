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
import org.json.JSONArray
import org.json.JSONObject

data class GridWidgetItem(
    val id: Int,
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
                    loadWidgets()
                }
            }
        }
    }

    init {
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
                list.add(GridWidgetItem(
                    obj.getInt("id"),
                    obj.optInt("cols", 2),
                    obj.optInt("rows", 2)
                ))
            } else {
                val id = arr.optInt(i, -1)
                if (id != -1) {
                    list.add(GridWidgetItem(id, 2, 2))
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
        items.add(GridWidgetItem(widgetId, 2, 2))
        saveWidgetItems(items)
    }

    fun getCurrentHeightPx(): Int {
        val density = context.resources.displayMetrics.density
        return (500 * density).toInt()
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
            
            for (item in items) {
                try {
                    val info = appWidgetManager.getAppWidgetInfo(item.id)
                    if (info != null) {
                        val hostView = host.createView(context, item.id, info)
                        
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
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
            onHeightChanged(getCurrentHeightPx())
        }
    }
}
