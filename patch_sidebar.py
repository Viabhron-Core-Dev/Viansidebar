import re

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "r") as f:
    content = f.read()

target = """        } else if (id.startsWith("settings_shortcut:")) {
                val actionId = id.substringAfter("settings_shortcut:")
                val settingsAction = ALL_SETTINGS_SHORTCUTS.find { it.action == actionId }
                if (settingsAction != null) {
                    return SidebarItem.SettingsShortcut(actionId, settingsAction.label, settingsAction.iconResId)
                }
            
        } else if (id.startsWith("widget:")) {"""

replacement = """        } else if (id.startsWith("popup_widget:")) {
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

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "w") as f:
    f.write(content)
