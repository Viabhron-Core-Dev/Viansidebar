sed -i 's/                if (page is WidgetPageView || page is WidgetsGridPageView) {/                val page = pages.getOrNull(actualPos)\n                val pageConfig = pageConfigs.getOrNull(actualPos)\n                if (page is WidgetPageView || page is WidgetsGridPageView) {/g' app/src/main/java/com/example/service/SidebarView.kt
sed -i 's/                val page = pages.getOrNull(actualPos)//g' app/src/main/java/com/example/service/SidebarView.kt
sed -i 's/                val pageConfig = pageConfigs.getOrNull(actualPos)//g' app/src/main/java/com/example/service/SidebarView.kt
