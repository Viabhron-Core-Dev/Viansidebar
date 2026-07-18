with open("app/src/main/java/com/example/service/QRCropActivity.kt", "r") as f:
    content = f.read()

content = content.replace(
"""                        detectTapGestures { offset ->
                            polygonPoints.add(offset)
                        }""",
"""                        androidx.compose.foundation.gestures.detectTapGestures(
                            onTap = { offset ->
                                polygonPoints.add(offset)
                            }
                        )"""
)

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "w") as f:
    f.write(content)
