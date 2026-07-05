import re

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'r') as f:
    content = f.read()

old_draw = """    override fun draw(canvas: Canvas) {
        val w = bounds.width().toFloat()
        val h = bounds.height().toFloat()
        val cx = bounds.centerX().toFloat()
        val cy = bounds.centerY().toFloat()
        
        // No background circle as per user request

        val symbolSize = w * 0.6f
        val sx = cx - symbolSize / 2f
        val sy = cy - symbolSize / 2f
        
        paint.alpha = 255
        
        if (styleIndex == 1) {
            drawStack(canvas, sx, sy, symbolSize)
        } else {
            drawGrid(canvas, sx, sy, symbolSize)
        }
    }"""
new_draw = """    override fun draw(canvas: Canvas) {
        val w = bounds.width().toFloat()
        val h = bounds.height().toFloat()
        val cx = bounds.centerX().toFloat()
        val cy = bounds.centerY().toFloat()
        
        // Draw circular background (like Lawnchair)
        paint.color = android.graphics.Color.parseColor("#33FFFFFF") // Translucent white/gray
        paint.style = Paint.Style.FILL
        val bgRadius = minOf(w, h) * 0.45f
        canvas.drawCircle(cx, cy, bgRadius, paint)
        
        // Draw an outer ring matching the theme color slightly
        paint.color = themeColor
        paint.alpha = 100
        paint.style = Paint.Style.STROKE
        paint.strokeWidth = 2f
        canvas.drawCircle(cx, cy, bgRadius, paint)
        
        // Reset paint
        paint.style = Paint.Style.FILL
        paint.alpha = 255

        val symbolSize = w * 0.6f
        val sx = cx - symbolSize / 2f
        val sy = cy - symbolSize / 2f
        
        if (styleIndex == 1) {
            drawStack(canvas, sx, sy, symbolSize)
        } else {
            drawGrid(canvas, sx, sy, symbolSize)
        }
    }"""
content = content.replace(old_draw, new_draw)

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'w') as f:
    f.write(content)
