import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

old_code = """        dialog.window?.let { window ->
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

new_code = """        dialog.window?.let { window ->
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
            params.y = anchorY - (totalHeight / 2) + (anchor.height / 2)
            window.attributes = params
        }"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)
