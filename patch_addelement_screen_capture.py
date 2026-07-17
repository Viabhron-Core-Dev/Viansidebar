import re

with open("app/src/main/java/com/example/AddElementActivity.kt", "r") as f:
    content = f.read()

target = """        addHeader("Screen Capture")
        addItem(android.R.drawable.ic_menu_camera, "Screenshot") { finishWithId("system:screenshot") }
        addItem(android.R.drawable.ic_menu_crop, "Region Capture") { finishWithId("system:region_capture") }
        addItem(android.R.drawable.ic_media_play, "Screen Record") { finishWithId("system:screen_record") }
        
        addHeader("Android actions")
        fun openActionPicker(category: String, title: String) {"""

replacement = """        addHeader("Android actions")
        fun openActionPicker(category: String, title: String) {
            val intent = Intent(this, ActionPickerActivity::class.java).apply {
                putExtra("CATEGORY", category)
                putExtra("TITLE", title)
            }
            startActivityForResult(intent, 500)
        }
        
        addItem(android.R.drawable.ic_menu_camera, "Screen Capture") { openActionPicker("screen_capture", "Screen Capture") }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/AddElementActivity.kt", "w") as f:
    f.write(content)
