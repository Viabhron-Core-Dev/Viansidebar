import os
import re

with open("app/src/main/java/com/example/WidgetsGridEditActivity.kt", "r") as f:
    content = f.read()

# Change onAddWidget intent
content = content.replace(
    'val intent = Intent(this@WidgetsGridEditActivity, AddElementActivity::class.java)\n                            startActivityForResult(intent, 201)',
    'val intent = Intent(this@WidgetsGridEditActivity, WidgetPickerActivity::class.java).apply {\n                                putExtra("ACTION_TYPE", "RETURN_ID")\n                            }\n                            startActivityForResult(intent, 201)'
)

# Change Text
content = content.replace('Text("Add Widget / Element")', 'Text("Add Widget")')

with open("app/src/main/java/com/example/WidgetsGridEditActivity.kt", "w") as f:
    f.write(content)
