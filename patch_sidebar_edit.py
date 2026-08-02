with open("app/src/main/java/com/example/service/SidebarView.kt", "r") as f:
    content = f.read()

content = content.replace(
    'private val dots = mutableListOf<View>()',
    'private val dots = mutableListOf<View>()\n    private lateinit var editButton: ImageView'
)

content = content.replace(
    'val addIcon = ImageView(context).apply {',
    'editButton = ImageView(context).apply {'
)

content = content.replace(
    'addView(addIcon)',
    'addView(editButton)'
)

old_onPageSelected = """            override fun onPageSelected(position: Int) {
                val actualPos = position % pages.size
                updateDots(actualPos)
                val page = pages.getOrNull(actualPos)
                val pageConfig = pageConfigs.getOrNull(actualPos)
                com.example.utils.AppWidgetHelper.startListening(context)"""

new_onPageSelected = """            override fun onPageSelected(position: Int) {
                val actualPos = position % pages.size
                updateDots(actualPos)
                val page = pages.getOrNull(actualPos)
                val pageConfig = pageConfigs.getOrNull(actualPos)
                com.example.utils.AppWidgetHelper.startListening(context)
                
                if (::editButton.isInitialized) {
                    val isEditable = page is AppsPageView || page is WidgetsGridPageView || page is HybridGridPageView || page is AppTrackerPageView
                    editButton.visibility = if (isEditable) View.VISIBLE else View.INVISIBLE
                }"""

content = content.replace(old_onPageSelected, new_onPageSelected)

with open("app/src/main/java/com/example/service/SidebarView.kt", "w") as f:
    f.write(content)

