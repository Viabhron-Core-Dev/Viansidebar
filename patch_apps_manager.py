import re

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "r") as f:
    content = f.read()

helper_method = """
    fun bindIcon(id: String, icon: android.widget.ImageView, prefs: android.content.SharedPreferences, coroutineScope: kotlinx.coroutines.CoroutineScope, onUpdate: () -> Unit) {
        val parsed = parseId(id) ?: return
        val customIconFile = java.io.File(context.filesDir, "custom_icons/${id.replace(Regex("[^a-zA-Z0-9.-]"), "_")}.webp")
        if (customIconFile.exists()) {
            val customCached = iconCache.get("custom_${id}") ?: android.graphics.BitmapFactory.decodeFile(customIconFile.absolutePath)?.also { iconCache.put("custom_${id}", it) }
            if (customCached != null) {
                icon.setImageDrawable(null)
                icon.clearColorFilter()
                icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                icon.setImageBitmap(customCached)
                return
            }
        }
        val customIconStr = prefs.getString("custom_icon_${id}", null)
        if (!customIconStr.isNullOrEmpty()) {
            icon.setImageDrawable(null)
            icon.clearColorFilter()
            icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
            if (customIconStr.length <= 4 && !customIconStr.contains(".")) {
                val paint = android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG)
                paint.textSize = 28f * context.resources.displayMetrics.density
                paint.color = android.graphics.Color.WHITE
                paint.textAlign = android.graphics.Paint.Align.LEFT
                val baseline = -paint.ascent()
                val width = (paint.measureText(customIconStr) + 0.5f).toInt().coerceAtLeast(1)
                val height = (baseline + paint.descent() + 0.5f).toInt().coerceAtLeast(1)
                val bitmap = android.graphics.Bitmap.createBitmap(width, height, android.graphics.Bitmap.Config.ARGB_8888)
                val canvas = android.graphics.Canvas(bitmap)
                canvas.drawText(customIconStr, 0f, baseline, paint)
                icon.setImageBitmap(bitmap)
            } else {
                val cached = iconCache.get(customIconStr)
                if (cached != null) {
                    icon.setImageBitmap(cached)
                } else {
                    coroutineScope.launch {
                        val bitmap = loadIcon(customIconStr)
                        if (bitmap != null) {
                            kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                                icon.setImageBitmap(bitmap)
                            }
                        }
                    }
                }
            }
            return
        }
        
        if (parsed is SidebarItem.App) {
            val cached = getIconBitmap(id)
            if (cached != null) {
                icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                icon.setImageBitmap(cached)
            } else {
                coroutineScope.launch {
                    val bitmap = loadIcon(parsed.packageName)
                    if (bitmap != null) {
                        kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                            icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                            icon.setImageBitmap(bitmap)
                        }
                    }
                }
            }
        } else if (parsed is SidebarItem.IntentAction) {
            val pkg = try {
                android.content.Intent.parseUri(parsed.uri, android.content.Intent.URI_INTENT_SCHEME).`package` ?: android.content.Intent.parseUri(parsed.uri, android.content.Intent.URI_INTENT_SCHEME).component?.packageName ?: ""
            } catch (e: Exception) { "" }
            val cached = getIconBitmap(id)
            if (cached != null) {
                icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                icon.setImageBitmap(cached)
            } else {
                coroutineScope.launch {
                    var customIconBitmap: android.graphics.Bitmap? = null
                    if (parsed.iconPath != null) {
                        try {
                            val file = java.io.File(parsed.iconPath)
                            if (file.exists()) {
                                customIconBitmap = android.graphics.BitmapFactory.decodeFile(file.absolutePath)
                            }
                        } catch(e: Exception) {}
                    }
                    val bitmap = customIconBitmap ?: loadIcon(pkg)
                    if (bitmap != null) {
                        kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                            icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                            icon.setImageBitmap(bitmap)
                        }
                    }
                }
            }
        } else if (parsed is SidebarItem.Widget) {
            val cached = getIconBitmap(id)
            if (cached != null) {
                icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                icon.setImageBitmap(cached)
            }
        } else if (parsed is SidebarItem.QuickTile) {
            icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
            icon.setImageResource(parsed.iconResId)
            icon.setColorFilter(android.graphics.Color.WHITE)
        } else if (parsed is SidebarItem.SystemAction) {
            icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
            if (parsed.action == "screen_record" && com.example.service.ScreenRecordService.isRecording) {
                icon.setImageResource(android.R.drawable.ic_media_pause)
                icon.setColorFilter(android.graphics.Color.RED)
            } else {
                icon.setImageResource(parsed.iconResId)
                icon.setColorFilter(android.graphics.Color.WHITE)
            }
        } else if (parsed is SidebarItem.VolumeAction || parsed is SidebarItem.MediaAction || parsed is SidebarItem.DisplayAction || parsed is SidebarItem.SettingsShortcut || parsed is SidebarItem.Link) {
            val cached = getIconBitmap(id)
            if (cached != null) {
                icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                icon.setImageBitmap(cached)
            } else {
                icon.setImageResource(android.R.drawable.ic_menu_gallery)
            }
        } else if (parsed is SidebarItem.Folder) {
            icon.setImageDrawable(null)
            icon.clearColorFilter()
            icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
            
            val cHex = try { android.graphics.Color.parseColor(parsed.colorHex) } catch(e:Exception){ android.graphics.Color.parseColor("#00BFA5") }
            val iconC = android.graphics.Color.WHITE
            
            val miniIcons = parsed.items.take(9).mapNotNull { getIconBitmap(it) }
            icon.setImageDrawable(com.example.service.FolderStyleDrawable(parsed.folderStyle, cHex, iconC, miniIcons))
            
            if (miniIcons.size < kotlin.math.min(parsed.items.size, 9)) {
                coroutineScope.launch {
                    var newlyLoaded = false
                    for (subItem in parsed.items.take(9)) {
                        if (getIconBitmap(subItem) == null) {
                            val pkg = when {
                                subItem.startsWith("app:") -> subItem.substringAfter("app:")
                                subItem.startsWith("intent:") -> subItem.substringAfter("intent:").split("/").getOrNull(0) ?: ""
                                else -> ""
                            }
                            if (pkg.isNotEmpty()) {
                                val bitmap = loadIcon(pkg)
                                if (bitmap != null) {
                                    newlyLoaded = true
                                }
                            }
                        }
                    }
                    if (newlyLoaded) {
                        kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                            onUpdate()
                        }
                    }
                }
            }
        }
    }
"""

content = content.replace("    fun getIconBitmap(id: String): Bitmap? {", helper_method + "\n    fun getIconBitmap(id: String): Bitmap? {")

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "w") as f:
    f.write(content)
