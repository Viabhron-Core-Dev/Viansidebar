import re

with open("app/src/main/java/com/example/WidgetPickerActivity.kt", "r") as f:
    content = f.read()

target = """                                    val is1x1 = spanX <= 1 && spanY <= 1
                                    val isSidebar = actionType == "ADD_ELEMENT" || actionType == "RETURN_ID"
                                    val enabled = !isSidebar || is1x1"""

replacement = """                                    val is1x1 = spanX <= 1 && spanY <= 1
                                    val isSidebar = actionType == "ADD_ELEMENT" || actionType == "RETURN_ID"
                                    val enabled = true"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/WidgetPickerActivity.kt", "w") as f:
    f.write(content)
