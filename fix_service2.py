import re

def remove_from_file(path):
    with open(path, 'r') as f:
        content = f.read()

    content = re.sub(r'    private lateinit var floatingView: View\n', '', content)
    content = re.sub(r'    private var savedWindowWidth = 800\n', '', content)
    content = re.sub(r'    private var savedWindowHeight = 1200\n', '', content)
    content = re.sub(r'    private var initialX = 0\n', '', content)
    content = re.sub(r'    private var initialY = 0\n', '', content)
    content = re.sub(r'    private var initialTouchX = 0f\n', '', content)
    content = re.sub(r'    private var initialTouchY = 0f\n', '', content)
    content = re.sub(r'    private var foldedX = 0\n', '', content)
    content = re.sub(r'    private var foldedY = 0\n', '', content)
    content = re.sub(r'    private var savedWindowX = 0\n', '', content)
    content = re.sub(r'    private var savedWindowY = 0\n', '', content)
    
    # Remove floatingView usage in updateKeepScreenOn
    content = re.sub(r'        if \(this::windowManager\.isInitialized\) \{\n            windowManager\.updateViewLayout\(floatingView, layoutParams\)\n        \}\n', '', content)

    # Remove floatingView usage in createLongPressDragListener
    content = re.sub(r'                            windowManager\.updateViewLayout\(floatingView, layoutParams\)\n', '', content)

    # Remove floatingView usage in onDestroy
    content = re.sub(r'        if \(::windowManager\.isInitialized && ::floatingView\.isInitialized\) \{\n            windowManager\.removeView\(floatingView\)\n        \}\n', '', content)

    # Replace showToast body
    replacement_toast = """    private fun showToast(message: String) {
        serviceScope.launch(Dispatchers.Main) {
            Toast.makeText(this@SidebarService, message, Toast.LENGTH_SHORT).show()
        }
    }"""
    content = re.sub(r'    private fun showToast\(message: String\) \{[\s\S]*?Toast\.makeText\(this@SidebarService, message, Toast\.LENGTH_SHORT\)\.show\(\)\n            \}\n        \}\n    \}', replacement_toast, content)
    
    # Remove unneeded layoutParams
    content = re.sub(r'    private lateinit var layoutParams: WindowManager\.LayoutParams\n', '', content)
    
    with open(path, 'w') as f:
        f.write(content)

remove_from_file('app/src/main/java/com/example/service/SidebarService.kt')
