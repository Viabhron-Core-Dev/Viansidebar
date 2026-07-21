import re

with open("app/src/main/java/com/example/HandlesListSettingsScreen.kt", "r") as f:
    content = f.read()

content = content.replace("com.example.utils.PageManager.getPages(prefs)", "com.example.utils.PageManager.getPages(prefs, handle.id)")

with open("app/src/main/java/com/example/HandlesListSettingsScreen.kt", "w") as f:
    f.write(content)
