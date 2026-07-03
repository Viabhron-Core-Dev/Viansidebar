import re
with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'r') as f:
    content = f.read()

old_grid = """    private fun drawGrid(canvas: Canvas, x: Float, y: Float, size: Float) {
        if (miniIcons.isEmpty()) return"""

new_grid = """    private fun drawGrid(canvas: Canvas, x: Float, y: Float, size: Float) {
        if (miniIcons.isEmpty()) {
            paint.style = Paint.Style.STROKE
            paint.strokeWidth = 4f
            canvas.drawRect(x + size*0.1f, y + size*0.2f, x + size*0.9f, y + size*0.8f, paint)
            canvas.drawLine(x + size*0.1f, y + size*0.4f, x + size*0.9f, y + size*0.4f, paint)
            return
        }"""

content = content.replace(old_grid, new_grid)

old_stack = """    private fun drawStack(canvas: Canvas, x: Float, y: Float, size: Float) {
        if (miniIcons.isEmpty()) return"""

new_stack = """    private fun drawStack(canvas: Canvas, x: Float, y: Float, size: Float) {
        if (miniIcons.isEmpty()) {
            paint.style = Paint.Style.STROKE
            paint.strokeWidth = 4f
            canvas.drawRect(x + size*0.1f, y + size*0.2f, x + size*0.9f, y + size*0.8f, paint)
            canvas.drawLine(x + size*0.1f, y + size*0.4f, x + size*0.9f, y + size*0.4f, paint)
            return
        }"""
content = content.replace(old_stack, new_stack)

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'w') as f:
    f.write(content)
