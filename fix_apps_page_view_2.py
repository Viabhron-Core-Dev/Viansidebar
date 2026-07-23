import re

with open("app/src/main/java/com/example/service/AppsPageView.kt", "r") as f:
    content = f.read()

content = content.replace(
"""class AppsPageView(
    context: Context,
    val handleId: String,
    val pageConfig: SidebarPage?,
    private val manager: SidebarAppsManager,
    private val coroutineScope: CoroutineScope,
    private val onCloseSidebar: () -> Unit,
    private val onHeightChanged: (Int) -> Unit
) : FrameLayout(context) {

    private val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)""",
"""class AppsPageView(
    context: Context,
    val handleId: String,
    val pageConfig: SidebarPage?,
    private val manager: SidebarAppsManager,
    private val coroutineScope: CoroutineScope,
    private val onCloseSidebar: () -> Unit,
    private val onHeightChanged: (Int) -> Unit
) : FrameLayout(context) {

    private val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
    private var columns: Int = 3"""
)

content = content.replace(
"""        val defaultCols = if (handleId == "sidebar" && pageConfig?.id == "default_apps") prefs.getInt("sidebar_columns", 3) else 3
        val columns = if (pageConfig?.useCustomSettings == true) pageConfig.gridColumns else (if (c != -1) c else defaultCols)""",
"""        val defaultCols = if (handleId == "sidebar" && pageConfig?.id == "default_apps") prefs.getInt("sidebar_columns", 3) else 3
        columns = if (pageConfig?.useCustomSettings == true) pageConfig.gridColumns else (if (c != -1) c else defaultCols)"""
)

with open("app/src/main/java/com/example/service/AppsPageView.kt", "w") as f:
    f.write(content)
