import os
import re

with open("app/src/main/java/com/example/AddElementActivity.kt", "r") as f:
    content = f.read()

# Add Popup Widget item
content = content.replace(
'''        addHeader("Special items")''',
'''        addItem(android.R.drawable.ic_menu_gallery, "Popup Widget") {
            val intent = Intent(this, WidgetPickerActivity::class.java).apply {
                putExtra("ACTION_TYPE", "RETURN_ID")
            }
            startActivityForResult(intent, 500)
        }

        addHeader("Special items")''')

# Handle result 500
content = content.replace(
'''            val id = data.getStringExtra("ELEMENT_ID")
            if (id != null) {
                finishWithId(id)''',
'''            val id = data.getStringExtra("ELEMENT_ID")
            if (id != null) {
                if (requestCode == 500 && id.startsWith("widget:")) {
                    finishWithId("popup_widget:" + id.removePrefix("widget:"))
                } else {
                    finishWithId(id)
                }''')

with open("app/src/main/java/com/example/AddElementActivity.kt", "w") as f:
    f.write(content)
