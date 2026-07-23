with open("app/src/main/java/com/example/service/DictionaryWindowManager.kt", "r") as f:
    content = f.read()

# Replace `private var isFullScreen = false` with `private val isFullScreenState = androidx.compose.runtime.mutableStateOf(false)`
content = content.replace("private var isFullScreen = false", "private var isFullScreen = false\n    private val isFullScreenState = androidx.compose.runtime.mutableStateOf(false)")

# In show(), when isFullScreen is updated, also update state
content = content.replace("isFullScreen = fullScreen", "isFullScreen = fullScreen\n        isFullScreenState.value = fullScreen")
content = content.replace("isFullScreen = !isFullScreen", "isFullScreen = !isFullScreen\n                                isFullScreenState.value = isFullScreen")

# In DictionaryWindowContent call, pass isFullScreenState.value instead of isFullScreen
content = content.replace("isFullScreen = isFullScreen\n                        )", "isFullScreen = isFullScreenState.value\n                        )")

with open("app/src/main/java/com/example/service/DictionaryWindowManager.kt", "w") as f:
    f.write(content)
