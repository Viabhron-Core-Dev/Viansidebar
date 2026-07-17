import re

with open("app/src/main/java/com/example/AddElementActivity.kt", "r") as f:
    content = f.read()

target = """        addItem(android.R.drawable.ic_menu_camera, "Screen Capture") { openActionPicker("screen_capture", "Screen Capture") }
            val intent = Intent(this, ActionPickerActivity::class.java).apply {
                putExtra("CATEGORY", category)
                putExtra("TITLE", title)
            }
            startActivityForResult(intent, 500)
        }"""

replacement = """        addItem(android.R.drawable.ic_menu_camera, "Screen Capture") { openActionPicker("screen_capture", "Screen Capture") }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/AddElementActivity.kt", "w") as f:
    f.write(content)
