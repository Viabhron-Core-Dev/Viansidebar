import re

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "r") as f:
    content = f.read()

content = content.replace(
"""                    p = AppsPageView(this, config, manager, serviceScope,""",
"""                    p = AppsPageView(this, handleId, config, manager, serviceScope,"""
)
content = content.replace(
"""                val p = AppsPageView(this, config, manager, serviceScope,""",
"""                val p = AppsPageView(this, currentHandleId, config, manager, serviceScope,"""
)

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "w") as f:
    f.write(content)
