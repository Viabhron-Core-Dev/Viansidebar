import re

with open("app/src/main/java/com/example/utils/PageManager.kt", "r") as f:
    content = f.read()

content = content.replace("fun getPages(prefs: SharedPreferences): List<SidebarPage> {", "fun getPages(prefs: SharedPreferences, handleId: String): List<SidebarPage> {")
content = content.replace('val pagesJson = prefs.getString("sidebar_pages", null)', 'val pagesJson = prefs.getString("handle_${handleId}_pages", prefs.getString("sidebar_pages", null))')

content = content.replace("fun savePages(prefs: SharedPreferences, pages: List<SidebarPage>) {", "fun savePages(prefs: SharedPreferences, handleId: String, pages: List<SidebarPage>) {")
content = content.replace('prefs.edit().putString("sidebar_pages", arr.toString()).apply()', 'prefs.edit().putString("handle_${handleId}_pages", arr.toString()).apply()')

with open("app/src/main/java/com/example/utils/PageManager.kt", "w") as f:
    f.write(content)
