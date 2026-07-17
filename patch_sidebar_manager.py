import re

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "r") as f:
    content = f.read()

target = """        if (id.startsWith("app:")) {
            val pkg = id.substringAfter("app:")
            val appInfo = allInstalledApps.find { it.packageName == pkg }
            if (appInfo != null) {
                return SidebarItem.App(appInfo.packageName, appInfo.label)
            }
        }"""

replacement = """        if (id.startsWith("app:")) {
            val pkg = id.substringAfter("app:")
            val appInfo = allInstalledApps.find { it.packageName == pkg }
            if (appInfo != null) {
                return SidebarItem.App(appInfo.packageName, appInfo.label)
            } else {
                try {
                    val pm = context.packageManager
                    val info = pm.getApplicationInfo(pkg, 0)
                    val label = pm.getApplicationLabel(info).toString()
                    return SidebarItem.App(pkg, label)
                } catch(e: Exception) {
                    return SidebarItem.App(pkg, pkg)
                }
            }
        }"""

content = content.replace(target, replacement)

target2 = """        val result = mutableListOf<SidebarItem>()
        for (id in selectedIds) {
            if (id.startsWith("app:")) {
                val pkg = id.substringAfter("app:")
                val appInfo = allInstalledApps.find { it.packageName == pkg }
                if (appInfo != null) {
                    result.add(SidebarItem.App(appInfo.packageName, appInfo.label))
                }
            } else if (id.startsWith("intent:")) {"""

replacement2 = """        val result = mutableListOf<SidebarItem>()
        for (id in selectedIds) {
            val parsed = parseId(id)
            if (parsed != null) {
                result.add(parsed)
                continue
            }
            if (id.startsWith("app:")) {
                val pkg = id.substringAfter("app:")
                val appInfo = allInstalledApps.find { it.packageName == pkg }
                if (appInfo != null) {
                    result.add(SidebarItem.App(appInfo.packageName, appInfo.label))
                }
            } else if (id.startsWith("intent:")) {"""

content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "w") as f:
    f.write(content)
