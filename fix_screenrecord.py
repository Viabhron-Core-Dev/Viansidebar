import re

with open('app/src/main/java/com/example/service/ScreenRecordService.kt', 'r') as f:
    content = f.read()

old_code = """            if (resultCode == -1 || data == null) {
                stopSelf()
                return START_NOT_STICKY
            }

            startForeground(NOTIFICATION_ID, createNotification())"""

new_code = """            if (resultCode != android.app.Activity.RESULT_OK || data == null) {
                stopSelf()
                return START_NOT_STICKY
            }

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                startForeground(NOTIFICATION_ID, createNotification(), android.content.pm.ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PROJECTION)
            } else {
                startForeground(NOTIFICATION_ID, createNotification())
            }"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/service/ScreenRecordService.kt', 'w') as f:
    f.write(content)
