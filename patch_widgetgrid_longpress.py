import os
import re

with open("app/src/main/java/com/example/service/WidgetsGridPageView.kt", "r") as f:
    content = f.read()

# Make sure imports are present
if 'import android.widget.PopupWindow' not in content:
    content = content.replace('import android.widget.ScrollView', 'import android.widget.ScrollView\nimport android.widget.PopupWindow\nimport android.widget.TextView\nimport android.widget.LinearLayout\n')

pattern = r'gridLayout\.addView\(hostView, params\)\n                            maxHeight = max\(maxHeight, item\.y \* cellHeight \+ cellHeight \* wRows\)'

repl = '''gridLayout.addView(hostView, params)
                            maxHeight = max(maxHeight, item.y * cellHeight + cellHeight * wRows)
                            
                            hostView.setOnLongClickListener {
                                val actionList = mutableListOf("App Info", "Remove")

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
                                                    val newItems = items.toMutableList()
                                                    newItems.removeAll { it.id == item.id }
                                                    saveItems(prefs, pageId, newItems)
                                                    context.sendBroadcast(Intent("WIDGET_ADDED_TO_GRID").apply { putExtra("PAGE_ID", pageId) })
                                                }
                                                "App Info" -> {
                                                    try {
                                                        val intent = Intent(android.provider.Settings.ACTION_APPLICATION_DETAILS_SETTINGS)
                                                        intent.data = android.net.Uri.parse("package:${info.provider.packageName}")
                                                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                                                        context.startActivity(intent)
                                                    } catch (e: Exception) {}
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
                                hostView.getLocationOnScreen(location)
                                val x = location[0]
                                var y = location[1] - popupLayout.measuredHeight
                                if (y < 0) y = location[1] + hostView.height
                                popupWindow?.showAtLocation(hostView, Gravity.NO_GRAVITY, x, y)
                                true
                            }'''

content = re.sub(pattern, repl, content)

with open("app/src/main/java/com/example/service/WidgetsGridPageView.kt", "w") as f:
    f.write(content)
