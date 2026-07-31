import re
with open('app/src/main/java/com/example/service/ReaderHandleView.kt', 'r') as f:
    content = f.read()

content = content.replace("import com.example.utils.getEdgeFlag", "")
content = content.replace("val gravity = getEdgeFlag(edgeStr)", 'val gravity = if (edgeStr == "left") Gravity.START else Gravity.END')
content = content.replace("import com.example.utils.DisplayUtils", "import com.example.utils.Utils")
content = content.replace("DisplayUtils", "Utils")
content = content.replace("import com.example.R", "")

with open('app/src/main/java/com/example/service/ReaderHandleView.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/service/TriggerHandleView.kt', 'r') as f:
    content = f.read()

content = content.replace("import com.example.utils.getEdgeFlag", "")
content = content.replace("val gravity = getEdgeFlag(edgeStr)", 'val gravity = if (edgeStr == "left") Gravity.START else Gravity.END')
content = content.replace("import com.example.utils.DisplayUtils", "import com.example.utils.Utils")
content = content.replace("DisplayUtils", "Utils")
content = content.replace("import com.example.R", "")

with open('app/src/main/java/com/example/service/TriggerHandleView.kt', 'w') as f:
    f.write(content)
