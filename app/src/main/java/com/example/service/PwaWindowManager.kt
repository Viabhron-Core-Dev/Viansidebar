package com.example.service

import android.annotation.SuppressLint
import android.content.Context
import android.graphics.PixelFormat
import android.os.Build
import android.view.Gravity
import android.view.LayoutInflater
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import com.example.R
import java.net.ServerSocket
import kotlin.math.roundToInt

class PwaWindowManager(private val context: Context, private val pwa: PwaEntry) {
    private val windowManager = context.getSystemService(Context.WINDOW_SERVICE) as WindowManager
    private val prefs = context.getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
    
    private var floatingView: View? = null
    private var layoutParams: WindowManager.LayoutParams? = null

    private var pwaServer: PwaServer? = null
    private var port: Int = 0

    private var isFullScreen = !pwa.isLightweight
    private var preFullScreenWidth = 800
    private var preFullScreenHeight = 1000
    private var preFullScreenX = 100
    private var preFullScreenY = 100
    
    private var isFolded = false

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

    private fun toggleFullScreen(windowContainer: View, topDragBar: View) {
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
            windowContainer.background = null
        } else {
            layoutParams?.width = preFullScreenWidth
            layoutParams?.height = preFullScreenHeight
            layoutParams?.x = preFullScreenX
            layoutParams?.y = preFullScreenY
            isFullScreen = false
            windowContainer.setBackgroundResource(R.drawable.bg_floating_window)
        }
        windowManager.updateViewLayout(floatingView, layoutParams)
    }

    @SuppressLint("ClickableViewAccessibility", "SetJavaScriptEnabled")
    fun show() {
        val defaultW = (context.resources.displayMetrics.widthPixels * 0.85).toInt()
        val defaultH = (context.resources.displayMetrics.heightPixels * 0.6).toInt()
        if (floatingView != null) return

        if (pwaServer == null) {
            port = findFreePort()
            pwaServer = PwaServer(port, pwa.zipPath)
            pwaServer?.start()
        }

        val width = prefs.getInt("pwa_${pwa.id}_width", defaultW)
        val height = prefs.getInt("pwa_${pwa.id}_height", defaultH)
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

        floatingView = LayoutInflater.from(context).inflate(R.layout.layout_pwa, null)
        com.example.utils.ActiveAppTracker.addApp("pwa_${pwa.id}", pwa.name, "PWA", 45)
        
        val bubbleIcon = floatingView!!.findViewById<TextView>(R.id.bubble_icon)
        val windowContainer = floatingView!!.findViewById<LinearLayout>(R.id.window_container)
        val topDragBar = floatingView!!.findViewById<LinearLayout>(R.id.top_drag_bar)
        
        val tvTitle = floatingView!!.findViewById<TextView>(R.id.tv_title)
        val webView = floatingView!!.findViewById<WebView>(R.id.webview)
        
        val btnClose = floatingView!!.findViewById<ImageView>(R.id.btn_exit_bottom)
        val btnMinimize = floatingView!!.findViewById<ImageView>(R.id.btn_minimize_bottom)
        val btnResize = floatingView!!.findViewById<ImageView>(R.id.resize_handle)

        bubbleIcon.text = pwa.name.take(1).uppercase()
        tvTitle.text = pwa.name
        
        webView.apply {
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

        // --- Dragging Window ---
        var initialX = 0
        var initialY = 0
        var initialTouchX = 0f
        var initialTouchY = 0f
        var lastTouchTime = 0L

        topDragBar.setOnTouchListener { _, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    initialX = layoutParams!!.x
                    initialY = layoutParams!!.y
                    initialTouchX = event.rawX
                    initialTouchY = event.rawY
                    
                    val clickTime = System.currentTimeMillis()
                    if (clickTime - lastTouchTime < 300) {
                        toggleFullScreen(windowContainer, topDragBar)
                    }
                    lastTouchTime = clickTime
                    true
                }
                MotionEvent.ACTION_MOVE -> {
                    if (!isFullScreen) {
                        layoutParams!!.x = initialX + (event.rawX - initialTouchX).roundToInt()
                        layoutParams!!.y = initialY + (event.rawY - initialTouchY).roundToInt()
                        windowManager.updateViewLayout(floatingView, layoutParams)
                    }
                    true
                }
                MotionEvent.ACTION_UP -> {
                    if (!isFullScreen) {
                        prefs.edit()
                            .putInt("pwa_${pwa.id}_x", layoutParams!!.x)
                            .putInt("pwa_${pwa.id}_y", layoutParams!!.y)
                            .apply()
                    }
                    true
                }
                else -> false
            }
        }

        // --- Resizing ---
        btnResize.setOnTouchListener { _, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    initialX = layoutParams!!.width
                    initialY = layoutParams!!.height
                    initialTouchX = event.rawX
                    initialTouchY = event.rawY
                    true
                }
                MotionEvent.ACTION_MOVE -> {
                    if (!isFullScreen) {
                        layoutParams!!.width = Math.max(300, initialX + (event.rawX - initialTouchX).roundToInt())
                        layoutParams!!.height = Math.max(300, initialY + (event.rawY - initialTouchY).roundToInt())
                        windowManager.updateViewLayout(floatingView, layoutParams)
                    }
                    true
                }
                MotionEvent.ACTION_UP -> {
                    if (!isFullScreen) {
                        prefs.edit()
                            .putInt("pwa_${pwa.id}_width", layoutParams!!.width)
                            .putInt("pwa_${pwa.id}_height", layoutParams!!.height)
                            .apply()
                    }
                    true
                }
                else -> false
            }
        }
        
        // --- Dragging Bubble ---
        bubbleIcon.setOnTouchListener { _, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    initialX = layoutParams!!.x
                    initialY = layoutParams!!.y
                    initialTouchX = event.rawX
                    initialTouchY = event.rawY
                    
                    val clickTime = System.currentTimeMillis()
                    if (clickTime - lastTouchTime < 300) {
                        unfold()
                    }
                    lastTouchTime = clickTime
                    true
                }
                MotionEvent.ACTION_MOVE -> {
                    layoutParams!!.x = initialX + (event.rawX - initialTouchX).roundToInt()
                    layoutParams!!.y = initialY + (event.rawY - initialTouchY).roundToInt()
                    windowManager.updateViewLayout(floatingView, layoutParams)
                    true
                }
                MotionEvent.ACTION_UP -> {
                    val dx = Math.abs(event.rawX - initialTouchX)
                    val dy = Math.abs(event.rawY - initialTouchY)
                    if (dx < 10 && dy < 10) {
                        unfold()
                    } else {
                        prefs.edit()
                            .putInt("pwa_${pwa.id}_x", layoutParams!!.x)
                            .putInt("pwa_${pwa.id}_y", layoutParams!!.y)
                            .apply()
                    }
                    true
                }
                else -> false
            }
        }

        btnClose.setOnClickListener { close() }
        btnMinimize.setOnClickListener { fold() }

        windowManager.addView(floatingView, layoutParams)

        if (isFolded) {
            fold()
        } else {
            unfold()
        }
    }

    fun fold() {
        isFolded = true
        if (floatingView != null) {
            val bubbleIcon = floatingView!!.findViewById<TextView>(R.id.bubble_icon)
            val windowContainer = floatingView!!.findViewById<LinearLayout>(R.id.window_container)
            
            windowContainer.visibility = View.GONE
            bubbleIcon.visibility = View.VISIBLE
            
            layoutParams?.width = WindowManager.LayoutParams.WRAP_CONTENT
            layoutParams?.height = WindowManager.LayoutParams.WRAP_CONTENT
            layoutParams?.flags = WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL or WindowManager.LayoutParams.FLAG_WATCH_OUTSIDE_TOUCH
            windowManager.updateViewLayout(floatingView, layoutParams)
        }
    }

    private fun unfold() {
        val defaultW = (context.resources.displayMetrics.widthPixels * 0.85).toInt()
        val defaultH = (context.resources.displayMetrics.heightPixels * 0.6).toInt()
        isFolded = false
        if (floatingView != null) {
            val bubbleIcon = floatingView!!.findViewById<TextView>(R.id.bubble_icon)
            val windowContainer = floatingView!!.findViewById<LinearLayout>(R.id.window_container)
            
            bubbleIcon.visibility = View.GONE
            windowContainer.visibility = View.VISIBLE
            
            if (isFullScreen) {
                val metrics = context.resources.displayMetrics
                layoutParams?.width = metrics.widthPixels
                layoutParams?.height = metrics.heightPixels
                layoutParams?.x = 0
                layoutParams?.y = 0
            } else {
                layoutParams?.width = prefs.getInt("pwa_${pwa.id}_width", defaultW)
                layoutParams?.height = prefs.getInt("pwa_${pwa.id}_height", defaultH)
            }
            layoutParams?.flags = WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL or WindowManager.LayoutParams.FLAG_WATCH_OUTSIDE_TOUCH
            windowManager.updateViewLayout(floatingView, layoutParams)
        }
    }

    fun close() {
        if (floatingView != null) {
            com.example.utils.ActiveAppTracker.removeApp("pwa_${pwa.id}")
            windowManager.removeView(floatingView)
            floatingView = null
        }
        pwaServer?.stop()
        pwaServer = null
        (context as? SidebarService)?.removePwaWindow(pwa.id)
    }
}
