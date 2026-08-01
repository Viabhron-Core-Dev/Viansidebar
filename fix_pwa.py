import os

filepath = "app/src/main/java/com/example/service/PwaWindowManager.kt"
if os.path.exists(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    bad_call = "onDoubleTap = { toggleFullScreen() }"
    good_call = """onDoubleTap = { 
                                isFullScreen = !isFullScreen
                                if (isFullScreen) {
                                    this@PwaWindowManager.layoutParams?.width = WindowManager.LayoutParams.MATCH_PARENT
                                    this@PwaWindowManager.layoutParams?.height = WindowManager.LayoutParams.MATCH_PARENT
                                    this@PwaWindowManager.layoutParams?.x = 0
                                    this@PwaWindowManager.layoutParams?.y = 0
                                } else {
                                    this@PwaWindowManager.layoutParams?.width = prefs.getInt("pwa_${pwa.id}_width", 800)
                                    this@PwaWindowManager.layoutParams?.height = prefs.getInt("pwa_${pwa.id}_height", 1000)
                                    this@PwaWindowManager.layoutParams?.x = prefs.getInt("pwa_${pwa.id}_x", 100)
                                    this@PwaWindowManager.layoutParams?.y = prefs.getInt("pwa_${pwa.id}_y", 100)
                                }
                                windowManager.updateViewLayout(floatingView, this@PwaWindowManager.layoutParams)
                            }"""
    
    content = content.replace(bad_call, good_call)
    
    # Also I need to remove the original top bar logic that had the double tap
    # Wait, the original double tap was inside some clickable or pointerInput that I didn't remove, maybe?
    # Let's write this back first.
    with open(filepath, 'w') as f:
        f.write(content)

