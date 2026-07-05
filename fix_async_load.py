import re

def update_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # AppsPageView pattern
    old_code1 = """                if (miniIcons.size < minOf(item.items.size, 9) && item.items.any { it.startsWith("app:") }) {
                    serviceScope.launch {
                        var newlyLoaded = false
                        for (it in item.items.take(9)) {
                            if (it.startsWith("app:")) {
                                if (manager.getIconBitmap(it) == null) {
                                    val bitmap = manager.loadIcon(it.substringAfter("app:"))
                                    if (bitmap != null) {
                                        newlyLoaded = true
                                    }
                                }
                            }
                        }"""
    
    new_code1 = """                if (miniIcons.size < minOf(item.items.size, 9)) {
                    serviceScope.launch {
                        var newlyLoaded = false
                        for (subItem in item.items.take(9)) {
                            if (manager.getIconBitmap(subItem) == null) {
                                val pkg = when {
                                    subItem.startsWith("app:") -> subItem.substringAfter("app:")
                                    subItem.startsWith("intent:") -> subItem.substringAfter("intent:").split("/").getOrNull(0) ?: ""
                                    else -> ""
                                }
                                if (pkg.isNotEmpty()) {
                                    val bitmap = manager.loadIcon(pkg)
                                    if (bitmap != null) {
                                        newlyLoaded = true
                                    }
                                }
                            }
                        }"""

    if old_code1 in content:
        content = content.replace(old_code1, new_code1)

    # SidebarEditOverlayView pattern
    old_code2 = """                if (miniIcons.size < minOf(item.items.size, 9) && item.items.any { it.startsWith("app:") }) {
                    serviceScope.launch {
                        var newlyLoaded = false
                        for (subItem in item.items.take(9)) {
                            if (subItem.startsWith("app:")) {
                                if (manager.getIconBitmap(subItem) == null) {
                                    val bitmap = manager.loadIcon(subItem.substringAfter("app:"))
                                    if (bitmap != null) {
                                        newlyLoaded = true
                                    }
                                }
                            }
                        }"""

    if old_code2 in content:
        content = content.replace(old_code2, new_code1)

    with open(filename, 'w') as f:
        f.write(content)

update_file('app/src/main/java/com/example/service/AppsPageView.kt')
update_file('app/src/main/java/com/example/service/SidebarEditOverlayView.kt')

