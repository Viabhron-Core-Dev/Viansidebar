import re

with open("app/src/main/java/com/example/service/AppsPageView.kt", "r") as f:
    content = f.read()

content = content.replace(
"""class AppsPageView(
    context: Context,
    private val pageConfig: com.example.utils.SidebarPage?,
    private val manager: SidebarAppsManager,
    private val serviceScope: CoroutineScope,
    private val onCloseSidebar: () -> Unit,
    private val onHeightChanged: ((Int) -> Unit)? = null,
    private val onEditModeClicked: (() -> Unit)? = null
) : FrameLayout(context) {""",
"""class AppsPageView(
    context: Context,
    private val handleId: String,
    val pageConfig: com.example.utils.SidebarPage?,
    private val manager: SidebarAppsManager,
    private val serviceScope: CoroutineScope,
    private val onCloseSidebar: () -> Unit,
    private val onHeightChanged: ((Int) -> Unit)? = null,
    private val onEditModeClicked: (() -> Unit)? = null
) : FrameLayout(context) {"""
)

with open("app/src/main/java/com/example/service/AppsPageView.kt", "w") as f:
    f.write(content)
