import os
import re

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "r") as f:
    content = f.read()

# in showStandalonePage
content = content.replace(
'''            "widgets_grid" -> WidgetsGridPageView(this, config.id) { newHeight ->
                standaloneSidebarView?.updatePageStyles(config, newHeight)
            }''',
'''            "widgets_grid" -> WidgetsGridPageView(this, config.id) { newHeight ->
                standaloneSidebarView?.updatePageStyles(config, newHeight)
            }
            "hybrid_grid" -> HybridGridPageView(this, config.id) { newHeight ->
                standaloneSidebarView?.updatePageStyles(config, newHeight)
            }''')

# in rebuildSidebarPages
content = content.replace(
'''                "widgets_grid" -> {
                    val p = WidgetsGridPageView(this, config.id) { newHeight ->
                        if (sidebarView != null && sidebarPagesList.indexOf(it) == sidebarView!!.getCurrentPageIndex()) {
                            sidebarView?.updatePageStyles(config, newHeight)
                        }
                    }
                    p
                }''',
'''                "widgets_grid" -> {
                    val p = WidgetsGridPageView(this, config.id) { newHeight ->
                        if (sidebarView != null && sidebarPagesList.indexOf(it) == sidebarView!!.getCurrentPageIndex()) {
                            sidebarView?.updatePageStyles(config, newHeight)
                        }
                    }
                    p
                }
                "hybrid_grid" -> {
                    val p = HybridGridPageView(this, config.id) { newHeight ->
                        if (sidebarView != null) {
                            sidebarView?.updatePageStyles(config, newHeight)
                        }
                    }
                    p
                }''')

# in showSidebar (onEditPageClicked)
content = content.replace(
'''                    } else if (page is WidgetsGridPageView) {
                        showWidgetsGridEditOverlay(config.id)
                    } else if (page is AppTrackerPageView) {''',
'''                    } else if (page is WidgetsGridPageView) {
                        showWidgetsGridEditOverlay(config.id)
                    } else if (page is HybridGridPageView) {
                        showHybridGridEditOverlay(config.id)
                    } else if (page is AppTrackerPageView) {''')

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "w") as f:
    f.write(content)
