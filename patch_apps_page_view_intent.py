import re

with open("app/src/main/java/com/example/service/AppsPageView.kt", "r") as f:
    content = f.read()

target = """            } else if (item is SidebarItem.IntentAction) {
                val pkg = try {
                    android.content.Intent.parseUri(item.uri, android.content.Intent.URI_INTENT_SCHEME).`package` ?: android.content.Intent.parseUri(item.uri, android.content.Intent.URI_INTENT_SCHEME).component?.packageName ?: ""
                } catch (e: Exception) { "" }
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
            } else if (item is SidebarItem.QuickTile) {"""

replacement = """            } else if (item is SidebarItem.IntentAction) {
                val pkg = try {
                    android.content.Intent.parseUri(item.uri, android.content.Intent.URI_INTENT_SCHEME).`package` ?: android.content.Intent.parseUri(item.uri, android.content.Intent.URI_INTENT_SCHEME).component?.packageName ?: ""
                } catch (e: Exception) { "" }
                val cached = manager.getIconBitmap(item.id)
                if (cached != null) {
                    icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                    icon.setImageBitmap(cached)
                } else {
                    serviceScope.launch {
                        var customIconBitmap: android.graphics.Bitmap? = null
                        if (item.iconPath != null) {
                            try {
                                val file = java.io.File(item.iconPath)
                                if (file.exists()) {
                                    customIconBitmap = android.graphics.BitmapFactory.decodeFile(file.absolutePath)
                                }
                            } catch(e: Exception) {}
                        }
                        
                        val bitmap = customIconBitmap ?: manager.loadIcon(pkg)
                        if (bitmap != null) {
                            withContext(Dispatchers.Main) {
                                icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                                icon.setImageBitmap(bitmap)
                            }
                        }
                    }
                }
            } else if (item is SidebarItem.QuickTile) {"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/service/AppsPageView.kt", "w") as f:
    f.write(content)
