import re

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "r") as f:
    content = f.read()

# Replace appsManager with appsManagers map
content = content.replace("private lateinit var appsManager: SidebarAppsManager", "private val appsManagers = mutableMapOf<String, SidebarAppsManager>()")

# Remove appsManager initialization in onCreate
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

# In rebuildSidebarPages:
content = content.replace(
"""                "apps" -> {
                    var p: AppsPageView? = null
                    p = AppsPageView(this, config, appsManager, serviceScope,
                        onCloseSidebar = { closeSidebar() },
                        onHeightChanged = { newHeight ->
                            // Only update height if this is the currently selected page
                            if (sidebarView != null && p != null && sidebarPagesList.indexOf(p!!) == sidebarView!!.getCurrentPageIndex()) {
                                sidebarView?.updatePageStyles(config, newHeight)
                            }
                        }
                    )
                    p.updateData(appsManager.activeItems)
                    appsPageViews.add(p)
                    p
                }""",
"""                "apps" -> {
                    var p: AppsPageView? = null
                    val prefKey = "sidebar_apps_" + handleId + "_" + config.id
                    val manager = appsManagers.getOrPut(prefKey) {
                        SidebarAppsManager(this, prefs, serviceScope, prefKey) {
                            appsPageViews.find { it.pageConfig?.id == config.id }?.updateData(appsManagers[prefKey]?.activeItems ?: emptyList())
                        }
                    }
                    manager.ensureLoaded()
                    p = AppsPageView(this, config, manager, serviceScope,
                        onCloseSidebar = { closeSidebar() },
                        onHeightChanged = { newHeight ->
                            if (sidebarView != null && p != null && sidebarPagesList.indexOf(p!!) == sidebarView!!.getCurrentPageIndex()) {
                                sidebarView?.updatePageStyles(config, newHeight)
                            }
                        }
                    )
                    p.updateData(manager.activeItems)
                    appsPageViews.add(p)
                    p
                }"""
)

# In showStandalonePage:
content = content.replace(
"""        val pageView = when (config.type) {
            "apps" -> {
                val p = AppsPageView(this, config, appsManager, serviceScope,
                    onCloseSidebar = { windowManager.removeView(standaloneSidebarView); standaloneSidebarView = null },
                    onHeightChanged = {}
                )
                p.updateData(appsManager.activeItems)
                p
            }""",
"""        val pageView = when (config.type) {
            "apps" -> {
                val prefKey = "sidebar_apps_" + currentHandleId + "_" + config.id
                val manager = appsManagers.getOrPut(prefKey) {
                    SidebarAppsManager(this, prefs, serviceScope, prefKey) {
                        // For standalone, we might not have it in appsPageViews, but we can just find it
                    }
                }
                manager.ensureLoaded()
                val p = AppsPageView(this, config, manager, serviceScope,
                    onCloseSidebar = { windowManager.removeView(standaloneSidebarView); standaloneSidebarView = null },
                    onHeightChanged = {}
                )
                p.updateData(manager.activeItems)
                p
            }"""
)

# In onStartCommand for UPDATE_CONFIG
content = content.replace(
"""        if (intent?.action == "UPDATE_CONFIG") {
            appsManager.reloadActiveApps()
            return START_NOT_STICKY
        }""",
"""        if (intent?.action == "UPDATE_CONFIG") {
            appsManagers.values.forEach { it.reloadActiveApps() }
            return START_NOT_STICKY
        }"""
)

# In onStartCommand for ADD_ELEMENT
content = content.replace(
"""            if (isElementCallback) {
                pendingElementCallback?.invoke(elementId)
                pendingElementCallback = null
            } else if (folderUuid != null) {
                appsManager.addItemToFolder(folderUuid, elementId)
            } else {
                appsManager.addItem(elementId)
            }""",
"""            if (isElementCallback) {
                pendingElementCallback?.invoke(elementId)
                pendingElementCallback = null
            } else {
                val prefKey = "sidebar_apps_" + currentHandleId + "_default_apps" // Defaulting to default_apps for now
                val manager = appsManagers.getOrPut(prefKey) {
                    SidebarAppsManager(this, prefs, serviceScope, prefKey) {}
                }
                if (folderUuid != null) {
                    manager.addItemToFolder(folderUuid, elementId)
                } else {
                    manager.addItem(elementId)
                }
            }"""
)

# onDestroy
content = content.replace(
"""        if (::appsManager.isInitialized) {
            appsManager.destroy()
        }""",
"""        appsManagers.values.forEach { it.destroy() }
        appsManagers.clear()"""
)

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "w") as f:
    f.write(content)
