import re

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "r") as f:
    content = f.read()

target1 = """                            CoroutineScope(Dispatchers.Main).launch {
                                val bmp = appsManager.getIconBitmap(item.id)
                                if (bmp != null) {
                                    icon.setImageBitmap(bmp)
                                }
                            }"""
replacement1 = """                            appsManager.bindIcon(item.id, icon, prefs, serviceScope) {
                                // For folders, we need to refresh the view to show the loaded mini icons
                                appsManager.bindIcon(item.id, icon, prefs, serviceScope) {}
                            }"""
content = content.replace(target1, replacement1)

target2 = """            CoroutineScope(Dispatchers.Main).launch {
                val bmp = appsManager.getIconBitmap(itemId)
                if (bmp != null) icon.setImageBitmap(bmp)
            }"""
replacement2 = """            appsManager.bindIcon(itemId, icon, prefs, serviceScope) {}"""
content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "w") as f:
    f.write(content)
