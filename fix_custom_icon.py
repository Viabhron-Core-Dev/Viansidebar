import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

old_code = """                } else {
                    serviceScope.launch {
                        val bitmap = manager.loadIcon(customIconStr)
                        if (bitmap != null) {
                            withContext(Dispatchers.Main) {
                                icon.setImageBitmap(bitmap)
                            }
                        }
                    }
                }
                return
            }"""

new_code = """                } else {
                    val cached = manager.iconCache.get(customIconStr)
                    if (cached != null) {
                        icon.setImageBitmap(cached)
                    } else {
                        serviceScope.launch {
                            val bitmap = manager.loadIcon(customIconStr)
                            if (bitmap != null) {
                                withContext(Dispatchers.Main) {
                                    icon.setImageBitmap(bitmap)
                                }
                            }
                        }
                    }
                }
                return
            }"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)
