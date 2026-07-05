import re

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

# Fix parseId
bad_code1 = """        } else if (id.startsWith("system:")) {
            val action = id.substringAfter("system:")
            val qTile = ALL_QUICK_TILES.find { it.action == action }
            if (qTile != null) {
                return getDrawableBitmap(context.resources.getDrawable(qTile.iconResId, context.theme))
            }
            val sysAction = ALL_SYSTEM_ACTIONS.find { it.action == action }
            if (sysAction != null) {
                return SidebarItem.SystemAction(action, sysAction.label, sysAction.iconResId)
            }
        }"""
good_code1 = """        } else if (id.startsWith("quicktile:")) {
            val action = id.substringAfter("quicktile:")
            val qTile = ALL_QUICK_TILES.find { it.action == action }
            if (qTile != null) {
                return SidebarItem.QuickTile(action, qTile.label, qTile.iconResId)
            }
        } else if (id.startsWith("system:")) {
            val action = id.substringAfter("system:")
            val sysAction = ALL_SYSTEM_ACTIONS.find { it.action == action }
            if (sysAction != null) {
                return SidebarItem.SystemAction(action, sysAction.label, sysAction.iconResId)
            }
        }"""
content = content.replace(bad_code1, good_code1)

# Fix getSidebarItems
bad_code2 = """            } else if (id.startsWith("system:")) {
                val action = id.substringAfter("system:")
                val qTile = ALL_QUICK_TILES.find { it.action == action }
            if (qTile != null) {
                return getDrawableBitmap(context.resources.getDrawable(qTile.iconResId, context.theme))
            }
            val sysAction = ALL_SYSTEM_ACTIONS.find { it.action == action }
                if (sysAction != null) {
                    result.add(SidebarItem.SystemAction(action, sysAction.label, sysAction.iconResId))
                }
            }"""
good_code2 = """            } else if (id.startsWith("quicktile:")) {
                val action = id.substringAfter("quicktile:")
                val qTile = ALL_QUICK_TILES.find { it.action == action }
                if (qTile != null) {
                    result.add(SidebarItem.QuickTile(action, qTile.label, qTile.iconResId))
                }
            } else if (id.startsWith("system:")) {
                val action = id.substringAfter("system:")
                val sysAction = ALL_SYSTEM_ACTIONS.find { it.action == action }
                if (sysAction != null) {
                    result.add(SidebarItem.SystemAction(action, sysAction.label, sysAction.iconResId))
                }
            }"""
content = content.replace(bad_code2, good_code2)

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)
