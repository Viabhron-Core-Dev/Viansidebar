import re

with open("app/src/main/java/com/example/service/FolderStyleDialog.kt", "r") as f:
    content = f.read()

target = """        } else {
            val maxCount = minOf(4, count)"""

replacement = """        } else if (count == 3) {
            val padding = size * 0.015f
            val iconSize = (size - padding * 3) / 2f
            
            // Top center
            val startY = y + padding
            val topX = x + (size - iconSize) / 2f
            canvas.drawBitmap(miniIcons[0], null, RectF(topX, startY, topX + iconSize, startY + iconSize), iconPaint)
            
            // Bottom left and right
            val bottomY = y + padding * 2 + iconSize
            val bottomLeftX = x + padding
            val bottomRightX = x + padding * 2 + iconSize
            canvas.drawBitmap(miniIcons[1], null, RectF(bottomLeftX, bottomY, bottomLeftX + iconSize, bottomY + iconSize), iconPaint)
            canvas.drawBitmap(miniIcons[2], null, RectF(bottomRightX, bottomY, bottomRightX + iconSize, bottomY + iconSize), iconPaint)
        } else {
            val maxCount = minOf(4, count)"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/FolderStyleDialog.kt", "w") as f:
    f.write(content)
