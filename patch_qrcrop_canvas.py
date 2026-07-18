import re

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "r") as f:
    content = f.read()

target = """                        Canvas(modifier = Modifier
                .fillMaxSize()
                .pointerInput(Unit) {"""

replacement = """                        Canvas(modifier = Modifier
                .fillMaxSize()
                .androidx.compose.ui.graphics.graphicsLayer { alpha = 0.99f }
                .pointerInput(Unit) {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/service/QRCropActivity.kt", "w") as f:
    f.write(content)
