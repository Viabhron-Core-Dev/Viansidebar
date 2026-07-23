import re

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "r") as f:
    content = f.read()

content = content.replace(
"""        appsManager = SidebarAppsManager(this, prefs, serviceScope) {
            appsPageViews.forEach { it.updateData(appsManager.activeItems) }
        }
        
        callRecorderManager = CallRecorderManager(this, prefs)
        callRecorderManager?.startListening()
        
        rebuildSidebarPages("sidebar")
        appsManager.ensureLoaded()""",
"""        callRecorderManager = CallRecorderManager(this, prefs)
        callRecorderManager?.startListening()
        
        rebuildSidebarPages("sidebar")"""
)

content = content.replace(
"""            "apps" -> {
                val p = AppsPageView(this, config, appsManager, serviceScope,
                    onCloseSidebar = { standaloneSidebarView?.close() },
                    onHeightChanged = { newHeight -> standaloneSidebarView?.updatePageStyles(config, newHeight) }
                )
                p.updateData(appsManager.activeItems)
                p
            }""",
"""            "apps" -> {
                val prefKey = "sidebar_apps_" + currentHandleId + "_" + config.id
                val manager = appsManagers.getOrPut(prefKey) {
                    SidebarAppsManager(this, prefs, serviceScope, prefKey) {}
                }
                manager.ensureLoaded()
                val p = AppsPageView(this, config, manager, serviceScope,
                    onCloseSidebar = { standaloneSidebarView?.close() },
                    onHeightChanged = { newHeight -> standaloneSidebarView?.updatePageStyles(config, newHeight) }
                )
                p.updateData(manager.activeItems)
                p
            }"""
)

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "w") as f:
    f.write(content)
