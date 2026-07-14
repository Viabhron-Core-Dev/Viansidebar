import sys

with open('app/src/main/java/com/example/service/WidgetsGridEditOverlayView.kt', 'r') as f:
    content = f.read()

target = "val callback = object : ItemTouchHelper.SimpleCallback(ItemTouchHelper.UP or ItemTouchHelper.DOWN, 0)"
replacement = "val callback = object : ItemTouchHelper.SimpleCallback(ItemTouchHelper.UP or ItemTouchHelper.DOWN or ItemTouchHelper.LEFT or ItemTouchHelper.RIGHT, 0)"
content = content.replace(target, replacement)

with open('app/src/main/java/com/example/service/WidgetsGridEditOverlayView.kt', 'w') as f:
    f.write(content)
