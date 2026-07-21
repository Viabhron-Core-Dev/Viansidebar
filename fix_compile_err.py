import re

with open("app/src/main/java/com/example/HandlesListSettingsScreen.kt", "r") as f:
    content = f.read()

# Fix HandleItem signature back to () -> Unit
content = content.replace(
    'onNavigateToSidebarSettings: (String) -> Unit,\n    onUpdate: (HandleConfig) -> Unit',
    'onNavigateToSidebarSettings: () -> Unit,\n    onUpdate: (HandleConfig) -> Unit'
)

with open("app/src/main/java/com/example/HandlesListSettingsScreen.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/SettingsActivity.kt", "r") as f:
    content = f.read()

# Fix 'general' SidebarSettingsScreen
content = content.replace(
"""                "general" -> SidebarSettingsScreen(
                    onBack = { currentRoute = "main" }
                )""",
"""                "general" -> SidebarSettingsScreen(
                    handleId = "sidebar",
                    onBack = { currentRoute = "main" }
                )"""
)

# Remove the broken when clause
content = content.replace(
"""                currentRoute.startsWith("pages_") -> SidebarSettingsScreen(
                    handleId = currentRoute.removePrefix("pages_"),
                    onBack = { currentRoute = "main" }
                )""",
"""                "pages" -> SidebarSettingsScreen(
                    handleId = "sidebar",
                    onBack = { currentRoute = "main" }
                )"""
)

# Insert the pages handler at the bottom, alongside handle_ check
content = content.replace(
"""            if (currentRoute.startsWith("handle_")) {""",
"""            if (currentRoute.startsWith("pages_")) {
                val handleId = currentRoute.removePrefix("pages_")
                SidebarSettingsScreen(
                    handleId = handleId,
                    onBack = { currentRoute = "handles" }
                )
            } else if (currentRoute.startsWith("handle_")) {"""
)

with open("app/src/main/java/com/example/SettingsActivity.kt", "w") as f:
    f.write(content)
