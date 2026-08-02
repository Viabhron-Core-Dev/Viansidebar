with open("app/src/main/java/com/example/HandlesListSettingsScreen.kt", "r") as f:
    content = f.read()

old_add = """            FloatingActionButton(onClick = {
                val newId = UUID.randomUUID().toString()
                handles = handles + HandleConfig(id = newId, name = "Handle ${handles.size + 1}", enabled = true)
                save()
            })"""

new_add = """            FloatingActionButton(onClick = {
                val newId = UUID.randomUUID().toString()
                prefs.edit().putString("handle_${newId}_tap", "toggle_sidebar").apply()
                handles = handles + HandleConfig(id = newId, name = "Handle ${handles.size + 1}", enabled = true)
                save()
            })"""

content = content.replace(old_add, new_add)

with open("app/src/main/java/com/example/HandlesListSettingsScreen.kt", "w") as f:
    f.write(content)
