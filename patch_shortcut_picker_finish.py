import re

with open("app/src/main/java/com/example/ShortcutPickerActivity.kt", "r") as f:
    content = f.read()

target = """        if (requestCode == 100 || requestCode == 101) {
            finish()
        }"""

replacement = """        if (resultCode != Activity.RESULT_OK) {
            finish()
        }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ShortcutPickerActivity.kt", "w") as f:
    f.write(content)
