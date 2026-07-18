with open("app/src/main/java/com/example/service/QRCropActivity.kt", "r") as f:
    content = f.read()

target_scan = "private fun scanCroppedArea(bitmap: Bitmap, x: Float, y: Float, w: Float, h: Float) {"
replacement_scan = "private fun scanCroppedArea(bitmap: Bitmap, x: Float, y: Float, w: Float, h: Float, shape: String, points: List<Offset>) {"
content = content.replace(target_scan, replacement_scan)

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "w") as f:
    f.write(content)
