import os
import re

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "r") as f:
    content = f.read()

# Append methods before the last closing brace
methods = '''
    private fun showFolderPopup(anchor: View, folder: SidebarItem.Folder) {
        val density = context.resources.displayMetrics.density
        val popupView = FrameLayout(context)
        val recyclerView = RecyclerView(context)
        val padding = (16 * density).toInt()
        recyclerView.setPadding(padding, padding, padding, padding)
        popupView.addView(recyclerView, FrameLayout.LayoutParams(FrameLayout.LayoutParams.WRAP_CONTENT, FrameLayout.LayoutParams.WRAP_CONTENT))
        
        val folderItems = mutableListOf<SidebarItem>()
        for (itemId in folder.items) {
            val parsedItem = appsManager.parseId(itemId)
            if (parsedItem != null) {
                folderItems.add(parsedItem)
            }
        }
        
        val maxCols = if (folder.popupColumns > 0) folder.popupColumns else prefs.getInt("sidebar_columns", 3)
        val columns = if (folderItems.size <= maxCols && folderItems.isNotEmpty()) folderItems.size else maxCols
        val validCols = if (columns > 0) columns else 1
        
        recyclerView.layoutManager = GridLayoutManager(context, validCols)
        // We don't have AppsAdapter accessible easily here if it's private or not accessible, 
        // Wait, is AppsAdapter accessible? Let's check. 
'''
