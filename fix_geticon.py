import re

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

old_code = """    fun getIconBitmap(id: String): Bitmap? {
        val parsed = parseId(id) ?: return null
        if (parsed is SidebarItem.App) {
            return iconCache.get(parsed.packageName)
        }"""

new_code = """    fun getIconBitmap(id: String): Bitmap? {
        if (id.startsWith("app:")) {
            val pkg = id.substringAfter("app:")
            iconCache.get(pkg)?.let { return it }
        } else if (id.startsWith("intent:")) {
            val pkg = id.substringAfter("intent:").split("/").getOrNull(0) ?: ""
            iconCache.get(pkg)?.let { return it }
        }
        val parsed = parseId(id) ?: return null
        if (parsed is SidebarItem.App) {
            return iconCache.get(parsed.packageName)
        }"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)
