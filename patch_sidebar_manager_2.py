import re

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "r") as f:
    content = f.read()

target = """        val result = mutableListOf<SidebarItem>()
        for (id in selectedIds) {
            val parsed = parseId(id)
            if (parsed != null) {
                result.add(parsed)
                continue
            }
            if (id.startsWith("app:")) {"""

# Find the end of the loop, which is around line 620 or so. Let's find it.
