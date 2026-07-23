import re

with open("app/src/main/java/com/example/AppPickerActivity.kt", "r") as f:
    content = f.read()

content = content.replace(
    'manager = SidebarAppsManager(this, getSharedPreferences("prefs", Context.MODE_PRIVATE), CoroutineScope(Dispatchers.IO)) {',
    'manager = SidebarAppsManager(this, getSharedPreferences("prefs", Context.MODE_PRIVATE), CoroutineScope(Dispatchers.IO), "dummy") {'
)

with open("app/src/main/java/com/example/AppPickerActivity.kt", "w") as f:
    f.write(content)
