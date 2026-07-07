import re

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'r') as f:
    content = f.read()

old_code = """        readerHandleView = ReaderHandleView(this, prefs, windowManager) {
            android.util.Log.d("VianSide", "reader trigger tapped")
            toggleReader()
        }
        readerHandleView?.attach()"""

new_code = """        // readerHandleView = ReaderHandleView(this, prefs, windowManager) {
        //     android.util.Log.d("VianSide", "reader trigger tapped")
        //     toggleReader()
        // }
        // readerHandleView?.attach()"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'w') as f:
    f.write(content)

