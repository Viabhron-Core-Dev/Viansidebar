import re

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'r') as f:
    content = f.read()

old_if = """            } else if (item is SidebarItem.SystemAction || item is SidebarItem.VolumeAction || item is SidebarItem.MediaAction || item is SidebarItem.DisplayAction || item is SidebarItem.SettingsShortcut) {
                val resId = when (item) {
                    is SidebarItem.SystemAction -> item.iconResId
                    is SidebarItem.VolumeAction -> item.iconResId
                    is SidebarItem.MediaAction -> item.iconResId
                    is SidebarItem.SettingsShortcut -> item.iconResId
                    is SidebarItem.DisplayAction -> item.iconResId
                    else -> 0
                }"""

new_if = """            } else if (item is SidebarItem.SystemAction || item is SidebarItem.VolumeAction || item is SidebarItem.MediaAction || item is SidebarItem.DisplayAction || item is SidebarItem.SettingsShortcut || item is SidebarItem.QuickTile) {
                val resId = when (item) {
                    is SidebarItem.SystemAction -> item.iconResId
                    is SidebarItem.VolumeAction -> item.iconResId
                    is SidebarItem.MediaAction -> item.iconResId
                    is SidebarItem.SettingsShortcut -> item.iconResId
                    is SidebarItem.DisplayAction -> item.iconResId
                    is SidebarItem.QuickTile -> item.iconResId
                    else -> 0
                }"""
content = content.replace(old_if, new_if)

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'w') as f:
    f.write(content)
