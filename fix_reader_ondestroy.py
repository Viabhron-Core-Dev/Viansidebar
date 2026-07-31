import re

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'r') as f:
    content = f.read()

content = content.replace("        widgetPickerReceiver?.let { unregisterReceiver(it) }\n", "")
content = content.replace("        screenStateReceiver?.let { unregisterReceiver(it) }\n", "")
content = content.replace("        readerHandleView = null\n", "")

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'w') as f:
    f.write(content)
