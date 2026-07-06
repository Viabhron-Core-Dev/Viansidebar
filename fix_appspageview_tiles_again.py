import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

old_click = """                    currentFolderPopup?.dismiss()
                        onCloseSidebar()
                } else if (item is SidebarItem.SystemAction) {"""
new_click = """                    currentFolderPopup?.dismiss()
                        onCloseSidebar()
                } else if (item is SidebarItem.QuickTile) {
                    QuickTileHandler.handleQuickTileAction(context, item.action)
                    currentFolderPopup?.dismiss()
                    onCloseSidebar()
                } else if (item is SidebarItem.SystemAction) {"""
content = content.replace(old_click, new_click)

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)
