import re

with open("app/src/main/java/com/example/service/AppsPageView.kt", "r") as f:
    content = f.read()

target = """            } else if (item is SidebarItem.QuickTile) {
                icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                icon.setImageResource(item.iconResId)
                icon.setColorFilter(android.graphics.Color.WHITE)
            } else if (item is SidebarItem.SystemAction) {"""

replacement = """            } else if (item is SidebarItem.Widget) {
                val cached = manager.getIconBitmap(item.id)
                if (cached != null) {
                    icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                    icon.setImageBitmap(cached)
                }
            } else if (item is SidebarItem.QuickTile) {
                icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                icon.setImageResource(item.iconResId)
                icon.setColorFilter(android.graphics.Color.WHITE)
            } else if (item is SidebarItem.SystemAction) {"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/service/AppsPageView.kt", "w") as f:
    f.write(content)
