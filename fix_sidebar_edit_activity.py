import re

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "r") as f:
    content = f.read()

# Add pageId property
content = content.replace(
    'private var folderUuid: String? = null',
    'private var folderUuid: String? = null\n    private var pageId: String = "default_apps"'
)

# Read pageId from intent
content = content.replace(
    'folderUuid = intent.getStringExtra("FOLDER_UUID")',
    'folderUuid = intent.getStringExtra("FOLDER_UUID")\n        pageId = intent.getStringExtra("PAGE_ID") ?: "default_apps"'
)

# Change instantiation
content = content.replace(
    'manager = SidebarAppsManager(this, prefs, serviceScope) {',
    'manager = SidebarAppsManager(this, prefs, serviceScope, pageId) {'
)

# Update sidebar_apps references
content = content.replace('"sidebar_apps"', '"sidebar_apps_${pageId}"')

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "w") as f:
    f.write(content)
