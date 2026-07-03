import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

# Replace the entire function using regex
pattern = r'    private fun showFolderPopup\(anchor: View, folder: SidebarItem\.Folder\) \{.*?(?=    private inner class AppsAdapter)'

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
    }

"""

content = re.sub(pattern, show_popup_new, content, flags=re.DOTALL)

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)

print("Updated popup")
