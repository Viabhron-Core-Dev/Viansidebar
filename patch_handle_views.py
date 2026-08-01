import os
for filename in ["app/src/main/java/com/example/service/TriggerHandleView.kt", "app/src/main/java/com/example/service/ReaderHandleView.kt"]:
    with open(filename, "r") as f:
        content = f.read()

    # Add import
    content = content.replace("import com.example.utils.Utils", "import com.example.utils.Utils\nimport com.example.utils.HandleShapeDrawable")

    # Replace handleView?.setBackgroundColor(colorInt)
    # with reading shape and edge, then setting background
    old_bg = "        handleView?.setBackgroundColor(colorInt)"
    new_bg = """        val shapeStr = prefs.getString("${prefix}shape", "rectangle") ?: "rectangle"
        val edgeStrForShape = prefs.getString("${prefix}edge", "right") ?: "right"
        handleView?.background = HandleShapeDrawable(colorInt, shapeStr, edgeStrForShape)"""

    content = content.replace(old_bg, new_bg)

    with open(filename, "w") as f:
        f.write(content)

