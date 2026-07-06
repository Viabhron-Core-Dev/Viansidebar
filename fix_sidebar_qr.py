import re

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

old_list = """val ALL_SCREEN_CAPTURE_ACTIONS = listOf(
    SidebarItem.SystemAction("screenshot", "Screenshot", android.R.drawable.ic_menu_camera),
    SidebarItem.SystemAction("screen_record", "Screen Record", android.R.drawable.ic_media_play)
)"""

new_list = """val ALL_SCREEN_CAPTURE_ACTIONS = listOf(
    SidebarItem.SystemAction("screenshot", "Screenshot", android.R.drawable.ic_menu_camera),
    SidebarItem.SystemAction("screen_record", "Screen Record", android.R.drawable.ic_media_play),
    SidebarItem.SystemAction("qr_scan", "Screen QR Scanner", android.R.drawable.ic_menu_search)
)"""

content = content.replace(old_list, new_list)

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'w') as f:
    f.write(content)
