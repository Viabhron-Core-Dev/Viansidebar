import re

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'r') as f:
    content = f.read()

old_code = """                val actionList = mutableListOf("Change Icon", "Remove")
                if (item is SidebarItem.Folder) {
                    actionList.add(0, "Edit Contents")
                }"""

new_code = """                val actionList = mutableListOf("Change Icon", "Remove")
                if (item is SidebarItem.Folder) {
                    actionList.add(0, "Folder Style")
                    actionList.add(0, "Edit Contents")
                }"""

content = content.replace(old_code, new_code)

old_code2 = """                                "Change Icon" -> {"""

new_code2 = """                                "Folder Style" -> {
                                    if (item is SidebarItem.Folder) {
                                        showFolderStyleDialog(context, item, manager) { styleIndex ->
                                            // Handle saving style from menu
                                        }
                                    }
                                }
                                "Change Icon" -> {"""

content = content.replace(old_code2, new_code2)

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'w') as f:
    f.write(content)
