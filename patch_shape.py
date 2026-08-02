with open("app/src/main/java/com/example/utils/HandleShapeDrawable.kt", "r") as f:
    content = f.read()

import re

# Fix half_oval
old_half_oval = """            "half_oval" -> {
                when (edge) {
                    "right" -> {
                        rect.set(-w, 0f, w, h)
                    }
                    "left" -> {
                        rect.set(0f, 0f, w * 2, h)
                    }
                    "bottom" -> {
                        rect.set(0f, -h, w, h)
                    }
                }
                path.addOval(rect, Path.Direction.CW)
            }"""

new_half_oval = """            "half_oval" -> {
                when (edge) {
                    "right" -> {
                        rect.set(0f, 0f, w * 2, h)
                    }
                    "left" -> {
                        rect.set(-w, 0f, w, h)
                    }
                    "bottom" -> {
                        rect.set(0f, 0f, w, h * 2)
                    }
                }
                path.addOval(rect, Path.Direction.CW)
            }"""

if old_half_oval in content:
    content = content.replace(old_half_oval, new_half_oval)
else:
    print("Could not find half_oval code block")

# Add slanted_block
slanted_block = """            "slanted_block" -> {
                val d = Math.min(w * 0.577f, h / 2f)
                val dw = Math.min(h * 0.577f, w / 2f)
                when (edge) {
                    "right" -> {
                        path.moveTo(w, 0f)
                        path.lineTo(0f, d)
                        path.lineTo(0f, h - d)
                        path.lineTo(w, h)
                    }
                    "left" -> {
                        path.moveTo(0f, 0f)
                        path.lineTo(w, d)
                        path.lineTo(w, h - d)
                        path.lineTo(0f, h)
                    }
                    "bottom" -> {
                        path.moveTo(0f, h)
                        path.lineTo(dw, 0f)
                        path.lineTo(w - dw, 0f)
                        path.lineTo(w, h)
                    }
                    else -> path.addRect(rect, Path.Direction.CW)
                }
                path.close()
            }
"""

if '"slanted_block"' not in content:
    content = content.replace('            else -> { // "rectangle"', slanted_block + '            else -> { // "rectangle"')

with open("app/src/main/java/com/example/utils/HandleShapeDrawable.kt", "w") as f:
    f.write(content)
