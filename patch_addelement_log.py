import re

with open("app/src/main/java/com/example/AddElementActivity.kt", "r") as f:
    content = f.read()

target = """    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode == Activity.RESULT_OK && data != null) {
            val id = data.getStringExtra("ELEMENT_ID")
            if (id != null) {
                finishWithId(id)
            }
        }
    }"""

replacement = """    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        com.example.LogKeeper.writeLog("AddElementActivity", "onActivityResult req=$requestCode res=$resultCode data=$data")
        if (resultCode == Activity.RESULT_OK && data != null) {
            val id = data.getStringExtra("ELEMENT_ID")
            if (id != null) {
                finishWithId(id)
            } else {
                com.example.LogKeeper.writeLog("AddElementActivity", "ELEMENT_ID was null in data!")
            }
        } else {
            // Did it fail? If they cancelled, we might just stay here. 
            // But if it was a failure in picking, they are stuck. 
            // Let's just finish the AddElementActivity if a picker is cancelled so they don't get stuck.
            if (requestCode == 300) { // ShortcutPickerActivity
                com.example.LogKeeper.writeLog("AddElementActivity", "ShortcutPicker cancelled or failed.")
            }
        }
    }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/AddElementActivity.kt", "w") as f:
    f.write(content)
