with open("app/src/main/java/com/example/service/PageWindowManager.kt", "r") as f:
    content = f.read()

imports_to_add = """import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleRegistry
import androidx.lifecycle.ViewModelStore
import androidx.lifecycle.ViewModelStoreOwner
import androidx.lifecycle.setViewTreeLifecycleOwner
import androidx.lifecycle.setViewTreeViewModelStoreOwner
import androidx.savedstate.SavedStateRegistry
import androidx.savedstate.SavedStateRegistryController
import androidx.savedstate.SavedStateRegistryOwner
import androidx.savedstate.setViewTreeSavedStateRegistryOwner
"""

content = content.replace("import kotlin.math.roundToInt", "import kotlin.math.roundToInt\n" + imports_to_add)

content = content.replace("class PageWindowManager(private val context: Context, private val pageType: String) {", "class PageWindowManager(private val context: Context, private val pageType: String, private val onCloseCallback: (() -> Unit)? = null) {")

content = content.replace("windowManager.addView(floatingView, layoutParams)", "setupLifecycle(floatingView!!)\n        windowManager.addView(floatingView, layoutParams)")

lifecycle_code = """
    private fun setupLifecycle(view: View) {
        val lifecycleOwner = CustomLifecycleOwner()
        lifecycleOwner.performRestore(null)
        lifecycleOwner.handleLifecycleEvent(Lifecycle.Event.ON_CREATE)
        view.setViewTreeLifecycleOwner(lifecycleOwner)
        view.setViewTreeSavedStateRegistryOwner(lifecycleOwner)
        view.setViewTreeViewModelStoreOwner(lifecycleOwner)
        lifecycleOwner.handleLifecycleEvent(Lifecycle.Event.ON_START)
        lifecycleOwner.handleLifecycleEvent(Lifecycle.Event.ON_RESUME)
    }

    class CustomLifecycleOwner : SavedStateRegistryOwner, ViewModelStoreOwner {
        private val lifecycleRegistry = LifecycleRegistry(this)
        private val savedStateRegistryController = SavedStateRegistryController.create(this)
        private val store = ViewModelStore()

        override val lifecycle: Lifecycle get() = lifecycleRegistry
        override val savedStateRegistry: SavedStateRegistry get() = savedStateRegistryController.savedStateRegistry
        override val viewModelStore: ViewModelStore get() = store

        fun handleLifecycleEvent(event: Lifecycle.Event) {
            lifecycleRegistry.handleLifecycleEvent(event)
        }

        fun performRestore(savedState: android.os.Bundle?) {
            savedStateRegistryController.performRestore(savedState)
        }
    }
}
"""

content = content.replace("    }\n\n}", "    }\n\n" + lifecycle_code)

content = content.replace("""        if (floatingView != null) {
            windowManager.removeView(floatingView)
            floatingView = null
        }""", """        if (floatingView != null) {
            windowManager.removeView(floatingView)
            floatingView = null
            onCloseCallback?.invoke()
        }""")

with open("app/src/main/java/com/example/service/PageWindowManager.kt", "w") as f:
    f.write(content)
