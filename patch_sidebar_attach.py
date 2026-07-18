import re

with open("app/src/main/java/com/example/service/SidebarView.kt", "r") as f:
    content = f.read()

target = """    fun attach() {
        if (!isAttached) {
            try {
                windowManager.addView(this, wmParams)
                isAttached = true
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }"""

replacement = """    fun attach() {
        if (!isAttached) {
            try {
                windowManager.addView(this, wmParams)
                isAttached = true
                com.example.utils.AppWidgetHelper.startListening(context)
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }"""

content = content.replace(target, replacement)

target2 = """    fun detach() {
        if (isAttached) {
            try {
                windowManager.removeView(this)
            } catch (e: Exception) {
                e.printStackTrace()
            }
            isAttached = false
            com.example.utils.AppWidgetHelper.stopListening()
        }
    }"""

replacement2 = """    fun detach() {
        if (isAttached) {
            try {
                windowManager.removeView(this)
            } catch (e: Exception) {
                e.printStackTrace()
            }
            isAttached = false
            com.example.utils.AppWidgetHelper.stopListening()
        }
    }"""

content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/service/SidebarView.kt", "w") as f:
    f.write(content)
