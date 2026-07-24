import os
import re

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "r") as f:
    content = f.read()

content = re.sub(r'data class GridWidgetItem\([\s\S]*?\n\)\n', '', content)

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "w") as f:
    f.write(content)
