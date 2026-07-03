import re

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'r') as f:
    content = f.read()

replacement_grid = """
    private fun drawGrid(canvas: Canvas, x: Float, y: Float, size: Float) {
        if (miniIcons.isEmpty()) return
        val count = minOf(4, miniIcons.size)
        val padding = size * 0.05f
        
        if (count == 1) {
            // Full size
            val p = size * 0.1f
            val ix = x + p
            val iy = y + p
            val isize = size - 2*p
            canvas.drawBitmap(miniIcons[0], null, RectF(ix, iy, ix + isize, iy + isize), iconPaint)
        } else if (count == 2) {
            // Side by side
            val iconSize = (size - padding * 3) / 2f
            val startY = y + (size - iconSize) / 2f
            for (i in 0 until 2) {
                val ix = x + padding + i * (iconSize + padding)
                canvas.drawBitmap(miniIcons[i], null, RectF(ix, startY, ix + iconSize, startY + iconSize), iconPaint)
            }
        } else {
            // 2x2 grid
            val iconSize = (size - padding * 3) / 2f
            for (i in 0 until count) {
                val row = i / 2
                val col = i % 2
                val ix = x + padding + col * (iconSize + padding)
                val iy = y + padding + row * (iconSize + padding)
                canvas.drawBitmap(miniIcons[i], null, RectF(ix, iy, ix + iconSize, iy + iconSize), iconPaint)
            }
        }
    }
"""

content = re.sub(r'private fun drawGrid\(canvas: Canvas, x: Float, y: Float, size: Float\) \{.*?(?=private fun drawStack)', replacement_grid.strip() + '\n    \n    ', content, flags=re.DOTALL)

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'w') as f:
    f.write(content)

print("Fixed grid.")
