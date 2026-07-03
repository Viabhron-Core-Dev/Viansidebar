import re

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

get_icon_bitmap_code = """
    fun getIconBitmap(id: String): Bitmap? {
        val parsed = parseId(id) ?: return null
        if (parsed is SidebarItem.App) {
            return iconCache.get(parsed.packageName)
        }
        val resId = when (parsed) {
            is SidebarItem.SystemAction -> parsed.iconResId
            is SidebarItem.VolumeAction -> parsed.iconResId
            is SidebarItem.MediaAction -> parsed.iconResId
            is SidebarItem.DisplayAction -> parsed.iconResId
            is SidebarItem.SettingsShortcut -> parsed.iconResId
            is SidebarItem.Link -> android.R.drawable.ic_menu_set_as
            else -> 0
        }
        if (resId != 0) {
            val drawable = androidx.core.content.ContextCompat.getDrawable(context, resId)
            if (drawable != null) {
                // Check if we need to tint it white for the folder preview
                drawable.mutate().setColorFilter(android.graphics.Color.WHITE, android.graphics.PorterDuff.Mode.SRC_IN)
                return getBitmapFromDrawable(drawable)
            }
        }
        return null
    }
"""

if 'fun getIconBitmap' not in content:
    content = content.replace('fun parseId(id: String): SidebarItem? {', get_icon_bitmap_code + '\n    fun parseId(id: String): SidebarItem? {')

# Fix getBitmapFromDrawable to handle VectorDrawable correctly
get_bitmap_old = """    private fun getBitmapFromDrawable(drawable: Drawable): Bitmap? {
        if (drawable is BitmapDrawable) {
            return drawable.bitmap
        }
        try {
            val bitmap = Bitmap.createBitmap(drawable.intrinsicWidth.coerceAtLeast(1), drawable.intrinsicHeight.coerceAtLeast(1), Bitmap.Config.ARGB_8888)
            val canvas = Canvas(bitmap)
            drawable.setBounds(0, 0, canvas.width, canvas.height)
            drawable.draw(canvas)
            return bitmap
        } catch (e: Exception) {
            return null
        }
    }"""

get_bitmap_new = """    fun getBitmapFromDrawable(drawable: Drawable): Bitmap? {
        if (drawable is BitmapDrawable) {
            return drawable.bitmap
        }
        try {
            val width = if (drawable.intrinsicWidth > 0) drawable.intrinsicWidth else 100
            val height = if (drawable.intrinsicHeight > 0) drawable.intrinsicHeight else 100
            val bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888)
            val canvas = Canvas(bitmap)
            drawable.setBounds(0, 0, canvas.width, canvas.height)
            drawable.draw(canvas)
            return bitmap
        } catch (e: Exception) {
            return null
        }
    }"""

content = content.replace(get_bitmap_old, get_bitmap_new)
content = content.replace('private fun getBitmapFromDrawable', 'fun getBitmapFromDrawable')

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)

def replace_in_file(filename):
    with open(filename, 'r') as f:
        c = f.read()
    
    old_mini = """val miniIcons = item.items.mapNotNull { 
                    if (it.startsWith("app:")) manager.iconCache.get(it.substringAfter("app:")) else null 
                }"""
    
    new_mini = """val miniIcons = item.items.take(9).mapNotNull { manager.getIconBitmap(it) }"""
    
    c = c.replace(old_mini, new_mini)
    
    old_cond = """if (miniIcons.isEmpty() && item.items.any { it.startsWith("app:") }) {"""
    new_cond = """if (miniIcons.size < minOf(item.items.size, 9) && item.items.any { it.startsWith("app:") }) {"""
    
    c = c.replace(old_cond, new_cond)
    
    with open(filename, 'w') as f:
        f.write(c)

replace_in_file('app/src/main/java/com/example/service/AppsPageView.kt')
replace_in_file('app/src/main/java/com/example/service/SidebarEditOverlayView.kt')

# Also for FolderStyleDialog.kt
with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'r') as f:
    c = f.read()
    old_mini2 = """val miniIcons = item.items.mapNotNull { 
            if (it.startsWith("app:")) manager.iconCache.get(it.substringAfter("app:")) else null 
        }"""
    new_mini2 = """val miniIcons = item.items.take(9).mapNotNull { manager.getIconBitmap(it) }"""
    c = c.replace(old_mini2, new_mini2)
    with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'w') as f:
        f.write(c)

print("Fixed folder icons.")
