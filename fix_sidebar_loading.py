import re

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

old_get1 = """        } else if (id.startsWith("system:")) {
            val action = id.substringAfter("system:")
            val sysAction = ALL_SYSTEM_ACTIONS.find { it.action == action }
            if (sysAction != null) {
                return SidebarItem.SystemAction(action, sysAction.label, sysAction.iconResId)
            }
        }"""

new_get1 = """        } else if (id.startsWith("system:")) {
            val action = id.substringAfter("system:")
            val sysAction = ALL_SYSTEM_ACTIONS.find { it.action == action } ?: ALL_SCREEN_CAPTURE_ACTIONS.find { it.action == action }
            if (sysAction != null) {
                return SidebarItem.SystemAction(action, sysAction.label, sysAction.iconResId)
            }
        }"""
content = content.replace(old_get1, new_get1)

old_get2 = """            } else if (id.startsWith("system:")) {
                val action = id.substringAfter("system:")
                val sysAction = ALL_SYSTEM_ACTIONS.find { it.action == action }
                if (sysAction != null) {
                    result.add(SidebarItem.SystemAction(action, sysAction.label, sysAction.iconResId))
                }
            }"""

new_get2 = """            } else if (id.startsWith("system:")) {
                val action = id.substringAfter("system:")
                val sysAction = ALL_SYSTEM_ACTIONS.find { it.action == action } ?: ALL_SCREEN_CAPTURE_ACTIONS.find { it.action == action }
                if (sysAction != null) {
                    result.add(SidebarItem.SystemAction(action, sysAction.label, sysAction.iconResId))
                }
            }"""
content = content.replace(old_get2, new_get2)

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)
