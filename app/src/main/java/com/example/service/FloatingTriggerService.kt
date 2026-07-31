package com.example.service
import android.app.Service
import android.content.Context
import android.content.Intent
import android.graphics.PixelFormat
import android.os.Build
import android.os.IBinder
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import android.widget.ImageView
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import android.util.DisplayMetrics

class FloatingTriggerService : Service() {

    private lateinit var windowManager: WindowManager
    private val activeTriggers = mutableMapOf<String, View>()
    private lateinit var appsManager: SidebarAppsManager
    private lateinit var prefs: android.content.SharedPreferences

    override fun onCreate() {
        super.onCreate()
        windowManager = getSystemService(Context.WINDOW_SERVICE) as WindowManager
        prefs = getSharedPreferences("FloatingReaderPrefs", Context.MODE_PRIVATE)
        appsManager = SidebarAppsManager(this, prefs, CoroutineScope(Dispatchers.IO), "floating_trigger") {}
        appsManager.ensureLoaded()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val action = intent?.action
        if (action == "STOP_TRIGGER") {
            val targetId = intent.getStringExtra("TARGET_ID")
            if (targetId != null) {
                removeTrigger(targetId)
            }
            if (activeTriggers.isEmpty()) {
                stopSelf()
            }
            return START_NOT_STICKY
        }
        
        val targetId = intent?.getStringExtra("TARGET_ID") ?: return START_NOT_STICKY
        
        if (activeTriggers.containsKey(targetId)) {
            removeTrigger(targetId)
        } else {
            addTrigger(targetId)
        }
        
        return START_STICKY
    }
    
    private fun removeTrigger(targetId: String) {
        val view = activeTriggers.remove(targetId)
        if (view != null) {
            try { windowManager.removeView(view) } catch(e: Exception) {}
        }
    }

    private fun addTrigger(targetId: String) {
        val density = resources.displayMetrics.density
        val size = (56 * density).toInt()

        val imageView = ImageView(this).apply {
            setBackgroundResource(android.R.drawable.dialog_frame) // Or transparent with elevation
        }
        
        // Fetch the icon for targetId using appsManager
        val innerBmp = appsManager.getIconBitmap(targetId)
        imageView.setImageDrawable(BubbleDrawable(innerBmp))

        val type = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        } else {
            WindowManager.LayoutParams.TYPE_PHONE
        }
        
        val lastX = prefs.getInt("floating_trigger_${targetId}_x", 0)
        val lastY = prefs.getInt("floating_trigger_${targetId}_y", 200)

        val params = WindowManager.LayoutParams(
            size, size,
            type,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = lastX
            y = lastY
        }

        var initialX = 0
        var initialY = 0
        var initialTouchX = 0f
        var initialTouchY = 0f
        var isDragging = false

        imageView.setOnTouchListener { view, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    initialX = params.x
                    initialY = params.y
                    initialTouchX = event.rawX
                    initialTouchY = event.rawY
                    isDragging = false
                    true
                }
                MotionEvent.ACTION_MOVE -> {
                    val dx = event.rawX - initialTouchX
                    val dy = event.rawY - initialTouchY
                    if (Math.abs(dx) > 10 || Math.abs(dy) > 10) {
                        isDragging = true
                    }
                    if (isDragging) {
                        params.x = initialX + dx.toInt()
                        params.y = initialY + dy.toInt()
                        windowManager.updateViewLayout(view, params)
                    }
                    true
                }
                MotionEvent.ACTION_UP -> {
                    if (!isDragging) {
                        // Click
                        executeAction(targetId)
                    } else {
                        prefs.edit()
                            .putInt("floating_trigger_${targetId}_x", params.x)
                            .putInt("floating_trigger_${targetId}_y", params.y)
                            .apply()
                    }
                    true
                }
                else -> false
            }
        }

        windowManager.addView(imageView, params)
        activeTriggers[targetId] = imageView
    }
    
    private fun executeAction(targetId: String) {
        val parsed = appsManager.parseId(targetId) ?: return
        
        if (parsed is SidebarItem.App) {
            val launchIntent = packageManager.getLaunchIntentForPackage(parsed.packageName)
            if (launchIntent != null) {
                launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                try { startActivity(launchIntent) } catch (e: Exception) {}
            }
        } else if (parsed is SidebarItem.PageWindow) {
            val intent = Intent(this, PageWindowService::class.java).apply {
                action = "TOGGLE"
                putExtra("PAGE_TYPE", parsed.pageType)
            }
            startService(intent)
        } else if (parsed is SidebarItem.Link) {
            try {
                val launchIntent = if (parsed.url.startsWith("intent:")) {
                    Intent.parseUri(parsed.url, Intent.URI_INTENT_SCHEME)
                } else {
                    Intent(Intent.ACTION_VIEW, android.net.Uri.parse(parsed.url))
                }
                launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                startActivity(launchIntent)
            } catch (e: Exception) {}
        } else if (parsed is SidebarItem.QuickTile) {
            QuickTileHandler.handleQuickTileAction(this, parsed.action)
        } else if (parsed is SidebarItem.IntentAction) {
            try {
                val launchIntent = Intent.parseUri(parsed.uri, Intent.URI_INTENT_SCHEME)
                launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                startActivity(launchIntent)
            } catch (e: Exception) {}
        } else if (parsed is SidebarItem.SystemAction) {
            if (parsed.action == "log_keeper") {
                val launchIntent = Intent(this, com.example.LogKeeperActivity::class.java)
                launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                startActivity(launchIntent)
            } else if (parsed.action == "ebook_reader") {
                val launchIntent = Intent(this, FloatingReaderService::class.java)
                launchIntent.action = "TOGGLE"
                startService(launchIntent)
            } else if (parsed.action == "work_notes") {
                val launchIntent = Intent(this, WorkNotesService::class.java)
                launchIntent.action = "TOGGLE"
                startService(launchIntent)
            } else if (parsed.action == "screenshot") {
                val launchIntent = Intent(this, VianSideAccessibilityService::class.java)
                launchIntent.action = "com.example.ACTION_TAKE_SCREENSHOT"
                startService(launchIntent)
            } else if (parsed.action == "qr_scan") {
                val launchIntent = Intent(this, VianSideAccessibilityService::class.java)
                launchIntent.action = "com.example.ACTION_START_CROP"
                startService(launchIntent)
            } else if (parsed.action == "screen_record") {
                val launchIntent = Intent(this, ScreenRecordService::class.java)
                launchIntent.action = if (ScreenRecordService.isRecording) "STOP_RECORDING" else "START_RECORDING"
                startService(launchIntent)
            } else {
                val launchIntent = Intent(this, VianSideAccessibilityService::class.java)
                launchIntent.action = "com.example.ACTION_SYSTEM_UI"
                launchIntent.putExtra("ACTION", parsed.action)
                startService(launchIntent)
            }
        } else if (parsed is SidebarItem.DisplayAction) {
            if (parsed.action == "brightness_up") {
                adjustBrightness(0.1f)
            } else if (parsed.action == "brightness_down") {
                adjustBrightness(-0.1f)
            } else if (parsed.action == "blue_light_filter") {
                BlueLightFilterManager.toggle(this)
            } else if (parsed.action == "lock_screen_time") {
                // Not supported
            }
        } else if (parsed is SidebarItem.VolumeAction) {
            val audioManager = getSystemService(Context.AUDIO_SERVICE) as android.media.AudioManager
            val streamType = when (parsed.stream) {
                "ringer" -> android.media.AudioManager.STREAM_RING
                "music" -> android.media.AudioManager.STREAM_MUSIC
                "alarm" -> android.media.AudioManager.STREAM_ALARM
                else -> android.media.AudioManager.STREAM_RING
            }
            if (parsed.action == "vol_up") {
                audioManager.adjustStreamVolume(streamType, android.media.AudioManager.ADJUST_RAISE, android.media.AudioManager.FLAG_SHOW_UI)
            } else if (parsed.action == "vol_down") {
                audioManager.adjustStreamVolume(streamType, android.media.AudioManager.ADJUST_LOWER, android.media.AudioManager.FLAG_SHOW_UI)
            } else if (parsed.action == "mute") {
                audioManager.adjustStreamVolume(streamType, android.media.AudioManager.ADJUST_MUTE, android.media.AudioManager.FLAG_SHOW_UI)
            } else if (parsed.action == "unmute") {
                audioManager.adjustStreamVolume(streamType, android.media.AudioManager.ADJUST_UNMUTE, android.media.AudioManager.FLAG_SHOW_UI)
            }
        } else if (parsed is SidebarItem.MediaAction) {
            val audioManager = getSystemService(Context.AUDIO_SERVICE) as android.media.AudioManager
            val keyEvent = when (parsed.action) {
                "play_pause" -> android.view.KeyEvent.KEYCODE_MEDIA_PLAY_PAUSE
                "next" -> android.view.KeyEvent.KEYCODE_MEDIA_NEXT
                "prev" -> android.view.KeyEvent.KEYCODE_MEDIA_PREVIOUS
                else -> -1
            }
            if (keyEvent != -1) {
                audioManager.dispatchMediaKeyEvent(android.view.KeyEvent(android.view.KeyEvent.ACTION_DOWN, keyEvent))
                audioManager.dispatchMediaKeyEvent(android.view.KeyEvent(android.view.KeyEvent.ACTION_UP, keyEvent))
            }
        }
    }
    
    private fun adjustBrightness(delta: Float) {
        // Just send intent to DisplayActionHandler if any
    }

    override fun onBind(intent: Intent?): IBinder? = null
    
    override fun onDestroy() {
        super.onDestroy()
        for (view in activeTriggers.values) {
            try { windowManager.removeView(view) } catch(e: Exception) {}
        }
        activeTriggers.clear()
    }
}
