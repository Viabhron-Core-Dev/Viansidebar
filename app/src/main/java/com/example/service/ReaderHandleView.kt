package com.example.service

import android.content.Context
import android.content.SharedPreferences
import android.graphics.PixelFormat
import android.os.Build
import android.view.Gravity
import android.view.LayoutInflater
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import android.widget.FrameLayout

import com.example.utils.Utils
import com.example.utils.getEdgeFlag

import kotlin.math.abs

class ReaderHandleView(
    private val context: Context,
    private val prefs: SharedPreferences,
    private val windowManager: WindowManager
) {

    private val handleId = "reader"
    private val prefix = "handle_${handleId}_"

    private var handleView: View? = null
    private var layoutParams: WindowManager.LayoutParams? = null
    private var isAttached = false
    
    fun attach() {
        if (isAttached) return
        
        handleView = View(context)
        
        val windowType = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        } else {
            @Suppress("DEPRECATION")
            WindowManager.LayoutParams.TYPE_PHONE
        }
        
        layoutParams = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            windowType,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
            WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
            PixelFormat.TRANSLUCENT
        )
        
        updatePosition()
        setupListeners()
        
        windowManager.addView(handleView, layoutParams)
        isAttached = true
    }
    
    fun detach() {
        if (!isAttached) return
        if (handleView != null) {
            try {
                windowManager.removeView(handleView)
            } catch (e: Exception) {}
        }
        isAttached = false
    }
    
    fun updatePosition() {
        if (handleView == null || layoutParams == null) return
        
        val edgeStr = prefs.getString("${prefix}edge", "right") ?: "right"
        val gravity = getEdgeFlag(edgeStr)
        
        val yPos = prefs.getInt("${prefix}y", 50)
        
        layoutParams?.gravity = gravity or Gravity.TOP
        layoutParams?.y = (Utils.getScreenHeight(context) * (yPos / 100f)).toInt()
        
        val heightStr = prefs.getString("${prefix}height", "medium") ?: "medium"
        val widthStr = prefs.getString("${prefix}width", "medium") ?: "medium"
        
        val heightMap = mapOf("small" to 100, "medium" to 150, "large" to 200, "xlarge" to 300)
        val widthMap = mapOf("small" to 4, "medium" to 6, "large" to 10, "xlarge" to 15)
        
        val heightDp = heightMap[heightStr] ?: 150
        val widthDp = widthMap[widthStr] ?: 6
        
        val heightPx = Utils.dpToPx(context, heightDp)
        val widthPx = Utils.dpToPx(context, widthDp)
        
        layoutParams?.height = heightPx
        layoutParams?.width = widthPx
        
        val colorInt = try {
            val c = prefs.all["${prefix}color"]
            when (c) {
                is Int -> c
                is String -> android.graphics.Color.parseColor(c)
                else -> android.graphics.Color.GRAY
            }
        } catch(e: Exception) { android.graphics.Color.GRAY }
        val transparency = prefs.getInt("${prefix}transparency", 50)
        val alpha = (transparency / 100f * 255).toInt()
        val finalColor = android.graphics.Color.argb(alpha, android.graphics.Color.red(colorInt), android.graphics.Color.green(colorInt), android.graphics.Color.blue(colorInt))
        
        handleView?.setBackgroundColor(finalColor)
        
        if (isAttached) {
            windowManager.updateViewLayout(handleView, layoutParams)
        }
    }
    
    private fun setupListeners() {
        handleView?.setOnTouchListener(object : View.OnTouchListener {
            var initialX = 0f
            var initialY = 0f
            var isClick = false
            
            override fun onTouch(v: View, event: MotionEvent): Boolean {
                when (event.action) {
                    MotionEvent.ACTION_DOWN -> {
                        initialX = event.rawX
                        initialY = event.rawY
                        isClick = true
                        return true
                    }
                    MotionEvent.ACTION_MOVE -> {
                        val dx = abs(event.rawX - initialX)
                        val dy = abs(event.rawY - initialY)
                        if (dx > 10 || dy > 10) {
                            isClick = false
                        }
                    }
                    MotionEvent.ACTION_UP -> {
                        if (isClick) {
                            if (com.example.service.FloatingReaderService.instance != null) {
                                com.example.service.FloatingReaderService.instance?.toggleReader()
                            } else {
                                val intent = android.content.Intent(context, com.example.service.FloatingReaderService::class.java)
                                intent.putExtra("UNFOLD", true)
                                androidx.core.content.ContextCompat.startForegroundService(context, intent)
                            }
                        }
                    }
                }
                return false
            }
        })
    }
}
