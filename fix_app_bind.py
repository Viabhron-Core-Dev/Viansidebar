import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

old_code = """            if (item is SidebarItem.App) {
                serviceScope.launch {
                    val bitmap = manager.loadIcon(item.packageName)
                    if (bitmap != null) {
                        withContext(Dispatchers.Main) {
                            icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                            icon.setImageBitmap(bitmap)
                        }
                    }
                }
            } else if (item is SidebarItem.IntentAction) {"""

new_code = """            if (item is SidebarItem.App) {
                val cached = manager.getIconBitmap(item.id)
                if (cached != null) {
                    icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                    icon.setImageBitmap(cached)
                } else {
                    serviceScope.launch {
                        val bitmap = manager.loadIcon(item.packageName)
                        if (bitmap != null) {
                            withContext(Dispatchers.Main) {
                                icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                                icon.setImageBitmap(bitmap)
                            }
                        }
                    }
                }
            } else if (item is SidebarItem.IntentAction) {"""

content = content.replace(old_code, new_code)

old_code2 = """            } else if (item is SidebarItem.IntentAction) {
                val pkg = item.componentStr.split("/").getOrNull(0) ?: ""
                serviceScope.launch {
                    val bitmap = manager.loadIcon(pkg)
                    if (bitmap != null) {
                        withContext(Dispatchers.Main) {
                            icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                            icon.setImageBitmap(bitmap)
                        }
                    }
                }
            }"""

new_code2 = """            } else if (item is SidebarItem.IntentAction) {
                val pkg = item.componentStr.split("/").getOrNull(0) ?: ""
                val cached = manager.getIconBitmap(item.id)
                if (cached != null) {
                    icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                    icon.setImageBitmap(cached)
                } else {
                    serviceScope.launch {
                        val bitmap = manager.loadIcon(pkg)
                        if (bitmap != null) {
                            withContext(Dispatchers.Main) {
                                icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                                icon.setImageBitmap(bitmap)
                            }
                        }
                    }
                }
            }"""

content = content.replace(old_code2, new_code2)

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)
