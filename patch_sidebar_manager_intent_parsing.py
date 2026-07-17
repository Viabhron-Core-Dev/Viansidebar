import re

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "r") as f:
    content = f.read()

target1 = """        } else if (id.startsWith("intent:")) {
            val parts = id.split(":")
            if (parts.size >= 3) {
                val encodedLabel = parts[1]
                val encodedUri = id.substringAfter("intent:$encodedLabel:")
                val label = java.net.URLDecoder.decode(encodedLabel, "UTF-8")
                val uri = java.net.URLDecoder.decode(encodedUri, "UTF-8")
                return SidebarItem.IntentAction(uri, label)
            } else {
                val componentStr = id.substringAfter("intent:")
                return SidebarItem.IntentAction(componentStr, componentStr)
            }
        }"""

replacement1 = """        } else if (id.startsWith("intent:")) {
            val parts = id.split(":", limit = 4)
            if (parts.size >= 3) {
                val encodedLabel = parts[1]
                val encodedUri = parts[2]
                val iconPath = if (parts.size >= 4) parts[3] else null
                val label = java.net.URLDecoder.decode(encodedLabel, "UTF-8")
                val uri = java.net.URLDecoder.decode(encodedUri, "UTF-8")
                return SidebarItem.IntentAction(uri, label, iconPath)
            } else {
                val componentStr = id.substringAfter("intent:")
                return SidebarItem.IntentAction(componentStr, componentStr)
            }
        }"""

content = content.replace(target1, replacement1)

target2 = """            } else if (id.startsWith("intent:")) {
                val parts = id.split(":")
                if (parts.size >= 3) {
                    val encodedLabel = parts[1]
                    val encodedUri = id.substringAfter("intent:$encodedLabel:")
                    val label = java.net.URLDecoder.decode(encodedLabel, "UTF-8")
                    val uri = java.net.URLDecoder.decode(encodedUri, "UTF-8")
                    result.add(SidebarItem.IntentAction(uri, label))
                } else {
                    val componentStr = id.substringAfter("intent:")
                    result.add(SidebarItem.IntentAction(componentStr, componentStr))
                }
            }"""

replacement2 = """            } else if (id.startsWith("intent:")) {
                val parts = id.split(":", limit = 4)
                if (parts.size >= 3) {
                    val encodedLabel = parts[1]
                    val encodedUri = parts[2]
                    val iconPath = if (parts.size >= 4) parts[3] else null
                    val label = java.net.URLDecoder.decode(encodedLabel, "UTF-8")
                    val uri = java.net.URLDecoder.decode(encodedUri, "UTF-8")
                    result.add(SidebarItem.IntentAction(uri, label, iconPath))
                } else {
                    val componentStr = id.substringAfter("intent:")
                    result.add(SidebarItem.IntentAction(componentStr, componentStr))
                }
            }"""

content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "w") as f:
    f.write(content)
