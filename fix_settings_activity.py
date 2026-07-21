import re

with open("app/src/main/java/com/example/SettingsActivity.kt", "r") as f:
    content = f.read()

content = content.replace(
    '"pages" -> SidebarSettingsScreen(',
    'currentRoute.startsWith("pages_") -> SidebarSettingsScreen(\n                    handleId = currentRoute.removePrefix("pages_"),'
)

content = content.replace(
    'onNavigateToSidebarSettings = { currentRoute = "pages" }',
    'onNavigateToSidebarSettings = { currentRoute = "pages_$it" }'
)

with open("app/src/main/java/com/example/SettingsActivity.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/HandlesListSettingsScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    'onNavigateToSidebarSettings: () -> Unit,',
    'onNavigateToSidebarSettings: (String) -> Unit,'
)

content = content.replace(
    'onNavigateToSidebarSettings = onNavigateToSidebarSettings,',
    'onNavigateToSidebarSettings = { onNavigateToSidebarSettings(handle.id) },'
)

content = content.replace(
    'onNavigateToSidebarSettings: () -> Unit,',
    'onNavigateToSidebarSettings: () -> Unit,'
)
# Wait, HandleItem has onNavigateToSidebarSettings: () -> Unit
# so it doesn't need string, it just invokes the lambda that captures handle.id.

with open("app/src/main/java/com/example/HandlesListSettingsScreen.kt", "w") as f:
    f.write(content)
