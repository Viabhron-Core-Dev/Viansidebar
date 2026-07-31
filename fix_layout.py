import re
# If layout doesn't exist, just create a View programmatically
with open('app/src/main/java/com/example/service/ReaderHandleView.kt', 'r') as f:
    content = f.read()

content = content.replace("handleView = LayoutInflater.from(context).inflate(R.layout.layout_trigger_handle, null)", "handleView = View(context)")

with open('app/src/main/java/com/example/service/ReaderHandleView.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/service/TriggerHandleView.kt', 'r') as f:
    content = f.read()

content = content.replace("handleView = LayoutInflater.from(context).inflate(R.layout.layout_trigger_handle, null)", "handleView = View(context)")

with open('app/src/main/java/com/example/service/TriggerHandleView.kt', 'w') as f:
    f.write(content)
