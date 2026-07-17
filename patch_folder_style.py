import re

with open("app/src/main/java/com/example/service/FolderStyleDialog.kt", "r") as f:
    content = f.read()

target = """        // Draw transparent bubble background
        paint.style = Paint.Style.FILL
        paint.color = themeColor
        paint.alpha = 100
        canvas.drawCircle(cx, cy, w / 2.2f, paint)

        val symbolSize = w * 0.75f"""

replacement = """        val symbolSize = w * 0.9f"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/FolderStyleDialog.kt", "w") as f:
    f.write(content)
