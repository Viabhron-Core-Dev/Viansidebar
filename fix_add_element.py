import re

with open('app/src/main/java/com/example/service/AddElementOverlayView.kt', 'r') as f:
    content = f.read()

old_code = """                        showFolderStyleDialog(context, dummyFolder, manager) { styleIndex ->
                            val json = org.json.JSONObject().apply {
                                put("name", name)
                                put("colorHex", color)
                                put("items", org.json.JSONArray())
                                put("folderStyle", styleIndex)
                            }"""

new_code = """                        showFolderStyleDialog(context, dummyFolder, manager) { styleIndex, popupCols ->
                            val json = org.json.JSONObject().apply {
                                put("name", name)
                                put("colorHex", color)
                                put("items", org.json.JSONArray())
                                put("folderStyle", styleIndex)
                                put("popupColumns", popupCols)
                            }"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/service/AddElementOverlayView.kt', 'w') as f:
    f.write(content)
