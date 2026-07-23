with open("app/src/main/java/com/example/service/WidgetsGridPageView.kt", "r") as f:
    content = f.read()

# Replace getWidgetItems parsing
old_parse = """                list.add(GridWidgetItem(
                    obj.getInt("id"),
                    obj.optInt("cols", 2),
                    obj.optInt("rows", 2)
                ))"""

new_parse = """                val idStr = if (obj.has("id")) {
                    val rawId = obj.get("id")
                    if (rawId is Int) "widget:$rawId" else rawId.toString()
                } else ""
                if (idStr.isNotEmpty()) {
                    list.add(GridWidgetItem(
                        idStr,
                        obj.optInt("cols", 2),
                        obj.optInt("rows", 2)
                    ))
                }"""
content = content.replace(old_parse, new_parse)

old_fallback = """            } else {
                val id = arr.optInt(i, -1)
                if (id != -1) {
                    list.add(GridWidgetItem(id, 2, 2))
                }
            }"""
new_fallback = """            } else {
                val id = arr.optInt(i, -1)
                if (id != -1) {
                    list.add(GridWidgetItem("widget:$id", 2, 2))
                }
            }"""
content = content.replace(old_fallback, new_fallback)

# Replace addWidgetIdToPrefs
old_add = """    private fun addWidgetIdToPrefs(widgetId: Int) {
        val items = getWidgetItems().toMutableList()
        // Default size 2x2
        items.add(GridWidgetItem(widgetId, 2, 2))
        saveWidgetItems(items)
    }"""
new_add = """    private fun addWidgetIdToPrefs(widgetId: Int) {
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
    }"""
content = content.replace(old_add, new_add)

# In onReceive
old_receive = """                    val widgetId = intent.getIntExtra("WIDGET_ID", -1)
                    if (widgetId != -1) {
                        addWidgetIdToPrefs(widgetId)
                    }"""
new_receive = """                    val widgetId = intent.getIntExtra("WIDGET_ID", -1)
                    if (widgetId != -1) {
                        addWidgetIdToPrefs(widgetId)
                    }
                    val elementId = intent.getStringExtra("ELEMENT_ID")
                    if (elementId != null) {
                        addElementIdToPrefs(elementId)
                    }"""
content = content.replace(old_receive, new_receive)

with open("app/src/main/java/com/example/service/WidgetsGridPageView.kt", "w") as f:
    f.write(content)
