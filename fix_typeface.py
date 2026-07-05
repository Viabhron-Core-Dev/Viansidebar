import re

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'r') as f:
    content = f.read()

content = content.replace("typeface = Typeface.DEFAULT_BOLD", "typeface = android.graphics.Typeface.DEFAULT_BOLD")
content = content.replace("setBackgroundColor(Color.WHITE)", "setBackgroundColor(android.graphics.Color.WHITE)")
content = content.replace("setTextColor(Color.BLACK)", "setTextColor(android.graphics.Color.BLACK)")
content = content.replace("setTextColor(Color.DKGRAY)", "setTextColor(android.graphics.Color.DKGRAY)")

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'w') as f:
    f.write(content)
