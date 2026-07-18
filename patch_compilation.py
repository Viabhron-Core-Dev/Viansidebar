import re

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "r") as f:
    content = f.read()

target_action = """                        onAction = { action, x, y, width, height, shape ->
                            if (action == "scan") {
                                scanCroppedArea(bitmap, x, y, width, height)
                            } else if (action == "share") {
                                shareCroppedArea(bitmap, x, y, width, height, shape)
                            }
                        },"""
replacement_action = """                        onAction = { action, x, y, width, height, shape, points ->
                            if (action == "scan") {
                                scanCroppedArea(bitmap, x, y, width, height, shape, points)
                            } else if (action == "share") {
                                shareCroppedArea(bitmap, x, y, width, height, shape, points)
                            }
                        },"""
content = content.replace(target_action, replacement_action)

content = content.replace("androidx.compose.foundation.gestures.detectTapGestures", "detectTapGestures")

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "w") as f:
    f.write(content)
