import re

with open('app/src/main/java/com/example/service/ScreenRecordActivity.kt', 'r') as f:
    content = f.read()

old_activity = re.search(r'class ScreenRecordActivity : Activity\(\) \{.*\}', content, re.DOTALL).group(0)

new_activity = """class ScreenRecordActivity : Activity() {

    private lateinit var projectionManager: MediaProjectionManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        if (ScreenRecordService.isRecording) {
            val stopIntent = Intent(this, ScreenRecordService::class.java).apply {
                action = "STOP_RECORDING"
            }
            startService(stopIntent)
            finish()
            return
        }

        val prefs = getSharedPreferences("ScreenCapPrefs", Context.MODE_PRIVATE)
        val recordAudio = prefs.getBoolean("record_audio", false)

        if (recordAudio && checkSelfPermission(android.Manifest.permission.RECORD_AUDIO) != android.content.pm.PackageManager.PERMISSION_GRANTED) {
            requestPermissions(arrayOf(android.Manifest.permission.RECORD_AUDIO), REQUEST_AUDIO_CODE)
            return
        }

        startProjection()
    }

    private fun startProjection() {
        projectionManager = getSystemService(Context.MEDIA_PROJECTION_SERVICE) as MediaProjectionManager
        startActivityForResult(projectionManager.createScreenCaptureIntent(), REQUEST_CODE)
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        if (requestCode == REQUEST_AUDIO_CODE) {
            if (grantResults.isNotEmpty() && grantResults[0] == android.content.pm.PackageManager.PERMISSION_GRANTED) {
                startProjection()
            } else {
                Toast.makeText(this, "Microphone permission denied", Toast.LENGTH_SHORT).show()
                finish()
            }
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        if (requestCode == REQUEST_CODE) {
            if (resultCode == RESULT_OK && data != null) {
                val serviceIntent = Intent(this, ScreenRecordService::class.java).apply {
                    action = "START_RECORDING"
                    putExtra("resultCode", resultCode)
                    putExtra("data", data)
                }
                if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                    startForegroundService(serviceIntent)
                } else {
                    startService(serviceIntent)
                }
            } else {
                Toast.makeText(this, "Screen recording permission denied", Toast.LENGTH_SHORT).show()
            }
        }
        finish()
    }

    companion object {
        private const val REQUEST_CODE = 1000
        private const val REQUEST_AUDIO_CODE = 1001
    }
}"""

content = content.replace(old_activity, new_activity)

with open('app/src/main/java/com/example/service/ScreenRecordActivity.kt', 'w') as f:
    f.write(content)
