with open("app/src/main/java/com/example/service/SidebarView.kt", "r") as f:
    content = f.read()

import re

old_header_start = """        val headerHeight = (24 * density).toInt()
        val header = FrameLayout(context).apply {
            layoutParams = LayoutParams(LayoutParams.MATCH_PARENT, headerHeight)
            
            val closeText = TextView(context).apply {
                text = "✕"
                textSize = 16f
                setTextColor(Color.WHITE)
                gravity = Gravity.CENTER
                layoutParams = LayoutParams(headerHeight, headerHeight).apply {
                    gravity = Gravity.END or Gravity.CENTER_VERTICAL
                }
                setOnClickListener { close() }
            }
            addView(closeText)

            val settingsIcon = ImageView(context).apply {
                setImageResource(android.R.drawable.ic_menu_preferences)
                setColorFilter(Color.WHITE)
                setPadding((4*density).toInt(), (4*density).toInt(), (4*density).toInt(), (4*density).toInt())
                layoutParams = LayoutParams(headerHeight, headerHeight).apply {
                    gravity = Gravity.END or Gravity.CENTER_VERTICAL
                    marginEnd = headerHeight // Position it before the close button
                }
                setOnClickListener {
                    val intent = android.content.Intent(context, com.example.SettingsActivity::class.java).apply {
                        flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK or android.content.Intent.FLAG_ACTIVITY_CLEAR_TOP
                    }
                    context.startActivity(intent)
                    close()
                }
            }
            addView(settingsIcon)

            val addIcon = ImageView(context).apply {
                setImageResource(android.R.drawable.ic_menu_edit)
                setColorFilter(Color.WHITE)
                val pad = (6 * resources.displayMetrics.density).toInt()
                setPadding(pad, pad, pad, pad)
                layoutParams = LayoutParams(headerHeight, headerHeight).apply {
                    gravity = Gravity.START or Gravity.CENTER_VERTICAL
                }
                setOnClickListener {
                    val currentActual = viewPager.currentItem % pages.size
                    val page = pages.getOrNull(currentActual)
                    val config = pageConfigs.getOrNull(currentActual)
                    if (page != null && config != null) {
                        onEditPageClicked?.invoke(page, config)
                    }
                }
            }
            addView(addIcon)
        }"""

new_header_start = """        val headerHeight = (36 * density).toInt()
        val edgeMargin = (16 * density).toInt() // Push icons away from screen edge to avoid handle overlap
        val header = FrameLayout(context).apply {
            layoutParams = LayoutParams(LayoutParams.MATCH_PARENT, headerHeight)
            
            val closeText = TextView(context).apply {
                text = "✕"
                textSize = 18f
                setTextColor(Color.WHITE)
                gravity = Gravity.CENTER
                layoutParams = LayoutParams(headerHeight, headerHeight).apply {
                    gravity = Gravity.END or Gravity.CENTER_VERTICAL
                    marginEnd = edgeMargin
                }
                setOnClickListener { close() }
            }
            addView(closeText)

            val settingsIcon = ImageView(context).apply {
                setImageResource(android.R.drawable.ic_menu_preferences)
                setColorFilter(Color.WHITE)
                setPadding((8*density).toInt(), (8*density).toInt(), (8*density).toInt(), (8*density).toInt())
                layoutParams = LayoutParams(headerHeight, headerHeight).apply {
                    gravity = Gravity.END or Gravity.CENTER_VERTICAL
                    marginEnd = edgeMargin + headerHeight // Position it before the close button
                }
                setOnClickListener {
                    val intent = android.content.Intent(context, com.example.SettingsActivity::class.java).apply {
                        flags = android.content.Intent.FLAG_ACTIVITY_NEW_TASK or android.content.Intent.FLAG_ACTIVITY_CLEAR_TOP
                    }
                    context.startActivity(intent)
                    close()
                }
            }
            addView(settingsIcon)

            val addIcon = ImageView(context).apply {
                setImageResource(android.R.drawable.ic_menu_edit)
                setColorFilter(Color.WHITE)
                val pad = (8 * resources.displayMetrics.density).toInt()
                setPadding(pad, pad, pad, pad)
                layoutParams = LayoutParams(headerHeight, headerHeight).apply {
                    gravity = Gravity.START or Gravity.CENTER_VERTICAL
                    marginStart = edgeMargin
                }
                setOnClickListener {
                    val currentActual = viewPager.currentItem % pages.size
                    val page = pages.getOrNull(currentActual)
                    val config = pageConfigs.getOrNull(currentActual)
                    if (page != null && config != null) {
                        onEditPageClicked?.invoke(page, config)
                    }
                }
            }
            addView(addIcon)
        }"""

content = content.replace(old_header_start, new_header_start)

with open("app/src/main/java/com/example/service/SidebarView.kt", "w") as f:
    f.write(content)

