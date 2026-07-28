package com.example.utils

import android.content.Context
import android.content.SharedPreferences
import org.json.JSONArray
import org.json.JSONObject
import java.util.UUID

data class SidebarPage(
    val id: String,
    val type: String,
    var title: String,
    var gridColumns: Int = 3,
    var gridWrapContent: Boolean = true,
    var stickAlignment: String = "bottom",
    var useCustomSettings: Boolean = false,
    var width: Int = 180,
    var height: Int = 450,
    var wrapContentHeight: Boolean = true,
    var transparency: Float = 0.9f
) {
    fun toJson(): JSONObject {
        val obj = JSONObject()
        obj.put("id", id)
        obj.put("type", type)
        obj.put("title", title)
        obj.put("gridColumns", gridColumns)
        obj.put("gridWrapContent", gridWrapContent)
        obj.put("stickAlignment", stickAlignment)
        obj.put("useCustomSettings", useCustomSettings)
        obj.put("width", width)
        obj.put("height", height)
        obj.put("wrapContentHeight", wrapContentHeight)
        obj.put("transparency", transparency.toDouble())
        return obj
    }

    companion object {
        fun createDefault(id: String, type: String, title: String): SidebarPage {
            val wrap = when(type) { "calculator", "compass", "notification", "scheduler", "widget", "widgets_grid", "hybrid_grid", "app_tracker", "dictionary", "pwa_loader" -> false else -> true }
            val h = when(type) { "calculator" -> 450; "compass" -> 500; "notification", "scheduler", "widget", "widgets_grid", "hybrid_grid" -> 500; "app_tracker" -> 600; "dictionary" -> 500; else -> 450 }
            return SidebarPage(
                id = id, type = type, title = title,
                wrapContentHeight = wrap, height = h, width = 320
            )
        }
        
        fun fromJson(obj: JSONObject): SidebarPage {
            return SidebarPage(
                id = obj.getString("id"),
                type = obj.getString("type"),
                title = obj.getString("title"),
                gridColumns = obj.optInt("gridColumns", 3),
                gridWrapContent = obj.optBoolean("gridWrapContent", true),
                stickAlignment = obj.optString("stickAlignment", "bottom"),
                useCustomSettings = obj.optBoolean("useCustomSettings", false),
                width = obj.optInt("width", 180),
                height = obj.optInt("height", 450),
                wrapContentHeight = obj.optBoolean("wrapContentHeight", true),
                transparency = obj.optDouble("transparency", 0.9).toFloat()
            )
        }
    }
}

object PageManager {
    fun getPages(prefs: SharedPreferences, handleId: String): List<SidebarPage> {
        val legacy = if (handleId == "sidebar") prefs.getString("sidebar_pages", null) else null
        val pagesJson = prefs.getString("handle_${handleId}_pages", legacy)
        val defaultPage = SidebarPage(id = "default_hybrid", type = "hybrid_grid", title = "Home Grid")
        if (pagesJson == null) {
            // Default setup
            return listOf(defaultPage)
        }
        val list = mutableListOf<SidebarPage>()
        try {
            val arr = JSONArray(pagesJson)
            for (i in 0 until arr.length()) {
                val page = SidebarPage.fromJson(arr.getJSONObject(i))
                if (page.type != "dictionary") {
                    list.add(page)
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
            return listOf(defaultPage)
        }
        
        // Ensure first page is always default_hybrid
        if (list.isEmpty()) {
            list.add(defaultPage)
        } else if (list[0].id != "default_hybrid") {
            list.removeAll { it.id == "default_hybrid" }
            list.add(0, defaultPage)
        }
        
        return list
    }

    fun savePages(prefs: SharedPreferences, handleId: String, pages: List<SidebarPage>) {
        val arr = JSONArray()
        pages.forEach { arr.put(it.toJson()) }
        prefs.edit().putString("handle_${handleId}_pages", arr.toString()).apply()
    }

    fun getDefaultPageIndex(prefs: SharedPreferences, handleId: String): Int {
        return prefs.getInt("handle_${handleId}_default_page_index", prefs.getInt("sidebar_default_page_index", 0))
    }

    fun saveDefaultPageIndex(prefs: SharedPreferences, handleId: String, index: Int) {
        prefs.edit().putInt("handle_${handleId}_default_page_index", index).apply()
    }
}
