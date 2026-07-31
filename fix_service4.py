import re

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # tvContent and windowContainer
    content = re.sub(r'        if \(!::windowContainer\.isInitialized\) return\n', '', content)
    content = re.sub(r'        windowContainer\.setBackgroundColor\(bgColor\)\n', '', content)
    content = re.sub(r'        if \(!::tvContent\.isInitialized\) return\n', '', content)
    content = re.sub(r'        tvContent\.setTextColor\(txColor\)\n', '', content)

    # Saved Window variables
    content = re.sub(r'        savedWindowWidth = prefs\.getInt\("win_w", 800\)\n', '', content)
    content = re.sub(r'        savedWindowHeight = prefs\.getInt\("win_h", 1200\)\n', '', content)
    content = re.sub(r'        savedWindowX = prefs\.getInt\("win_x", 0\)\n', '', content)
    content = re.sub(r'        savedWindowY = prefs\.getInt\("win_y", 0\)\n', '', content)
    content = re.sub(r'        foldedX = prefs\.getInt\("fold_x", 0\)\n', '', content)
    content = re.sub(r'        foldedY = prefs\.getInt\("fold_y", 0\)\n', '', content)
    
    # layoutParams in updateKeepScreenOn
    content = re.sub(r'    private fun updateKeepScreenOn\(\) \{\n        if \(prefs\.getBoolean\("keep_screen_on", false\)\) \{\n            layoutParams\.flags = layoutParams\.flags or WindowManager\.LayoutParams\.FLAG_KEEP_SCREEN_ON\n        \} else \{\n            layoutParams\.flags = layoutParams\.flags and WindowManager\.LayoutParams\.FLAG_KEEP_SCREEN_ON\.inv\(\)\n        \}\n    \}\n', '', content)
    content = re.sub(r'    private fun updateKeepScreenOn\(\) \{\n        if \(prefs\.getBoolean\("keep_screen_on", false\)\) \{\n            layoutParams\.flags = layoutParams\.flags or WindowManager\.LayoutParams\.FLAG_KEEP_SCREEN_ON\n        \} else \{\n            layoutParams\.flags = layoutParams\.flags and WindowManager\.LayoutParams\.FLAG_KEEP_SCREEN_ON\.inv\(\)\n        \}\n', '', content)
    
    content = re.sub(r'        updateKeepScreenOn\(\)\n', '', content)

    # scrollHandler in onDestroy
    content = re.sub(r'        scrollHandler\.removeCallbacks\(scrollRunnable\)\n', '', content)
    
    with open(path, 'w') as f:
        f.write(content)

fix_file('app/src/main/java/com/example/service/SidebarService.kt')
