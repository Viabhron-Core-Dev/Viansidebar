import re

files = [
    "app/src/main/java/com/example/service/WidgetsGridPageView.kt",
    "app/src/main/java/com/example/WidgetsGridEditActivity.kt"
]

for f in files:
    with open(f, "r") as file:
        content = file.read()
    
    # Change val id: Int to val id: String
    content = content.replace("val id: Int", "val id: String")
    
    with open(f, "w") as file:
        file.write(content)
