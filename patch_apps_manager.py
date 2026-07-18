import re

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "r") as f:
    content = f.read()

target = """    SidebarItem.SystemAction("qr_scan", "Screen QR Scanner", android.R.drawable.ic_menu_search)"""

replacement = """    SidebarItem.SystemAction("qr_scan", "Screen Crop / QR", android.R.drawable.ic_menu_search)"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "w") as f:
    f.write(content)
