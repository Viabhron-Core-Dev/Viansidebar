import os
import re

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "r") as f:
    content = f.read()

# Fix the mess with SidebarItem
content = re.sub(r'com\.example\.service\.[a-zA-Z0-9_.]*SidebarItem', 'SidebarItem', content)
content = content.replace('is SidebarItem.PopupWidget', 'is SidebarItem.PopupWidget')
content = content.replace('is SidebarItem.App', 'is SidebarItem.App')
content = content.replace('is SidebarItem.Folder', 'is SidebarItem.Folder')
content = content.replace('is SidebarItem.Link', 'is SidebarItem.Link')
content = content.replace('folder: SidebarItem.Folder, appsManager: SidebarAppsManager', 'folder: SidebarItem.Folder, appsManager: SidebarAppsManager')

# And I need to add import for ViewGroup if it is missing
if 'import android.view.ViewGroup' not in content:
    content = content.replace('import android.view.View', 'import android.view.View\nimport android.view.ViewGroup')

# Also the method signature for showFolderPopup in the patch_hybridgrid_fix didn't match the new appsManager correctly or maybe it did? Let's fix it explicitly:
content = re.sub(r'private fun showFolderPopup\(anchor: View, folder: SidebarItem\.Folder\)', 
                 'private fun showFolderPopup(anchor: View, folder: SidebarItem.Folder, appsManager: SidebarAppsManager)', content)

# And inside showWidgetPopup signature:
content = re.sub(r'private fun showWidgetPopup\(anchor: View, widget: SidebarItem\.PopupWidget\)', 
                 'private fun showWidgetPopup(anchor: View, widget: SidebarItem.PopupWidget)', content)


with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "w") as f:
    f.write(content)
