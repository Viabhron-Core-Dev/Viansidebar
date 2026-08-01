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
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job

class PageWindowManager(private val context: Context, private val pageType: String) {
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

        val width = prefs.getInt("page_window_${pageType}_width", 400)
        val height = prefs.getInt("page_window_${pageType}_height", 500)
        val x = prefs.getInt("page_window_${pageType}_x", 100)
        val y = prefs.getInt("page_window_${pageType}_y", 100)

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
                        PageWindowContent(
                            onClose = { close() },
                            onMinimize = { fold() },
                            onDrag = { dx, dy ->
                                this@PageWindowManager.layoutParams?.x = (this@PageWindowManager.layoutParams?.x ?: 0) + dx.roundToInt()
                                this@PageWindowManager.layoutParams?.y = (this@PageWindowManager.layoutParams?.y ?: 0) + dy.roundToInt()
                                windowManager.updateViewLayout(floatingView, this@PageWindowManager.layoutParams)
                                prefs.edit().putInt("page_window_${pageType}_x", this@PageWindowManager.layoutParams?.x ?: 0)
                                    .putInt("page_window_${pageType}_y", this@PageWindowManager.layoutParams?.y ?: 0).apply()
                            },
                            onResize = { dx, dy ->
                                this@PageWindowManager.layoutParams?.width = ((this@PageWindowManager.layoutParams?.width ?: 0) + dx.roundToInt()).coerceAtLeast(300)
                                this@PageWindowManager.layoutParams?.height = ((this@PageWindowManager.layoutParams?.height ?: 0) + dy.roundToInt()).coerceAtLeast(400)
                                windowManager.updateViewLayout(floatingView, this@PageWindowManager.layoutParams)
                                prefs.edit().putInt("page_window_${pageType}_width", this@PageWindowManager.layoutParams?.width ?: 0)
                                    .putInt("page_window_${pageType}_height", this@PageWindowManager.layoutParams?.height ?: 0).apply()
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
            val fx = prefs.getInt("page_window_${pageType}_folded_x", 100)
            val fy = prefs.getInt("page_window_${pageType}_folded_y", 100)

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
                            Text("P", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 24.sp)
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
    private fun PageWindowContent(
        onClose: () -> Unit,
        onMinimize: () -> Unit,
        onDrag: (dx: Float, dy: Float) -> Unit,
        onResize: (dx: Float, dy: Float) -> Unit
    ) {
        val title = when (pageType) {
            "calculator" -> "Calculator"
            "compass" -> "Compass"
            "scheduler" -> "Scheduler"
            "notifications" -> "Notifications"
            "app_tracker" -> "App Tracker"
            else -> "Page Window"
        }

        Box(modifier = Modifier.fillMaxSize().clip(RoundedCornerShape(12.dp)).background(Color(0xFF1E1E2E))) {
        Column(
            modifier = Modifier.fillMaxSize()
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
                Text(title, color = Color.White, fontWeight = FontWeight.Bold, modifier = Modifier.padding(start = 8.dp))
                
            }

            // Content
            Box(modifier = Modifier.weight(1f).fillMaxWidth()) {
                AndroidView(
                    factory = { ctx ->
                        when (pageType) {
                            "calculator" -> CalculatorPageView(ctx)
                            "compass" -> CompassPageView(ctx)
                            "scheduler" -> SchedulerPageView(ctx, CoroutineScope(Dispatchers.Main + Job()))
                            "notifications" -> NotificationPageView(ctx, { close() }) { }
                            "app_tracker" -> AppTrackerPageView(ctx, { close() }) { }
                            else -> FrameLayout(ctx)
                        }
                    },
                    modifier = Modifier.fillMaxSize()
                )
            }
            
        } // end column

        // Overlay Bottom Controls
        com.example.ui.WindowBottomControls(
            onClose = onClose,
            onMinimize = onMinimize,
            onResize = onResize,
            modifier = Modifier.align(Alignment.BottomEnd)
        )
    } // end outer box
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
