import re

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'r') as f:
    content = f.read()

# Replace the drawing logic to match the new rules: <= 4 items = grid, > 4 items = stack
# Since the user says "forget past", we can just completely overwrite the draw method.
replacement_draw = """
    override fun draw(canvas: Canvas) {
        val w = bounds.width().toFloat()
        val h = bounds.height().toFloat()
        val cx = bounds.centerX().toFloat()
        val cy = bounds.centerY().toFloat()
        
        paint.style = Paint.Style.FILL
        paint.color = themeColor
        paint.alpha = 100
        canvas.drawCircle(cx, cy, w / 2f, paint)

        val symbolSize = w * 0.6f
        val sx = cx - symbolSize / 2f
        val sy = cy - symbolSize / 2f
        
        paint.alpha = 255
        
        if (miniIcons.size <= 4) {
            drawGrid(canvas, sx, sy, symbolSize)
        } else {
            drawStack(canvas, sx, sy, symbolSize)
        }
    }
    
    private fun drawGrid(canvas: Canvas, x: Float, y: Float, size: Float) {
        if (miniIcons.isEmpty()) return
        val count = miniIcons.size
        val padding = size * 0.05f
        val iconSize = (size - padding * 3) / 2f
        
        for (i in 0 until count) {
            val row = i / 2
            val col = i % 2
            val ix = x + padding + col * (iconSize + padding)
            val iy = y + padding + row * (iconSize + padding)
            canvas.drawBitmap(miniIcons[i], null, RectF(ix, iy, ix + iconSize, iy + iconSize), iconPaint)
        }
    }
    
    private fun drawStack(canvas: Canvas, x: Float, y: Float, size: Float) {
        if (miniIcons.isEmpty()) return
        val count = minOf(3, miniIcons.size)
        val gap = size * 0.15f
        val cardSize = size - gap * (count - 1)
        
        for (i in count - 1 downTo 0) {
            val tx = x + i * gap
            val ty = y + i * gap
            canvas.drawBitmap(miniIcons[i], null, RectF(tx, ty, tx + cardSize, ty + cardSize), iconPaint)
        }
    }
"""

content = re.sub(r'override fun draw\(canvas: Canvas\) \{.*?(?=override fun setAlpha)', replacement_draw.strip() + '\n\n    ', content, flags=re.DOTALL)

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'w') as f:
    f.write(content)

print("Fixed FolderStyleDrawable.")
