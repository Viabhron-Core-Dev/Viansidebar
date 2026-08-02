with open("app/src/main/java/com/example/service/PageWindowManager.kt", "r") as f:
    content = f.read()

# Remove the last closing brace
content = content.rstrip()
if content.endswith("}"):
    content = content[:-1]

lifecycle_code = """
    private fun setupLifecycle(view: View) {
        val lifecycleOwner = CustomLifecycleOwner()
        lifecycleOwner.performRestore(null)
        lifecycleOwner.handleLifecycleEvent(androidx.lifecycle.Lifecycle.Event.ON_CREATE)
        view.setViewTreeLifecycleOwner(lifecycleOwner)
        view.setViewTreeSavedStateRegistryOwner(lifecycleOwner)
        view.setViewTreeViewModelStoreOwner(lifecycleOwner)
        lifecycleOwner.handleLifecycleEvent(androidx.lifecycle.Lifecycle.Event.ON_START)
        lifecycleOwner.handleLifecycleEvent(androidx.lifecycle.Lifecycle.Event.ON_RESUME)
    }

    class CustomLifecycleOwner : androidx.savedstate.SavedStateRegistryOwner, androidx.lifecycle.ViewModelStoreOwner {
        private val lifecycleRegistry = androidx.lifecycle.LifecycleRegistry(this)
        private val savedStateRegistryController = androidx.savedstate.SavedStateRegistryController.create(this)
        private val store = androidx.lifecycle.ViewModelStore()

        override val lifecycle: androidx.lifecycle.Lifecycle get() = lifecycleRegistry
        override val savedStateRegistry: androidx.savedstate.SavedStateRegistry get() = savedStateRegistryController.savedStateRegistry
        override val viewModelStore: androidx.lifecycle.ViewModelStore get() = store

        fun handleLifecycleEvent(event: androidx.lifecycle.Lifecycle.Event) {
            lifecycleRegistry.handleLifecycleEvent(event)
        }

        fun performRestore(savedState: android.os.Bundle?) {
            savedStateRegistryController.performRestore(savedState)
        }
    }
}
"""

with open("app/src/main/java/com/example/service/PageWindowManager.kt", "w") as f:
    f.write(content + "\n" + lifecycle_code)
