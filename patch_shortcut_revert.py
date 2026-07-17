import re

with open("app/src/main/java/com/example/ShortcutPickerActivity.kt", "r") as f:
    content = f.read()

target = """    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val pickIntent = Intent(Intent.ACTION_CREATE_SHORTCUT)
        startActivityForResult(pickIntent, 101)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 101 && resultCode == Activity.RESULT_OK && data != null) {"""

replacement = """    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val pickIntent = Intent(Intent.ACTION_PICK_ACTIVITY)
        pickIntent.putExtra(Intent.EXTRA_INTENT, Intent(Intent.ACTION_CREATE_SHORTCUT))
        pickIntent.putExtra(Intent.EXTRA_TITLE, "Select Shortcut")
        startActivityForResult(pickIntent, 100)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 100 && resultCode == Activity.RESULT_OK && data != null) {
            try {
                startActivityForResult(data, 101)
            } catch (e: Exception) {
                android.util.Log.e("ShortcutPicker", "Error starting shortcut config: ${e.message}")
                finish()
            }
        } else if (requestCode == 101 && resultCode == Activity.RESULT_OK && data != null) {"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ShortcutPickerActivity.kt", "w") as f:
    f.write(content)
