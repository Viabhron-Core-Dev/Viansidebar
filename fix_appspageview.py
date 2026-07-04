import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

old_code = """                if (miniIcons.size < minOf(item.items.size, 9) && item.items.any { it.startsWith("app:") }) {
                    serviceScope.launch {
                        var loadedAny = false
                        for (it in item.items.take(9)) {
                            if (it.startsWith("app:")) {
                                val bitmap = manager.loadIcon(it.substringAfter("app:"))
                                if (bitmap != null) {
                                    loadedAny = true
                                }
                            }
                        }
                        if (loadedAny) {
                            withContext(Dispatchers.Main) {
                                adapter.notifyItemChanged(position)
                            }
                        }
                    }
                }"""

new_code = """                if (miniIcons.size < minOf(item.items.size, 9) && item.items.any { it.startsWith("app:") }) {
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
                        }
                        if (newlyLoaded) {
                            withContext(Dispatchers.Main) {
                                adapter.notifyItemChanged(position)
                            }
                        }
                    }
                }"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)
