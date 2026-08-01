with open("app/src/main/java/com/example/service/ReaderHandleView.kt", "r") as f:
    content = f.read()

bad = """        handleView?.setOnTouchListener { _, event ->
            gestureDetector.onTouchEvent(event)
        handleView?.setOnTouchListener { _, event ->"""
good = """        handleView?.setOnTouchListener { _, event ->"""

content = content.replace(bad, good)

with open("app/src/main/java/com/example/service/ReaderHandleView.kt", "w") as f:
    f.write(content)

