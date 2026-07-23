import re

with open("app/src/main/java/com/example/service/DictionaryWindowManager.kt", "r") as f:
    content = f.read()

# 1. Add isFullScreen
content = re.sub(r'(private val db = .*?)\n', r'\1\n    private var isFullScreen = false\n', content)

# 2. Modify layoutParams = WindowManager.LayoutParams(...)
layout_params_orig = """layoutParams = WindowManager.LayoutParams(
            width,
            height,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY else WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL or WindowManager.LayoutParams.FLAG_WATCH_OUTSIDE_TOUCH,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            this.x = x
            this.y = y
        }"""
        
layout_params_new = """layoutParams = WindowManager.LayoutParams(
            if (isFullScreen) WindowManager.LayoutParams.MATCH_PARENT else width,
            if (isFullScreen) WindowManager.LayoutParams.MATCH_PARENT else height,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY else WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL or WindowManager.LayoutParams.FLAG_WATCH_OUTSIDE_TOUCH,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            this.x = if (isFullScreen) 0 else x
            this.y = if (isFullScreen) 0 else y
        }"""

content = content.replace(layout_params_orig, layout_params_new)

# 3. Add onToggleFullscreen to DictionaryWindowContent call
call_orig = """DictionaryWindowContent(
                            onClose = { close() },
                            onFold = { fold() },
                            onDrag = { dx, dy ->
                                this@DictionaryWindowManager.layoutParams?.x = (this@DictionaryWindowManager.layoutParams?.x ?: 0) + dx.roundToInt()
                                this@DictionaryWindowManager.layoutParams?.y = (this@DictionaryWindowManager.layoutParams?.y ?: 0) + dy.roundToInt()
                                windowManager.updateViewLayout(floatingView, this@DictionaryWindowManager.layoutParams)
                                prefs.edit().putInt("dict_window_x", this@DictionaryWindowManager.layoutParams?.x ?: 0)
                                    .putInt("dict_window_y", this@DictionaryWindowManager.layoutParams?.y ?: 0).apply()
                            },
                            onResize = { dx, dy ->
                                this@DictionaryWindowManager.layoutParams?.width = ((this@DictionaryWindowManager.layoutParams?.width ?: 0) + dx.roundToInt()).coerceAtLeast(300)
                                this@DictionaryWindowManager.layoutParams?.height = ((this@DictionaryWindowManager.layoutParams?.height ?: 0) + dy.roundToInt()).coerceAtLeast(400)
                                windowManager.updateViewLayout(floatingView, this@DictionaryWindowManager.layoutParams)
                                prefs.edit().putInt("dict_window_width", this@DictionaryWindowManager.layoutParams?.width ?: 0)
                                    .putInt("dict_window_height", this@DictionaryWindowManager.layoutParams?.height ?: 0).apply()
                            }
                        )"""
call_new = """DictionaryWindowContent(
                            onClose = { close() },
                            onFold = { fold() },
                            onDrag = { dx, dy ->
                                if (!isFullScreen) {
                                    this@DictionaryWindowManager.layoutParams?.x = (this@DictionaryWindowManager.layoutParams?.x ?: 0) + dx.roundToInt()
                                    this@DictionaryWindowManager.layoutParams?.y = (this@DictionaryWindowManager.layoutParams?.y ?: 0) + dy.roundToInt()
                                    windowManager.updateViewLayout(floatingView, this@DictionaryWindowManager.layoutParams)
                                    prefs.edit().putInt("dict_window_x", this@DictionaryWindowManager.layoutParams?.x ?: 0)
                                        .putInt("dict_window_y", this@DictionaryWindowManager.layoutParams?.y ?: 0).apply()
                                }
                            },
                            onResize = { dx, dy ->
                                if (!isFullScreen) {
                                    this@DictionaryWindowManager.layoutParams?.width = ((this@DictionaryWindowManager.layoutParams?.width ?: 0) + dx.roundToInt()).coerceAtLeast(300)
                                    this@DictionaryWindowManager.layoutParams?.height = ((this@DictionaryWindowManager.layoutParams?.height ?: 0) + dy.roundToInt()).coerceAtLeast(400)
                                    windowManager.updateViewLayout(floatingView, this@DictionaryWindowManager.layoutParams)
                                    prefs.edit().putInt("dict_window_width", this@DictionaryWindowManager.layoutParams?.width ?: 0)
                                        .putInt("dict_window_height", this@DictionaryWindowManager.layoutParams?.height ?: 0).apply()
                                }
                            },
                            onToggleFullscreen = {
                                isFullScreen = !isFullScreen
                                if (isFullScreen) {
                                    this@DictionaryWindowManager.layoutParams?.width = WindowManager.LayoutParams.MATCH_PARENT
                                    this@DictionaryWindowManager.layoutParams?.height = WindowManager.LayoutParams.MATCH_PARENT
                                    this@DictionaryWindowManager.layoutParams?.x = 0
                                    this@DictionaryWindowManager.layoutParams?.y = 0
                                } else {
                                    this@DictionaryWindowManager.layoutParams?.width = prefs.getInt("dict_window_width", 800)
                                    this@DictionaryWindowManager.layoutParams?.height = prefs.getInt("dict_window_height", 1000)
                                    this@DictionaryWindowManager.layoutParams?.x = prefs.getInt("dict_window_x", 100)
                                    this@DictionaryWindowManager.layoutParams?.y = prefs.getInt("dict_window_y", 100)
                                }
                                windowManager.updateViewLayout(floatingView, this@DictionaryWindowManager.layoutParams)
                            },
                            isFullScreen = isFullScreen
                        )"""
content = content.replace(call_orig, call_new)

# 4. Modify DictionaryWindowContent signature
def_orig = """    @Composable
    private fun DictionaryWindowContent(
        onClose: () -> Unit,
        onFold: () -> Unit,
        onDrag: (Float, Float) -> Unit,
        onResize: (Float, Float) -> Unit
    ) {"""
def_new = """    @Composable
    private fun DictionaryWindowContent(
        onClose: () -> Unit,
        onFold: () -> Unit,
        onDrag: (Float, Float) -> Unit,
        onResize: (Float, Float) -> Unit,
        onToggleFullscreen: () -> Unit,
        isFullScreen: Boolean
    ) {"""
content = content.replace(def_orig, def_new)

# 5. Modify Surface to handle isFullScreen for corner radius
surface_orig = """        Surface(
            modifier = Modifier.fillMaxSize().clip(RoundedCornerShape(12.dp)),
            color = Color(0xFF1E1E2C)
        ) {"""
surface_new = """        Surface(
            modifier = Modifier.fillMaxSize().clip(if (isFullScreen) RoundedCornerShape(0.dp) else RoundedCornerShape(12.dp)),
            color = Color(0xFF1E1E2C)
        ) {"""
content = content.replace(surface_orig, surface_new)

# 6. Top Bar detectTapGestures for double tap
topbar_orig = """                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(Color(0xFF2A2A3C))
                        .pointerInput(Unit) {
                            detectDragGestures { change, dragAmount ->
                                change.consume()
                                onDrag(dragAmount.x, dragAmount.y)
                            }
                        }
                        .padding(8.dp),"""
topbar_new = """                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(Color(0xFF2A2A3C))
                        .pointerInput(Unit) {
                            androidx.compose.foundation.gestures.detectTapGestures(
                                onDoubleTap = { onToggleFullscreen() }
                            )
                        }
                        .pointerInput(Unit) {
                            detectDragGestures { change, dragAmount ->
                                change.consume()
                                onDrag(dragAmount.x, dragAmount.y)
                            }
                        }
                        .padding(8.dp),"""
content = content.replace(topbar_orig, topbar_new)

# 7. Hide Resize handle when full screen
resize_orig = """                // Resize handle
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(20.dp)
                        .background(Color(0xFF2A2A3C))
                        .pointerInput(Unit) {
                            detectDragGestures { change, dragAmount ->
                                change.consume()
                                onResize(dragAmount.x, dragAmount.y)
                            }
                        }
                ) {
                    Text("///", color = Color.Gray, modifier = Modifier.align(Alignment.CenterEnd).padding(end = 8.dp))
                }"""
resize_new = """                // Resize handle
                if (!isFullScreen) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(20.dp)
                            .background(Color(0xFF2A2A3C))
                            .pointerInput(Unit) {
                                detectDragGestures { change, dragAmount ->
                                    change.consume()
                                    onResize(dragAmount.x, dragAmount.y)
                                }
                            }
                    ) {
                        Text("///", color = Color.Gray, modifier = Modifier.align(Alignment.CenterEnd).padding(end = 8.dp))
                    }
                }"""
content = content.replace(resize_orig, resize_new)

with open("app/src/main/java/com/example/service/DictionaryWindowManager.kt", "w") as f:
    f.write(content)
