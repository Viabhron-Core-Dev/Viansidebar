package com.example.service

import android.appwidget.AppWidgetManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.graphics.Color
import android.view.Gravity
import android.view.View
import android.widget.Button
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import com.example.utils.AppWidgetHelper
import org.json.JSONArray

class WidgetsGridPageView(
    context: Context,
    private val pageId: String,
    private val onHeightChanged: (Int) -> Unit
) : FrameLayout(context) {

    private val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
    private val widgetsContainer = LinearLayout(context).apply {
        orientation = LinearLayout.VERTICAL
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
                        loadWidgets()
                    }
                }
            }
        }
    }

    init {
        val scrollView = ScrollView(context).apply {
            layoutParams = LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT)
            addView(widgetsContainer)
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

    private fun getWidgetIds(): List<Int> {
        val jsonStr = prefs.getString("widgets_grid_$pageId", "[]") ?: "[]"
        val arr = JSONArray(jsonStr)
        val list = mutableListOf<Int>()
        for (i in 0 until arr.length()) {
            list.add(arr.getInt(i))
        }
        return list
    }

    private fun addWidgetIdToPrefs(widgetId: Int) {
        val ids = getWidgetIds().toMutableList()
        ids.add(widgetId)
        val arr = JSONArray()
        ids.forEach { arr.put(it) }
        prefs.edit().putString("widgets_grid_$pageId", arr.toString()).apply()
    }

    private fun removeWidgetIdFromPrefs(widgetId: Int) {
        val ids = getWidgetIds().toMutableList()
        ids.remove(widgetId)
        val arr = JSONArray()
        ids.forEach { arr.put(it) }
        prefs.edit().putString("widgets_grid_$pageId", arr.toString()).apply()
        
        // Also delete the widget
        try {
            AppWidgetHelper.getHost(context).deleteAppWidgetId(widgetId)
        } catch (e: Exception) {}
    }

    fun getCurrentHeightPx(): Int {
        val density = context.resources.displayMetrics.density
        return (500 * density).toInt()
    }

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
