import re

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'r') as f:
    content = f.read()

old_code = """    val styles = listOf(
        "Grid", "Stack"
    )

    val adapter = object : BaseAdapter() {"""

new_code = """    val styles = listOf(
        "Grid", "Stack"
    )

    var selectedStyle = item.folderStyle

    val adapter = object : BaseAdapter() {"""

content = content.replace(old_code, new_code)

old_code2 = """    gridView.adapter = adapter
    layout.addView(gridView, LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT))

    var selectedStyle = item.folderStyle"""

new_code2 = """    gridView.adapter = adapter
    layout.addView(gridView, LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT))"""

content = content.replace(old_code2, new_code2)

with open('app/src/main/java/com/example/service/FolderStyleDialog.kt', 'w') as f:
    f.write(content)
