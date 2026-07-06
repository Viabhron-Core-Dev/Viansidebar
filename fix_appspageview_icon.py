import re

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'r') as f:
    content = f.read()

old_bind = """            } else if (item is SidebarItem.SystemAction) {
                icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                icon.setImageResource(item.iconResId)
                icon.setColorFilter(android.graphics.Color.WHITE)"""

new_bind = """            } else if (item is SidebarItem.SystemAction) {
                icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
                if (item.action == "screen_record" && com.example.service.ScreenRecordService.isRecording) {
                    icon.setImageResource(android.R.drawable.ic_media_pause)
                    icon.setColorFilter(android.graphics.Color.RED)
                } else {
                    icon.setImageResource(item.iconResId)
                    icon.setColorFilter(android.graphics.Color.WHITE)
                }"""

content = content.replace(old_bind, new_bind)

with open('app/src/main/java/com/example/service/AppsPageView.kt', 'w') as f:
    f.write(content)
