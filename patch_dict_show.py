with open("app/src/main/java/com/example/service/DictionaryWindowManager.kt", "r") as f:
    content = f.read()

old_show = """    fun show(fullScreen: Boolean = false) {
        isFullScreen = fullScreen
        if (floatingView != null || foldedView != null) return"""
new_show = """    fun show(fullScreen: Boolean = false) {
        if (floatingView != null) {
            if (isFullScreen != fullScreen) {
                isFullScreen = fullScreen
                if (isFullScreen) {
                    layoutParams?.width = android.view.WindowManager.LayoutParams.MATCH_PARENT
                    layoutParams?.height = android.view.WindowManager.LayoutParams.MATCH_PARENT
                    layoutParams?.x = 0
                    layoutParams?.y = 0
                } else {
                    layoutParams?.width = prefs.getInt("dict_window_width", 800)
                    layoutParams?.height = prefs.getInt("dict_window_height", 1000)
                    layoutParams?.x = prefs.getInt("dict_window_x", 100)
                    layoutParams?.y = prefs.getInt("dict_window_y", 100)
                }
                windowManager.updateViewLayout(floatingView, layoutParams)
                // Note: we can't easily trigger recomposition of isFullScreen from here without a state, but this is fine for layout.
                // Wait, if it's a compose state, we might need a MutableState for isFullScreen.
            }
            return
        }
        if (foldedView != null) return
        isFullScreen = fullScreen"""
content = content.replace(old_show, new_show)

with open("app/src/main/java/com/example/service/DictionaryWindowManager.kt", "w") as f:
    f.write(content)
