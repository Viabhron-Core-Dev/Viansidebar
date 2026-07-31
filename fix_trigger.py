import re

with open('app/src/main/java/com/example/service/TriggerHandleView.kt', 'r') as f:
    content = f.read()

content = content.replace("VianSideAccessibilityService.instance?.performAction(sysAction)", "")
content = content.replace('val sysAction = action.removePrefix("action_")', 'val sysAction = action.removePrefix("action_")\n            com.example.service.VianSideAccessibilityService.instance?.performAction(sysAction)')


with open('app/src/main/java/com/example/service/TriggerHandleView.kt', 'w') as f:
    f.write(content)
