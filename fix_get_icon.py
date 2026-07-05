import re

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

old_res_id = """            is SidebarItem.SystemAction -> parsed.iconResId"""
new_res_id = """            is SidebarItem.SystemAction -> parsed.iconResId
            is SidebarItem.QuickTile -> parsed.iconResId"""
content = content.replace(old_res_id, new_res_id)

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)
