import re

with open("app/src/main/java/com/example/service/FolderStyleDialog.kt", "r") as f:
    content = f.read()

target = """        val symbolSize = w * 0.9f
        val sx = cx - symbolSize / 2f
        val sy = cy - symbolSize / 2f"""

replacement = """        val symbolSize = w * 0.98f
        val sx = cx - symbolSize / 2f
        val sy = cy - symbolSize / 2f"""

content = content.replace(target, replacement)

target2 = """            val maxCount = minOf(4, count)
            val padding = size * 0.04f
            val iconSize = (size - padding * 3) / 2f
            for (i in 0 until maxCount) {"""

replacement2 = """            val maxCount = minOf(4, count)
            val padding = size * 0.015f
            val iconSize = (size - padding * 3) / 2f
            for (i in 0 until maxCount) {"""

content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/service/FolderStyleDialog.kt", "w") as f:
    f.write(content)
