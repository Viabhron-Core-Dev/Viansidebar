import re
with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

old_dialog = """        val dialog = android.app.AlertDialog.Builder(context, android.R.style.Theme_DeviceDefault_Light_Dialog_Alert)
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
        dialog.show()"""

new_dialog = """        val dialog = android.app.AlertDialog.Builder(context, android.R.style.Theme_DeviceDefault_Light_Dialog_Alert)
            .setView(popupView)
            .create()
        
        dialog.window?.let { window ->
            val layoutType = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                android.view.WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            } else {
                @Suppress("DEPRECATION")
                android.view.WindowManager.LayoutParams.TYPE_PHONE
            }
            window.setType(layoutType)
            window.setBackgroundDrawable(android.graphics.drawable.ColorDrawable(android.graphics.Color.TRANSPARENT))
            window.clearFlags(android.view.WindowManager.LayoutParams.FLAG_DIM_BEHIND)
            
            val loc = IntArray(2)
            anchor.getLocationOnScreen(loc)
            
            val params = window.attributes
            params.gravity = android.view.Gravity.TOP or android.view.Gravity.START
            
            // Adjust x so it doesn't go off screen on the right
            val screenWidth = context.resources.displayMetrics.widthPixels
            val estimatedWidth = (64 * density * validCols) + (padding * 2)
            
            var posX = loc[0] - (estimatedWidth / 2).toInt() + (anchor.width / 2)
            if (posX + estimatedWidth > screenWidth) posX = screenWidth - estimatedWidth.toInt()
            if (posX < 0) posX = 0
            
            params.x = posX
            params.y = loc[1] + anchor.height // Show below anchor
            
            // If it goes off the bottom, show above
            val screenHeight = context.resources.displayMetrics.heightPixels
            val estimatedRows = Math.ceil(folderItems.size.toDouble() / validCols).toInt()
            val estimatedHeight = (80 * density * estimatedRows) + (padding * 2)
            
            if (params.y + estimatedHeight > screenHeight) {
                params.y = loc[1] - estimatedHeight.toInt()
            }
            
            window.attributes = params
        }
        
        currentFolderPopup = dialog
        dialog.show()"""

content = content.replace(old_dialog, new_dialog)

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)
