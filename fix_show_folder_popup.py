import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

# Change type of currentFolderPopup
content = content.replace('private var currentFolderPopup: android.widget.PopupWindow? = null', 
                          'private var currentFolderPopup: android.app.Dialog? = null')

show_popup_old = """    private fun showFolderPopup(anchor: View, folder: SidebarItem.Folder) {
        currentFolderPopup?.dismiss()
        
        val density = context.resources.displayMetrics.density
        val popupView = FrameLayout(context)
        val recyclerView = RecyclerView(context)
        val padding = (8 * density).toInt()
        recyclerView.setPadding(padding, padding, padding, padding)
        popupView.addView(recyclerView, FrameLayout.LayoutParams(FrameLayout.LayoutParams.WRAP_CONTENT, FrameLayout.LayoutParams.WRAP_CONTENT))
        
        val folderItems = mutableListOf<SidebarItem>()
        for (itemId in folder.items) {
            val parsedItem = manager.parseId(itemId)
            if (parsedItem != null) {
                folderItems.add(parsedItem)
            }
        }
        
        val maxCols = prefs.getInt("sidebar_columns", 4)
        val columns = if (folderItems.size <= maxCols && folderItems.isNotEmpty()) folderItems.size else maxCols
        val validCols = if (columns > 0) columns else 1
        
        recyclerView.layoutManager = GridLayoutManager(context, validCols)
        val popupAdapter = AppsAdapter(folderItems)
        recyclerView.adapter = popupAdapter
        
        val popupOpacity = prefs.getFloat("sidebar_transparency", 0.9f)
        val popupBg = android.graphics.drawable.GradientDrawable()
        val cHex = try { android.graphics.Color.parseColor(folder.colorHex) } catch(e:Exception){ android.graphics.Color.parseColor("#333333") }
        // Use folder color or sidebar color? User said "same color and transparency as sidebar". 
        // We'll use dark gray which is default sidebar color, or #1A1A1A
        popupBg.setColor(android.graphics.Color.parseColor("#1A1A1A"))
        popupBg.alpha = (popupOpacity * 255).toInt()
        popupBg.cornerRadius = 16 * density
        popupView.background = popupBg
        
        val popupWindow = android.widget.PopupWindow(popupView, 
            ViewGroup.LayoutParams.WRAP_CONTENT, 
            ViewGroup.LayoutParams.WRAP_CONTENT, 
            true)
            
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.LOLLIPOP) {
            popupWindow.elevation = 10f * density
        }
        popupWindow.setBackgroundDrawable(android.graphics.drawable.ColorDrawable(android.graphics.Color.TRANSPARENT))
        
        currentFolderPopup = popupWindow
        
        popupWindow.showAsDropDown(anchor)
    }"""

show_popup_new = """    private fun showFolderPopup(anchor: View, folder: SidebarItem.Folder) {
        currentFolderPopup?.dismiss()
        
        com.example.LogKeeper.writeLog("Sidebar", "Folder opened: ${folder.label}")
        
        val density = context.resources.displayMetrics.density
        val popupView = FrameLayout(context)
        val recyclerView = RecyclerView(context)
        val padding = (16 * density).toInt()
        recyclerView.setPadding(padding, padding, padding, padding)
        popupView.addView(recyclerView, FrameLayout.LayoutParams(FrameLayout.LayoutParams.WRAP_CONTENT, FrameLayout.LayoutParams.WRAP_CONTENT))
        
        val folderItems = mutableListOf<SidebarItem>()
        for (itemId in folder.items) {
            val parsedItem = manager.parseId(itemId)
            if (parsedItem != null) {
                folderItems.add(parsedItem)
            }
        }
        
        val maxCols = prefs.getInt("sidebar_columns", 4)
        val columns = if (folderItems.size <= maxCols && folderItems.isNotEmpty()) folderItems.size else maxCols
        val validCols = if (columns > 0) columns else 1
        
        recyclerView.layoutManager = GridLayoutManager(context, validCols)
        val popupAdapter = AppsAdapter(folderItems)
        recyclerView.adapter = popupAdapter
        
        val popupOpacity = prefs.getFloat("sidebar_transparency", 0.9f)
        val popupBg = android.graphics.drawable.GradientDrawable()
        popupBg.setColor(android.graphics.Color.parseColor("#1A1A1A"))
        popupBg.alpha = (popupOpacity * 255).toInt()
        popupBg.cornerRadius = 16 * density
        popupView.background = popupBg
        
        val dialog = android.app.AlertDialog.Builder(context, android.R.style.Theme_DeviceDefault_Light_Dialog_Alert)
            .setView(popupView)
            .create()
            
        dialog.window?.let { window ->
            val layoutType = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                android.view.WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            } else {
                android.view.WindowManager.LayoutParams.TYPE_PHONE
            }
            window.setType(layoutType)
            window.setBackgroundDrawable(android.graphics.drawable.ColorDrawable(android.graphics.Color.TRANSPARENT))
            window.setDimAmount(0.3f)
        }
        
        currentFolderPopup = dialog
        dialog.show()
    }"""

content = content.replace(show_popup_old, show_popup_new)

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)

print("Updated popup")
