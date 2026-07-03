import re

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'r') as f:
    content = f.read()

init_old = """        setBackgroundColor(Color.parseColor("#E6000000")) // Semi-transparent black
        // Initialize local list with current items
        localIds.addAll(manager.activeItems.map { it.id })
            com.example.LogKeeper.writeLog("SidebarEdit", "localIds on attach: $localIds")

        val rootLayout = LinearLayout(context).apply {"""

init_new = """        setBackgroundColor(Color.parseColor("#E6000000")) // Semi-transparent black
        // State will be initialized in attach()

        val rootLayout = LinearLayout(context).apply {"""

content = content.replace(init_old, init_new)

with open('app/src/main/java/com/example/service/SidebarEditOverlayView.kt', 'w') as f:
    f.write(content)
