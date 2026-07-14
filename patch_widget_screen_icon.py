import sys

with open('app/src/main/java/com/example/WidgetPickerActivity.kt', 'r') as f:
    content = f.read()

target = """                                        Image(
                                            bitmap = bitmap.asImageBitmap(),
                                            contentDescription = null,
                                            modifier = Modifier.size(48.dp)
                                        )"""

replacement = """                                        Image(
                                            bitmap = bitmap.asImageBitmap(),
                                            contentDescription = null,
                                            modifier = Modifier.size(48.dp),
                                            alpha = if (enabled) 1f else 0.3f
                                        )"""

content = content.replace(target, replacement)

with open('app/src/main/java/com/example/WidgetPickerActivity.kt', 'w') as f:
    f.write(content)
