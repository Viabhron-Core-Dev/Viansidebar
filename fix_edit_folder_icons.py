import re

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'r') as f:
    content = f.read()

old_code = """                val miniIcons = item.items.mapNotNull { 
                    if (it.startsWith("app:")) manager.iconCache.get(it.substringAfter("app:")) else null 
                }
                holder.icon.setImageDrawable(FolderStyleDrawable(item.folderStyle, cHex, iconC, miniIcons))"""

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
                                notifyItemChanged(position)
                            }
                        }
                    }
                }"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'w') as f:
    f.write(content)
