import re

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'r') as f:
    content = f.read()

# Remove the background circle
old_code = """        paint.style = Paint.Style.FILL
        paint.color = themeColor
        paint.alpha = 100
        canvas.drawCircle(cx, cy, w / 2f, paint)"""

new_code = """        // No background circle as per user request"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'w') as f:
    f.write(content)
