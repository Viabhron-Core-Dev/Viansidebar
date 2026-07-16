import re

with open("app/src/main/java/com/example/service/FolderStyleDialog.kt", "r") as f:
    content = f.read()

target = """    override fun draw(canvas: Canvas) {
        val w = bounds.width().toFloat()
        val h = bounds.height().toFloat()
        val cx = bounds.centerX().toFloat()
        val cy = bounds.centerY().toFloat()
        
        // Reset paint
        paint.style = Paint.Style.FILL
        paint.alpha = 255

        val symbolSize = w * 0.9f
        val sx = cx - symbolSize / 2f
        val sy = cy - symbolSize / 2f
        
        if (styleIndex == 1) {
            drawStack(canvas, sx, sy, symbolSize)
        } else {
            drawGrid(canvas, sx, sy, symbolSize)
        }
    }"""

replacement = """    override fun draw(canvas: Canvas) {
        val w = bounds.width().toFloat()
        val h = bounds.height().toFloat()
        val cx = bounds.centerX().toFloat()
        val cy = bounds.centerY().toFloat()
        
        // Draw transparent bubble background
        paint.style = Paint.Style.FILL
        paint.color = themeColor
        paint.alpha = 100
        canvas.drawCircle(cx, cy, w / 2.2f, paint)

        val symbolSize = w * 0.75f
        val sx = cx - symbolSize / 2f
        val sy = cy - symbolSize / 2f
        
        if (styleIndex == 1) {
            drawStack(canvas, sx, sy, symbolSize)
        } else {
            drawGrid(canvas, sx, sy, symbolSize)
        }
    }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/FolderStyleDialog.kt", "w") as f:
    f.write(content)
