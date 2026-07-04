import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

old_code = """            val params = window.attributes
            params.gravity = Gravity.TOP or Gravity.START
            if (anchorX > screenWidth / 2) {
                params.x = anchorX - totalWidth
            } else {
                params.x = anchorX + anchor.width
            }
            params.y = anchorY - (totalHeight / 2) + (anchor.height / 2)
            window.attributes = params"""

new_code = """            val params = window.attributes
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
            window.attributes = params"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)
