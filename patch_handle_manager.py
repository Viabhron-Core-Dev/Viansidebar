with open("app/src/main/java/com/example/HandleManager.kt", "r") as f:
    content = f.read()

old_loop = """            for (i in 0 until arr.length()) {
                val obj = arr.getJSONObject(i)
                list.add(HandleConfig(
                    id = obj.optString("id"),
                    name = obj.optString("name", "Handle"),
                    enabled = obj.optBoolean("enabled", true)
                ))
            }"""

new_loop = """            for (i in 0 until arr.length()) {
                val obj = arr.getJSONObject(i)
                val id = obj.optString("id")
                if (!prefs.contains("handle_${id}_tap")) {
                    prefs.edit().putString("handle_${id}_tap", "toggle_sidebar").apply()
                }
                list.add(HandleConfig(
                    id = id,
                    name = obj.optString("name", "Handle"),
                    enabled = obj.optBoolean("enabled", true)
                ))
            }"""

content = content.replace(old_loop, new_loop)

with open("app/src/main/java/com/example/HandleManager.kt", "w") as f:
    f.write(content)
