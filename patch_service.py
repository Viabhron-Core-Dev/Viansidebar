with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "r") as f:
    content = f.read()

old_set_folded_true = """            bubbleIcon.visibility = View.GONE
            windowContainer.visibility = View.GONE
            floatingView.visibility = View.GONE"""
new_set_folded_true = """            bubbleIcon.visibility = View.VISIBLE
            windowContainer.visibility = View.GONE
            floatingView.visibility = View.VISIBLE"""
content = content.replace(old_set_folded_true, new_set_folded_true)

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "w") as f:
    f.write(content)
