import re

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'r') as f:
    content = f.read()

old_stack = """    private fun drawStack(canvas: Canvas, x: Float, y: Float, size: Float) {
        if (miniIcons.isEmpty()) {
            return
        }
        val count = minOf(3, miniIcons.size)
        val cardSize = size * 0.75f
        val gapX = if (count > 1) (size - cardSize) / (count - 1) else 0f
        val gapY = if (count > 1) (size - cardSize) / (count - 1) else 0f
        
        for (i in count - 1 downTo 0) {
            // i=0 (front) drawn last at bottom-left
            // i=2 (back) drawn first at top-right
            val tx = x + (count - 1 - i) * gapX
            val ty = y + i * gapY
            canvas.drawBitmap(miniIcons[i], null, RectF(tx, ty, tx + cardSize, ty + cardSize), iconPaint)
        }
    }"""
new_stack = """    private fun drawStack(canvas: Canvas, x: Float, y: Float, size: Float) {
        if (miniIcons.isEmpty()) {
            return
        }
        val count = minOf(3, miniIcons.size)
        val cardSize = size * 0.75f
        val gapX = if (count > 1) (size - cardSize) / (count - 1) else 0f
        val gapY = if (count > 1) (size - cardSize) / (count - 1) else 0f
        
        for (i in count - 1 downTo 0) {
            // i=2 (back) drawn first at top-left
            // i=0 (front) drawn last at bottom-right
            val tx = x + (count - 1 - i) * gapX
            val ty = y + (count - 1 - i) * gapY
            canvas.drawBitmap(miniIcons[i], null, RectF(tx, ty, tx + cardSize, ty + cardSize), iconPaint)
        }
    }"""
content = content.replace(old_stack, new_stack)

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'w') as f:
    f.write(content)
