import re

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'r') as f:
    content = f.read()

old_code = """            if (item is SidebarItem.App) {
                serviceScope.launch {
                    val bitmap = manager.loadIcon(item.packageName)
                    if (bitmap != null) {
                        withContext(Dispatchers.Main) {
                            holder.icon.setBackgroundColor(Color.TRANSPARENT)
                            holder.icon.setImageBitmap(bitmap)
                        }
                    } else {
                        withContext(Dispatchers.Main) {
                            holder.icon.setImageResource(android.R.mipmap.sym_def_app_icon)
                        }
                    }
                }
            } else if (item is SidebarItem.IntentAction) {"""

new_code = """            if (item is SidebarItem.App) {
                val cached = manager.getIconBitmap(item.id)
                if (cached != null) {
                    holder.icon.setBackgroundColor(Color.TRANSPARENT)
                    holder.icon.setImageBitmap(cached)
                } else {
                    serviceScope.launch {
                        val bitmap = manager.loadIcon(item.packageName)
                        if (bitmap != null) {
                            withContext(Dispatchers.Main) {
                                holder.icon.setBackgroundColor(Color.TRANSPARENT)
                                holder.icon.setImageBitmap(bitmap)
                            }
                        } else {
                            withContext(Dispatchers.Main) {
                                holder.icon.setImageResource(android.R.mipmap.sym_def_app_icon)
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
                            holder.icon.setBackgroundColor(Color.TRANSPARENT)
                            holder.icon.setImageBitmap(bitmap)
                        }
                    } else {
                        withContext(Dispatchers.Main) {
                            holder.icon.setImageResource(android.R.mipmap.sym_def_app_icon)
                        }
                    }
                }
            } else if (item is SidebarItem.SystemAction"""

new_code2 = """            } else if (item is SidebarItem.IntentAction) {
                val pkg = item.componentStr.split("/").getOrNull(0) ?: ""
                val cached = manager.getIconBitmap(item.id)
                if (cached != null) {
                    holder.icon.setBackgroundColor(Color.TRANSPARENT)
                    holder.icon.setImageBitmap(cached)
                } else {
                    serviceScope.launch {
                        val bitmap = manager.loadIcon(pkg)
                        if (bitmap != null) {
                            withContext(Dispatchers.Main) {
                                holder.icon.setBackgroundColor(Color.TRANSPARENT)
                                holder.icon.setImageBitmap(bitmap)
                            }
                        } else {
                            withContext(Dispatchers.Main) {
                                holder.icon.setImageResource(android.R.mipmap.sym_def_app_icon)
                            }
                        }
                    }
                }
            } else if (item is SidebarItem.SystemAction"""

content = content.replace(old_code2, new_code2)

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'w') as f:
    f.write(content)
