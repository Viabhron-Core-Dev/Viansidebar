import re

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

# Fix cache
old_cache = """    val iconCache = object : LruCache<String, Bitmap>(80) {
        override fun sizeOf(key: String, value: Bitmap): Int {
            return value.byteCount / 1024
        }
    }"""
new_cache = """    val iconCache = LruCache<String, Bitmap>(100) // 100 items"""
content = content.replace(old_cache, new_cache)

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)
