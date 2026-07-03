import re

def process_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    content = content.replace('FolderStyleDrawable(item.folderStyle, cHex, iconC, miniIcons)', 'FolderStyleDrawable(item.items.size, cHex, iconC, miniIcons)')

    with open(filename, 'w') as f:
        f.write(content)

process_file('app/src/main/java/com/example/service/AppsPageView.kt')
process_file('app/src/main/java/com/example/service/SidebarEditOverlayView.kt')


with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'r') as f:
    content = f.read()

# Update FolderStyleDialog for preview
content = content.replace('FolderStyleDrawable(position, Color.parseColor("#00BFA5"), Color.parseColor("#333333"), miniIcons)', 'FolderStyleDrawable(item.items.size, Color.parseColor("#00BFA5"), Color.parseColor("#333333"), miniIcons)')

# Update FolderStyleDrawable
# use styleIndex as itemCount
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
        
        if (styleIndex <= 4) {
            drawGrid(canvas, sx, sy, symbolSize)
        } else {
            drawStack(canvas, sx, sy, symbolSize)
        }
    }
"""

content = re.sub(r'override fun draw\(canvas: Canvas\) \{.*?(?=private fun drawGrid)', replacement_draw.strip() + '\n    \n    ', content, flags=re.DOTALL)

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'w') as f:
    f.write(content)

print("Fixed folder icon logic.")
