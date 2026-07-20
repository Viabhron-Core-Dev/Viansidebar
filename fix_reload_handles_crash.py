with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "r") as f:
    content = f.read()

bad_func = """    private fun reloadHandles() {
        triggerHandleViews.forEach { it.detach() }
        triggerHandleViews.clear()

        reloadHandles()
    }"""

good_func = """    private fun reloadHandles() {
        triggerHandleViews.forEach { it.detach() }
        triggerHandleViews.clear()

        val handles = com.example.HandleManager.getHandles(prefs)
        for (handle in handles) {
            if (handle.enabled) {
                val view = TriggerHandleView(this, prefs, windowManager, handle.id) { handleId ->
                    showSidebar()
                }
                view.attach()
                triggerHandleViews.add(view)
            }
        }
    }"""

content = content.replace(bad_func, good_func)

with open("app/src/main/java/com/example/service/FloatingReaderService.kt", "w") as f:
    f.write(content)
