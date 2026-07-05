import re

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'r') as f:
    content = f.read()

old_code = """                val miniIcons = item.items.take(9).mapNotNull { manager.getIconBitmap(it) }
                holder.icon.setImageDrawable(FolderStyleDrawable(item.folderStyle, cHex, iconC, miniIcons))
            } else if (item is SidebarItem.Link) {"""

new_code = """                val miniIcons = item.items.take(9).mapNotNull { manager.getIconBitmap(it) }
                holder.icon.setImageDrawable(FolderStyleDrawable(item.folderStyle, cHex, iconC, miniIcons))
                
                if (miniIcons.size < minOf(item.items.size, 9) && item.items.any { it.startsWith("app:") }) {
                    serviceScope.launch {
                        var newlyLoaded = false
                        for (subItem in item.items.take(9)) {
                            if (subItem.startsWith("app:")) {
                                if (manager.getIconBitmap(subItem) == null) {
                                    val bitmap = manager.loadIcon(subItem.substringAfter("app:"))
                                    if (bitmap != null) {
                                        newlyLoaded = true
                                    }
                                }
                            }
                        }
                        if (newlyLoaded) {
                            withContext(Dispatchers.Main) {
                                adapter.notifyItemChanged(position)
                            }
                        }
                    }
                }
            } else if (item is SidebarItem.Link) {"""

content = content.replace(old_code, new_code)

old_code2 = """            holder.view.setOnClickListener {
                val actionList = mutableListOf("Change Icon", "Remove")
                if (item is SidebarItem.Folder) {
                    actionList.add(0, "Folder Style")
                    actionList.add(0, "Edit Contents")
                }"""

new_code2 = """            holder.view.setOnClickListener {
                val actionList = mutableListOf("Change Icon", "Remove")
                if (item is SidebarItem.Folder) {
                    actionList.add(0, "Grid Size")
                    actionList.add(0, "Folder Style")
                    actionList.add(0, "Edit Contents")
                }"""

content = content.replace(old_code2, new_code2)

old_code3 = """                            when (action) {
                                "Edit Contents" -> {
                                    showFolderEditor(context, item, manager)
                                }
                                "Folder Style" -> {
                                    showFolderStyleDialog(context, item, manager) { styleIndex, popupCols ->
                                        item.folderStyle = styleIndex
                                        item.popupColumns = popupCols
                                        adapter.notifyItemChanged(position)
                                    }
                                }"""

new_code3 = """                            when (action) {
                                "Edit Contents" -> {
                                    showFolderEditor(context, item, manager)
                                }
                                "Folder Style" -> {
                                    showFolderStyleDialog(context, item, manager) { styleIndex, popupCols ->
                                        item.folderStyle = styleIndex
                                        item.popupColumns = popupCols
                                        adapter.notifyItemChanged(position)
                                    }
                                }
                                "Grid Size" -> {
                                    showGridSizeDialog(context, item, manager) { popupCols ->
                                        item.popupColumns = popupCols
                                        adapter.notifyItemChanged(position)
                                    }
                                }"""
content = content.replace(old_code3, new_code3)

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'w') as f:
    f.write(content)
