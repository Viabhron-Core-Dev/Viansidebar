import re

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "r") as f:
    content = f.read()

target = """        } else if (id.startsWith("popup_widget:")) {
            try {
                val widgetId = id.substringAfter("popup_widget:").toInt()
                val appWidgetManager = android.appwidget.AppWidgetManager.getInstance(context)
                val info = appWidgetManager.getAppWidgetInfo(widgetId)
                val label = info?.loadLabel(context.packageManager) ?: "Widget $widgetId"
                return SidebarItem.PopupWidget(widgetId, label, id)
            } catch (e: Exception) {
                e.printStackTrace()
            }
        } else if (id.startsWith("widget:")) {"""

replacement = """        } else if (id.startsWith("popup_widget:")) {
            try {
                val parts = id.split(":", limit = 3)
                if (parts.size >= 2) {
                    val widgetId = parts[1].toInt()
                    val appWidgetManager = android.appwidget.AppWidgetManager.getInstance(context)
                    val info = appWidgetManager.getAppWidgetInfo(widgetId)
                    val label = info?.loadLabel(context.packageManager) ?: "Widget $widgetId"
                    return SidebarItem.PopupWidget(widgetId, label, id)
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        } else if (id.startsWith("widget:")) {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "w") as f:
    f.write(content)
