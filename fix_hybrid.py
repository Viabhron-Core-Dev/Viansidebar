import re

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "r") as f:
    content = f.read()

content = content.replace("serviceScope", "CoroutineScope(Dispatchers.Main)")

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "w") as f:
    f.write(content)
