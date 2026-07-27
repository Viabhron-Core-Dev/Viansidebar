import re

with open("app/src/main/java/com/example/WidgetPickerActivity.kt", "r") as f:
    content = f.read()

target = """            val spanX = if (info != null) {
                if (android.os.Build.VERSION.SDK_INT >= 31) info.targetCellWidth else Math.max(1, Math.round(info.minWidth / 70.0).toInt())
            } else 2
            val spanY = if (info != null) {
                if (android.os.Build.VERSION.SDK_INT >= 31) info.targetCellHeight else Math.max(1, Math.round(info.minHeight / 70.0).toInt())
            } else 2"""

replacement = """            val spanX = if (info != null) {
                val cw = if (android.os.Build.VERSION.SDK_INT >= 31) info.targetCellWidth else 0
                if (cw > 0) cw else Math.max(1, Math.round(info.minWidth / 70.0).toInt())
            } else 2
            val spanY = if (info != null) {
                val ch = if (android.os.Build.VERSION.SDK_INT >= 31) info.targetCellHeight else 0
                if (ch > 0) ch else Math.max(1, Math.round(info.minHeight / 70.0).toInt())
            } else 2"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/WidgetPickerActivity.kt", "w") as f:
    f.write(content)
