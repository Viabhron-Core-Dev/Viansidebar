import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

bad_pattern = r'\} else if \(item is SidebarItem\.Folder\) \{\s*showFolderPopup\(itemView, item\)\s*\} else if \(item is SidebarItem\.Link\) \{'

# Ensure we only replace the SECOND match (the one in the bind method).
# Let's just find all matches.
parts = re.split(bad_pattern, content)
if len(parts) == 3: # meaning 2 matches found
    good_replacement = """} else if (item is SidebarItem.Folder) {
                icon.setImageDrawable(null)
                icon.clearColorFilter()
                icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                
                val cHex = try { android.graphics.Color.parseColor(item.colorHex) } catch(e:Exception){ android.graphics.Color.parseColor("#00BFA5") }
                val iconC = android.graphics.Color.WHITE
                
                val miniIcons = item.items.mapNotNull { 
                    if (it.startsWith("app:")) manager.iconCache.get(it.substringAfter("app:")) else null 
                }
                icon.setImageDrawable(FolderStyleDrawable(item.folderStyle, cHex, iconC, miniIcons))
                
                if (miniIcons.isEmpty() && item.items.any { it.startsWith("app:") }) {
                    serviceScope.launch {
                        var loadedAny = false
                        for (it in item.items.take(4)) {
                            if (it.startsWith("app:")) {
                                val bitmap = manager.loadIcon(it.substringAfter("app:"))
                                if (bitmap != null) {
                                    loadedAny = true
                                }
                            }
                        }
                        if (loadedAny) {
                            withContext(Dispatchers.Main) {
                                adapter.notifyItemChanged(position)
                            }
                        }
                    }
                }
            } else if (item is SidebarItem.Link) {"""
    
    # We keep the first match exactly as it was:
    first_match_replacement = """} else if (item is SidebarItem.Folder) {
                    showFolderPopup(itemView, item)
                } else if (item is SidebarItem.Link) {"""
                
    content = parts[0] + first_match_replacement + parts[1] + good_replacement + parts[2]
    
    with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
        f.write(content)
    print("Fixed.")
else:
    print("Found", len(parts) - 1, "matches instead of 2")

