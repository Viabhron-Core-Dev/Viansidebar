with open("app/src/main/java/com/example/service/QRCropActivity.kt", "r") as f:
    content = f.read()

content = content.replace("androidx.compose.foundation.gestures.detectTapGestures(", "detectTapGestures(")

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "w") as f:
    f.write(content)
