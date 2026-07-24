import os
import re

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "r") as f:
    content = f.read()

# Add to SidebarItem sealed class
content = re.sub(
r'sealed class SidebarItem \{\n    abstract var id: String\n    abstract val label: String',
'''sealed class SidebarItem {
    abstract var id: String
    abstract val label: String
    
    data class PopupWidget(val widgetId: Int, override val label: String, override var id: String = "popup_widget:$widgetId") : SidebarItem()''', content)

# Parse popup_widget: in parseIdInternal
content = content.replace(
'''        } else if (id.startsWith("widget:")) {
            try {
                val parts = id.split(":", limit = 3)
                if (parts.size >= 2) {
                    val widgetId = parts[1].toInt()
                    val jsonStr = parts.getOrNull(2)
                    var label = "Widget $widgetId"
                    
                    if (jsonStr != null && jsonStr.isNotEmpty()) {
                        val json = org.json.JSONObject(jsonStr)
                        label = json.optString("label", label)
                    }
                    return SidebarItem.Widget(widgetId, label)
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        } else if (id.startsWith("folder:")) {''',
'''        } else if (id.startsWith("widget:")) {
            try {
                val parts = id.split(":", limit = 3)
                if (parts.size >= 2) {
                    val widgetId = parts[1].toInt()
                    val jsonStr = parts.getOrNull(2)
                    var label = "Widget $widgetId"
                    
                    if (jsonStr != null && jsonStr.isNotEmpty()) {
                        val json = org.json.JSONObject(jsonStr)
                        label = json.optString("label", label)
                    }
                    return SidebarItem.Widget(widgetId, label)
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        } else if (id.startsWith("popup_widget:")) {
            try {
                val parts = id.split(":", limit = 3)
                if (parts.size >= 2) {
                    val widgetId = parts[1].toInt()
                    val jsonStr = parts.getOrNull(2)
                    var label = "Popup Widget $widgetId"
                    
                    if (jsonStr != null && jsonStr.isNotEmpty()) {
                        val json = org.json.JSONObject(jsonStr)
                        label = json.optString("label", label)
                    }
                    return SidebarItem.PopupWidget(widgetId, label, id)
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        } else if (id.startsWith("folder:")) {''')

content = content.replace(
'''        } else if (id.startsWith("widget:")) {
            val awm = android.appwidget.AppWidgetManager.getInstance(context)
            try {
                val parts = id.split(":", limit = 3)
                if (parts.size >= 2) {
                    val wId = parts[1].toInt()
                    val info = awm.getAppWidgetInfo(wId)
                    if (info != null) {
                        val pInfo = context.packageManager.getApplicationInfo(info.provider.packageName, 0)
                        val icon = pInfo.loadIcon(context.packageManager)
                        return drawableToBitmap(icon)
                    }
                }
            } catch(e: Exception) {}
            return null
        } else if (id.startsWith("pwa:")) {''',
'''        } else if (id.startsWith("widget:")) {
            val awm = android.appwidget.AppWidgetManager.getInstance(context)
            try {
                val parts = id.split(":", limit = 3)
                if (parts.size >= 2) {
                    val wId = parts[1].toInt()
                    val info = awm.getAppWidgetInfo(wId)
                    if (info != null) {
                        val pInfo = context.packageManager.getApplicationInfo(info.provider.packageName, 0)
                        val icon = pInfo.loadIcon(context.packageManager)
                        return drawableToBitmap(icon)
                    }
                }
            } catch(e: Exception) {}
            return null
        } else if (id.startsWith("popup_widget:")) {
            val awm = android.appwidget.AppWidgetManager.getInstance(context)
            try {
                val parts = id.split(":", limit = 3)
                if (parts.size >= 2) {
                    val wId = parts[1].toInt()
                    val info = awm.getAppWidgetInfo(wId)
                    if (info != null) {
                        val pInfo = context.packageManager.getApplicationInfo(info.provider.packageName, 0)
                        val icon = pInfo.loadIcon(context.packageManager)
                        return drawableToBitmap(icon)
                    }
                }
            } catch(e: Exception) {}
            return null
        } else if (id.startsWith("pwa:")) {''')

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "w") as f:
    f.write(content)
