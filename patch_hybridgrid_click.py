import os
import re

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "r") as f:
    content = f.read()

# Add imports if missing
if 'import android.widget.PopupWindow' not in content:
    content = content.replace('import android.widget.ScrollView', 'import android.widget.ScrollView\nimport android.widget.PopupWindow\nimport android.widget.TextView\nimport android.widget.LinearLayout\nimport androidx.recyclerview.widget.RecyclerView\nimport androidx.recyclerview.widget.GridLayoutManager\n')

# Find elementView.setOnClickListener and replace
pattern = r'elementView\.setOnClickListener \{[\s\S]*?context\.startService\(i\)\n                            \}'

repl = '''elementView.setOnClickListener {
                                if (parsed is SidebarItem.App) {
                                    val intent = context.packageManager.getLaunchIntentForPackage(parsed.packageName)
                                    if (intent != null) {
                                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                        try { context.startActivity(intent) } catch (e: Exception) {}
                                    }
                                } else if (parsed is SidebarItem.Folder) {
                                    showFolderPopup(elementView, parsed)
                                } else if (parsed is SidebarItem.PopupWidget) {
                                    showWidgetPopup(elementView, parsed)
                                } else if (parsed is SidebarItem.Link) {
                                    try {
                                        val intent = if (parsed.url.startsWith("intent:")) {
                                            Intent.parseUri(parsed.url, Intent.URI_INTENT_SCHEME)
                                        } else {
                                            Intent(Intent.ACTION_VIEW, android.net.Uri.parse(parsed.url))
                                        }
                                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                        context.startActivity(intent)
                                    } catch (e: Exception) {}
                                }
                            }
                            
                            elementView.setOnLongClickListener {
                                val actionList = mutableListOf<String>()
                                if (parsed is SidebarItem.App) {
                                    actionList.add("App Info")
                                }
                                actionList.add("Change Icon")
                                val customIconFile = java.io.File(context.filesDir, "custom_icons/${item.id.replace(Regex("[^a-zA-Z0-9.-]"), "_")}.webp")
                                if (customIconFile.exists()) {
                                    actionList.add("Reset Icon")
                                }
                                actionList.add("Remove")

                                var popupWindow: PopupWindow? = null
                                val popupLayout = LinearLayout(context).apply {
                                    orientation = LinearLayout.VERTICAL
                                    val pad = (8 * context.resources.displayMetrics.density).toInt()
                                    setPadding(pad, pad, pad, pad)
                                }

                                actionList.forEach { action ->
                                    val actionView = TextView(context).apply {
                                        text = action
                                        setTextColor(Color.WHITE)
                                        setPadding(0, (12 * context.resources.displayMetrics.density).toInt(), 0, (12 * context.resources.displayMetrics.density).toInt())
                                        gravity = Gravity.CENTER
                                        
                                        val shape = android.graphics.drawable.GradientDrawable()
                                        shape.cornerRadius = 8 * context.resources.displayMetrics.density
                                        shape.setColor(Color.parseColor("#333333"))
                                        shape.setStroke(1, Color.LTGRAY)
                                        background = shape
                                        
                                        layoutParams = LinearLayout.LayoutParams(
                                            LinearLayout.LayoutParams.WRAP_CONTENT,
                                            LinearLayout.LayoutParams.WRAP_CONTENT
                                        ).apply {
                                            setMargins(0, 0, 0, (8 * context.resources.displayMetrics.density).toInt())
                                        }
                                        
                                        setOnClickListener {
                                            popupWindow?.dismiss()
                                            when (action) {
                                                "Remove" -> {
                                                    // Need to remove from items and save
                                                    val newItems = items.toMutableList()
                                                    newItems.removeAll { it.id == item.id }
                                                    saveItems(prefs, pageId, newItems)
                                                    // Trigger reload
                                                    context.sendBroadcast(Intent("ELEMENT_ADDED_TO_HYBRID").apply { putExtra("PAGE_ID", pageId) })
                                                }
                                                "Change Icon" -> {
                                                    val intent = Intent(context, com.example.IconPickerActivity::class.java).apply {
                                                        putExtra("item_id", item.id)
                                                        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                                    }
                                                    context.startActivity(intent)
                                                }
                                                "Reset Icon" -> {
                                                    val file = java.io.File(context.filesDir, "custom_icons/${item.id.replace(Regex("[^a-zA-Z0-9.-]"), "_")}.webp")
                                                    if (file.exists()) file.delete()
                                                    appsManager.iconCache.remove("custom_${item.id}")
                                                    appsManager.iconCache.remove(item.id)
                                                    context.sendBroadcast(Intent("com.example.UPDATE_SIDEBAR_ICONS").apply {
                                                        putExtra("item_id", item.id)
                                                    })
                                                }
                                                "App Info" -> {
                                                    if (parsed is SidebarItem.App) {
                                                        try {
                                                            val intent = Intent(android.provider.Settings.ACTION_APPLICATION_DETAILS_SETTINGS)
                                                            intent.data = android.net.Uri.parse("package:${parsed.packageName}")
                                                            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                                            context.startActivity(intent)
                                                        } catch (e: Exception) {}
                                                    }
                                                }
                                            }
                                        }
                                    }
                                    popupLayout.addView(actionView)
                                }
                                
                                popupLayout.measure(View.MeasureSpec.UNSPECIFIED, View.MeasureSpec.UNSPECIFIED)
                                popupWindow = PopupWindow(
                                    popupLayout,
                                    (150 * context.resources.displayMetrics.density).toInt(),
                                    LinearLayout.LayoutParams.WRAP_CONTENT,
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
                                elementView.getLocationOnScreen(location)
                                val x = location[0]
                                var y = location[1] - popupLayout.measuredHeight
                                if (y < 0) y = location[1] + elementView.height
                                popupWindow?.showAtLocation(elementView, Gravity.NO_GRAVITY, x, y)
                                true
                            }'''

content = re.sub(pattern, repl, content)

with open("app/src/main/java/com/example/service/HybridGridPageView.kt", "w") as f:
    f.write(content)
