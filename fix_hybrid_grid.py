import re

# 1. Update SidebarAppsManager.kt
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
            } else if (parsed.action == "blue_light_filter" && com.example.service.BlueLightFilterManager.isEnabled) {
                icon.setImageResource(parsed.iconResId)
                icon.setColorFilter(android.graphics.Color.parseColor("#FF9900"))
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
if "fun bindIcon(id: String" not in content:
    content = content.replace("    fun getIconBitmap(id: String): Bitmap? {", helper_method + "\n    fun getIconBitmap(id: String): Bitmap? {")
    with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "w") as f:
        f.write(content)

# 2. Update HybridGridPageView.kt
with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "r") as f:
    content = f.read()

# Replace main grid icon loading
target1 = """                            CoroutineScope(Dispatchers.Main).launch {
                                val bmp = appsManager.getIconBitmap(item.id)
                                if (bmp != null) {
                                    icon.setImageBitmap(bmp)
                                }
                            }"""
replacement1 = """                            appsManager.bindIcon(item.id, icon, prefs, CoroutineScope(Dispatchers.Main)) {
                                appsManager.bindIcon(item.id, icon, prefs, CoroutineScope(Dispatchers.Main)) {}
                            }"""
content = content.replace(target1, replacement1)

# Replace showFolderPopup entirely
target_popup_start = "    private fun showFolderPopup(anchor: View, folder: SidebarItem.Folder, appsManager: SidebarAppsManager) {"
target_popup_end = "    private fun showWidgetPopup(anchor: View, widget: SidebarItem.PopupWidget) {"

start_idx = content.find(target_popup_start)
end_idx = content.find(target_popup_end)

if start_idx != -1 and end_idx != -1:
    new_popup = """    private fun showFolderPopup(anchor: View, folder: SidebarItem.Folder, appsManager: SidebarAppsManager) {
        val density = context.resources.displayMetrics.density
        val popupView = FrameLayout(context)
        val recyclerView = RecyclerView(context)
        val padding = (16 * density).toInt()
        recyclerView.setPadding(padding, padding, padding, padding)
        popupView.addView(recyclerView, FrameLayout.LayoutParams(FrameLayout.LayoutParams.WRAP_CONTENT, FrameLayout.LayoutParams.WRAP_CONTENT))

        val maxCols = if (folder.popupColumns > 0) folder.popupColumns else prefs.getInt("sidebar_columns", 3)
        val columns = if (folder.items.size <= maxCols && folder.items.isNotEmpty()) folder.items.size else maxCols
        val validCols = if (columns > 0) columns else 1
        
        recyclerView.layoutManager = GridLayoutManager(context, validCols)

        val popupOpacity = prefs.getFloat("sidebar_transparency", 0.9f)
        val popupBg = android.graphics.drawable.GradientDrawable()
        popupBg.setColor(Color.parseColor("#1A1A1A"))
        popupBg.alpha = (popupOpacity * 255).toInt()
        popupBg.cornerRadius = 16 * density
        popupView.background = popupBg

        val itemWidthDp = 72
        val itemHeightDp = 72
        val autoRows = Math.ceil(folder.items.size.toDouble() / validCols).toInt()
        val rows = if (folder.popupRows > 0) kotlin.math.min(folder.popupRows, autoRows) else autoRows
        val displayRows = if (folder.popupRows > 0) folder.popupRows else rows

        val totalWidth = (validCols * itemWidthDp * density + padding * 2).toInt()
        val totalHeight = (displayRows * itemHeightDp * density + padding * 2).toInt()
        
        popupView.layoutParams = ViewGroup.LayoutParams(totalWidth, totalHeight)

        var popupWindow: PopupWindow? = null
        
        val adapter = object : RecyclerView.Adapter<RecyclerView.ViewHolder>() {
            override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerView.ViewHolder {
                val view = android.view.LayoutInflater.from(context).inflate(com.example.R.layout.item_sidebar_app, parent, false)
                return object : RecyclerView.ViewHolder(view) {}
            }
            override fun getItemCount() = folder.items.size
            override fun onBindViewHolder(holder: RecyclerView.ViewHolder, position: Int) {
                val itemId = folder.items[position]
                val parsed = appsManager.parseId(itemId) ?: return
                val icon = holder.itemView.findViewById<android.widget.ImageView>(com.example.R.id.app_icon)
                val label = holder.itemView.findViewById<android.widget.TextView>(com.example.R.id.app_label)
                label.text = parsed.label
                
                appsManager.bindIcon(itemId, icon, prefs, CoroutineScope(Dispatchers.Main)) {}
                
                holder.itemView.setOnClickListener {
                    if (parsed is SidebarItem.App) {
                        val intent = context.packageManager.getLaunchIntentForPackage(parsed.packageName)
                        if (intent != null) {
                            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                            try { context.startActivity(intent) } catch (e: Exception) {}
                            popupWindow?.dismiss()
                        }
                    } else if (parsed is SidebarItem.Link) {
                        try {
                            val intent = if (parsed.url.startsWith("intent:")) {
                                Intent.parseUri(parsed.url, Intent.URI_INTENT_SCHEME)
                            } else {
                                Intent(Intent.ACTION_VIEW, android.net.Uri.parse(parsed.url))
                            }
                            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                            context.startActivity(intent)
                            popupWindow?.dismiss()
                        } catch (e: Exception) {}
                    }
                }
                
                holder.itemView.setOnLongClickListener {
                    val actionList = mutableListOf<String>()
                    if (parsed is SidebarItem.App) {
                        actionList.add("App Info")
                    }
                    actionList.add("Change Icon")
                    val customIconFile = java.io.File(context.filesDir, "custom_icons/${itemId.replace(Regex("[^a-zA-Z0-9.-]"), "_")}.webp")
                    if (customIconFile.exists()) {
                        actionList.add("Reset Icon")
                    }
                    actionList.add("Remove")
                    
                    var actionMenuPopup: PopupWindow? = null
                    val popupLayout = LinearLayout(context).apply {
                        orientation = LinearLayout.VERTICAL
                        val pad = (8 * density).toInt()
                        setPadding(pad, pad, pad, pad)
                    }
                    
                    actionList.forEach { action ->
                        val actionView = TextView(context).apply {
                            text = action
                            setTextColor(Color.BLACK)
                            val padV = (10 * density).toInt()
                            val padH = (16 * density).toInt()
                            setPadding(padH, padV, padH, padV)
                            textSize = 14f
                            
                            val shape = android.graphics.drawable.GradientDrawable()
                            shape.shape = android.graphics.drawable.GradientDrawable.RECTANGLE
                            shape.cornerRadius = 24f * density
                            shape.setColor(Color.WHITE)
                            shape.setStroke(1, Color.LTGRAY)
                            background = shape
                            
                            layoutParams = LinearLayout.LayoutParams(
                                LinearLayout.LayoutParams.WRAP_CONTENT,
                                LinearLayout.LayoutParams.WRAP_CONTENT
                            ).apply {
                                setMargins(0, 0, 0, (8 * density).toInt())
                            }
                            
                            setOnClickListener {
                                actionMenuPopup?.dismiss()
                                when (action) {
                                    "Remove" -> {
                                        appsManager.removeItem(itemId)
                                        popupWindow?.dismiss()
                                    }
                                    "Change Icon" -> {
                                        val intent = Intent(context, com.example.IconPickerActivity::class.java).apply {
                                            putExtra("item_id", itemId)
                                            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                        }
                                        context.startActivity(intent)
                                        popupWindow?.dismiss()
                                    }
                                    "Reset Icon" -> {
                                        val file = java.io.File(context.filesDir, "custom_icons/${itemId.replace(Regex("[^a-zA-Z0-9.-]"), "_")}.webp")
                                        if (file.exists()) file.delete()
                                        appsManager.iconCache.remove("custom_${itemId}")
                                        appsManager.iconCache.remove(itemId)
                                        context.sendBroadcast(Intent("com.example.UPDATE_SIDEBAR_ICONS").apply {
                                            putExtra("item_id", itemId)
                                        })
                                        popupWindow?.dismiss()
                                    }
                                    "App Info" -> {
                                        if (parsed is SidebarItem.App) {
                                            try {
                                                val intent = Intent(android.provider.Settings.ACTION_APPLICATION_DETAILS_SETTINGS)
                                                intent.data = android.net.Uri.parse("package:${parsed.packageName}")
                                                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                                context.startActivity(intent)
                                                popupWindow?.dismiss()
                                            } catch (e: Exception) {}
                                        }
                                    }
                                }
                            }
                        }
                        popupLayout.addView(actionView)
                    }
                    
                    actionMenuPopup = PopupWindow(popupLayout, ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT, true).apply {
                        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                            windowLayoutType = android.view.WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
                        } else {
                            @Suppress("DEPRECATION")
                            windowLayoutType = android.view.WindowManager.LayoutParams.TYPE_PHONE
                        }
                        setBackgroundDrawable(android.graphics.drawable.ColorDrawable(Color.TRANSPARENT))
                        elevation = 8f * density
                    }
                    
                    val loc = IntArray(2)
                    holder.itemView.getLocationOnScreen(loc)
                    actionMenuPopup?.showAtLocation(holder.itemView, Gravity.NO_GRAVITY, loc[0] + holder.itemView.width / 4, loc[1] + holder.itemView.height / 2)
                    
                    true
                }
            }
        }
        recyclerView.adapter = adapter

        popupWindow = PopupWindow(
            popupView,
            ViewGroup.LayoutParams.WRAP_CONTENT,
            ViewGroup.LayoutParams.WRAP_CONTENT,
            true
        ).apply {
            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                windowLayoutType = android.view.WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            } else {
                @Suppress("DEPRECATION")
                windowLayoutType = android.view.WindowManager.LayoutParams.TYPE_PHONE
            }
            setBackgroundDrawable(android.graphics.drawable.ColorDrawable(Color.TRANSPARENT))
            isOutsideTouchable = true
        }

        val location = IntArray(2)
        anchor.getLocationOnScreen(location)
        val anchorX = location[0]
        val anchorY = location[1]
        val screenWidth = context.resources.displayMetrics.widthPixels
        val screenHeight = context.resources.displayMetrics.heightPixels

        var x = anchorX
        if (anchorX > screenWidth / 2) {
            x = anchorX - totalWidth
        } else {
            x = anchorX + anchor.width
        }

        var y = anchorY - (totalHeight / 2) + (anchor.height / 2)
        if (y < 0) y = 0
        if (y + totalHeight > screenHeight) y = screenHeight - totalHeight

        popupWindow.showAtLocation(anchor, Gravity.NO_GRAVITY, x, y)
    }
"""
    content = content[:start_idx] + new_popup + "\n" + content[end_idx:]
    with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "w") as f:
        f.write(content)
