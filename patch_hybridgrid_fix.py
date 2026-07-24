import os
import re

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "r") as f:
    content = f.read()

# Fix SidebarItem references
content = content.replace("com.example.service.SidebarAppsManager.SidebarItem", "com.example.service.SidebarItem")

# Add appsManager argument to showFolderPopup
content = content.replace("private fun showFolderPopup(anchor: View, folder: com.example.service.SidebarItem.Folder) {", "private fun showFolderPopup(anchor: View, folder: com.example.service.SidebarItem.Folder, appsManager: SidebarAppsManager) {")

# Update showFolderPopup call
content = content.replace("showFolderPopup(elementView, parsed)", "showFolderPopup(elementView, parsed, appsManager)")

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "w") as f:
    f.write(content)
