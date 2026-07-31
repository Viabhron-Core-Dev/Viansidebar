import re
with open('app/src/main/java/com/example/service/ReaderHandleView.kt', 'r') as f:
    content = f.read()
content = content.replace("val gravity = if (edgeStr == \"left\") Gravity.START else Gravity.END", "val gravity = getEdgeFlag(edgeStr)")
content = content.replace("import com.example.utils.Utils", "import com.example.utils.Utils\nimport com.example.utils.getEdgeFlag")
with open('app/src/main/java/com/example/service/ReaderHandleView.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/service/TriggerHandleView.kt', 'r') as f:
    content = f.read()
content = content.replace("val gravity = if (edgeStr == \"left\") Gravity.START else Gravity.END", "val gravity = getEdgeFlag(edgeStr)")
content = content.replace("import com.example.utils.Utils", "import com.example.utils.Utils\nimport com.example.utils.getEdgeFlag")
with open('app/src/main/java/com/example/service/TriggerHandleView.kt', 'w') as f:
    f.write(content)
