import re

with open("app/src/main/java/com/example/AddElementActivity.kt", "r") as f:
    content = f.read()

target = """                .setItems(options) { _, which ->
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
                }"""

replacement = """                .setItems(options) { _, which ->
                    val input = android.widget.EditText(this)
                    input.hint = "Folder Name"
                    input.setText("New Folder")
                    android.app.AlertDialog.Builder(this)
                        .setTitle("Folder Name")
                        .setView(input)
                        .setPositiveButton("OK") { _, _ ->
                            val folderName = input.text.toString().takeIf { it.isNotEmpty() } ?: "New Folder"
                            val uuid = java.util.UUID.randomUUID().toString()
                            val folderJson = JSONObject().apply {
                                put("name", folderName)
                                put("colorHex", "#444444")
                                put("items", org.json.JSONArray())
                                put("folderStyle", which)
                                put("popupColumns", 3)
                                put("popupRows", 3)
                            }
                            finishWithId("folder:$uuid:${folderJson.toString()}")
                        }
                        .setNegativeButton("Cancel", null)
                        .show()
                }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/AddElementActivity.kt", "w") as f:
    f.write(content)
