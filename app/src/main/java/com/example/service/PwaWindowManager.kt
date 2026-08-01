package com.example.service

import android.content.Context
import android.graphics.PixelFormat
import android.os.Build
import android.view.Gravity
import android.view.View
import android.view.WindowManager
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.FrameLayout
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
import androidx.compose.material.icons.filled.Menu
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
import java.net.ServerSocket

class PwaWindowManager(private val context: Context, private val pwa: PwaEntry) {

    private val windowManager = context.getSystemService(Context.WINDOW_SERVICE) as WindowManager
    private val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)

    private var floatingView: View? = null
    private var foldedView: View? = null

    private var layoutParams: WindowManager.LayoutParams? = null
    private var foldedLayoutParams: WindowManager.LayoutParams? = null

    private var pwaServer: PwaServer? = null
    private var port: Int = 0
    private var isFullScreen = !pwa.isLightweight

    private fun findFreePort(): Int {
        return try {
            val socket = ServerSocket(0)
            val freePort = socket.localPort
            socket.close()
            freePort
        } catch (e: Exception) {
            8080
        }
    }


    fun show() {
        if (floatingView != null || foldedView != null) return

        if (pwaServer == null) {
            port = findFreePort()
            pwaServer = PwaServer(port, pwa.zipPath)
            pwaServer?.start()
        }

        val width = prefs.getInt("pwa_${pwa.id}_width", 800)
        val height = prefs.getInt("pwa_${pwa.id}_height", 1000)
        val x = prefs.getInt("pwa_${pwa.id}_x", 100)
        val y = prefs.getInt("pwa_${pwa.id}_y", 100)

        layoutParams = WindowManager.LayoutParams(
            if (isFullScreen) WindowManager.LayoutParams.MATCH_PARENT else width,
            if (isFullScreen) WindowManager.LayoutParams.MATCH_PARENT else height,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY else WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL or WindowManager.LayoutParams.FLAG_WATCH_OUTSIDE_TOUCH,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            this.x = if (isFullScreen) 0 else x
            this.y = if (isFullScreen) 0 else y
        }

        floatingView = FrameLayout(context).apply {
            addView(ComposeView(context).apply {
                setContent {
                    MaterialTheme(colorScheme = darkColorScheme()) {
                        PwaWindowContent(
                            onClose = { close() },
                            onFold = { fold() },
                            onDrag = { dx, dy ->
                                if (!isFullScreen) {
                                    this@PwaWindowManager.layoutParams?.x = (this@PwaWindowManager.layoutParams?.x ?: 0) + dx.roundToInt()
                                    this@PwaWindowManager.layoutParams?.y = (this@PwaWindowManager.layoutParams?.y ?: 0) + dy.roundToInt()
                                    windowManager.updateViewLayout(floatingView, this@PwaWindowManager.layoutParams)
                                    prefs.edit().putInt("pwa_${pwa.id}_x", this@PwaWindowManager.layoutParams?.x ?: 0)
                                        .putInt("pwa_${pwa.id}_y", this@PwaWindowManager.layoutParams?.y ?: 0).apply()
                                }
                            },
                            onResize = { dx, dy ->
                                if (!isFullScreen) {
                                    this@PwaWindowManager.layoutParams?.width = ((this@PwaWindowManager.layoutParams?.width ?: 0) + dx.roundToInt()).coerceAtLeast(300)
                                    this@PwaWindowManager.layoutParams?.height = ((this@PwaWindowManager.layoutParams?.height ?: 0) + dy.roundToInt()).coerceAtLeast(400)
                                    windowManager.updateViewLayout(floatingView, this@PwaWindowManager.layoutParams)
                                    prefs.edit().putInt("pwa_${pwa.id}_width", this@PwaWindowManager.layoutParams?.width ?: 0)
                                        .putInt("pwa_${pwa.id}_height", this@PwaWindowManager.layoutParams?.height ?: 0).apply()
                                }
                            },
                            onToggleFullscreen = {
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
                            }
                        )
                    }
                }
            })
        }
        
        setupLifecycle(floatingView!!)
        windowManager.addView(floatingView, layoutParams)
    }

    private fun fold() {
        if (floatingView != null) {
            windowManager.removeView(floatingView)
            floatingView = null
        }

        val x = prefs.getInt("pwa_${pwa.id}_folded_x", 100)
        val y = prefs.getInt("pwa_${pwa.id}_folded_y", 100)

        foldedLayoutParams = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY else WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            this.x = x
            this.y = y
        }

        foldedView = FrameLayout(context).apply {
            addView(ComposeView(context).apply {
                setContent {
                    MaterialTheme(colorScheme = darkColorScheme()) {
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .clip(CircleShape)
                                .background(Color(0xFF00B0FF))
                                .pointerInput(Unit) {
                                    detectDragGestures(
                                        onDrag = { change, dragAmount ->
                                            change.consume()
                                            foldedLayoutParams?.x = (foldedLayoutParams?.x ?: 0) + dragAmount.x.roundToInt()
                                            foldedLayoutParams?.y = (foldedLayoutParams?.y ?: 0) + dragAmount.y.roundToInt()
                                            windowManager.updateViewLayout(foldedView, foldedLayoutParams)
                                        },
                                        onDragEnd = {
                                            prefs.edit().putInt("pwa_${pwa.id}_folded_x", foldedLayoutParams?.x ?: 0)
                                                .putInt("pwa_${pwa.id}_folded_y", foldedLayoutParams?.y ?: 0).apply()
                                        }
                                    )
                                }
                                .clickable {
                                    unfold()
                                },
                            contentAlignment = Alignment.Center
                        ) {
                            Text(pwa.name.take(1).uppercase(), color = Color.White, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            })
        }
        
        setupLifecycle(foldedView!!)
        windowManager.addView(foldedView, foldedLayoutParams)
    }

    private fun unfold() {
        if (foldedView != null) {
            windowManager.removeView(foldedView)
            foldedView = null
        }
        show()
    }

    private fun close() {
        if (floatingView != null) {
            windowManager.removeView(floatingView)
            floatingView = null
        }
        if (foldedView != null) {
            windowManager.removeView(foldedView)
            foldedView = null
        }
        pwaServer?.stop()
        pwaServer = null
        (context as? FloatingReaderService)?.removePwaWindow(pwa.id)
    }

    @Composable
    private fun PwaWindowContent(
        onClose: () -> Unit,
        onFold: () -> Unit,
        onDrag: (Float, Float) -> Unit,
        onResize: (Float, Float) -> Unit,
        onToggleFullscreen: () -> Unit
    ) {
        Surface(
            modifier = Modifier.fillMaxSize().clip(if (isFullScreen) RoundedCornerShape(0.dp) else RoundedCornerShape(12.dp)),
            color = Color(0xFF1E1E2C)
        ) {
            Column(modifier = Modifier.fillMaxSize()) {
                // Top Bar
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(Color(0xFF2A2A3C))
                        .pointerInput(Unit) {
                            detectTapGestures(
                                onDoubleTap = { onToggleFullscreen() }
                            )
                        }
                        .pointerInput(Unit) {
                        detectTapGestures(
                            onDoubleTap = { 
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
                            }
                        )
                    }
                    .pointerInput(Unit) {
                        detectDragGesturesAfterLongPress { change, dragAmount ->
                            change.consume()
                            onDrag(dragAmount.x, dragAmount.y)
                        }
                    }
                        .padding(8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(pwa.name, color = Color.White, modifier = Modifier.weight(1f), fontWeight = FontWeight.Bold)
                    
                }

                // WebView
                Box(modifier = Modifier.weight(1f).fillMaxWidth()) {
                    AndroidView(
                        factory = { ctx ->
                            WebView(ctx).apply {
                                settings.javaScriptEnabled = true
                                settings.domStorageEnabled = true
                                settings.allowFileAccess = true
                                webChromeClient = WebChromeClient()
                                webViewClient = object : WebViewClient() {
                                    override fun shouldOverrideUrlLoading(view: WebView?, url: String?): Boolean {
                                        return false
                                    }
                                }
                                loadUrl("http://localhost:$port/")
                            }
                        },
                        modifier = Modifier.fillMaxSize()
                    )
                }

                if (!isFullScreen) {
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
                    onFold()
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
