import re

with open("app/src/main/java/com/example/AddElementActivity.kt", "r") as f:
    content = f.read()

target = """        addItem(android.R.drawable.ic_menu_more, "Folder") {
            val uuid = java.util.UUID.randomUUID().toString()
            val folderJson = JSONObject().apply {
                put("name", "New Folder")
                put("colorHex", "#333333")
                put("items", org.json.JSONArray())
                put("folderStyle", 0)
                put("popupColumns", 3)
                put("popupRows", 3)
            }
            finishWithId("folder:$uuid:${folderJson.toString()}")
        }"""

replacement = """        addItem(android.R.drawable.ic_menu_more, "Folder") {
            val options = arrayOf("Grid", "Stack")
            android.app.AlertDialog.Builder(this)
                .setTitle("Folder style")
                .setItems(options) { _, which ->
                    val uuid = java.util.UUID.randomUUID().toString()
                    val folderJson = JSONObject().apply {
                        put("name", "New Folder")
                        put("colorHex", "#444444")
                        put("items", org.json.JSONArray())
                        put("folderStyle", which)
                        put("popupColumns", 3)
                        put("popupRows", 3)
                    }
                    finishWithId("folder:$uuid:${folderJson.toString()}")
                }
                .show()
        }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/AddElementActivity.kt", "w") as f:
    f.write(content)
