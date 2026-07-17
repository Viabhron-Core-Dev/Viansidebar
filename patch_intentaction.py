import re

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "r") as f:
    content = f.read()

target = """    data class IntentAction(
        val uri: String,
        override val label: String
    ) : SidebarItem() {
        override var id = "intent:${java.net.URLEncoder.encode(label, "UTF-8")}:${java.net.URLEncoder.encode(uri, "UTF-8")}"
    }"""

replacement = """    data class IntentAction(
        val uri: String,
        override val label: String,
        val iconPath: String? = null
    ) : SidebarItem() {
        override var id = if (iconPath != null) "intent:${java.net.URLEncoder.encode(label, "UTF-8")}:${java.net.URLEncoder.encode(uri, "UTF-8")}:$iconPath" else "intent:${java.net.URLEncoder.encode(label, "UTF-8")}:${java.net.URLEncoder.encode(uri, "UTF-8")}"
    }"""

content = content.replace(target, replacement)

target2 = """            is SidebarItem.IntentAction -> {
                // If it's an intent, we try to load the icon of the package that handles it
                try {
                    val uriStr = item.uri
                    val intent = android.content.Intent.parseUri(uriStr, android.content.Intent.URI_INTENT_SCHEME)
                    val pkg = intent.`package` ?: intent.component?.packageName
                    if (pkg != null) {
                        return loadIcon(pkg)
                    }
                } catch (e: Exception) {}
                android.R.drawable.ic_menu_set_as
            }"""

replacement2 = """            is SidebarItem.IntentAction -> {
                if (item.iconPath != null) {
                    try {
                        val file = java.io.File(item.iconPath)
                        if (file.exists()) {
                            return android.graphics.BitmapFactory.decodeFile(file.absolutePath)
                        }
                    } catch(e:Exception){}
                }
                // If it's an intent, we try to load the icon of the package that handles it
                try {
                    val uriStr = item.uri
                    val intent = android.content.Intent.parseUri(uriStr, android.content.Intent.URI_INTENT_SCHEME)
                    val pkg = intent.`package` ?: intent.component?.packageName
                    if (pkg != null) {
                        return loadIcon(pkg)
                    }
                } catch (e: Exception) {}
                android.R.drawable.ic_menu_set_as
            }"""
content = content.replace(target2, replacement2)

target3 = """        } else if (id.startsWith("intent:")) {
            try {
                val parts = id.split(":", limit = 3)
                if (parts.size >= 3) {
                    val name = java.net.URLDecoder.decode(parts[1], "UTF-8")
                    val uri = java.net.URLDecoder.decode(parts[2], "UTF-8")
                    return SidebarItem.IntentAction(uri, name)
                }
            } catch (e: Exception) {}"""

replacement3 = """        } else if (id.startsWith("intent:")) {
            try {
                val parts = id.split(":", limit = 4)
                if (parts.size >= 3) {
                    val name = java.net.URLDecoder.decode(parts[1], "UTF-8")
                    val uri = java.net.URLDecoder.decode(parts[2], "UTF-8")
                    val iconPath = if (parts.size >= 4) parts[3] else null
                    return SidebarItem.IntentAction(uri, name, iconPath)
                }
            } catch (e: Exception) {}"""

content = content.replace(target3, replacement3)

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "w") as f:
    f.write(content)
