import re

with open('app/src/main/java/com/example/SidebarSettingsScreen.kt', 'r') as f:
    content = f.read()

old_save = """            onSave = { updated ->
                val newPages = PageManager.getPages(prefs).toMutableList()
                val idx = newPages.indexOfFirst { it.id == updated.id }
                if (idx != -1) {
                    newPages[idx] = updated
                    PageManager.savePages(prefs, newPages)
                }
            },"""
new_save = """            onSave = { updated ->
                val newPages = PageManager.getPages(prefs).toMutableList()
                val idx = newPages.indexOfFirst { it.id == updated.id }
                if (idx != -1) {
                    newPages[idx] = updated
                    PageManager.savePages(prefs, newPages)
                    pages = newPages
                }
            },"""
content = content.replace(old_save, new_save)

with open('app/src/main/java/com/example/SidebarSettingsScreen.kt', 'w') as f:
    f.write(content)
