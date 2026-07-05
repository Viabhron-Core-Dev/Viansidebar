import re

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'r') as f:
    content = f.read()

old_code = """        if (miniIcons.isEmpty()) {
            paint.style = Paint.Style.STROKE
            paint.strokeWidth = 4f
            canvas.drawRect(x + size*0.1f, y + size*0.2f, x + size*0.9f, y + size*0.8f, paint)
            canvas.drawLine(x + size*0.1f, y + size*0.4f, x + size*0.9f, y + size*0.4f, paint)
            return
        }"""

new_code = """        if (miniIcons.isEmpty()) {
            // User requested no default box, so draw nothing or leave it empty
            return
        }"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'w') as f:
    f.write(content)
