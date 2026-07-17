import re

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "r") as f:
    content = f.read()

target = """    fun parseId(id: String): SidebarItem? {
        if (id.startsWith("app:")) {"""

replacement = """    fun parseId(id: String): SidebarItem? {
        com.example.LogKeeper.writeLog("SidebarAppsManager", "parseId called for: $id")
        if (id.startsWith("app:")) {"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "w") as f:
    f.write(content)
