import re

with open('app/src/main/java/com/example/service/ScreenRecordActivity.kt', 'r') as f:
    content = f.read()

old_start = """    private fun startProjection() {
        try {
            // Try to launch MIUI system screen recorder (as requested for Redmi A5)
            val miuiIntent = Intent().apply {
                component = android.content.ComponentName("com.miui.screenrecorder", "com.miui.screenrecorder.ScreenRecorderActivity")
                flags = Intent.FLAG_ACTIVITY_NEW_TASK
            }
            startActivity(miuiIntent)
            finish()
            return
        } catch (e: Exception) {
            try {
                // Try another MIUI component
                val miuiIntent2 = Intent().apply {
                    component = android.content.ComponentName("com.miui.screenrecorder", "com.miui.screenrecorder.ScreenRecorder")
                    flags = Intent.FLAG_ACTIVITY_NEW_TASK
                }
                startActivity(miuiIntent2)
                finish()
                return
            } catch (e2: Exception) {
                // Fallback to our own MediaProjection
                projectionManager = getSystemService(Context.MEDIA_PROJECTION_SERVICE) as MediaProjectionManager
                startActivityForResult(projectionManager.createScreenCaptureIntent(), REQUEST_CODE)
            }
        }
    }"""

new_start = """    private fun startProjection() {
        val pm = packageManager
        
        // Try getting launch intent for MIUI screen recorder
        val launchIntent = pm.getLaunchIntentForPackage("com.miui.screenrecorder")
        if (launchIntent != null) {
            launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            try {
                startActivity(launchIntent)
                finish()
                return
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
        
        // If not, try explicit component
        try {
            val miuiIntent = Intent().apply {
                setClassName("com.miui.screenrecorder", "com.miui.screenrecorder.activity.ScreenRecorderHomeActivity")
                flags = Intent.FLAG_ACTIVITY_NEW_TASK
            }
            startActivity(miuiIntent)
            finish()
            return
        } catch (e: Exception) {
            e.printStackTrace()
        }
        
        try {
            val miuiIntent = Intent().apply {
                setClassName("com.miui.screenrecorder", "com.miui.screenrecorder.ScreenRecorderActivity")
                flags = Intent.FLAG_ACTIVITY_NEW_TASK
            }
            startActivity(miuiIntent)
            finish()
            return
        } catch (e: Exception) {
            e.printStackTrace()
        }

        // Try Xiaomi's screen recorder quick setting tile action or just the package
        try {
            val intent = Intent("miui.intent.action.SCREEN_RECORDER")
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            startActivity(intent)
            finish()
            return
        } catch (e: Exception) {
            e.printStackTrace()
        }
        
        // Fallback to our own MediaProjection
        projectionManager = getSystemService(Context.MEDIA_PROJECTION_SERVICE) as MediaProjectionManager
        startActivityForResult(projectionManager.createScreenCaptureIntent(), REQUEST_CODE)
    }"""

content = content.replace(old_start, new_start)

with open('app/src/main/java/com/example/service/ScreenRecordActivity.kt', 'w') as f:
    f.write(content)
