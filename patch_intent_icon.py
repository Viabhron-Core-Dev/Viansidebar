import re

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "r") as f:
    content = f.read()

target = """                            } else if (item is com.example.service.SidebarItem.IntentAction) {
                                try {
                                    val uriStr = item.uri
                                    val pkg = android.content.Intent.parseUri(uriStr, android.content.Intent.URI_INTENT_SCHEME).`package` ?: android.content.Intent.parseUri(uriStr, android.content.Intent.URI_INTENT_SCHEME).component?.packageName ?: ""
                                    val loaded = manager.loadIcon(pkg)
                                    if (loaded != null && holder.iconView.tag == id) {
                                        holder.iconView.setImageBitmap(loaded)
                                    }
                                } catch (e: Exception) {}
                            }"""

replacement = """                            } else if (item is com.example.service.SidebarItem.IntentAction) {
                                var customIconLoaded = false
                                if (item.iconPath != null) {
                                    try {
                                        val file = java.io.File(item.iconPath)
                                        if (file.exists()) {
                                            val bmp = android.graphics.BitmapFactory.decodeFile(file.absolutePath)
                                            if (bmp != null && holder.iconView.tag == id) {
                                                holder.iconView.setImageBitmap(bmp)
                                                customIconLoaded = true
                                            }
                                        }
                                    } catch(e: Exception){}
                                }
                                if (!customIconLoaded) {
                                    try {
                                        val uriStr = item.uri
                                        val pkg = android.content.Intent.parseUri(uriStr, android.content.Intent.URI_INTENT_SCHEME).`package` ?: android.content.Intent.parseUri(uriStr, android.content.Intent.URI_INTENT_SCHEME).component?.packageName ?: ""
                                        val loaded = manager.loadIcon(pkg)
                                        if (loaded != null && holder.iconView.tag == id) {
                                            holder.iconView.setImageBitmap(loaded)
                                        }
                                    } catch (e: Exception) {}
                                }
                            }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/SidebarEditActivity.kt", "w") as f:
    f.write(content)
