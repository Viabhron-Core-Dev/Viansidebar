import re

with open("app/src/main/java/com/example/SidebarEditActivity.kt", "r") as f:
    content = f.read()

target = """                        if (iconBitmap != null) {
                            holder.iconView.setImageBitmap(iconBitmap)
                        } else {
                            holder.iconView.setImageResource(android.R.drawable.sym_def_app_icon)
                            if (item is com.example.service.SidebarItem.App) {
                                val loaded = manager.loadIcon(item.packageName)
                                if (loaded != null) {
                                    holder.iconView.setImageBitmap(loaded)
                                }
                            } else if (item is com.example.service.SidebarItem.IntentAction) {
                                try {
                                    val uriStr = item.uri
                                    val pkg = android.content.Intent.parseUri(uriStr, android.content.Intent.URI_INTENT_SCHEME).`package` ?: android.content.Intent.parseUri(uriStr, android.content.Intent.URI_INTENT_SCHEME).component?.packageName ?: ""
                                    val loaded = manager.loadIcon(pkg)
                                    if (loaded != null) {
                                        holder.iconView.setImageBitmap(loaded)
                                    }
                                } catch (e: Exception) {}
                            }
                        }"""

replacement = """                        holder.iconView.tag = id
                        if (item is com.example.service.SidebarItem.Folder) {
                            holder.iconView.setImageDrawable(null)
                            holder.iconView.clearColorFilter()
                            holder.iconView.setBackgroundColor(Color.TRANSPARENT)
                            
                            val cHex = try { Color.parseColor(item.colorHex) } catch(e:Exception){ Color.parseColor("#00BFA5") }
                            val iconC = Color.WHITE
                            
                            val miniIcons = item.items.take(9).mapNotNull { manager.getIconBitmap(it) }
                            holder.iconView.setImageDrawable(com.example.service.FolderStyleDrawable(item.folderStyle, cHex, iconC, miniIcons))
                        } else if (iconBitmap != null) {
                            holder.iconView.setImageBitmap(iconBitmap)
                        } else {
                            holder.iconView.setImageResource(android.R.drawable.sym_def_app_icon)
                            if (item is com.example.service.SidebarItem.App) {
                                val loaded = manager.loadIcon(item.packageName)
                                if (loaded != null && holder.iconView.tag == id) {
                                    holder.iconView.setImageBitmap(loaded)
                                }
                            } else if (item is com.example.service.SidebarItem.IntentAction) {
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
