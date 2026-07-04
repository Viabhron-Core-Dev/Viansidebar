import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

old_code = """        val maxCols = prefs.getInt("sidebar_columns", 4)
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
        }"""

new_code = """        val maxCols = prefs.getInt("sidebar_columns", 4)
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
        
        // Calculate exact size for compact wrap_content appearance
        val itemWidthDp = 56 // 44dp icon + 6dp padding on each side
        val itemHeightDp = 56
        val rows = Math.ceil(folderItems.size.toDouble() / validCols).toInt()
        val totalWidth = (validCols * itemWidthDp * density + padding * 2).toInt()
        val totalHeight = (rows * itemHeightDp * density + padding * 2).toInt()
        
        popupView.layoutParams = ViewGroup.LayoutParams(totalWidth, totalHeight)
        
        val dialog = android.app.Dialog(context)
        dialog.requestWindowFeature(android.view.Window.FEATURE_NO_TITLE)
        dialog.setContentView(popupView)
            
        dialog.window?.let { window ->
            val layoutType = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                android.view.WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            } else {
                android.view.WindowManager.LayoutParams.TYPE_PHONE
            }
            window.setType(layoutType)
            window.setBackgroundDrawable(android.graphics.drawable.ColorDrawable(android.graphics.Color.TRANSPARENT))
            window.setLayout(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT)
            window.setDimAmount(0.3f)
        }"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)
