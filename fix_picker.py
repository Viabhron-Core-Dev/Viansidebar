import re

with open('app/src/main/java/com/example/WidgetPickerActivity.kt', 'r') as f:
    content = f.read()

picker_logic = """        if (actionType == "ADD_ELEMENT") {
            val widgetManager = AppWidgetManager.getInstance(this)
            val info = widgetManager.getAppWidgetInfo(widgetId)
            val label = info?.loadLabel(packageManager) ?: "Widget"
            
            val json = JSONObject()
            json.put("widgetId", widgetId)
            json.put("label", label)
            val id = "widget:${widgetId}:${json.toString()}"
            
            val serviceIntent = Intent(this, com.example.service.FloatingReaderService::class.java)"""

content = content.replace("""        if (actionType == "ADD_ELEMENT") {
            val json = JSONObject()
            json.put("widgetId", widgetId)
            val id = "widget:${widgetId}:${json.toString()}"
            
            val serviceIntent = Intent(this, com.example.service.FloatingReaderService::class.java)""", picker_logic)

with open('app/src/main/java/com/example/WidgetPickerActivity.kt', 'w') as f:
    f.write(content)

