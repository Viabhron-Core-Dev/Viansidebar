import re

with open("app/src/main/java/com/example/ShortcutPickerActivity.kt", "r") as f:
    content = f.read()

target = """    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 100 && resultCode == Activity.RESULT_OK && data != null) {
            try {
                startActivityForResult(data, 101)
            } catch (e: Exception) {
                android.util.Log.e("ShortcutPicker", "Error starting shortcut config: ${e.message}")
                finish()
            }
        } else if (requestCode == 101 && resultCode == Activity.RESULT_OK && data != null) {"""

replacement = """    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        com.example.LogKeeper.writeLog("ShortcutPicker", "onActivityResult req=$requestCode res=$resultCode data=$data")
        if (requestCode == 100 && resultCode == Activity.RESULT_OK && data != null) {
            try {
                com.example.LogKeeper.writeLog("ShortcutPicker", "Starting config intent: ${data.toUri(0)}")
                startActivityForResult(data, 101)
            } catch (e: Exception) {
                com.example.LogKeeper.writeLog("ShortcutPicker", "Error starting shortcut config: ${e.message}")
                finish()
            }
        } else if (requestCode == 101 && resultCode == Activity.RESULT_OK && data != null) {"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ShortcutPickerActivity.kt", "w") as f:
    f.write(content)
