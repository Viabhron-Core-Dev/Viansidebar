import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

content = content.replace("private var currentFolderPopup: android.app.Dialog? = null", "private var currentFolderPopup: android.widget.PopupWindow? = null")

old_popup_code = """        val dialog = android.app.Dialog(context)
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
            
            val location = IntArray(2)
            anchor.getLocationOnScreen(location)
            val anchorX = location[0]
            val anchorY = location[1]
            val screenWidth = context.resources.displayMetrics.widthPixels
            
            val params = window.attributes
            params.gravity = Gravity.TOP or Gravity.START
            if (anchorX > screenWidth / 2) {
                params.x = anchorX - totalWidth
            } else {
                params.x = anchorX + anchor.width
            }
            
            var newY = anchorY - (totalHeight / 2) + (anchor.height / 2)
            val screenHeight = context.resources.displayMetrics.heightPixels
            if (newY < 0) newY = 0
            if (newY + totalHeight > screenHeight) newY = screenHeight - totalHeight
            
            params.y = newY
            window.attributes = params
        }
        
        currentFolderPopup = dialog
        dialog.show()"""

new_popup_code = """        val popupWindow = android.widget.PopupWindow(
            popupView,
            ViewGroup.LayoutParams.WRAP_CONTENT,
            ViewGroup.LayoutParams.WRAP_CONTENT,
            true
        ).apply {
            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                windowLayoutType = android.view.WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            } else {
                @Suppress("DEPRECATION")
                windowLayoutType = android.view.WindowManager.LayoutParams.TYPE_PHONE
            }
            setBackgroundDrawable(android.graphics.drawable.ColorDrawable(android.graphics.Color.TRANSPARENT))
            isOutsideTouchable = true
        }

        val location = IntArray(2)
        anchor.getLocationOnScreen(location)
        val anchorX = location[0]
        val anchorY = location[1]
        val screenWidth = context.resources.displayMetrics.widthPixels
        val screenHeight = context.resources.displayMetrics.heightPixels

        var x = anchorX
        if (anchorX > screenWidth / 2) {
            x = anchorX - totalWidth
        } else {
            x = anchorX + anchor.width
        }

        var y = anchorY - (totalHeight / 2) + (anchor.height / 2)
        if (y < 0) y = 0
        if (y + totalHeight > screenHeight) y = screenHeight - totalHeight

        popupWindow.showAtLocation(anchor, Gravity.NO_GRAVITY, x, y)
        currentFolderPopup = popupWindow"""

content = content.replace(old_popup_code, new_popup_code)

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)
