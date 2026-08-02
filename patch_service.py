import re

with open("app/src/main/java/com/example/service/VianSideAccessibilityService.kt", "r") as f:
    content = f.read()

content = content.replace("private var autoScrollManager: AutoScrollManager? = null", "private var autoScrollManager: AutoScrollManager? = null\n    private var longScreenshotManager: LongScreenshotManager? = null")

old_onServiceConnected = """    override fun onServiceConnected() {
        super.onServiceConnected()
        instance = this
        autoScrollManager = AutoScrollManager(this)"""

new_onServiceConnected = """    override fun onServiceConnected() {
        super.onServiceConnected()
        instance = this
        autoScrollManager = AutoScrollManager(this)
        longScreenshotManager = LongScreenshotManager(this)"""

content = content.replace(old_onServiceConnected, new_onServiceConnected)

old_action = """        if (action == "auto_scroll") {
            autoScrollManager?.start()
            return true
        }"""

new_action = """        if (action == "auto_scroll") {
            autoScrollManager?.start()
            return true
        }
        if (action == "long_screenshot") {
            longScreenshotManager?.start()
            return true
        }"""

content = content.replace(old_action, new_action)

with open("app/src/main/java/com/example/service/VianSideAccessibilityService.kt", "w") as f:
    f.write(content)

