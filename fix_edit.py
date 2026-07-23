with open("app/src/main/java/com/example/WidgetsGridEditActivity.kt", "r") as f:
    content = f.read()

# Add import android.app.Activity
if "import android.app.Activity" not in content:
    content = content.replace("import android.content.Context", "import android.content.Context\nimport android.app.Activity")

# Fix loadLocalItems
old_load = """            if (obj != null) {
                localItems.add(GridWidgetItem(
                    obj.getInt("id"),
                    obj.optInt("cols", 2),
                    obj.optInt("rows", 2)
                ))
            } else {
                val id = arr.optInt(i, -1)
                if (id != -1) {
                    localItems.add(GridWidgetItem(id, 2, 2))
                }
            }"""
new_load = """            if (obj != null) {
                val idStr = if (obj.has("elementId")) obj.getString("elementId") 
                            else if (obj.has("id")) {
                                val rawId = obj.get("id")
                                if (rawId is Int) "widget:$rawId" else rawId.toString()
                            } else ""
                if (idStr.isNotEmpty()) {
                    localItems.add(GridWidgetItem(
                        idStr,
                        obj.optInt("cols", 2),
                        obj.optInt("rows", 2)
                    ))
                }
            } else {
                val id = arr.optInt(i, -1)
                if (id != -1) {
                    localItems.add(GridWidgetItem("widget:$id", 2, 2))
                }
            }"""
content = content.replace(old_load, new_load)

# Fix appWidgetManager.getAppWidgetInfo(item.id)
import re
content = re.sub(r'val info = appWidgetManager\.getAppWidgetInfo\(item\.id\)\s*holder\.tvName\.text = info\?\.loadLabel\(packageManager\) \?\: "Widget \$\{item\.id\} \(Unknown\)"',
    """if (item.id.startsWith("widget:")) {
                val wId = item.id.removePrefix("widget:").toIntOrNull() ?: -1
                val info = appWidgetManager.getAppWidgetInfo(wId)
                holder.tvName.text = info?.loadLabel(packageManager) ?: "Widget ${wId} (Unknown)"
            } else {
                val parsed = manager.parseId(item.id)
                holder.tvName.text = parsed?.label ?: item.id
            }""", content)

with open("app/src/main/java/com/example/WidgetsGridEditActivity.kt", "w") as f:
    f.write(content)
