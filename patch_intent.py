with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "r") as f:
    content = f.read()

target1 = """        } else if (id.startsWith("intent:")) {
            val componentStr = id.substringAfter("intent:")
            val pkg = componentStr.split("/").getOrNull(0) ?: ""
            val cls = componentStr.split("/").getOrNull(1) ?: ""
            val appInfo = allInstalledApps.find { it.packageName == pkg }
            val label = if (appInfo != null) "${appInfo.label} - ${cls.substringAfterLast(".")}" else cls
            return SidebarItem.IntentAction(componentStr, label)"""

replacement1 = """        } else if (id.startsWith("intent:")) {
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
            }"""

target2 = """            } else if (id.startsWith("intent:")) {
                val componentStr = id.substringAfter("intent:")
                val pkg = componentStr.split("/").getOrNull(0) ?: ""
                val cls = componentStr.split("/").getOrNull(1) ?: ""
                val appInfo = allInstalledApps.find { it.packageName == pkg }
                val label = if (appInfo != null) "${appInfo.label} - ${cls.substringAfterLast(".")}" else cls
                result.add(SidebarItem.IntentAction(componentStr, label))"""

replacement2 = """            } else if (id.startsWith("intent:")) {
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
                }"""

content = content.replace(target1, replacement1)
content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "w") as f:
    f.write(content)
