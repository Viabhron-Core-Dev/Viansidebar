with open("app/src/main/java/com/example/service/SidebarView.kt", "r") as f:
    content = f.read()

content = content.replace("    fun detach() {\n        com.example.utils.AppWidgetHelper.stopListening()\n        if (windowToken != null) {\n            windowManager.removeView(this)\n        }\n    }", "    fun detach() {\n        com.example.utils.AppWidgetHelper.stopListening()\n        try {\n            windowManager.removeView(this)\n        } catch(e: Exception) {}\n    }")

with open("app/src/main/java/com/example/service/SidebarView.kt", "w") as f:
    f.write(content)
