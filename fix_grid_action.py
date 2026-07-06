import re

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'r') as f:
    content = f.read()

old_action = """                                "Folder Style" -> {
                                    com.example.LogKeeper.writeLog("SidebarEdit", "Editing folder style for ${item.label}")
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

new_action = """                                "Folder Style" -> {
                                    com.example.LogKeeper.writeLog("SidebarEdit", "Editing folder style for ${item.label}")
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
                                                put("popupRows", item.popupRows)
                                            }
                                            val newId = "folder:${item.uuid}:$json"
                                            val pos = localIds.indexOf(item.id)
                                            if (pos != -1) {
                                                localIds[pos] = newId
                                                refresh()
                                            }
                                        }
                                    }
                                }
                                "Grid Size" -> {
                                    com.example.LogKeeper.writeLog("SidebarEdit", "Editing grid size for ${item.label}")
                                    if (item is SidebarItem.Folder) {
                                        showGridSizeDialog(context, item, manager) { cols, rows ->
                                            val json = org.json.JSONObject().apply {
                                                put("name", item.name)
                                                put("colorHex", item.colorHex)
                                                val jArr = org.json.JSONArray()
                                                item.items.forEach { jArr.put(it) }
                                                put("items", jArr)
                                                put("folderStyle", item.folderStyle)
                                                put("popupColumns", cols)
                                                put("popupRows", rows)
                                            }
                                            val newId = "folder:${item.uuid}:$json"
                                            val pos = localIds.indexOf(item.id)
                                            if (pos != -1) {
                                                localIds[pos] = newId
                                                refresh()
                                            }
                                        }
                                    }
                                }"""
content = content.replace(old_action, new_action)

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'w') as f:
    f.write(content)
