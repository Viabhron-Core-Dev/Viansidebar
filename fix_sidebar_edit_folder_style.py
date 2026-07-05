import re

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'r') as f:
    content = f.read()

old_code = """                                "Folder Style" -> {
                                    if (item is SidebarItem.Folder) {
                                        showFolderStyleDialog(context, item, manager) { styleIndex ->
                                            // Handle saving style from menu
                                        }
                                    }
                                }"""

new_code = """                                "Folder Style" -> {
                                    if (item is SidebarItem.Folder) {
                                        showFolderStyleDialog(context, item, manager) { styleIndex, popupCols ->
                                            val json = org.json.JSONObject().apply {
                                                put("name", item.name)
                                                put("colorHex", item.colorHex)
                                                val jArr = org.json.JSONArray()
                                                item.items.forEach { jArr.put(it) }
                                                put("items", jArr)
                                                put("folderStyle", styleIndex)
                                                put("popupColumns", popupCols)
                                            }
                                            val newId = "folder:${item.uuid}:$json"
                                            
                                            // Update localIds with the new ID
                                            val pos = localIds.indexOf(item.id)
                                            if (pos != -1) {
                                                localIds[pos] = newId
                                                refresh()
                                            }
                                        }
                                    }
                                }"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'w') as f:
    f.write(content)
