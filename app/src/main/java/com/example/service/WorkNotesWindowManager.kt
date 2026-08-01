package com.example.service

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.PixelFormat
import android.os.Build
import android.view.Gravity
import android.view.View
import android.view.WindowManager
import android.widget.FrameLayout
import android.widget.ImageView
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable

import androidx.compose.foundation.gestures.detectDragGesturesAfterLongPress
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.material.icons.filled.KeyboardArrowDown

import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.ComposeView
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import kotlin.math.roundToInt
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleRegistry
import androidx.lifecycle.ViewModelStore
import androidx.lifecycle.ViewModelStoreOwner
import androidx.lifecycle.setViewTreeLifecycleOwner
import androidx.lifecycle.setViewTreeViewModelStoreOwner
import androidx.savedstate.SavedStateRegistry
import androidx.savedstate.SavedStateRegistryController
import androidx.savedstate.SavedStateRegistryOwner
import androidx.savedstate.setViewTreeSavedStateRegistryOwner

class WorkNotesWindowManager(private val context: Context) {
    private val windowManager = context.getSystemService(Context.WINDOW_SERVICE) as WindowManager
    private val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)

    private var floatingView: View? = null
    private var foldedView: View? = null
    private var layoutParams: WindowManager.LayoutParams? = null
    private var foldedLayoutParams: WindowManager.LayoutParams? = null

    private var lastStateBitmap: Bitmap? = null


    private var isFullScreen = false
    private var preFullScreenWidth = 800
    private var preFullScreenHeight = 1000
    private var preFullScreenX = 100
    private var preFullScreenY = 100

    private fun toggleFullScreen() {
        if (!isFullScreen) {
            preFullScreenWidth = layoutParams?.width ?: 800
            preFullScreenHeight = layoutParams?.height ?: 1000
            preFullScreenX = layoutParams?.x ?: 100
            preFullScreenY = layoutParams?.y ?: 100
            
            val metrics = context.resources.displayMetrics
            layoutParams?.width = metrics.widthPixels
            layoutParams?.height = metrics.heightPixels
            layoutParams?.x = 0
            layoutParams?.y = 0
            isFullScreen = true
        } else {
            layoutParams?.width = preFullScreenWidth
            layoutParams?.height = preFullScreenHeight
            layoutParams?.x = preFullScreenX
            layoutParams?.y = preFullScreenY
            isFullScreen = false
        }
        windowManager.updateViewLayout(floatingView, layoutParams)
    }
    fun show() {
        if (floatingView != null || foldedView != null) return

        val width = prefs.getInt("work_notes_width", 800)
        val height = prefs.getInt("work_notes_height", 1000)
        val x = prefs.getInt("work_notes_x", 100)
        val y = prefs.getInt("work_notes_y", 100)

        layoutParams = WindowManager.LayoutParams(
            width,
            height,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY else WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL or WindowManager.LayoutParams.FLAG_WATCH_OUTSIDE_TOUCH,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            this.x = x
            this.y = y
        }

        floatingView = FrameLayout(context).apply {
            addView(ComposeView(context).apply {
                setContent {
                    MaterialTheme(colorScheme = darkColorScheme()) {
                        WorkNotesContent(
                            onClose = { close() },
                            onMinimize = { fold() },
                            onDrag = { dx, dy ->
                                this@WorkNotesWindowManager.layoutParams?.x = (this@WorkNotesWindowManager.layoutParams?.x ?: 0) + dx.roundToInt()
                                this@WorkNotesWindowManager.layoutParams?.y = (this@WorkNotesWindowManager.layoutParams?.y ?: 0) + dy.roundToInt()
                                windowManager.updateViewLayout(floatingView, this@WorkNotesWindowManager.layoutParams)
                                prefs.edit().putInt("work_notes_x", this@WorkNotesWindowManager.layoutParams?.x ?: 0)
                                    .putInt("work_notes_y", this@WorkNotesWindowManager.layoutParams?.y ?: 0).apply()
                            },
                            onResize = { dx, dy ->
                                this@WorkNotesWindowManager.layoutParams?.width = ((this@WorkNotesWindowManager.layoutParams?.width ?: 0) + dx.roundToInt()).coerceAtLeast(300)
                                this@WorkNotesWindowManager.layoutParams?.height = ((this@WorkNotesWindowManager.layoutParams?.height ?: 0) + dy.roundToInt()).coerceAtLeast(400)
                                windowManager.updateViewLayout(floatingView, this@WorkNotesWindowManager.layoutParams)
                                prefs.edit().putInt("work_notes_width", this@WorkNotesWindowManager.layoutParams?.width ?: 0)
                                    .putInt("work_notes_height", this@WorkNotesWindowManager.layoutParams?.height ?: 0).apply()
                            }
                        )
                    }
                }
            })
        }

        setupLifecycle(floatingView!!)
        windowManager.addView(floatingView, layoutParams)
    }

    private fun captureScreenshot(): Bitmap? {
        val view = floatingView ?: return null
        return try {
            val bitmap = Bitmap.createBitmap(view.width, view.height, Bitmap.Config.ARGB_8888)
            val canvas = Canvas(bitmap)
            view.draw(canvas)
            bitmap
        } catch (e: Exception) {
            null
        }
    }

    private fun fold() {
        if (floatingView != null) {
            lastStateBitmap = captureScreenshot()
            windowManager.removeView(floatingView)
            floatingView = null
        }

        if (foldedView == null) {
            val fx = prefs.getInt("work_notes_folded_x", 100)
            val fy = prefs.getInt("work_notes_folded_y", 100)

            foldedLayoutParams = WindowManager.LayoutParams(
                180,
                180,
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY else WindowManager.LayoutParams.TYPE_PHONE,
                WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_WATCH_OUTSIDE_TOUCH,
                PixelFormat.TRANSLUCENT
            ).apply {
                gravity = Gravity.TOP or Gravity.START
                x = fx
                y = fy
            }

            foldedView = ImageView(context).apply {
                background = BubbleDrawable(lastStateBitmap)
                setOnTouchListener { v, event ->
                    var handled = false
                    val detector = androidx.core.view.GestureDetectorCompat(context, object : android.view.GestureDetector.SimpleOnGestureListener() {
                        override fun onSingleTapConfirmed(e: android.view.MotionEvent): Boolean {
                            unfold()
                            return true
                        }
                    })
                    detector.onTouchEvent(event)
                    // We need pointer input for dragging
                    false
                }
            }
            
            // Re-implement the pointer input / dragging for ImageView since Compose pointerInput doesn't easily attach to ImageView in the same way without wrapping. 
            // Better yet, use ComposeView for the folded view to reuse gesture logic.
            val foldedComposeView = ComposeView(context).apply {
                setContent {
                    MaterialTheme(colorScheme = darkColorScheme()) {
                        Box(
                            modifier = Modifier
                                .size(64.dp)
                                .clip(CircleShape)
                                .background(Color(0xFF2A2A3C).copy(alpha = 0.9f))
                                .pointerInput(Unit) {
                                    detectTapGestures(onTap = { unfold() })
                                }
                                .pointerInput(Unit) {
                                    detectDragGestures { change, dragAmount ->
                                        change.consume()
                                        foldedLayoutParams?.x = (foldedLayoutParams?.x ?: 0) + dragAmount.x.roundToInt()
                                        foldedLayoutParams?.y = (foldedLayoutParams?.y ?: 0) + dragAmount.y.roundToInt()
                                        windowManager.updateViewLayout(this@apply, foldedLayoutParams)
                                    }
                                },
                            contentAlignment = Alignment.Center
                        ) {
                            Text("W", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 24.sp)
                        }
                    }
                }
            }
            setupLifecycle(foldedComposeView)
            foldedView = foldedComposeView
            windowManager.addView(foldedView, foldedLayoutParams)
        }
    }

    private fun unfold() {
        if (foldedView != null) {
            windowManager.removeView(foldedView)
            foldedView = null
        }
        show()
    }

    fun close() {
        if (floatingView != null) {
            windowManager.removeView(floatingView)
            floatingView = null
        }
        if (foldedView != null) {
            windowManager.removeView(foldedView)
            foldedView = null
        }
    }
    
    @Composable
    private fun WorkNotesContent(
        onClose: () -> Unit,
        onMinimize: () -> Unit,
        onDrag: (dx: Float, dy: Float) -> Unit,
        onResize: (dx: Float, dy: Float) -> Unit
    ) {
        var showSettings by remember { mutableStateOf(false) }
        var notesText by remember { mutableStateOf(prefs.getString("work_notes_text", "") ?: "") }
        
        LaunchedEffect(notesText) {
            prefs.edit().putString("work_notes_text", notesText).apply()
        }

        Column(
            modifier = Modifier
                .fillMaxSize()
                .clip(RoundedCornerShape(12.dp))
                .background(Color(0xFF1E1E2E))
        ) {
            // Top Bar
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color(0xFF2A2A3C))
                    .pointerInput(Unit) {
                        detectTapGestures(
                            onDoubleTap = { toggleFullScreen() }
                        )
                    }
                    .pointerInput(Unit) {
                        detectDragGesturesAfterLongPress { change, dragAmount ->
                            change.consume()
                            onDrag(dragAmount.x, dragAmount.y)
                        }
                    }
                    .padding(horizontal = 8.dp, vertical = 6.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text("Work Notes", color = Color.White, fontWeight = FontWeight.Bold, modifier = Modifier.padding(start = 8.dp))
                Row {
                    IconButton(onClick = { showSettings = !showSettings }, modifier = Modifier.size(32.dp)) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings", tint = Color.White, modifier = Modifier.size(18.dp))
                    }
                    IconButton(onClick = onMinimize, modifier = Modifier.size(32.dp)) {
                        Icon(Icons.Default.KeyboardArrowDown, contentDescription = "Minimize", tint = Color.White, modifier = Modifier.size(18.dp))
                    }
                    IconButton(onClick = onClose, modifier = Modifier.size(32.dp)) {
                        Icon(Icons.Default.Close, contentDescription = "Close", tint = Color.White, modifier = Modifier.size(18.dp))
                    }
                }
            }

            // Content
            Box(modifier = Modifier.weight(1f).fillMaxWidth()) {
                if (showSettings) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Settings", color = Color.White, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("No specific settings available yet.", color = Color.Gray)
                        Spacer(modifier = Modifier.height(16.dp))
                        Button(onClick = { showSettings = false }) {
                            Text("Back")
                        }
                    }
                } else {
                    OutlinedTextField(
                        value = notesText,
                        onValueChange = { notesText = it },
                        modifier = Modifier.fillMaxSize().padding(8.dp),
                        placeholder = { Text("Write your notes here...", color = Color.Gray) },
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Color.Transparent,
                            unfocusedBorderColor = Color.Transparent,
                            focusedTextColor = Color.White,
                            unfocusedTextColor = Color.White
                        )
                    )
                }
            }
            
            // Bottom controls
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(36.dp)
                    .background(Color(0xFF2A2A3C)),
                horizontalArrangement = Arrangement.End,
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = { 
                    onMinimize()
                }, modifier = Modifier.size(36.dp)) {
                    Icon(Icons.Default.KeyboardArrowDown, contentDescription = "Minimize", tint = Color.White, modifier = Modifier.size(20.dp))
                }
                IconButton(onClick = onClose, modifier = Modifier.size(36.dp)) {
                    Icon(Icons.Default.Close, contentDescription = "Close", tint = Color.White, modifier = Modifier.size(20.dp))
                }
                Box(
                    modifier = Modifier
                        .size(36.dp)
                        .background(Color(0xFF2A2A3C))
                        .pointerInput(Unit) {
                            detectDragGestures { change, dragAmount ->
                                change.consume()
                                onResize(dragAmount.x, dragAmount.y)
                            }
                        }
                ) {
                    Text("///", color = Color.Gray, modifier = Modifier.align(Alignment.Center).padding(end = 4.dp, bottom = 4.dp))
                }
            }
        }
    }

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
