import re

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

widget_fix = """            } else if (id.startsWith("widget:")) {
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
                    result.add(SidebarItem.Widget(widgetId, label))
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        } else if (id.startsWith("folder:")) {"""

content = re.sub(r'\} else if \(id.startsWith\("widget:"\)\) \{.*?return SidebarItem.Widget\(widgetId, label\).*?\} else if \(id.startsWith\("folder:"\)\) \{', widget_fix, content, flags=re.DOTALL)

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)

