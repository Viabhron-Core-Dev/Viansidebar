import re

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "r") as f:
    content = f.read()

target = """        } else if (parsed is SidebarItem.SystemAction) {
            icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
            if (parsed.action == "screen_record" && com.example.service.ScreenRecordService.isRecording) {
                icon.setImageResource(android.R.drawable.ic_media_pause)
                icon.setColorFilter(android.graphics.Color.RED)
            } else if (parsed.action == "blue_light_filter" && com.example.service.BlueLightFilterManager.isEnabled) {
                icon.setImageResource(parsed.iconResId)
                icon.setColorFilter(android.graphics.Color.parseColor("#FF9900"))
            } else {
                icon.setImageResource(parsed.iconResId)
                icon.setColorFilter(android.graphics.Color.WHITE)
            }
        } else if (parsed is SidebarItem.VolumeAction || parsed is SidebarItem.MediaAction || parsed is SidebarItem.DisplayAction || parsed is SidebarItem.SettingsShortcut || parsed is SidebarItem.Link) {"""
        
replacement = """        } else if (parsed is SidebarItem.SystemAction) {
            icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
            if (parsed.action == "screen_record" && com.example.service.ScreenRecordService.isRecording) {
                icon.setImageResource(android.R.drawable.ic_media_pause)
                icon.setColorFilter(android.graphics.Color.RED)
            } else {
                icon.setImageResource(parsed.iconResId)
                icon.setColorFilter(android.graphics.Color.WHITE)
            }
        } else if (parsed is SidebarItem.DisplayAction) {
            icon.setBackgroundColor(android.graphics.Color.TRANSPARENT)
            icon.setImageResource(parsed.iconResId)
            if (parsed.action == "blue_light_filter" && com.example.service.BlueLightFilterManager.isEnabled) {
                icon.setColorFilter(android.graphics.Color.parseColor("#FF9900"))
            } else {
                icon.setColorFilter(android.graphics.Color.WHITE)
            }
        } else if (parsed is SidebarItem.VolumeAction || parsed is SidebarItem.MediaAction || parsed is SidebarItem.SettingsShortcut || parsed is SidebarItem.Link) {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/SidebarAppsManager.kt", "w") as f:
    f.write(content)
