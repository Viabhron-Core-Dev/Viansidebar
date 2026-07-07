import re

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'r') as f:
    content = f.read()

old_drawGrid = """    private fun drawGrid(canvas: Canvas, x: Float, y: Float, size: Float) {
        if (miniIcons.isEmpty()) {
            // User requested no default box, so draw nothing or leave it empty
            return
        }
        val count = miniIcons.size
        
        if (count == 1) {
            val p = size * 0.1f
            val ix = x + p
            val iy = y + p
            val isize = size - 2*p
            canvas.drawBitmap(miniIcons[0], null, RectF(ix, iy, ix + isize, iy + isize), iconPaint)
        } else if (count == 2) {
            val padding = size * 0.05f
            val iconSize = (size - padding * 3) / 2f
            val startY = y + (size - iconSize) / 2f
            for (i in 0 until 2) {
                val ix = x + padding + i * (iconSize + padding)
                canvas.drawBitmap(miniIcons[i], null, RectF(ix, startY, ix + iconSize, startY + iconSize), iconPaint)
            }
        } else if (count <= 4) {
            val padding = size * 0.05f
            val iconSize = (size - padding * 3) / 2f
            for (i in 0 until count) {
                val row = i / 2
                val col = i % 2
                val ix = x + padding + col * (iconSize + padding)
                val iy = y + padding + row * (iconSize + padding)
                canvas.drawBitmap(miniIcons[i], null, RectF(ix, iy, ix + iconSize, iy + iconSize), iconPaint)
            }
        } else {
            // up to 9 (3x3 grid)
            val maxCount = minOf(9, count)
            val padding = size * 0.05f
            val iconSize = (size - padding * 4) / 3f
            for (i in 0 until maxCount) {
                val row = i / 3
                val col = i % 3
                val ix = x + padding + col * (iconSize + padding)
                val iy = y + padding + row * (iconSize + padding)
                canvas.drawBitmap(miniIcons[i], null, RectF(ix, iy, ix + iconSize, iy + iconSize), iconPaint)
            }
        }
    }"""

new_drawGrid = """    private fun drawGrid(canvas: Canvas, x: Float, y: Float, size: Float) {
        if (miniIcons.isEmpty()) {
            return
        }
        val count = miniIcons.size
        
        if (count == 1) {
            val p = size * 0.05f
            val ix = x + p
            val iy = y + p
            val isize = size - 2*p
            canvas.drawBitmap(miniIcons[0], null, RectF(ix, iy, ix + isize, iy + isize), iconPaint)
        } else if (count == 2) {
            val padding = size * 0.04f
            val iconSize = (size - padding * 3) / 2f
            val startY = y + (size - iconSize) / 2f
            for (i in 0 until 2) {
                val ix = x + padding + i * (iconSize + padding)
                canvas.drawBitmap(miniIcons[i], null, RectF(ix, startY, ix + iconSize, startY + iconSize), iconPaint)
            }
        } else {
            val maxCount = minOf(4, count)
            val padding = size * 0.04f
            val iconSize = (size - padding * 3) / 2f
            for (i in 0 until maxCount) {
                val row = i / 2
                val col = i % 2
                val ix = x + padding + col * (iconSize + padding)
                val iy = y + padding + row * (iconSize + padding)
                canvas.drawBitmap(miniIcons[i], null, RectF(ix, iy, ix + iconSize, iy + iconSize), iconPaint)
            }
        }
    }"""

content = content.replace(old_drawGrid, new_drawGrid)

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'w') as f:
    f.write(content)
