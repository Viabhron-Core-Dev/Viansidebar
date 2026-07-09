package com.example.service

import android.appwidget.AppWidgetHostView
import android.appwidget.AppWidgetManager
import android.content.Context
import android.graphics.PixelFormat
import android.os.Build
import android.view.Gravity
import android.view.KeyEvent
import android.view.View
import android.view.WindowManager
import android.widget.FrameLayout
import android.widget.ImageView
import com.example.R
import com.example.utils.AppWidgetHelper

class WidgetOverlayView(
    context: Context,
    private val widgetId: Int
) : FrameLayout(context) {

    private var windowManager: WindowManager = context.getSystemService(Context.WINDOW_SERVICE) as WindowManager
    private var isAttached = false
    private var widgetView: AppWidgetHostView? = null

    init {
        val wmParams = WindowManager.LayoutParams().apply {
            type = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            } else {
                @Suppress("DEPRECATION")
                WindowManager.LayoutParams.TYPE_PHONE
            }
            format = PixelFormat.TRANSLUCENT
            flags = WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL or WindowManager.LayoutParams.FLAG_WATCH_OUTSIDE_TOUCH
            gravity = Gravity.CENTER
            width = WindowManager.LayoutParams.WRAP_CONTENT
            height = WindowManager.LayoutParams.WRAP_CONTENT
        }

        val bg = FrameLayout(context).apply {
            setBackgroundColor(0xD0000000.toInt())
            setPadding(32, 32, 32, 32)
        }
        
        try {
            val appWidgetManager = AppWidgetManager.getInstance(context)
            val appWidgetInfo = appWidgetManager.getAppWidgetInfo(widgetId)
            
            if (appWidgetInfo != null) {
                widgetView = AppWidgetHelper.getHost(context).createView(context, widgetId, appWidgetInfo)
                
                // Close button
                val closeBtn = ImageView(context).apply {
                    setImageResource(android.R.drawable.ic_menu_close_clear_cancel)
                    setOnClickListener { detach() }
                }
                
                bg.addView(widgetView, LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT))
                bg.addView(closeBtn, LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT).apply {
                    gravity = Gravity.TOP or Gravity.END
                })
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }

        addView(bg)

        // Close on outside touch or back key
        isFocusableInTouchMode = true
        setOnKeyListener { _, keyCode, event ->
            if (keyCode == KeyEvent.KEYCODE_BACK && event.action == KeyEvent.ACTION_UP) {
                detach()
                true
            } else {
                false
            }
        }

        // Add to window
        try {
            windowManager.addView(this, wmParams)
            isAttached = true
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
    
    fun detach() {
        if (isAttached) {
            try {
                windowManager.removeView(this)
            } catch (e: Exception) {
                e.printStackTrace()
            }
            isAttached = false
        }
    }
}
