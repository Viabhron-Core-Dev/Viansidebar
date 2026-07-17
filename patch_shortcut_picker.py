import re

with open("app/src/main/java/com/example/ShortcutPickerActivity.kt", "r") as f:
    content = f.read()

target = """        if (requestCode == 100 && resultCode == Activity.RESULT_OK && data != null) {
            // Android gives us back an Intent to start the shortcut creation activity
            startActivityForResult(data, 101)
        }"""

replacement = """        if (requestCode == 100 && resultCode == Activity.RESULT_OK && data != null) {
            // Android gives us back an Intent to start the shortcut creation activity
            try {
                startActivityForResult(data, 101)
            } catch (e: Exception) {
                android.util.Log.e("ShortcutPicker", "Error starting shortcut config: ${e.message}")
                finish()
            }
        }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ShortcutPickerActivity.kt", "w") as f:
    f.write(content)
