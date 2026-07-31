import re

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # Add autoScrollManager property
    content = re.sub(r'class VianSideAccessibilityService : AccessibilityService\(\) \{\n', 'class VianSideAccessibilityService : AccessibilityService() {\n    private var autoScrollManager: AutoScrollManager? = null\n', content)

    # In onServiceConnected, init it
    content = re.sub(r'        instance = this\n', '        instance = this\n        autoScrollManager = AutoScrollManager(this)\n', content)

    # In onDestroy, remove it if needed, but not strictly required.
    
    # In performAction, handle auto_scroll
    content = re.sub(r'        if \(action == "screenshot"\) \{\n', '        if (action == "auto_scroll") {\n            autoScrollManager?.start()\n            return true\n        }\n\n        if (action == "screenshot") {\n', content)

    with open(path, 'w') as f:
        f.write(content)

fix_file('app/src/main/java/com/example/service/VianSideAccessibilityService.kt')
