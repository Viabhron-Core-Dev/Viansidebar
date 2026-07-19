import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

# Add BroadcastReceiver at the end of the class
if "iconUpdateReceiver" not in content:
    content = content.replace("    private inner class AppsAdapter", 
"""
    private val iconUpdateReceiver = object : android.content.BroadcastReceiver() {
        override fun onReceive(context: Context, intent: Intent) {
            val itemId = intent.getStringExtra("item_id")
            if (itemId != null) {
                manager.iconCache.remove("custom_$itemId")
                manager.iconCache.remove(itemId)
                adapter.notifyDataSetChanged()
            }
        }
    }

    override fun onAttachedToWindow() {
        super.onAttachedToWindow()
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
            context.registerReceiver(iconUpdateReceiver, android.content.IntentFilter("com.example.UPDATE_SIDEBAR_ICONS"), Context.RECEIVER_NOT_EXPORTED)
        } else {
            context.registerReceiver(iconUpdateReceiver, android.content.IntentFilter("com.example.UPDATE_SIDEBAR_ICONS"))
        }
    }

    override fun onDetachedFromWindow() {
        super.onDetachedFromWindow()
        try {
            context.unregisterReceiver(iconUpdateReceiver)
        } catch(e: Exception) {}
    }

    private inner class AppsAdapter""")

# Update setOnLongClickListener
long_click_pattern = r"""            itemView\.setOnLongClickListener \{
                val actionList = mutableListOf<String>\(\)
                if \(item is SidebarItem\.App\) \{
                    actionList\.add\("App Info"\)
                \}
                actionList\.add\("Remove"\)"""

long_click_replacement = """            itemView.setOnLongClickListener {
                val actionList = mutableListOf<String>()
                if (item is SidebarItem.App) {
                    actionList.add("App Info")
                }
                actionList.add("Change Icon")
                val customIconFile = java.io.File(context.filesDir, "custom_icons/${item.id.replace(Regex("[^a-zA-Z0-9.-]"), "_")}.webp")
                if (customIconFile.exists()) {
                    actionList.add("Reset Icon")
                }
                actionList.add("Remove")"""

content = re.sub(long_click_pattern, long_click_replacement, content)

# Update popup actions
action_pattern = r"""                            when \(action\) \{
                                "Remove" -> manager\.removeItem\(item\.id\)"""

action_replacement = """                            when (action) {
                                "Remove" -> manager.removeItem(item.id)
                                "Change Icon" -> {
                                    val intent = android.content.Intent(context, com.example.IconPickerActivity::class.java).apply {
                                        putExtra("item_id", item.id)
                                        addFlags(android.content.Intent.FLAG_ACTIVITY_NEW_TASK)
                                    }
                                    context.startActivity(intent)
                                    currentFolderPopup?.dismiss()
                                    onCloseSidebar()
                                }
                                "Reset Icon" -> {
                                    val file = java.io.File(context.filesDir, "custom_icons/${item.id.replace(Regex("[^a-zA-Z0-9.-]"), "_")}.webp")
                                    if (file.exists()) file.delete()
                                    manager.iconCache.remove("custom_${item.id}")
                                    manager.iconCache.remove(item.id)
                                    context.sendBroadcast(android.content.Intent("com.example.UPDATE_SIDEBAR_ICONS").apply {
                                        putExtra("item_id", item.id)
                                    })
                                    currentFolderPopup?.dismiss()
                                }"""

content = re.sub(action_pattern, action_replacement, content)

# Update icon binding logic inside AppViewHolder.bind
bind_pattern = r"""            val customIconStr = prefs\.getString\("custom_icon_\$\{item\.id\}", null\)"""

bind_replacement = """            val customIconFile = java.io.File(view.context.filesDir, "custom_icons/${item.id.replace(Regex("[^a-zA-Z0-9.-]"), "_")}.webp")
            if (customIconFile.exists()) {
                val customCached = manager.iconCache.get("custom_${item.id}") ?: android.graphics.BitmapFactory.decodeFile(customIconFile.absolutePath)?.also { manager.iconCache.put("custom_${item.id}", it) }
                if (customCached != null) {
                    icon.setImageDrawable(null)
                    icon.clearColorFilter()
                    icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                    icon.setImageBitmap(customCached)
                    return
                }
            }
            val customIconStr = prefs.getString("custom_icon_${item.id}", null)"""

content = re.sub(bind_pattern, bind_replacement, content)

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)

