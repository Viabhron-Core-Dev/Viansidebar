import re

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'r') as f:
    content = f.read()

# Replace updatePersistentNotification completely
notif_replacement = """    private fun updatePersistentNotification() {
        val manager = getSystemService(android.app.NotificationManager::class.java)
        
        val notificationIntent = Intent(this, com.example.MainActivity::class.java)
        val pendingIntent = android.app.PendingIntent.getActivity(this, 0, notificationIntent, android.app.PendingIntent.FLAG_IMMUTABLE)

        val notificationBuilder = androidx.core.app.NotificationCompat.Builder(this, "reader_channel")
            .setContentTitle("LiteReader")
            .setContentText("Reading active")
            .setSmallIcon(android.R.drawable.ic_media_play)
            .setContentIntent(pendingIntent)
            .setOnlyAlertOnce(true)

        manager.notify(2, notificationBuilder.build())
    }
"""

content = re.sub(r'    private fun updatePersistentNotification\(\) \{.*?manager\.notify\(2, notificationBuilder\.build\(\)\)\n    \}', notif_replacement, content, flags=re.DOTALL)
content = re.sub(r'    private fun updatePersistentNotification\(\) \{.*?manager\.notify\(1, notificationBuilder\.build\(\)\)\n    \}', notif_replacement, content, flags=re.DOTALL)

# Also remove references to appsManagers, pendingElementCallback, callRecorderManager, etc.
content = re.sub(r'        callRecorderManager = CallRecorderManager\(this, prefs\)\n        callRecorderManager\?\.startListening\(\)\n', '', content)
content = re.sub(r'    private fun getIconBitmap\(.*?\n    \}\n', '', content, flags=re.DOTALL)
content = re.sub(r'    private fun createSpeedIcon\(.*?\n    \}\n', '', content, flags=re.DOTALL)

with open('app/src/main/java/com/example/service/FloatingReaderService.kt', 'w') as f:
    f.write(content)
