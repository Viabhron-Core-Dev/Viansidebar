import re

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'r') as f:
    content = f.read()

old_drawStack = """    private fun drawStack(canvas: Canvas, x: Float, y: Float, size: Float) {
        if (miniIcons.isEmpty()) {
            return
        }
        val count = minOf(3, miniIcons.size)
        val cardSize = size * 0.85f
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

new_drawStack = """    private fun drawStack(canvas: Canvas, x: Float, y: Float, size: Float) {
        if (miniIcons.isEmpty()) {
            return
        }
        val count = minOf(2, miniIcons.size)
        if (count == 1) {
            val p = size * 0.05f
            val ix = x + p
            val iy = y + p
            val isize = size - 2 * p
            canvas.drawBitmap(miniIcons[0], null, RectF(ix, iy, ix + isize, iy + isize), iconPaint)
        } else {
            val cardSize = size * 0.85f
            val gapX = size - cardSize
            val gapY = size - cardSize
            
            // back icon (index 1) at top-right
            canvas.drawBitmap(miniIcons[1], null, RectF(x + gapX, y, x + gapX + cardSize, y + cardSize), iconPaint)
            // front icon (index 0) at bottom-left
            canvas.drawBitmap(miniIcons[0], null, RectF(x, y + gapY, x + cardSize, y + gapY + cardSize), iconPaint)
        }
    }"""

content = content.replace(old_drawStack, new_drawStack)

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'w') as f:
    f.write(content)
