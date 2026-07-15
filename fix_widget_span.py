import sys

with open('app/src/main/java/com/example/WidgetPickerActivity.kt', 'r') as f:
    content = f.read()

target = """                                    val spanX = Math.ceil((provider.minWidth + 30) / 70.0).toInt()
                                    val spanY = Math.ceil((provider.minHeight + 30) / 70.0).toInt()"""

replacement = """                                    val spanX = if (android.os.Build.VERSION.SDK_INT >= 31) provider.targetCellWidth else Math.max(1, Math.round(provider.minWidth / 70.0).toInt())
                                    val spanY = if (android.os.Build.VERSION.SDK_INT >= 31) provider.targetCellHeight else Math.max(1, Math.round(provider.minHeight / 70.0).toInt())"""

content = content.replace(target, replacement)

with open('app/src/main/java/com/example/WidgetPickerActivity.kt', 'w') as f:
    f.write(content)
