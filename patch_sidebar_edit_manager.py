import re

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "r") as f:
    content = f.read()

target = """        manager = SidebarAppsManager(this, prefs, serviceScope) {}"""
replacement = """        manager = SidebarAppsManager(this, prefs, serviceScope) {
            runOnUiThread {
                if (::adapter.isInitialized) {
                    adapter.notifyDataSetChanged()
                }
            }
        }"""
content = content.replace(target, replacement)
with open("app/src/main/java/com/example/SidebarEditActivity.kt", "w") as f:
    f.write(content)
