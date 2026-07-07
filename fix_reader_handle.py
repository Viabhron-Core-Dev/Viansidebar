import re

with open('app/src/main/java/com/example/service/ReaderHandleView.kt', 'r') as f:
    content = f.read()

content = content.replace('if (prefs.getBoolean("reader_handle_enabled", false)) {', 'if (false) {')

with open('app/src/main/java/com/example/service/ReaderHandleView.kt', 'w') as f:
    f.write(content)

