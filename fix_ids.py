import re

with open('app/src/main/java/com/example/service/SidebarAppsManager.kt', 'r') as f:
    content = f.read()

# Change override val id to override var id for Folder, Link, Spacer
content = content.replace('override val id = "folder:$uuid"', 'override var id = "folder:$uuid"')
content = content.replace('override val id = "link:$uuid"', 'override var id = "link:$uuid"')
content = content.replace('override val id = "spacer:$uuid"', 'override var id = "spacer:$uuid"')

# Also replace abstract val id: String to abstract var id: String? No, keeping abstract val is fine if we use open var in base class? Wait, if it's `abstract val`, we can't override with `var` unless we change base.
content = content.replace('abstract val id: String', 'abstract var id: String')
# Wait, if we change to `abstract var`, we must change all `override val id` to `override var id` for ALL subclasses.
