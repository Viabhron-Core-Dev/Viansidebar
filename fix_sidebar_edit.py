import re
with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'r') as f:
    content = f.read()

new_save = """    fun saveCurrentState() {
        val jArr = JSONArray()
        localIds.forEach { jArr.put(it) }
        prefs.edit().putString("sidebar_apps", jArr.toString()).apply()
        manager.reloadActiveApps()
    }

    private fun saveAndClose() {"""

content = content.replace("    private fun saveAndClose() {", new_save)

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'w') as f:
    f.write(content)
